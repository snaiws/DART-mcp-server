# 부가적인 오류처리
from typing import Optional

from .base import APIRequestError



class APIRateLimitExceeded(APIRequestError):
    """분당 요청 제한을 초과했을 때 발생하는 예외"""
    def __init__(self, message: str, status_code: Optional[int] = None, response=None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)



class APITimeoutError(APIRequestError):
    """API 요청 시간 초과 오류"""
    def __init__(self, message: str, status_code: Optional[int] = None, response=None):
        super().__init__(message,status_code,response)
