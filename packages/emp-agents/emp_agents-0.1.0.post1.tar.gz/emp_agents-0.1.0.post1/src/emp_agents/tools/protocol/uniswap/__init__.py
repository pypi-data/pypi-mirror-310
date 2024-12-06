import json
from typing import Annotated, Literal

from eth_typing import HexAddress, HexStr
from typing_extensions import Doc

from emp_agents.models.protocol import SkillSet, onchain_action, view_action

from .price import get_price
from .swap import (
    swap_exact_eth_for_tokens,
    swap_exact_tokens_for_eth,
    swap_exact_tokens_for_tokens,
)


class UniswapSkill(SkillSet):
    """
    Skills for interacting with UniswapV2.
    """

    @view_action
    @staticmethod
    async def get_price(
        network: Annotated[
            Literal["ethereum", "arbitrum", "base"],
            Doc("The network to query for price"),
        ],
        token_in: Annotated[HexAddress, Doc("The token to swap from")],
        token_out: Annotated[HexAddress, Doc("The token to swap to")],
    ) -> str:
        """Get the price of a token in terms of another token on UniswapV2"""

        price = await get_price(network, token_in, token_out)
        return json.dumps({"price": str(price)})

    @onchain_action
    @staticmethod
    async def swap(
        network: Annotated[
            Literal["ethereum", "arbitrum", "base"],
            Doc("The network to execute the swap on"),
        ],
        input_token: Annotated[
            HexAddress | None, Doc("The token to swap from.  None if ETH")
        ],
        output_token: Annotated[
            HexAddress | None, Doc("The token to swap to. None if ETH")
        ],
        amount_in: Annotated[float, Doc("The amount of tokens to swap")],
        recipient: Annotated[HexAddress, Doc("The recipient of the swapped tokens")],
        slippage: Annotated[float, Doc("The slippage tolerance")] = 0.01,
        deadline: Annotated[int | None, Doc("The deadline for the swap")] = None,
    ) -> HexStr:
        """Swap an exact amount of tokens for ETH.  Returns the transaction hash."""
        if input_token is None:
            if output_token is None:
                return "Invalid swap: both input and output tokens cannot be None"
            assert output_token is not None
            return await swap_exact_eth_for_tokens(
                network,
                output_token,
                amount_in,
                recipient,
                slippage,
                deadline,
            )
        elif output_token is None:
            return await swap_exact_tokens_for_eth(
                network,
                input_token,
                amount_in,
                recipient,
                slippage,
                deadline,
            )
        return await swap_exact_tokens_for_tokens(
            network,
            input_token,
            output_token,
            amount_in,
            recipient,
            slippage,
            deadline,
        )
