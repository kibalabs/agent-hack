# pylint: skip-file
"""Tool allows agents to interact with the cdp-sdk library and control an MPC Wallet onchain.

To use this tool, you must first set as environment variables:
    CDP_API_KEY_NAME
    CDP_API_KEY_PRIVATE_KEY
    NETWORK_ID

"""

from typing import Any
from typing import Callable

from cdp_agentkit_core.actions import CdpAction
from cdp_langchain.tools.cdp_tool import CdpTool
from cdp_langchain.utils.cdp_agentkit_wrapper import CdpAgentkitWrapper
from langchain_core.callbacks import CallbackManagerForToolRun


class KibaCdpTool(CdpTool):  # type: ignore[override]

    func: Callable[..., str] | None = None
    afunc: Callable[..., str] | None = None

    @classmethod
    def from_cdp_action(cls, cdp_action: CdpAction, cdp_agentkit_wrapper: CdpAgentkitWrapper) -> "CdpTool":
        """Create a CdpTool from a CdpAction."""
        if not hasattr(cdp_action, "func") and not hasattr(cdp_action, "afunc"):
            raise ValueError("CdpAction must have either func or afunc")
        return cls(
            name=cdp_action.name,
            description=cdp_action.description,
            cdp_agentkit_wrapper=cdp_agentkit_wrapper,
            args_schema=cdp_action.args_schema,
            func=cdp_action.func if hasattr(cdp_action, "func") else None,
            afunc=cdp_action.afunc if hasattr(cdp_action, "afunc") else None,
        )

    async def _arun(
        self,
        instructions: str | None = "",
        run_manager: CallbackManagerForToolRun | None = None,
        **kwargs: Any,
    ) -> str:
        """Use the CDP SDK to run an operation."""
        if not instructions or instructions == "{}":
            # Catch other forms of empty input that GPT-4 likes to send.
            instructions = ""
        if self.args_schema is not None:
            validated_input_data = self.args_schema(**kwargs)
            parsed_input_args = validated_input_data.model_dump()
        else:
            parsed_input_args = {"instructions": instructions}
        if self.afunc is not None:
            return await self.cdp_agentkit_wrapper.arun_action(self.afunc, **parsed_input_args)
        return self.cdp_agentkit_wrapper.run_action(self.func, **parsed_input_args)
