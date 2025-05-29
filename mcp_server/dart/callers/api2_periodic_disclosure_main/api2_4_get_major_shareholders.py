from apimanager import HttpxAPIManager



async def get_major_shareholders(
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
        "corp_name": "법인명",
        "nm": "성명",
        "relate": "관계(본인, 친인척 등)",
        "stock_knd": "주식 종류(보통주 등)",
        "bsis_posesn_stock_co": "기초 소유 주식 수",
        "bsis_posesn_stock_qota_rt": "기초 소유 주식 지분 율",
        "trmend_posesn_stock_co": "기말 소유 주식 수",
        "trmend_posesn_stock_qota_rt": "기말 소유 주식 지분 율",
        "rm": "비고",
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
