import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

@dataclass
class EnvDefine:
    '''
    파이썬 환경변수
    '''
    SERVER_NAME:str = os.getenv("SERVER_NAME", "DART")
    REGION:str = os.getenv("REGION", "Asia/Seoul")
    DART_API_KEY:str = os.getenv("DART_API_KEY")
    USECASE:str = os.getenv("USECASE", "-")
    PATH_DATA:str = os.getenv("PATH_DATA",".")

    BASE_URL:str ="https://opendart.fss.or.kr/api"
    CLIENT_MAX_PATIENT:float =4.0
    API_RATE_LIMIT:int =1000
    API_RATE_PERIOD:int=60
    