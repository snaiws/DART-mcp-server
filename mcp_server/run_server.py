import os
import asyncio
import argparse
import traceback

from mcp.server import Server
from mcp.server.stdio import stdio_server

from apimanager import HttpxAPIManager, APIServerError
from utils import setup_logger, get_now
from configs import ConfigDefineTool
from dart import McpFactory


parser = argparse.ArgumentParser()
parser.add_argument('--usecase', '-t', type=str, default='-', 
                   help='유즈케이스 (기본값: "모든 툴 로드")')
args = parser.parse_args()
usecase_key = args.usecase

app = Server("DART")


# 환경변수, 상수
config = ConfigDefineTool()
env = config.get_env()
mapping = config.get_mapping()
apiinfo = config.get_api().to_dict()
usecases = config.get_usecase().to_dict()

usecase = usecases.get(usecase_key, [])
if usecase:
    apiinfo = {key: apiinfo[key] for key in usecase if key in apiinfo}


# 내 문서에 mcp 서버용 디렉토리 생성(회사리스트, 로그)
os.makedirs(env.PATH_BASE, exist_ok=True)

# 로거 선언
now = get_now(env.REGION, form="%Y%m%d%H%M%S")
logger = setup_logger(env.PATH_BASE)

logger.info(f"server started, usecase = {usecase_key}")

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

factory = McpFactory(app, apiinfo)

factory.run()



async def run_stdio():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    # Initialize and run the server
    asyncio.run(run_stdio())
