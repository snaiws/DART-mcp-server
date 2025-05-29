from apimanager import HttpxAPIManager



async def get_contingent_convertible_balance(
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
        "yy1_below": "1년 이하",
        "yy1_excess_yy2_below": "1년초과 2년이하",
        "yy2_excess_yy3_below": "2년초과 3년이하",
        "yy3_excess_yy4_below": "3년초과 4년이하",
        "yy4_excess_yy5_below": "4년초과 5년이하",
        "yy5_excess_yy10_below": "5년초과 10년이하",
        "yy10_excess_yy20_below": "10년초과 20년이하",
        "yy20_excess_yy30_below": "20년초과 30년이하",
        "yy30_excess": "30년초과",
        "sm": "합계",
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
        datum = [f"{transform1[k]}: {datum[k]}" for k in transform1 if datum.get(k,"")]
        datum = "\n".join(datum)
        result.append(datum)
    return result

    