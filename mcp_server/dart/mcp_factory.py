import os
from typing import Any, Type
from urllib.parse import urlparse, parse_qs
from collections.abc import Sequence
import datetime
import logging
import inspect
import traceback

import mcp.types as types
from pydantic import ValidationError, BaseModel

from . import callers
from . import docstrings
from . import schemas
from . import parser
# from . import prompts

logger = logging.getLogger()

class McpFactory:
    def __init__(self, mcp, apiinfo:dict):
        # Import modules dynamically
        self.mcp = mcp
        self.apiinfo = apiinfo
        self.parser_module = parser
        self.function_module = callers
        self.docstring_module = docstrings
        self.schema_module = schemas
        # self.prompt_module = prompts
        # self.prompts = {name:obj for name, obj in inspect.getmembers(prompts)}


    def run(self):
        self.mcp.list_tools()(self.list_tools)
        # self.mcp.list_prompts()(self.list_prompts)
        self.mcp.call_tool()(self.call_tool)
        # self.mcp.get_prompt()(self.get_prompt)


    # async def list_prompts(self) -> list[types.Prompt]:
    #     return list(self.prompts.keys())
    

    # async def get_prompt(self, name:str, arguments:dict[str,str] | None = None) -> types.GetPromptResult:
    #     return types.GetPromptResult(
    #         description=self.prompts[name].description,
    #         messages=[
    #             types.PromptMessage(
    #                 role=self.prompts[name].role,
    #                 content=types.TextContent(type="text", text=self.prompts[name].text)
    #             )
    #         ]
    #     )
    

    async def list_tools(self) -> list[types.Tool]: 
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
            function = getattr(self.function_module, name, None) or getattr(self.parser_module, name, None)
            if function is None:
                raise AttributeError(f"Function '{name}' not found in any module")
            
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