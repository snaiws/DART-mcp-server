# 서버측 오류
from abc import ABC, abstractmethod



class APIServerError(ABC):
    """
    서버측 오류에 대한 커스텀 핸들링 클래스 인터페이스
    """
    @abstractmethod
    def handle(*args, **kwargs):
        pass

    @abstractmethod
    def is_server_error(response):
        pass