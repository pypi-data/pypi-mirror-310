from collections.abc import Callable
from typing import Annotated, Optional

import httpx
from eth_rpc import PrivateKeyWallet
from eth_rpc.networks import get_network_by_name
from eth_typeshed import ERC20
from eth_typeshed.multicall import make_multicall
from fast_depends import Provider
from typing_extensions import Doc

from emp_agents.implicits import Depends, IgnoreDepends, inject
from emp_agents.models.protocol import SkillSet, onchain_action, view_action

from ..network import NetworkOptions, NetworkSkill

wallet_provider = Provider()


def load_wallet() -> PrivateKeyWallet:
    """
    This can be overridden by using the scope for your agent.
    Use `scope_load_wallet` to scope this method.
    """
    raise NotImplementedError("Scope this method so your agent can access it's wallet")


def scope_load_wallet(
    new_load_wallet: Callable[..., PrivateKeyWallet]
) -> tuple[Provider, Callable, Callable]:
    return (wallet_provider, load_wallet, new_load_wallet)


class ERC20Skill(SkillSet):
    """
    Tools for interacting with ERC20 tokens.
    """

    @view_action
    @staticmethod
    async def describe_protocol():
        """Returns the complete protocol specification of the ERC20 protocol"""

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://raw.githubusercontent.com/ethereum/ercs/refs/heads/master/ERCS/erc-20.md"
            )
            return response.text

    @view_action
    @staticmethod
    @inject
    async def get_token_info(
        token_address: Annotated[str, Doc("The address of the ERC20 token.")],
        network: Annotated[
            NetworkOptions,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
    ) -> str:
        """Returns the name, symbol and decimals for an ERC20 token"""

        try:
            network_type = get_network_by_name(network)
        except ValueError:
            return "Invalid network"

        token = ERC20[network_type](address=token_address)

        multicall = make_multicall(network_type)
        try:
            (name, symbol, decimals) = await multicall[network_type].execute(
                token.name(), token.symbol(), token.decimals()
            )
        except Exception as e:
            return f"Error getting token info: {e}"

        return f"name: {name}; symbol: {symbol}; decimals: {decimals}"

    @view_action
    @staticmethod
    @inject
    async def get_balance(
        token_address: Annotated[str, Doc("The address of the ERC20 token.")],
        address: Annotated[
            str, Doc("The address of the account to get the balance of.")
        ],
        decimals: Annotated[
            Optional[int], Doc("How many decimals the token has")
        ] = None,
        network: Annotated[
            NetworkOptions,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
    ) -> str:
        """Returns the balance of an account for an ERC20 token"""

        try:
            network_type = get_network_by_name(network)
        except ValueError:
            return "Invalid network, try setting the network first"

        token = ERC20[network_type](address=token_address)
        balance = await token.balance_of(address).get()
        if not decimals:
            decimals = await token.decimals().get()
        assert decimals is not None
        return f"Balance: {balance / 10 ** decimals}"

    @onchain_action
    @staticmethod
    @inject(dependency_overrides_provider=wallet_provider)  # type: ignore
    async def transfer(
        token_address: Annotated[str, Doc("The address of the ERC20 token.")],
        to_address: Annotated[str, Doc("The address of the account to transfer to.")],
        amount: Annotated[float, Doc("The amount to transfer as a decimal.")],
        wallet: Annotated[
            PrivateKeyWallet, Doc("The wallet to use to transfer the token.")
        ] = IgnoreDepends(load_wallet),
        network: Annotated[
            NetworkOptions,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
    ) -> str:
        """Transfer an amount of an ERC20 token to a recipient"""

        try:
            network_type = get_network_by_name(network)
        except ValueError:
            return "Invalid network"

        token = ERC20[network_type](address=token_address)
        decimals = await token.decimals().get()
        token_amount = int(amount * 10**decimals)
        tx = await token.transfer(to_address, token_amount).execute(wallet)
        return f"Transaction sent: {tx}"

    @onchain_action
    @staticmethod
    @inject(dependency_overrides_provider=wallet_provider)  # type: ignore
    async def approve(
        token_address: Annotated[str, Doc("The address of the ERC20 token.")],
        spender: Annotated[str, Doc("The address of the account to transfer to.")],
        amount: Annotated[float, Doc("The amount to transfer.")],
        network: Annotated[
            NetworkOptions,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
        wallet: Annotated[
            PrivateKeyWallet, Doc("The wallet to use to transfer the token.")
        ] = IgnoreDepends(load_wallet),
    ) -> str:
        """Approve an amount of an ERC20 token to be spent by a spender"""

        try:
            network_type = get_network_by_name(network)
        except ValueError:
            return "Invalid network"

        token = ERC20[network_type](address=token_address)
        tx = await token.approve(spender, amount).execute(wallet)
        return f"Transaction sent: {tx.hash}"

    @onchain_action
    @staticmethod
    @inject(dependency_overrides_provider=wallet_provider)  # type: ignore
    async def transfer_from(
        token_address: Annotated[str, Doc("The address of the ERC20 token.")],
        from_address: Annotated[
            str, Doc("The address of the account to transfer from.")
        ],
        to_address: Annotated[str, Doc("The address of the account to transfer to.")],
        amount: Annotated[float, Doc("The amount to transfer.")],
        network: Annotated[
            NetworkOptions,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
        wallet: Annotated[
            PrivateKeyWallet, Doc("The wallet to use to transfer the token.")
        ] = IgnoreDepends(load_wallet),
    ) -> str:
        """Transfer an amount of an ERC20 token from an external, approved account to another account"""

        try:
            network_type = get_network_by_name(network)
        except ValueError:
            return "Invalid network, try setting the network first"

        token = ERC20[network_type](address=token_address)
        tx = await token.transfer_from(from_address, to_address, amount).execute(wallet)
        return f"Transaction sent: {tx.hash}"
