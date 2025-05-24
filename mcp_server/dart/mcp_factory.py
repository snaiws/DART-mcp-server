from typing import Callable
import inspect
import traceback

import mcp.types as types

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
        for apiname in self.apiinfo:
            self.create_function(function_name = apiname, params = self.apiinfo[apiname])


    def create_function(self, function_name: str, params:dict) -> Callable:
        
        # Get original function
        function = getattr(callers, function_name)
        # Get matching docstring
        docstring = self._get_matching_docstring(function_name)
        
        
        # 새로운 시그니처 생성 (고정된 파라미터는 제외)
        signature = inspect.signature(function)
        valid_params = set(signature.parameters.keys())

        # 함수 정의
        async def dynamic_function(*args, **kwargs):
            answer = ["[Execution result]"]
            try:
                # 사용자 제공 kwargs에 고정된 params 값을 추가 (사용자 값이 우선)
                merged_kwargs = {}
                
                # params 딕셔너리에서 유효한 파라미터만 포함
                for key, value in params.items():
                    if key in valid_params:
                        merged_kwargs[key] = value

                kwargs.update(merged_kwargs)

                responses = await function(*args, **kwargs)
                for i, response in enumerate(responses):
                    answer.append(f"result_{i+1} : {response}")
            except Exception as e:
                error_msg = traceback.format_exc()
                answer.append(f"error : {error_msg}")
            
            return "\n---\n".join(answer)
        
        # 함수 속성 설정
        dynamic_function.__name__ = function_name
        dynamic_function.__doc__ = docstring
        dynamic_function.__signature__ = signature
        
        # mcp.tool() 데코레이터 적용
        wrapped_function = self.mcp.tool()(dynamic_function)
        
        return wrapped_function


    def _get_matching_docstring(self, function_name: str) -> str:
        """
        Find the appropriate docstring based on function name and parameters.
        
        Args:
            function_name: Name of the function to match
            parameters: Parameters that might affect which docstring to use
            
        Returns:
            The matching docstring
        """
        # Simple case: direct match by name
        docstring_attr = f"Docstring_{function_name}"
        return getattr(docstrings, docstring_attr).docstring