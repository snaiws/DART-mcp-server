import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

@dataclass
class EnvDefineUnit:
    '''
    환경변수
    나중에 바뀌는 서버환경마다 적응시킬 수 있을까
    '''
    SERVER_NAME:str = "DART"
    BASE_URL:str = "https://opendart.fss.or.kr/api"
    PATH_BASE:str = os.getenv("PATH_DARTMCPSERVER", os.path.join(os.path.expanduser('~'), 'Documents', 'mcp', 'DART'))
    PATH_CORPLIST:str = os.getenv("PATH_DARTMCPSERVER_CORPLIST",os.path.join(PATH_BASE, "CORPCODE.xml"))
    API_KEY:str = os.getenv("DART_API_KEY", "")
    REGION:str = os.getenv("REGION","Asia/Seoul")
    CLIENT_MAX_PATIENT:float = 4.0
    API_RATE_LIMIT:int = 1000
    API_RATE_PERIOD:int = 60

    
    def to_dict(self):
        return asdict(self)
    

if __name__ == "__main__":
    import json
    endpoint = EnvDefineUnit()
    
    d = endpoint.to_dict()
    print(d)
    with open("endpoints.json", "w") as f:
        json.dump(d, f)
