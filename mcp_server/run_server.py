import os
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server

from apimanager import HttpxAPIManager, APIServerError
from utils import setup_logger, get_now, Configs
from configs import EnvDefine, PathDefine, ToolDefine, UsecaseDefine
from dart import McpFactory


app = Server("DART")


# 환경변수, 상수
configs = Configs()
configs.add(EnvDefine())
configs.add(PathDefine())
configs.register_env()

usecase = UsecaseDefine().__dict__.get(configs.USECASE,"-")
tools = ToolDefine().__dict__


# 내 문서에 mcp 서버용 디렉토리 생성(회사리스트, 로그)
os.makedirs(configs.PATH_DATA, exist_ok=True)

# 로거 선언
now = get_now(configs.REGION, form="%Y%m%d%H%M%S")
logger = setup_logger(configs.PATH_DATA)

logger.info(f"server started, usecase = {configs.USECASE}")

# API 클라이언트 선언
class Dart_server_exception(APIServerError):
    def handle(response):
        raise Exception(response.json()['message'])


    def is_server_error(response):

        try:
            if response.json().get('status'):
                status = response.json()['status']
                if status == "000":
                    return False
                else:
                    return True
        except:
            return False
        
client = HttpxAPIManager(
    configs.BASE_URL, 
    timeout = configs.CLIENT_MAX_PATIENT, 
    rate_limit = configs.API_RATE_LIMIT, 
    rate_period = configs.API_RATE_PERIOD,
    exception_server_error = Dart_server_exception
    )

factory = McpFactory(mcp=app, apiinfo=tools)

factory.run()



async def run_stdio():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    # Initialize and run the server
    asyncio.run(run_stdio())
