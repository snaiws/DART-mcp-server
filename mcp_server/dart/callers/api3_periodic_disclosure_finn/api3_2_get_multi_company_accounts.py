from apimanager import HttpxAPIManager



async def get_multi_company_accounts(
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
        "rcept_no": "접수번호",
        "bsns_year": "사업 연도",
        "stock_code": "상장회사 종목코드(6자리)",
        "reprt_code": "보고서 코드",
        "account_nm": "계정명",
        "fs_div": "개별/연결구분",
        "fs_nm": "개별/연결명",
        "sj_div": "재무제표항목",
        "sj_nm": "재무제표명",
        "thstrm_nm": "당기명",
        "thstrm_dt": "당기일자",
        "thstrm_amount": "당기금액",
        "thstrm_add_amount": "당기누적금액",
        "frmtrm_nm": "전기명",
        "frmtrm_dt": "전기일자",
        "frmtrm_amount": "전기금액",
        "frmtrm_add_amount": "전기누적금액",
        "bfefrmtrm_nm": "전전기명(사업보고서만)",
        "bfefrmtrm_dt": "전전기일자(사업보고서만)",
        "bfefrmtrm_amount": "전전기금액(사업보고서만)",
        "ord": "계정과목 정렬순서",
        "currency": "통화 단위"
    }

    transform2 = {
        "11013":"1분기보고서",
        "11012":"반기보고서",
        "11014":"3분기보고서",
        "11011":"사업보고서",
    }

    transform3 = {
        "OFS" : "개별재무제표",
        "CFS" : "연결재무제표"
    }

    transform4 = {
        "BS" : "재무상태표",
        "IS" : "손익계산서",
    }

    result = []
    for datum in data['list']:
        # 이중변환 처리
        datum['reprt_code'] = transform2[datum['reprt_code']]
        datum['fs_div'] = transform3[datum['fs_div']]
        datum['sj_div'] = transform4[datum['sj_div']]
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result
