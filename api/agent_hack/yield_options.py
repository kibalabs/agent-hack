import asyncio
import datetime

from core.requester import Requester
from pydantic import BaseModel

from agent_hack import aerodrome
from agent_hack import morpho
from agent_hack import uniswap


class Asset(BaseModel):
    address: str
    decimals: int
    name: str
    symbol: str
    logoURI: str | None
    totalSupply: int
    priceUsd: float | None
    oraclePriceUsd: float | None
    spotPriceEth: float | None


class YieldOptionReward(BaseModel):
    asset: Asset
    apy: float
    riskAdjustedApy: float
    uniswapTotalValueLockedUSD: float | None
    uniswapVolumeUSD: float | None
    uniswapTxCount: int | None
    uniswapRiskFactor: float
    aerodromeTotalValueLockedUSD: float | None
    aerodromeVolumeUSD: float | None
    aerodromeTxCount: int | None
    aerodromeRiskFactor: float


class YieldOption(BaseModel):
    name: str
    symbol: str
    address: str
    totalDepositsUsd: float
    totalDeposits: float
    creationDate: datetime.datetime
    totalApy: float
    baseApy: float
    riskAdjustedApy: float
    rewards: list[YieldOptionReward]


BASE_CHAIN_ID = 8453
MIN_TVL_USD = 100_000
GOOD_TVL_USD = 1_000_000
MIN_VOLUME_USD = 50_000
GOOD_VOLUME_USD = 500_000
MIN_TX_COUNT = 100
GOOD_TX_COUNT = 1000


def _calculate_token_quality_factor(token: uniswap.TokenWithPools | None) -> float:
    if token is None or isinstance(token, Exception):
        return 0.0
    tvlFactor = min(1.0, max(0.0, (token.totalValueLockedUSD - MIN_TVL_USD) / (GOOD_TVL_USD - MIN_TVL_USD)))
    volumeFactor = min(1.0, max(0.0, (token.volumeUSD - MIN_VOLUME_USD) / (GOOD_VOLUME_USD - MIN_VOLUME_USD)))
    txFactor = min(1.0, max(0.0, (token.txCount - MIN_TX_COUNT) / (GOOD_TX_COUNT - MIN_TX_COUNT)))
    weightedFactor = (tvlFactor * 0.5) + (volumeFactor * 0.3) + (txFactor * 0.2)
    print(token.address, 'weightedFactor', weightedFactor)
    return weightedFactor


async def list_morpho_yield_options(chainId: int) -> list[YieldOption]:
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
    uniswapRewardTokens = [(token if isinstance(token, uniswap.Token) else None) for token in uniswapRewardTokens]
    uniswapRewardTokensMap = dict(zip(allRewardAssets.keys(), uniswapRewardTokens))
    print('uniswapRewardTokensMap', uniswapRewardTokensMap)
    aerodromeRewardTokenPromises = [aerodrome.get_token_by_address(requester=requester, chainId=chainId, tokenAddress=rewardAsset.address) for rewardAsset in allRewardAssets.values()]
    aerodromeRewardTokens = await asyncio.gather(*aerodromeRewardTokenPromises, return_exceptions=True)
    aerodromeRewardTokens = [(token if isinstance(token, uniswap.Token) else None) for token in aerodromeRewardTokens]
    aerodromeRewardTokensMap = dict(zip(allRewardAssets.keys(), aerodromeRewardTokens))
    print('aerodromeRewardTokensMap', aerodromeRewardTokensMap)
    yieldOptions: list[YieldOption] = []
    for vault in vaults:
        overallRiskAdjustedApy = vault.baseApy
        rewards: list[YieldOptionReward] = []
        for reward in vault.rewardApys:
            uniswapToken = uniswapRewardTokensMap.get(reward.asset.address)
            aerodromeToken = aerodromeRewardTokensMap.get(reward.asset.address)
            uniswapFactor = _calculate_token_quality_factor(uniswapToken)
            aerodromeFactor = _calculate_token_quality_factor(aerodromeToken)
            qualityFactor = max(uniswapFactor, aerodromeFactor)
            adjustedRewardApy = reward.apy * qualityFactor
            overallRiskAdjustedApy += adjustedRewardApy
            rewards.append(
                YieldOptionReward(
                    asset=Asset(
                        address=reward.asset.address,
                        decimals=reward.asset.decimals,
                        name=reward.asset.name,
                        symbol=reward.asset.symbol,
                        logoURI=reward.asset.logoURI,
                        totalSupply=reward.asset.totalSupply,
                        priceUsd=reward.asset.priceUsd,
                        oraclePriceUsd=reward.asset.oraclePriceUsd,
                        spotPriceEth=reward.asset.spotPriceEth,
                    ),
                    apy=reward.apy,
                    riskAdjustedApy=adjustedRewardApy,
                    uniswapTotalValueLockedUSD=uniswapToken.totalValueLockedUSD if uniswapToken else None,
                    uniswapVolumeUSD=uniswapToken.volumeUSD if uniswapToken else None,
                    uniswapTxCount=uniswapToken.txCount if uniswapToken else None,
                    uniswapRiskFactor=uniswapFactor,
                    aerodromeTotalValueLockedUSD=aerodromeToken.totalValueLockedUSD if aerodromeToken else None,
                    aerodromeVolumeUSD=aerodromeToken.volumeUSD if aerodromeToken else None,
                    aerodromeTxCount=aerodromeToken.txCount if aerodromeToken else None,
                    aerodromeRiskFactor=aerodromeFactor,
                )
            )
        yieldOptions.append(
            YieldOption(
                name=vault.name,
                symbol=vault.symbol,
                address=vault.address,
                totalDepositsUsd=vault.totalDepositsUsd,
                totalDeposits=vault.totalDeposits,
                creationDate=datetime.datetime.fromtimestamp(vault.creationTimestamp),
                totalApy=vault.totalApy,
                baseApy=vault.baseApy,
                riskAdjustedApy=overallRiskAdjustedApy,
                rewards=rewards,
            )
        )
    yieldOptions.sort(key=lambda x: x.riskAdjustedApy, reverse=True)
    return yieldOptions


async def list_spark_yield_options(chainId: int) -> list[YieldOption]:  # pylint: disable=unused-argument
    # TODO(krishan711): where do i get this via api??
    return [YieldOption(
        name="Spark.fi",
        symbol="SPARK",
        address="0x0000000000000000000000000000000000000000",
        totalDepositsUsd=0,
        totalDeposits=0,
        creationDate=datetime.datetime.fromtimestamp(0),
        totalApy=12.5,
        baseApy=12.5,
        riskAdjustedApy=12.5,
        rewards=[],
    )]


async def list_all_yield_options(chainId: int) -> list[YieldOption]:
    allPromises = [
        list_morpho_yield_options(chainId=chainId),
        list_spark_yield_options(chainId=chainId),
    ]
    yieldOptionLists = await asyncio.gather(*allPromises, return_exceptions=True)
    for yieldOptionList in yieldOptionLists:
        if isinstance(yieldOptionList, Exception):
            raise yieldOptionList
    return [yieldOption for yieldOptionList in yieldOptionLists for yieldOption in yieldOptionList]
