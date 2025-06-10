from apimanager import HttpxAPIManager



async def get_audit_service_contract(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bsns_year:str, 
    reprt_code:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()
    
    transform1 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "고유번호(8자리)",
        "corp_name": "회사명",
        "bsns_year": "사업연도(당기, 전기, 전전기)",
        "adtor": "감사인",
        "cn": "내용",
        "mendng": "보수(2020년 7월 5일까지 사용된 사항)",
        "tot_reqre_time": "총소요시간(2020년 7월 5일까지 사용된 사항)",
        "adt_cntrct_dtls_mendng": "감사계약내역 보수(2020년 7월 6일부터 추가된 사항)",
        "adt_cntrct_dtls_time": "감사계약내역 시간(2020년 7월 6일부터 추가된 사항)",
        "real_exc_dtls_mendng": "실제수행내역 보수(2020년 7월 6일부터 추가된 사항)",
        "real_exc_dtls_time": "실제수행내역 시간(2020년 7월 6일부터 추가된 사항)",
        "stlm_dt": "결산기준일"
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

    