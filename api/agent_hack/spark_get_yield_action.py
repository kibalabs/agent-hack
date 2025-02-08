from typing import Callable

from cdp import Wallet
from core.exceptions import KibaException
from pydantic import BaseModel

from agent_hack import yield_options
from agent_hack.base_action import BaseAction

# NOTE(krishan711): this could really be a langchain tool directly but easier to just follow the cdp pattern for now.
PROMPT = """
This tool will get the current APY yield offered by spark.fi.
"""

class GetSparkYieldInput(BaseModel):
    pass


async def get_spark_yield(wallet: Wallet) -> str:
    if wallet.network_id == 'base-mainnet':
        chainId = yield_options.BASE_CHAIN_ID
    else:
        raise KibaException('Unsupported network, only base is supported')
    yieldOptions = await yield_options.list_spark_yield_options(chainId=chainId)
    output = f'Current spark APY is: {yieldOptions[0].totalApy}'
    return output


class GetSparkYieldAction(BaseAction):
    name: str = "get_spark_yield"
    description: str = PROMPT
    args_schema: type[BaseModel] | None = GetSparkYieldInput
    afunc: Callable[..., str] = get_spark_yield
