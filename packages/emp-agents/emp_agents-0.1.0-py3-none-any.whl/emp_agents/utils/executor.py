from asyncio import iscoroutine
from typing import Any

from pydantic.types import Json


async def execute_tool(tools_map, function_name: str, arguments: Json[Any]):
    print("EXECUTING TOOL", function_name, arguments)

    func = tools_map[function_name]
    response = func(**arguments)
    if iscoroutine(response):
        return await response
    return response
