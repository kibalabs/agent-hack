import datetime
import json
import asyncio
from typing import Any

from core import logging
from core.requester import Requester
from core.util import file_util
from core.exceptions import KibaException

from agent_hack import morpho_queries


BASE_CHAIN_ID = 8453


async def load_or_query(requester: Requester, entityName: str,url: str, dataDict: dict[str, Any]) -> dict[str, Any]:
    filePath = f'../secrets/{entityName}.json'
    if await file_util.file_exists(filePath=filePath):
        print(f'loading {entityName}...')
        items = json.loads(await file_util.read_file(filePath=filePath))
    else:
        print(f'querying {entityName}...')
        items = []
        while True:
            dataDict['variables']['skip'] = len(items)
            repsonse = await requester.post_json(url=url, dataDict=dataDict)
            data = repsonse.json()
            items += data['data'][entityName]['items']
            pageInfo = data['data'][entityName].get('pageInfo')
            if pageInfo is None:
                break
            if pageInfo['count'] < pageInfo['limit']:
                break
        await file_util.write_file(filePath=filePath, content=json.dumps(items, indent=2))
    return items


async def main():
    logging.init_basic_logging()
    requester = Requester()

    assets = await load_or_query(requester=requester, entityName='assets', url='https://blue-api.morpho.org/graphql', dataDict={
        'query': morpho_queries.LIST_CHAIN_ASSETS_QUERY,
        'variables': {
            'chainId': BASE_CHAIN_ID,
        },
    })
    print(f'Loaded {len(assets)} assets')
    usdcAsset = next((a for a in assets if a['symbol'] == 'USDC'), None)
    if usdcAsset is None:
        raise KibaException('USDC asset not found')
    print(f'Loaded USDC asset: {usdcAsset}')
    vaults = await load_or_query(requester=requester, entityName='vaults', url='https://blue-api.morpho.org/graphql', dataDict={
        'query': morpho_queries.LIST_CHAIN_ASSET_VAULTS_QUERY,
        'variables': {
            'chainId': BASE_CHAIN_ID,
            'assetAddress': usdcAsset['address'],
        },
    })
    print(f'Loaded {len(vaults)} vaults')
    orderedVaults = sorted(vaults, key=lambda vault: vault['state']['totalAssetsUsd'], reverse=True)
    for vault in orderedVaults:
        vaultState = vault['state']
        netApy = vaultState['netApy']
        netApyWithoutRewards = vaultState['netApyWithoutRewards']
        # NOTE(krishan711): why is this apr??
        rewardsApy = sum(reward['supplyApr'] for reward in vaultState['rewards'])
        morphoApy = netApy - netApyWithoutRewards -rewardsApy
        print(f"{vault['name']} ({vault['symbol']}): {vault['address']}")
        print(f"  Creation: {datetime.datetime.fromtimestamp(vault['creationTimestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  DepositsUsd: {int(vaultState['totalAssetsUsd']):,}")
        print(f"  Deposits: {int(vaultState['totalAssets'] / (10 ** usdcAsset['decimals'])):,}")
        print(f"  APY: {netApy:.2%} (without rewards: {netApyWithoutRewards:.2%})")
        print(f"    Raw: {netApyWithoutRewards:.2%}")
        if netApy > netApyWithoutRewards:
            print(f"    Morpho: {morphoApy:.2%}")
        for reward in vaultState['rewards']:
            print(f"    {reward['asset']['symbol']}: {reward['supplyApr']:.2%}")
        print(f"  fee: {vaultState['fee']:.2%}")
        if len(vault['warnings']) > 0:
            print(f"  Warnings: {'; '.join([warning['type'] for warning in vault['warnings']])}")
        print('---')


if __name__ == "__main__":
    asyncio.run(main())
