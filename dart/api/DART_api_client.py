from typing import Dict, Any, Optional
import logging

import httpx

from .base import BaseAPIClient



logger = logging.get()


class DARTAPIClient(BaseAPIClient):
    """
    DART 서버에 대한 비동기 HTTP API 클라이언트
    """
    def __init__(self, base_url, timeout: float = 10.0, 
                 rate_limit: int = 1000, rate_period: int = 60):
        super().__init__(base_url, timeout, rate_limit, rate_period)
        
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


    def _is_server_error(self, response):
        pass
    
    def _handle_response(self, response: httpx.Response):
        """HTTPX 응답 처리 및 에러 확인"""
        try:
            response.raise_for_status()
            return response
        except httpx.TimeoutException as e:
            self._handle_timeout_error(e)
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e, status_code=e.response.status_code, response=e.response)
        except httpx.RequestError as e:
            self._handle_request_error(e)
        except Exception as e:
            self._handle_unexpected_error(e)
        

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """GET 요청 수행"""
        await self._check_rate_limit()

        await self.open_client()
        async with self.client as api:
            response = await api.get(endpoint, params=params, headers=headers)
        return self._handle_response(response)
    

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                   json_data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """POST 요청 수행"""
        await self._check_rate_limit()

        await self.open_client()
        async with self.client as api:
            response = await api.post(endpoint, data=data, json=json_data, headers=headers)
        return self._handle_response(response)
    
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  json_data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PUT 요청 수행"""
        await self._check_rate_limit()

        await self.open_client()
        async with self.client as api:
            response = await api.put(endpoint, data=data, json=json_data, headers=headers)
        return self._handle_response(response)
    
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """DELETE 요청 수행"""
        await self._check_rate_limit()

        await self.open_client()
        async with self.client as api:
            response = await api.delete(endpoint, params=params, headers=headers)
        return self._handle_response(response)
    
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PATCH 요청 수행"""
        await self._check_rate_limit()

        await self.open_client()
        async with self.client as api:
            response = await api.patch(endpoint, data=data, json=json_data, headers=headers)
        return self._handle_response(response)
