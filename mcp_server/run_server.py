import os
import traceback

from mcp.server.fastmcp import FastMCP

from apimanager import HttpxAPIManager, APIServerError
from utils import setup_logger, get_now
from configs import ConfigDefineTool
from dart import McpFactory

raise

mcp = FastMCP("DART")


# 환경변수, 상수
config = ConfigDefineTool()
env = config.get_env()
mapping = config.get_mapping()
apiinfo = config.get_api().to_dict()

# 내 문서에 mcp 서버용 디렉토리 생성(회사리스트, 로그)
os.makedirs(env.PATH_BASE, exist_ok=True)

# 로거 선언
now = get_now(env.REGION, form="%Y%m%d%H%M%S")
logger = setup_logger(env.PATH_BASE)

# API 클라이언트 선언
class Dart_server_exception(APIServerError):
    def handle(response):
        raise Exception(response.json()['message'])


    def is_server_error(response):
        if response.json().get('status'):
            status = response.json()['status']
            if status == "000":
                return False
            else:
                return True
                
client = HttpxAPIManager(
    env.BASE_URL, 
    timeout = env.CLIENT_MAX_PATIENT, 
    rate_limit = env.API_RATE_LIMIT, 
    rate_period = env.API_RATE_PERIOD,
    exception_server_error = Dart_server_exception
    )

factory = McpFactory(mcp, apiinfo)

factory.run()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
