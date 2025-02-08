from typing import Callable

from cdp import Wallet
from core.exceptions import KibaException
from pydantic import BaseModel

from agent_hack import yield_options
from agent_hack.base_action import BaseAction

# NOTE(krishan711): this could really be a langchain tool directly but easier to just follow the cdp pattern for now.
PROMPT = """
This tool will list vaults for achieving yield that are hosted on the Morpho protocol.
Each yield will come with details about its APY and rewards.
"""

class ListAllYieldOptionsInput(BaseModel):
    pass

async def list_all_yield_options(wallet: Wallet) -> str:
    if wallet.network_id == 'base-mainnet':
        chainId = yield_options.BASE_CHAIN_ID
    else:
        raise KibaException('Unsupported network, only base is supported')
    yieldOptions = await yield_options.list_all_yield_options(chainId=chainId)
    yieldOptionJsons = [yieldOption.model_dump_json() for yieldOption in yieldOptions]
    output = f'Available vaults are here in a json list: {yieldOptionJsons}'
    return output


class ListAllYieldOptionsAction(BaseAction):
    name: str = "list_all_yield_options"
    description: str = PROMPT
    args_schema: type[BaseModel] | None = ListAllYieldOptionsInput
    afunc: Callable[..., str] = list_all_yield_options
