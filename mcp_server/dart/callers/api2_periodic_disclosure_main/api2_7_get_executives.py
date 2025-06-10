from apimanager import HttpxAPIManager



async def get_executives(
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
        "sexdstn": "성별",
        "birth_ym": "출생 년월",
        "ofcps": "직위(회장, 사장, 사외이사 등)",
        "rgist_exctv_at": "등기 임원 여부(등기임원, 미등기임원 등)",
        "fte_at": "상근 여부(상근, 비상근)",
        "chrg_job": "담당 업무(대표이사, 이사, 사외이사 등)",
        "main_career": "주요 경력",
        "mxmm_shrholdr_relate": "최대 주주 관계",
        "hffc_pd": "재직 기간",
        "tenure_end_on": "임기 만료 일",
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
