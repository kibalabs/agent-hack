# pylint: skip-file
"""Util that calls CDP."""

import inspect
from collections.abc import Callable

from cdp import Wallet
from cdp_langchain import __version__
from cdp_langchain.utils.cdp_agentkit_wrapper import CdpAgentkitWrapper


class KibaCdpAgentkitWrapper(CdpAgentkitWrapper):

    async def arun_action(self, func: Callable[..., str], **kwargs) -> str:
        """Run a CDP Action."""
        func_signature = inspect.signature(func)

        first_kwarg = next(iter(func_signature.parameters.values()), None)

        if first_kwarg and first_kwarg.annotation is Wallet:
            return await func(self.wallet, **kwargs)
        else:
            return await func(**kwargs)
