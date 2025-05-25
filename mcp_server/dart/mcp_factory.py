from typing import Any, Type
from collections.abc import Sequence
from functools import partial
import inspect
import traceback

import mcp.types as types
from pydantic import ValidationError, BaseModel

from . import callers
from . import docstrings
from . import schemas


class McpFactory:
    def __init__(self, mcp, apiinfo):
        # Import modules dynamically
        self.mcp = mcp
        self.apiinfo = apiinfo
        self.function_module = callers
        self.docstring_module = docstrings
        self.schema_module = schemas


    def run(self):
        self.mcp.list_tools()(self.list_tools)
        self.mcp.call_tool()(self.call_tool)


    async def list_tools(self) -> list[types.Tool]: # self 조심. 데코레이터
        list_of_tools = [
            types.Tool(
                name = fn_name,
                description = self._get_matching_docstring(fn_name),
                inputSchema = self._get_matching_schema(fn_name).model_json_schema()
            )
            for fn_name in self.apiinfo
        ]
        return list_of_tools
    

    async def call_tool(
        self, name: str, arguments: Any
        ) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:

        if arguments is None:
            arguments = {}

        result = ""

        try:
            function = getattr(self.function_module, name)
            
            dynamic_args = self._get_matching_schema(name)(**arguments)
            dynamic_args = dict(dynamic_args)

            static_args = self.apiinfo[name]
            sig = inspect.signature(function)
            all_args = {}
            for param_name in sig.parameters:
                if param_name in static_args:
                    all_args[param_name] = static_args[param_name]

            all_args.update(dynamic_args)

            async def dynamic_function(*args, **kwargs):
                answer = ["[Execution result]"]
                try:
                    responses = await function(*args, **kwargs)
                    for i, response in enumerate(responses):
                        answer.append(f"result_{i+1} : {response}")
                except Exception as e:
                    error_msg = traceback.format_exc()
                    answer.append(f"error : {error_msg}")
                
                return "\n---\n".join(answer)
            
            result = await dynamic_function(**all_args)



        except ValidationError as e:
            await self.mcp.request_context.session.send_log_message(
                "error", "Failed to validate input provided by LLM: " + str(e)
            )
            return [
                types.TextContent(
                    type="text", text=f"ERROR: You provided invalid Tool inputs: {e}"
                )
            ]
        
        return [types.TextContent(type="text", text=result)]


    def _get_matching_docstring(self, function_name: str) -> str:
        # Simple case: direct match by name
        docstring_attr = f"Docstring_{function_name}"
        return getattr(self.docstring_module, docstring_attr).docstring
    

    def _get_matching_schema(self, function_name: str) -> Type[BaseModel]:
        # Simple case: direct match by name
        schema_attr = f"Schema_{function_name}"
        return getattr(self.schema_module, schema_attr)