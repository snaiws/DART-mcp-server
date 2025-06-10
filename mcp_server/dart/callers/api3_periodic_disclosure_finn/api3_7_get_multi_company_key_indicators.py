from apimanager import HttpxAPIManager



async def get_multi_company_key_indicators(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bsns_year:str,
    reprt_code:str,
    idx_cl_code:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code,
        'idx_cl_code': idx_cl_code
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()
    
    transform1 = {
        "reprt_code": "보고서 종류",
        "bsns_year": "사업 연도",
        "corp_code": "공시대상회사 고유번호(8자리)",
        "stock_code": "상장회사 종목코드(6자리)",
        "stlm_dt": "결산기준일(YYYY-MM-DD)",
        "idx_cl_code": "지표분류코드",
        "idx_cl_nm": "지표분류명",
        "idx_code": "지표코드",
        "idx_nm": "지표명",
        "idx_val": "지표값" # 결과 없는 경우 존재
    }

    transform2 = {
        "11013":"1분기보고서",
        "11012":"반기보고서",
        "11014":"3분기보고서",
        "11011":"사업보고서",
    }

    result = []
    for datum in data['list']:
        # 보고서종류 처리
        datum['reprt_code'] = transform2[datum['reprt_code']]
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result
