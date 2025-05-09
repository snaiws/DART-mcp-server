import os
import traceback

from mcp.server.fastmcp import FastMCP

from apimanager import HttpxAPIManager
from utils import setup_logger, get_now
from configs import ConfigDefineTool
from dart import McpFactory



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
client = HttpxAPIManager(
    env.BASE_URL, 
    timeout = env.CLIENT_MAX_PATIENT, 
    rate_limit = env.API_RATE_LIMIT, 
    rate_period = env.API_RATE_PERIOD
    )

factory = McpFactory(mcp, apiinfo)

factory.run()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
