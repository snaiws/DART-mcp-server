import os

import pandas as pd

import unicodedata
import difflib



def safe_distance(s1, s2):
    # NaN이나 None 값 처리
    if pd.isna(s1) or pd.isna(s2):
        return 0  # NaN인 경우 무한대 거리 반환
    # 분해 변환
    s1, s2 = unicodedata.normalize('NFD', str(s1)), unicodedata.normalize('NFD', str(s2))
    return difflib.SequenceMatcher(None,s1, s2).ratio()


async def get_corp_candidates(path_corplist:str, user_input:str, n:int):
    if not os.path.exists(path_corplist):
        return ["there is no corp_list file."]
    df = pd.read_xml(path_corplist)
    
    df['dist'] = df.apply(lambda row: max(
        safe_distance(user_input, row['corp_name']),
        safe_distance(user_input, row['corp_eng_name'])
    ), axis=1)

    search = df.sort_values(by='dist', ascending=False)
    search['corp_code'] = search['corp_code'].map(lambda x: str(x).zfill(8))
    return list(search.head(n).T.to_dict().values())

    

# 사용 예시
if __name__ == "__main__":
    import os
    import asyncio
    
    async def test():
    # uv run -m dart.callers.api1_disclosure_info.api1_6_search_candidates
        path_corplist = os.path.join(os.path.expanduser('~'), 'Documents', 'mcp', 'DART', 'CORPCODE.xml')
        user_input = "진성전지"
        n = 5
        res = await get_corp_candidates(path_corplist, user_input, n)

        print(res)
        return res

    
    asyncio.run(test())