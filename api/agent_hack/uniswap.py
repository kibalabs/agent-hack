import os

from core.exceptions import KibaException
from core.exceptions import NotFoundException
from core.requester import Requester
from pydantic import BaseModel
from pydantic import Field

from agent_hack import uniswap_queries
from agent_hack.util import load_or_query


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


async def get_token_by_address(requester: Requester, chainId: int, tokenAddress: str) -> TokenWithPools:
    if chainId == 8453:
        queryUrl = f'https://gateway.thegraph.com/api/{os.environ["GRAPH_API_KEY"]}/subgraphs/id/GqzP4Xaehti8KSfQmv3ZctFSjnSUYZ4En5NRsiTbvZpz'
    else:
        raise KibaException('Unsupported network, only base is supported')
    tokenDicts = await load_or_query(requester=requester, source='uniswap', entityName='tokens', cacheEntityName=f'token-{tokenAddress}', hasInlinedItems=True, url=queryUrl, dataDict={
        'query': uniswap_queries.GET_TOKEN,
        'variables': {
            'tokenAddress': tokenAddress.lower(),
        },
    })
    tokenDict = next((tokenDict for tokenDict in tokenDicts if tokenDict['id'].lower() == tokenAddress.lower()), None)
    if tokenDict is None:
        raise NotFoundException()
    return TokenWithPools.model_validate(tokenDict)
