from apimanager import HttpxAPIManager



async def get_treasury_stock(
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
        "acqs_mth1": "취득방법 대분류(배당가능이익범위 이내 취득, 기타취득, 총계 등)",
        "acqs_mth2": "취득방법 중분류(직접취득, 신탁계약에 의한취득, 기타취득, 총계 등)",
        "acqs_mth3": "취득방법 소분류(장내직접취득, 장외직접취득, 공개매수, 주식매수청구권행사, 수탁자보유물량, 현물보유량, 기타취득, 소계, 총계 등)",
        "stock_knd": "주식 종류(보통주, 우선주 등)",
        "bsis_qy": "기초 수량",
        "change_qy_acqs": "변동 수량 취득",
        "change_qy_dsps": "변동 수량 처분",
        "change_qy_incnr": "변동 수량 소각",
        "trmend_qy": "기말 수량",
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

    