import json
import os
from typing import Any

from core.exceptions import KibaException
from core.exceptions import NotFoundException
from core.requester import Requester
from core.util import file_util
from pydantic import BaseModel
from pydantic import Field

from agent_hack import uniswap_queries


class Token(BaseModel):
    address: str = Field(alias='id')
    name: str
    symbol: str
    decimals: int
    totalSupply: int
    volume: float
    volumeUSD: float
    untrackedVolumeUSD: float
    feesUSD: float
    txCount: int
    poolCount: int
    totalValueLocked: float
    totalValueLockedUSD: float
    totalValueLockedUSDUntracked: float
    derivedETH: float


class WhitelistPool(BaseModel):
    liquidity: str  # Keep as string due to potential large numbers
    feeTier: int
    feesUSD: float
    token0Price: float
    token1Price: float
    volumeToken0: float
    volumeToken1: float
    volumeUSD: float
    txCount: int
    totalValueLockedToken0: float
    totalValueLockedToken1: float
    totalValueLockedUSD: float
    totalValueLockedETH: float
    token0: Token
    token1: Token


class TokenWithPools(Token):
    whitelistPools: list[WhitelistPool] | None = None


async def load_or_query(requester: Requester, entityName: str, url: str, dataDict: dict[str, Any], cacheEntityName: str | None = None) -> dict[str, Any]:
    if cacheEntityName is None:
        cacheEntityName = entityName
    cacheFilePath = f'../secrets/uniswap-{cacheEntityName}.json'
    if await file_util.file_exists(filePath=cacheFilePath):
        print(f'loading {entityName}...')
        items = json.loads(await file_util.read_file(filePath=cacheFilePath))
    else:
        print(f'querying {entityName}...')
        response = await requester.post_json(url=url, dataDict=dataDict)
        data = response.json()
        items = data['data'][entityName]
        await file_util.write_file(filePath=cacheFilePath, content=json.dumps(items, indent=2))
    return items


async def get_token_by_address(requester: Requester, chainId: int, tokenAddress: str) -> TokenWithPools:
    if chainId == 8453:
        queryUrl = f'https://gateway.thegraph.com/api/{os.environ["GRAPH_API_KEY"]}/subgraphs/id/GqzP4Xaehti8KSfQmv3ZctFSjnSUYZ4En5NRsiTbvZpz'
    else:
        raise KibaException('Unsupported network, only base is supported')
    tokenDicts = await load_or_query(requester=requester, entityName='tokens', cacheEntityName=f'token-{tokenAddress}', url=queryUrl, dataDict={
        'query': uniswap_queries.GET_TOKEN,
        'variables': {
            'tokenAddress': tokenAddress,
        },
    })
    tokenDict = next((tokenDict for tokenDict in tokenDicts if tokenDict['id'].lower() == tokenAddress.lower()), None)
    if tokenDict is None:
        raise NotFoundException()
    return TokenWithPools.model_validate(tokenDict)
