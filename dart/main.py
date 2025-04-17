import os
import traceback
import json

from mcp.server.fastmcp import FastMCP

from corp_code import update_corplist, get_corpcode, get_corp_candidates
from corp_info import get_corpinfo



# Initialize FastMCP server
mcp = FastMCP("DART")

# constants
URL_CORPCODE = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={key}"
URL_CORPINFO = "https://opendart.fss.or.kr/api/company.json"
PATH_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'mcp', 'DART') # for Windows
os.makedirs(PATH_DIR, exist_ok=True)
PATH_CORPLIST = os.path.join(PATH_DIR, "CORPCODE.xml")

with open("termap.json", "r", encoding='utf-8') as f:
    TERMAP = json.load(f)

def format_dict(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    result = [f"{TERMAP.get(x, x)}: {feature[x]}" for x in feature]
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
    answer = ["[실행 결과]"]
    try:
        response = await update_corplist(URL_CORPCODE, key, PATH_CORPLIST)
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
    answer = ["[실행 결과]"]
    try:
        if os.path.exists(PATH_CORPLIST):
            response = await get_corpcode(PATH_CORPLIST, corp_name_input)
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
    answer = ["[실행 결과]"]
    try:
        if os.path.exists(PATH_CORPLIST):
            response = await get_corp_candidates(PATH_CORPLIST, corp_name_input, n)
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
    answer = ["[실행 결과]"]
    try:
        response = await get_corpinfo(key, URL_CORPINFO, corp_code)
        answer.append(format_dict(response))

    except Exception as e:
        error_msg = traceback.format_exc()
        answer.append(error_msg)

    return "\n---\n".join(answer)



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    pass