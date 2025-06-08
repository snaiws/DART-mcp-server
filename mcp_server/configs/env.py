import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

@dataclass
class EnvDefineUnit:
    '''
    파이썬 환경변수
    '''
    SERVER_NAME:str = os.getenv("SERVER_NAME", "DART")
    API_KEY:str = os.getenv("DART_API_KEY", "")
    USECASE:str = os.getenv("USECASE", "")
    PATH_DATA:str = os.getenv("PATH_DATA","")

    BASE_URL: "https://opendart.fss.or.kr/api",
    CLIENT_MAX_PATIENT: 4.0,
    API_RATE_LIMIT: 1000,
    API_RATE_PERIOD:60
    
    def to_dict(self):
        return asdict(self)
    

if __name__ == "__main__":
    import json
    endpoint = EnvDefineUnit()
    
    d = endpoint.to_dict()
    print(d)
    with open("endpoints.json", "w") as f:
        json.dump(d, f)
