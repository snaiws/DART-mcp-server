from apimanager import HttpxAPIManager



async def get_short_term_bond_balance(
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
        "remndr_exprtn1": "잔여만기",
        "remndr_exprtn2": "잔여만기",
        "de10_below": "10일 이하",
        "de10_excess_de30_below": "10일초과 30일이하",
        "de30_excess_de90_below": "30일초과 90일이하",
        "de90_excess_de180_below": "90일초과 180일이하",
        "de180_excess_yy1_below": "180일초과 1년이하",
        "sm": "합계",
        "isu_lmt": "발행 한도",
        "remndr_lmt": "잔여 한도",
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

    