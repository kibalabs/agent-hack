from collections.abc import Callable
from decimal import Decimal

from cdp import Asset
from cdp import Wallet
from cdp_agentkit_core.actions import CdpAction
from cdp_agentkit_core.actions.morpho.constants import METAMORPHO_ABI
from cdp_agentkit_core.actions.utils import approve
from pydantic import BaseModel
from pydantic import Field


class MorphoDepositInput(BaseModel):
    """Input schema for Morpho Vault deposit action."""

    vault_address: str = Field(..., description="The address of the Morpho Vault to deposit to")  # pylint: disable=invalid-name
    asset_amount: str = Field(..., description="The quantity of assets to deposit, in whole units")  # pylint: disable=invalid-name
    asset_address: str = Field(..., description="The address of the assets token to approve for deposit")  # pylint: disable=invalid-name
    receiver: str = Field(..., description="The address that will own the position on the vault which will receive the shares")


DEPOSIT_PROMPT = """
This tool allows depositing assets into a Morpho Vault.
It takes:

- vault_address: The address of the Morpho Vault to deposit to
- asset_amount: The amount of assets to deposit in whole units
- asset_address: The address of the token to approve
- receiver: The address to receive the shares

Important notes:
- Make sure to use the exact amount provided. Do not convert units for assets for this action.
- Please use a token address (example 0x4200000000000000000000000000000000000006) for the asset_address field. If you are unsure of the token address, please clarify what the requested token address is before continuing.
"""


def deposit_to_morpho(
    wallet: Wallet,
    vault_address: str,  # pylint: disable=invalid-name
    asset_amount: str,  # pylint: disable=invalid-name
    asset_address: str,  # pylint: disable=invalid-name
    receiver: str,
) -> str:
    """Deposit assets into a Morpho Vault.

    Args:
        wallet (Wallet): The wallet to execute the deposit from
        vault_address (str): The address of the Morpho Vault
        asset_amount (str): The amount of assets to deposit in whole units (e.g., 0.01 WETH)
        receiver (str): The address to receive the shares
        asset_address (str): The address of the token to approve

    Returns:
        str: A success message with transaction hash or error message

    """
    if float(asset_amount) <= 0:
        return "Error: Assets amount must be greater than 0"
    tokenAsset = Asset.fetch(wallet.network_id, asset_address)
    atomicAssets = str(int(tokenAsset.to_atomic_amount(Decimal(asset_amount))))
    approvalResult = approve(wallet, asset_address, vault_address, atomicAssets)
    if approvalResult.startswith("Error"):
        return f"Error approving Morpho Vault as spender: {approvalResult}"
    depositArgs = {"assets": atomicAssets, "receiver": receiver}
    invocation = wallet.invoke_contract(
        contract_address=vault_address,
        method="deposit",
        abi=METAMORPHO_ABI,
        args=depositArgs,
    ).wait()
    return f"Deposited {atomicAssets} to Morpho Vault {vault_address} with transaction hash: {invocation.transaction_hash} and transaction link: {invocation.transaction_link}"


class MorphoDepositAction(CdpAction):
    """Morpho Vault deposit action."""

    name: str = "morpho_deposit"
    description: str = DEPOSIT_PROMPT
    args_schema: type[BaseModel] = MorphoDepositInput
    func: Callable[..., str] = deposit_to_morpho
