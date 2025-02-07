from typing import Callable

from cdp import Wallet
from cdp import hash_message
from cdp_agentkit_core.actions import CdpAction
from pydantic import BaseModel
from pydantic import Field

SIGN_MESSAGE_PROMPT = """
This tool will sign arbitrary messages using EIP-191 Signed Message Standard hashing.
"""

class SignMessageInput(BaseModel):
    """Input argument schema for sign message action."""

    message: str = Field(
        ...,
        description="The message to sign. e.g. `hello world`"
    )

def sign_message(wallet: Wallet, message: str) -> str:
    """Sign message using EIP-191 message hash from the wallet.

    Args:
        wallet (Wallet): The wallet to sign the message from.
        message (str): The message to hash and sign.

    Returns:
        str: The message and corresponding signature.

    """
    signature = wallet.sign_payload(hash_message(message)).wait()

    return f"The payload signature {signature}"


class SignMessageAction(CdpAction):
    name: str = "sign_message"
    description: str = SIGN_MESSAGE_PROMPT
    args_schema: type[BaseModel] | None = SignMessageInput
    func: Callable[..., str] = sign_message
