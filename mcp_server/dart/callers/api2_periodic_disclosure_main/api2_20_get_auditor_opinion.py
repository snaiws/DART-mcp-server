from apimanager import HttpxAPIManager



async def get_auditor_opinion(
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
        "adt_opinion": "감사의견",
        "adt_reprt_spcmnt_matter": "감사보고서 특기사항(2019년 12월 8일까지 사용된 사항)",
        "emphs_matter": "강조사항 등(2019년 12월 9일부터 추가된 사항)",
        "core_adt_matter": "핵심감사사항(2019년 12월 9일부터 추가된 사항)",
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

    