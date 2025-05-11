from typing import Dict, Any, Optional

import httpx

from .base import BaseAPIManager



class HttpxAPIManager(BaseAPIManager):
    """
    Httpx 비동기 API 매니저
    """
    def __init__(
        self, 
        base_url, 
        timeout: float = 10.0, 
        rate_limit: int = 1000, 
        rate_period: int = 60, 
        exception_server_error = None
        ):
        super().__init__(
            base_url = base_url, 
            timeout =timeout, 
            rate_limit = rate_limit, 
            rate_period = rate_period, 
            exception_server_error = exception_server_error)
        
        # HTTP 클라이언트 생성
        self._initialized = True

    async def open_client(self):
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout
        )
    
    async def close(self):
        """클라이언트 세션 종료"""
        if hasattr(self, 'client'):
            await self.client.aclose()

    
    def _handle_response(self, response: httpx.Response):
        """HTTPX 응답 처리 및 에러 확인"""
        try:
            response.raise_for_status()
        except httpx.TimeoutException as e:
            self._handle_timeout_error(e)
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e, status_code=e.response.status_code, response=e.response)
        except httpx.RequestError as e:
            self._handle_request_error(e)
        except Exception as e:
            self._handle_unexpected_error(e)
        
        if self._is_server_error(response):
            self._handle_server_error(response)
        else:
            return response

            

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """GET 요청 수행"""
        async with self.client as api:
            response = await api.get(endpoint, params=params, headers=headers)
        return response
    

    async def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                   json_data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """POST 요청 수행"""
        async with self.client as api:
            response = await api.post(endpoint, data=data, json=json_data, headers=headers)
        return response
    
    
    async def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  json_data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PUT 요청 수행"""
        async with self.client as api:
            response = await api.put(endpoint, data=data, json=json_data, headers=headers)
        return response
    
    
    async def _delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """DELETE 요청 수행"""
        async with self.client as api:
            response = await api.delete(endpoint, params=params, headers=headers)
        return response
    
    
    async def _patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PATCH 요청 수행"""
        async with self.client as api:
            response = await api.patch(endpoint, data=data, json=json_data, headers=headers)
        return response
