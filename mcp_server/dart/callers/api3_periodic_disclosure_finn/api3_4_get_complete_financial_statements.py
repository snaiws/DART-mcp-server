from apimanager import HttpxAPIManager



async def get_complete_financial_statements(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bsns_year:str,
    reprt_code:str,
    fs_div:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code,
        'fs_div' : fs_div
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()

    transform1 = {
        "rcept_no": "접수번호(14자리)",
        "reprt_code": "보고서 코드",
        "bsns_year": "사업 연도",
        "corp_code": "고유번호 (공시대상회사 8자리 코드)",
        "sj_div": "재무제표구분",
        "sj_nm": "재무제표명 (재무상태표 또는 손익계산서 등)",
        "account_id": "계정ID (XBRL 표준계정ID)",
        "account_nm": "계정명 (계정명칭",
        "account_detail": "계정상세 (자본변동표에만 출력되는 상세명칭)",
        "thstrm_nm": "당기명",
        "thstrm_amount": "당기금액 (분/반기 손익계산서는 3개월 금액)",
        "thstrm_add_amount": "당기누적금액",
        "frmtrm_nm": "전기명",
        "frmtrm_amount": "전기금액",
        "frmtrm_q_nm": "전기명(분/반기)",
        "frmtrm_q_amount": "전기금액(분/반기) (분/반기 손익계산서는 3개월 금액)",
        "frmtrm_add_amount": "전기누적금액",
        "bfefrmtrm_nm": "전전기명 (사업보고서만)",
        "bfefrmtrm_amount": "전전기금액 (사업보고서만)",
        "ord": "계정과목 정렬순서",
        "currency": "통화 단위"
    }

    transform2 = {
        "11013":"1분기보고서",
        "11012":"반기보고서",
        "11014":"3분기보고서",
        "11011":"사업보고서",
    }


    transform4 = {
        "BS" : "재무상태표",
        "IS" : "손익계산서",
        "CIS" : "포괄손익계산서",
        "CF" : "현금흐름표",
        "SCE" : "자본변동표",
    }

    result = []
    for datum in data['list']:
        # 이중변환 처리
        datum['reprt_code'] = transform2[datum['reprt_code']]
        datum['sj_div'] = transform4[datum['sj_div']]
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result
