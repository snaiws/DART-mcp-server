from apimanager import HttpxAPIManager



async def get_xbrl_taxonomy_format(
    base_url:str,
    endpoint:str,
    api_key:str, 
    sj_div:str, 
    )->list:
    params = {
        'crtfc_key': api_key,
        'sj_div': sj_div,
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()

    transform1 = {
        "sj_div": "재무제표구분",
        "account_id": "계정ID",
        "account_nm": "계정명",
        "bsns_de": "적용 기준일",
        "label_kor": "한글 출력명",
        "label_eng": "영문 출력명",
        "data_tp": "데이터 유형(text block(제목), Text(텍스트), yyyy-mm-dd(날짜), X(화폐단위), (X)(음수 화폐단위), X.XX(소수점), Shares(주식수), For each(반복공시), 공란(입력불필요))",
        "ifrs_ref": "IFRS Reference"
    }

    result = []
    for datum in data['list']:
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result
