import os

from core.exceptions import KibaException
from core.exceptions import NotFoundException
from core.requester import Requester

from agent_hack import uniswap_queries
from agent_hack.uniswap import TokenWithPools
from agent_hack.util import load_or_query


async def get_token_by_address(requester: Requester, chainId: int, tokenAddress: str) -> TokenWithPools:
    if chainId == 8453:
        queryUrl = f'https://gateway.thegraph.com/api/{os.environ["GRAPH_API_KEY"]}/subgraphs/id/GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM'
    else:
        raise KibaException('Unsupported network, only base is supported')
    tokenDicts = await load_or_query(requester=requester, source='aerodrome', entityName='tokens', cacheEntityName=f'token-{tokenAddress}', hasInlinedItems=True, url=queryUrl, dataDict={
        'query': uniswap_queries.GET_TOKEN,
        'variables': {
            'tokenAddress': tokenAddress.lower(),
        },
    })
    tokenDict = next((tokenDict for tokenDict in tokenDicts if tokenDict['id'].lower() == tokenAddress.lower()), None)
    if tokenDict is None:
        raise NotFoundException()
    return TokenWithPools.model_validate(tokenDict)
