import os
import traceback

from mcp.server.fastmcp import FastMCP

from corp_code import update_corplist, get_corpcode, get_corp_candidates



# Initialize FastMCP server
mcp = FastMCP("DART")

# constants
URL_CORPCODE = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={key}"
PATH_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'mcp', 'DART') # for Windows
os.makedirs(PATH_DIR, exist_ok=True)
PATH_CORPLIST = os.path.join(PATH_DIR, "CORPCODE.xml")


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

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    pass