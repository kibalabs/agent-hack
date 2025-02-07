from core.exceptions import NotFoundException
from core.requester import Requester
from pydantic import BaseModel
from pydantic import Field

from agent_hack import morpho_queries
from agent_hack.util import load_or_query


class Asset(BaseModel):
    morphoId: str = Field(default=None, serialization_alias='data')
    address: str
    decimals: int
    name: str
    symbol: str
    tags: list[str] | None
    logoURI: str | None
    totalSupply: int
    priceUsd: float | None
    oraclePriceUsd: float | None
    spotPriceEth: float | None


class VaultReward(BaseModel):
    asset: Asset
    apy: float


class Vault(BaseModel):
    name: str
    symbol: str
    address: str
    totalDepositsUsd: float
    totalDeposits: float
    creationTimestamp: int
    totalApy: float
    baseApy: float
    rewardApys: list[VaultReward]


async def get_asset_by_symbol(requester: Requester, chainId: int, assetSymbol: str) -> Asset:
    assetDicts = await load_or_query(requester=requester, source='morpho', entityName='assets', cacheEntityName=f'asset-{assetSymbol}', url='https://blue-api.morpho.org/graphql', dataDict={
        'query': morpho_queries.GET_CHAIN_ASSET_QUERY,
        'variables': {
            'chainId': chainId,
            'assetSymbol': assetSymbol,
        },
    })
    assetDict = next((assetDict for assetDict in assetDicts if assetDict['symbol'] == assetSymbol), None)
    if assetDict is None:
        raise NotFoundException()
    return Asset.model_validate(assetDict)


async def get_asset_by_address(requester: Requester, chainId: int, assetAddress: str) -> Asset:
    assetDicts = await load_or_query(requester=requester, source='morpho', entityName='assets', cacheEntityName=f'asset-{assetAddress}', url='https://blue-api.morpho.org/graphql', dataDict={
        'query': morpho_queries.GET_CHAIN_ASSET_BY_ADDRESS_QUERY,
        'variables': {
            'chainId': chainId,
            'assetAddress': assetAddress,
        },
    })
    assetDict = next((assetDict for assetDict in assetDicts if assetDict['address'].lower() == assetAddress.lower()), None)
    if assetDict is None:
        raise NotFoundException()
    return Asset.model_validate(assetDict)


async def list_vaults(requester: Requester, chainId: int, assetAddress: str) -> list[Vault]:
    vaults = await load_or_query(requester=requester, source='morpho', entityName='vaults', cacheEntityName=f'vaults-{assetAddress}', url='https://blue-api.morpho.org/graphql', dataDict={
        'query': morpho_queries.LIST_CHAIN_ASSET_VAULTS_QUERY,
        'variables': {
            'chainId': chainId,
            'assetAddress': assetAddress,
        },
    })
    print(f'Loaded {len(vaults)} vaults')
    orderedVaults = sorted(vaults, key=lambda vault: vault['state']['totalAssetsUsd'], reverse=True)
    vaults: list[Vault] = []
    morphoAsset = await get_asset_by_address(requester=requester, chainId=chainId, assetAddress='0xbaa5cc21fd487b8fcc2f632f3f4e8d37262a0842')
    for vault in orderedVaults:
        if len(vault['warnings']) > 0:
            continue
        vaultState = vault['state']
        netApy = vaultState['netApy']
        netApyWithoutRewards = vaultState['netApyWithoutRewards']
        # NOTE(krishan711): why is this apr??
        rewardsApy = sum(reward['supplyApr'] for reward in vaultState['rewards'])
        morphoApy = netApy - netApyWithoutRewards - rewardsApy
        rewardApys = [VaultReward(asset=morphoAsset, apy=morphoApy)] + [
            VaultReward(
                asset=Asset.model_validate(reward['asset']),
                apy=reward['supplyApr']
            )
            for reward in vaultState['rewards']
        ]
        vaultObject = Vault(
            name=vault['name'],
            symbol=vault['symbol'],
            address=vault['address'],
            totalDepositsUsd=vaultState['totalAssetsUsd'],
            totalDeposits=vaultState['totalAssets'],
            creationTimestamp=vault['creationTimestamp'],
            totalApy=netApy,
            baseApy=netApyWithoutRewards,
            rewardApys=rewardApys
        )
        vaults.append(vaultObject)
    return vaults
