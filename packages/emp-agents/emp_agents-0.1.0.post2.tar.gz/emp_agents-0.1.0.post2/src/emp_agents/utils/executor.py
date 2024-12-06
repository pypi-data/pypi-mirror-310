import logging
from asyncio import iscoroutine
from typing import Any

from pydantic.types import Json


async def execute_tool(
    tools_map,
    function_name: str,
    arguments: Json[Any],
):
    logging.debug(f"EXECUTING TOOL {function_name} with arguments {arguments}")

    func = tools_map[function_name]
    response = func(**arguments)
    if iscoroutine(response):
        return await response
    return response
