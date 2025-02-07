import asyncio
import json
from typing import Callable

from cdp import Wallet
from core.exceptions import KibaException
from core.requester import Requester
from pydantic import BaseModel

from agent_hack import morpho
from agent_hack import uniswap
from agent_hack.base_action import BaseAction

# NOTE(krishan711): this could really be a langchain tool directly but easier to just follow the cdp pattern for now.

BASE_CHAIN_ID = 8453


PROMPT = """
This tool will list vaultsfor achieving yield that are hosted on the Morpho protocol.
Each yield will come with details about its APY and rewards.
"""

class MorphoListVaultsInput(BaseModel):
    # assetAddress: str = Field(..., description="The asset address to find vaults for, e.g. 0x18090cDA49B21dEAffC21b4F886aed3eB787d032")
    pass


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
    rewardTokenPromises = [uniswap.get_token_by_address(requester=requester, chainId=chainId, tokenAddress=rewardAsset.address) for rewardAsset in allRewardAssets.values()]
    rewardTokens = await asyncio.gather(*rewardTokenPromises, return_exceptions=True)
    print('rewardTokens', rewardTokens)
    rewardTokensMap = zip(allRewardAssets.keys(), rewardTokens)
    print('rewardTokensMap', rewardTokensMap)
    vaultDicts = [vault.model_dump() for vault in vaults]
    # for vault in vaults:
    #     # calculate adjusted apy based on risk of each token
    #     riskScore = 0
    #     for reward in vault.rewardApys:
    #         riskScore += reward.asset.riskScore
    #     vault['adjustedRewardApys'] = [reward.model_dump() for reward in vault.rewardApys]
    output = f'Avaiable vaults are below in a json list:\n{json.dumps(vaultDicts)}'
    return output


class MorphoListVaultsAction(BaseAction):
    name: str = "morpho_list_vaults"
    description: str = PROMPT
    args_schema: type[BaseModel] | None = MorphoListVaultsInput
    afunc: Callable[..., str] = morpho_list_vaults
