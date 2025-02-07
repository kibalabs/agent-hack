import asyncio
import json
from typing import Callable

from cdp import Wallet
from core.exceptions import KibaException
from core.requester import Requester
from pydantic import BaseModel

from agent_hack import aerodrome
from agent_hack import morpho
from agent_hack import uniswap
from agent_hack.base_action import BaseAction

# NOTE(krishan711): this could really be a langchain tool directly but easier to just follow the cdp pattern for now.

BASE_CHAIN_ID = 8453
MIN_TVL_USD = 100_000  #
GOOD_TVL_USD = 1_000_000
MIN_VOLUME_USD = 50_000
GOOD_VOLUME_USD = 500_000
MIN_TX_COUNT = 100
GOOD_TX_COUNT = 1000


PROMPT = """
This tool will list vaultsfor achieving yield that are hosted on the Morpho protocol.
Each yield will come with details about its APY and rewards.
"""

class MorphoListVaultsInput(BaseModel):
    # assetAddress: str = Field(..., description="The asset address to find vaults for, e.g. 0x18090cDA49B21dEAffC21b4F886aed3eB787d032")
    pass


def calculate_token_quality_factor(token: uniswap.TokenWithPools | None) -> float:
    if token is None or isinstance(token, Exception):
        return 0.0
    tvlFactor = min(1.0, max(0.0, (token.totalValueLockedUSD - MIN_TVL_USD) / (GOOD_TVL_USD - MIN_TVL_USD)))
    volumeFactor = min(1.0, max(0.0, (token.volumeUSD - MIN_VOLUME_USD) / (GOOD_VOLUME_USD - MIN_VOLUME_USD)))
    txFactor = min(1.0, max(0.0, (token.txCount - MIN_TX_COUNT) / (GOOD_TX_COUNT - MIN_TX_COUNT)))
    weightedFactor = (tvlFactor * 0.5) + (volumeFactor * 0.3) + (txFactor * 0.2)
    return weightedFactor


async def morpho_list_vaults(wallet: Wallet) -> str:
    """List vaults for achieving yield that are hosted on the Morpho protocol. Each yield will come with details about its APY and rewards.
    The assetAddress are used to find vaults for the given asset. If you don't know it, ask the user.

    Args:
        assetAddress (str): The asset address to find vaults for, e.g. 0x18090cDA49B21dEAffC21b4F886aed3eB787d032

    Returns:
        str: The message and corresponding signature.

    """
    if wallet.network_id == 'base-mainnet':
        chainId = BASE_CHAIN_ID
    else:
        raise KibaException('Unsupported network, only base is supported')
    requester = Requester()
    usdcAsset = await morpho.get_asset_by_symbol(requester=requester, chainId=chainId, assetSymbol="USDC")
    print(f'Loaded USDC asset: {usdcAsset}')
    vaults = await morpho.list_vaults(requester=requester, chainId=chainId, assetAddress=usdcAsset.address)
    print(f'Loaded {len(vaults)} vaults')
    allRewardAssets: dict[str, morpho.Asset] = {}
    for vault in vaults:
        allRewardAssets.update({reward.asset.address: reward.asset for reward in vault.rewardApys})
    print('allRewardAssets', allRewardAssets)
    uniswapRewardTokenPromises = [uniswap.get_token_by_address(requester=requester, chainId=chainId, tokenAddress=rewardAsset.address) for rewardAsset in allRewardAssets.values()]
    uniswapRewardTokens = await asyncio.gather(*uniswapRewardTokenPromises, return_exceptions=True)
    uniswapRewardTokensMap = dict(zip(allRewardAssets.keys(), uniswapRewardTokens))
    print('uniswapRewardTokensMap', uniswapRewardTokensMap)
    aerodromeRewardTokenPromises = [aerodrome.get_token_by_address(requester=requester, chainId=chainId, tokenAddress=rewardAsset.address) for rewardAsset in allRewardAssets.values()]
    aerodromeRewardTokens = await asyncio.gather(*aerodromeRewardTokenPromises, return_exceptions=True)
    aerodromeRewardTokensMap = dict(zip(allRewardAssets.keys(), aerodromeRewardTokens))
    print('aerodromeRewardTokensMap', aerodromeRewardTokensMap)
    vaultDicts = []
    for vault in vaults:
        riskAdjustedApy = vault.baseApy
        rewardDetails = []
        for reward in vault.rewardApys:
            uniswapToken = uniswapRewardTokensMap.get(reward.asset.address)
            aerodromeToken = aerodromeRewardTokensMap.get(reward.asset.address)
            uniswapFactor = calculate_token_quality_factor(uniswapToken)
            aerodromeFactor = calculate_token_quality_factor(aerodromeToken)
            qualityFactor = max(uniswapFactor, aerodromeFactor)
            adjustedRewardApy = reward.apy * qualityFactor
            riskAdjustedApy += adjustedRewardApy
            rewardDetails.append({
                'asset': reward.asset.model_dump(),
                'originalApy': reward.apy,
                'qualityFactor': qualityFactor,
                'riskAdjustedApy': adjustedRewardApy,
                'uniswapFactor': uniswapFactor,
                'aerodromeFactor': aerodromeFactor,
            })
        vaultDict = {
            **vault.model_dump(),
            'riskAdjustedApy': riskAdjustedApy,
            'rewardDetails': rewardDetails,
        }
        vaultDicts.append(vaultDict)
    vaultDicts.sort(key=lambda x: x['riskAdjustedApy'], reverse=True)
    output = f'Available vaults are below in a json list:\n{json.dumps(vaultDicts)}'
    return output


class MorphoListVaultsAction(BaseAction):
    name: str = "morpho_list_vaults"
    description: str = PROMPT
    args_schema: type[BaseModel] | None = MorphoListVaultsInput
    afunc: Callable[..., str] = morpho_list_vaults
