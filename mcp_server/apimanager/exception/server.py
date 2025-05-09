# 서버측 오류
from typing import Dict, Any

from .base import APIRequestError



class APIServerError(APIRequestError):
    """서버 응답은 200이지만 내부 상태 코드가 오류를 나타내는 경우"""
    def __init__(self, message: str, status_code: str, response_data: Dict[str, Any]):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)