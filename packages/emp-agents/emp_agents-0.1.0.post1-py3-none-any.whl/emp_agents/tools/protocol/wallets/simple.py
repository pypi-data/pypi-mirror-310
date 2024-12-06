from contextvars import ContextVar
from typing import Optional

from eth_rpc import PrivateKeyWallet

from emp_agents.models.protocol import SkillSet, tool_method

# Context variable to store private key
_private_key: ContextVar[Optional[str]] = ContextVar("_private_key", default=None)


class SimpleWalletSkill(SkillSet):
    """A simple wallet tool that stores private key in memory using context vars"""

    @tool_method
    @staticmethod
    def create_wallet() -> str:
        """Create a new private key wallet"""

        wallet = PrivateKeyWallet.create_new()
        _private_key.set(wallet.private_key)
        return (
            f"Wallet created: {wallet.address} with private key: {wallet.private_key}"
        )

    @tool_method
    @staticmethod
    def set_private_key(private_key: str) -> str:
        """Set the private key in the context"""

        _private_key.set(private_key)
        return "Private key set successfully"

    @tool_method
    @staticmethod
    def get_private_key() -> str:
        """Get the private key from the context"""

        key = _private_key.get()
        if key is None:
            return "No private key set"
        return key

    @tool_method
    @staticmethod
    def clear_private_key() -> str:
        """Clear the private key from the context"""

        _private_key.set(None)
        return "Private key cleared"

    @tool_method
    @staticmethod
    def get_address() -> str:
        """Get the address of the wallet"""

        key = _private_key.get()
        if key is None:
            return "No private key set"
        wallet = PrivateKeyWallet(private_key=key)
        return wallet.address
