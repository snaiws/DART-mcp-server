import os
import traceback
import json

from mcp.server.fastmcp import FastMCP

from api import DARTAPIClient
from search_info import get_corpinfo, update_corplist, get_corpcode, get_corp_candidates, get_disclosurelist
from periodic_disclosure import get_capitalstatus
from utils import setup_logger, get_now
from configs import ConfigDefineTool


# 환경변수, 상수
config = ConfigDefineTool()
env = config.get_env()
endpoint = config.get_endpoint()

# 내 문서에 mcp 서버용 디렉토리 생성(회사리스트, 로그)
os.makedirs(env.PATH_BASE, exist_ok=True)

# 로거 선언
now = get_now(env.REGION, form="%Y%m%d%H%M%S")
logger = setup_logger(env.PATH_BASE, now)

# API 클라이언트 선언
client = DARTAPIClient(
    env.BASE_URL, 
    logger, 
    timeout = env.CLIENT_MAX_PATIENT, 
    rate_limit = env.API_RATE_LIMIT, 
    rate_period = env.API_RATE_PERIOD
    )

# MCP 서버 선언
mcp = FastMCP(env.SERVER_NAME)


# mcp 템플릿
def format_dict(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    result = [f"{x}: {feature[x]}" for x in feature]
    result = "\n".join(result)
    return result


@mcp.tool()
async def mcp_update_corplist(key:str) -> str:
    """download corp_list, that contains corp_code/corp_name, for using other APIs. 

    Args:
        key(str): API Key for DART system. Ask to user to get this.
    Return:
        response(str): answering corp_code or questioning candidates
    """
    answer = ["[Execution result]"]
    try:
        response = await update_corplist(client, endpoint.URL_CORPCODE, key, env.PATH_CORPLIST)
        answer.append(f"응답코드 : {response}")
    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)
    
    return "\n---\n".join(answer)
        

@mcp.tool()
async def mcp_get_corpcode(corp_name_input:str) -> str:
    """Get corp_code for using other APIs. 

    Args:
        corp_name_input(str): a corp name that user requested. Korean or English name available.
    Return:
        response(str): answering corp_code
    """
    answer = ["[Execution result]"]
    try:
        if os.path.exists(env.PATH_CORPLIST):
            response = await get_corpcode(env.PATH_CORPLIST, corp_name_input)
            answer.append(f"corp_code : {response}")
        else:
            answer.append("there is no corp_list file.")
    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)

    return "\n---\n".join(answer)


@mcp.tool()
async def mcp_get_corp_candidates(corp_name_input:str, n:int) -> str:
    """Use this when user-requested-corp-name is not exactly matching official corp-names.
if a company reveals twice in the result, select recent one using modify_date.
    Args:
        corp_name_input(str): a corp name that user requested. Korean or English name available.
        n(int) : number of candidates
    Return:
        response(str): corp candidates that is similar to user-request
    """
    answer = ["[Execution result]"]
    try:
        if os.path.exists(env.PATH_CORPLIST):
            response = await get_corp_candidates(env.PATH_CORPLIST, corp_name_input, n)
            answer.append(f"후보 목록 :\n{response}")
        else:
            answer.append("there is no corp_list file.")
    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)

    return "\n---\n".join(answer)


@mcp.tool()
async def mcp_get_corp_info(key:str, corp_code:str) -> str:
    """Get rough infomation of a company(기업개황) from DART system.

    Args:
        key(str): API Key for DART system. Ask to user to get this.
        corp_code(str) : a unique code of a company, which is used in DART system.(8 lengths)
    Return:
        response(str): a message including information()
    """
    answer = ["[Execution result]"]
    try:
        response = await get_corpinfo(client, endpoint.URL_CORPINFO, key, corp_code)
        answer.append(format_dict(response))

    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)

    return "\n---\n".join(answer)


@mcp.tool()
async def mcp_get_disclosurelist(key:str, corp_code:str, bgn_de:str, end_de:str, last_reprt_at:str,
                                 pblntf_ty:str, pblntf_detail_ty:str, corp_cls:str, sort:str, sort_mth:str, 
                                 page_no:int, page_count:int) -> str:
    """Get list of disclosure of a company. you can narrow the result by optional inputs.

    Args:
        key (str): API Key for DART system. Ask to user to get this.
        corp_code(str) : a unique code of a company, which is used in DART system.(8 lengths)
        bgn_de (str): Start date for search (YYYYMMDD)
        end_de (str): End date for search (YYYYMMDD)
        last_reprt_at (str, optional): Search only final reports (Y or N, default: N)  
        pblntf_ty (str, optional): Disclosure type (A, B, C, D, E, F, G, H, I, J)  
        pblntf_detail_ty (str, optional): Detailed disclosure type  
        corp_cls (str, optional): Corporation classification (Y: KOSPI, K: KOSDAQ, N: KONEX, E: Etc)  
        sort (str, optional): Sort field (date: Filing date, crp: Company name, rpt: Report name, default: date)  
        sort_mth (str, optional): Sort order (asc: Ascending, desc: Descending, default: desc)  
        page_no (int, optional): Page number (1~n, default: 1)  
        page_count (int, optional): Number of items per page (1~100, default: 10, max: 100)  
    Return:
        response(str): a message including information()
    """
    answer = ["[Execution result]"]
    try:
        response = await get_disclosurelist(client, endpoint.URL_DICSLIST, key, corp_code, bgn_de, end_de,
                                      last_reprt_at, pblntf_ty, pblntf_detail_ty, corp_cls, sort,
                                      sort_mth, page_no, page_count)
        answer.append(format_dict(response))

    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)

    return "\n---\n".join(answer)


# 정기보고서 주요정보 - 증자(감자) 현황
@mcp.tool()
async def mcp_get_capitalstatus(key:str, corp_code:str, bsns_year:str, reprt_code:str) -> str:
    """Get infomation of a company's capital status from it's periodic disclosure in DART system.(증자/감자 현황)

    Args:
        key(str): API Key for DART system. Ask to user to get this.
        corp_code(str) : a unique code of a company, which is used in DART system.(8 lengths)
        bsns_year(str) : business year for which capital status is reported(4 lengths, available after of 2015)
        reprt_code(str) : a unique code of a period(1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011)
    Return:
        response(str): a message including information()
    """
    answer = ["[실행 결과]"]
    try:
        response = await get_capitalstatus(client, endpoint.URL_CORPINFO, key, corp_code, bsns_year, reprt_code)
        answer.append(format_dict(response))

    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)

    return "\n---\n".join(answer)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')