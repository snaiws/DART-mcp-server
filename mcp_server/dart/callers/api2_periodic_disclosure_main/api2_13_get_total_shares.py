from apimanager import HttpxAPIManager



async def get_total_shares(
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
        "se": "구분(증권의종류, 합계, 비고)",
        "isu_stock_totqy": "발행할 주식의 총수",
        "now_to_isu_stock_totqy": "현재까지 발행한 주식의 총수",
        "now_to_dcrs_stock_totqy": "현재까지 감소한 주식의 총수",
        "redc": "감자",
        "profit_incnr": "이익소각",
        "rdmstk_repy": "상환주식의 상환",
        "etc": "기타",
        "istc_totqy": "발행주식의 총수",
        "tesstk_co": "자기주식수",
        "distb_stock_co": "유통주식수",
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

    