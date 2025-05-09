import os

import pandas as pd


async def get_corpcode(path_corplist, user_input):
    if not os.path.exists(path_corplist):
        return ["there is no corp_list file."]
    df = pd.read_xml(path_corplist)
    search = df[df['corp_name']==user_input]

    if not search.empty:
        search['corp_code'] = search['corp_code'].map(lambda x: str(x).zfill(8))
        return list(search.T.to_dict().values())
    
    search = df[df['corp_eng_name']==user_input]
    if not search.empty:
        search['corp_code'] = search['corp_code'].map(lambda x: str(x).zfill(8))
        return list(search.T.to_dict().values())
    
    return ["딱 맞는 결과가 없습니다. get_corp_candidates를 사용하여 유사한 후보를 추려보세요."]
    



if __name__ == "__main__":
    path_corplist = "C:\\Users\\lghmk\\Documents\\mcp\\DART\\CORPCODE.xml"
    user_input = "진성전지"
    res = get_corpcode(path_corplist, user_input)