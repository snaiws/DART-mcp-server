# 기본 API 예외처리
from typing import Optional

class APIRequestError(Exception):
    """API 요청 중 발생하는 일반적인 오류"""
    def __init__(self, message: str, status_code: Optional[int] = None, response=None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)