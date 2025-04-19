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


async def get_corpcode(path_corplist, user_input):
    df = pd.read_xml(path_corplist)
    search = df[df['corp_name']==user_input]

    if not search.empty:
        search['corp_code'] = search['corp_code'].map(lambda x: str(x).zfill(8))
        return list(search.T.to_dict().values())
    
    search = df[df['corp_eng_name']==user_input]
    if not search.empty:
        search['corp_code'] = search['corp_code'].map(lambda x: str(x).zfill(8))
        return list(search.T.to_dict().values())
    
    return "딱 맞는 결과가 없습니다. get_corp_candidates를 사용하여 유사한 후보를 추려보세요."
    

async def get_corp_candidates(path_corplist, user_input, n):
    df = pd.read_xml(path_corplist)
    
    df['dist'] = df.apply(lambda row: max(
        safe_distance(user_input, row['corp_name']),
        safe_distance(user_input, row['corp_eng_name'])
    ), axis=1)

    search = df.sort_values(by='dist', ascending=False)
    search['corp_code'] = search['corp_code'].map(lambda x: str(x).zfill(8))
    return list(search.head(n).T.to_dict().values())



if __name__ == "__main__":
    path_corplist = "C:\\Users\\lghmk\\Documents\\mcp\\DART\\CORPCODE.xml"
    user_input = "진성전지"
    n = 5
    res = get_corp_candidates(path_corplist, user_input, n)
    # res = get_corpcode(path_corplist, user_input)
    # s1 = unicodedata.normalize('NFD', str('진성정주'))
    # s2 = unicodedata.normalize('NFD', str('진성전자'))
    # res = difflib.SequenceMatcher(None, s1, s2).ratio()
    print(res.sort_values(by='dist',ascending=False))