from apimanager import HttpxAPIManager


async def get_overseas_delisting(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bgn_de:str, 
    end_de:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': bgn_de,
        'end_de': end_de
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()
    
    transform1 = {
        "rcept_no": "접수번호",
        "corp_cls": "법인구분", 
        "corp_code": "고유번호",
        "corp_name": "회사명",
        "lstex_nt": "상장거래소 및 소재국가",
        "dlststk_ostk_cnt": "상장폐지주식의 종류(보통주식(주))",
        "dlststk_estk_cnt": "상장폐지주식의 종류(기타주식(주))",
        "tredd": "매매거래종료일",
        "dlst_rs": "폐지사유",
        "cfd": "확인일자"
    }

    transform2 = {
        "Y":"유가",
        "K":"코스닥",
        "N":"코넥스",
        "E":"기타",
    }
    

    result = []
    for datum in data['list']:
        # 법인구분처리
        datum['corp_cls'] = transform2[datum['corp_cls']]
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result