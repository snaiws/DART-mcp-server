from abc import ABC, abstractmethod
import asyncio
import time
from typing import Dict, Any, Optional, ClassVar
import logging

from .exception import APIRequestError, APIServerError, APITimeoutError, APIRateLimitExceeded



logger = logging.getLogger()


class BaseAPIManager(ABC):
    """
    싱글턴 템플릿 메소드 어댑터
    분당 최대 1000회 요청 제한이 있음
    """
    _instances: ClassVar[Dict[str, 'BaseAPIManager']] = {}
    _lock = asyncio.Lock()
    
    def __new__(cls, base_url, *args, **kwargs):
        # base_url을 키로 사용하여 인스턴스 관리
        if base_url not in cls._instances:
            cls._instances[base_url] = super(BaseAPIManager, cls).__new__(cls)
        return cls._instances[base_url]
    
    def __init__(self, base_url, 
                 timeout: float = None, 
                 rate_limit: int = None, 
                 rate_period: int = None,
                 exception_server_error: APIServerError = None,
                 ):
        # 이미 초기화된 경우 중복 초기화 방지
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.base_url = base_url
        self.timeout = timeout
        self.rate_limit = rate_limit  # 분당 최대 요청 수
        self.rate_period = rate_period  # 초 단위 기간 (60초 = 1분)
        self.exception_server_error = exception_server_error
        self._request_timestamps = []  # 요청 타임스탬프 기록
        
        self._initialized = True
    
    async def __aenter__(self):
        '''
        아래처럼 사용 가능
        async with APIClient(base_url="https://api.example.com") as api:
            response = await api.get("/endpoint")
        '''
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        '''
        아래처럼 사용 가능
        async with APIClient(base_url="https://api.example.com") as api:
            response = await api.get("/endpoint")
        '''
        await self.close()

    @abstractmethod
    async def open_client(self):
        '''
        어댑터, 항상 여는게 아니라 사용할 때만 연결하도록 get 메소드 등에서 구현
        '''
        pass


    @abstractmethod
    async def close(self):
        pass
    
    async def _check_rate_limit(self):
        """요청 속도 제한 확인"""

        current_time = time.time()
        
        # 현재 타임스탬프 추가
        self._request_timestamps.append(current_time)
        
        # rate_period 시간 이전의 타임스탬프 제거
        cutoff = current_time - self.rate_period
        self._request_timestamps = [ts for ts in self._request_timestamps if ts > cutoff]
        
        # 현재 기간 내 요청 수 확인
        if len(self._request_timestamps) > self.rate_limit:
            oldest = min(self._request_timestamps)
            reset_time = oldest + self.rate_period - current_time
            raise APIRateLimitExceeded(
                f"Rate limit exceeded: {len(self._request_timestamps)} requests in {self.rate_period}s. "
                f"Try again in {reset_time:.2f} seconds."
            )
    
    @abstractmethod
    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """GET 요청 수행"""
        pass
    
    @abstractmethod
    async def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                   json_data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """POST 요청 수행"""
        pass
    
    @abstractmethod
    async def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  json_data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PUT 요청 수행"""
        pass
    
    @abstractmethod
    async def _delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """DELETE 요청 수행"""
        pass
    
    @abstractmethod
    async def _patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PATCH 요청 수행"""
        pass


    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """GET 요청 수행"""
        await self._check_rate_limit()
        await self.open_client()
        logger.debug(endpoint)
        response = await self._get(
            endpoint=endpoint,
            params=params,
            headers=headers
            )
        return self._handle_response(response)
        
    
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                   json_data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """POST 요청 수행"""
        await self._check_rate_limit()
        await self.open_client()
        logger.debug(endpoint)
        response = await self._post(
            endpoint=endpoint,
            data=data,
            json_data=json_data,
            headers=headers
            )
        return self._handle_response(response)
    
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  json_data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PUT 요청 수행"""
        await self._check_rate_limit()
        await self.open_client()
        logger.debug(endpoint)
        response = await self._put(
            endpoint=endpoint,
            data=data,
            json_data=json_data,
            headers=headers
            )
        return self._handle_response(response)
    
    
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """DELETE 요청 수행"""
        await self._check_rate_limit()
        await self.open_client()
        logger.debug(endpoint)
        response = await self._delete(
            endpoint=endpoint,
            params=params,
            headers=headers
            )
        return self._handle_response(response)
    
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """PATCH 요청 수행"""
        await self._check_rate_limit()
        await self.open_client()
        logger.debug(endpoint)
        response = await self._patch(
            endpoint=endpoint,
            data=data,
            json_data=json_data,
            headers=headers
            )
        return self._handle_response(response)


    @abstractmethod
    def _handle_response(self, response):
        """응답 처리 및 에러 확인"""
        try:
            response.raise_for_status()
            if self._is_server_error(response):
                self._handle_server_error(response)
            else:
                return response
        except:
            pass
    

    def _handle_timeout_error(self, error):
        """타임아웃 에러 처리 헬퍼 메소드"""
        error_msg = f"Request timed out: {str(error)}"
        logger.error(error_msg)
        raise APITimeoutError(error_msg)
    
    def _handle_http_error(self, error, status_code=None, response=None):
        """HTTP 에러 처리 헬퍼 메소드"""
        error_msg = f"HTTP error occurred: {status_code} - {str(error)}"
        logger.error(error_msg)
        raise APIRequestError(error_msg, status_code=status_code, response=response)
    
    def _handle_request_error(self, error):
        """요청 에러 처리 헬퍼 메소드"""
        error_msg = f"Request error occurred: {str(error)}"
        logger.error(error_msg)
        raise APIRequestError(error_msg)
    
    
    def _handle_unexpected_error(self, error):
        """예상치 못한 에러 처리 헬퍼 메소드"""
        error_msg = f"Unexpected error: {str(error)}"
        logger.error(error_msg)
        raise APIRequestError(error_msg)


    def _handle_server_error(self, response):
        """서버 에러 처리 헬퍼 메소드"""
        if self.exception_server_error is None:
            pass
        self.exception_server_error.handle(response)


    def _is_server_error(self, response):
        if self.exception_server_error is None:
            return False
        return self.exception_server_error.is_server_error(response)