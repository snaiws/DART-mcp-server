from apimanager import HttpxAPIManager



async def get_paid_capital_increase(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bgn_de:str, 
    end_de:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': bgn_de,
        'end_de': end_de
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()

    transform1 = {
    "rcept_no": "접수번호",
    "corp_cls": "법인구분",
    "corp_code": "고유번호(8자리)",
    "corp_name": "회사명",
    "nstk_ostk_cnt": "신주 보통주식 수(주)",
    "nstk_estk_cnt": "신주 기타주식 수(주)",
    "fv_ps": "1주당 액면가액(원)",
    "bfic_tisstk_ostk": "증자전 발행주식총수 보통주식(주)",
    "bfic_tisstk_estk": "증자전 발행주식총수 기타주식(주)",
    "fdpp_fclt": "자금조달목적 시설자금(원)",
    "fdpp_bsninh": "자금조달목적 영업양수자금(원)",
    "fdpp_op": "자금조달목적 운영자금(원)",
    "fdpp_dtrp": "자금조달목적 채무상환자금(원)",
    "fdpp_ocsa": "자금조달목적 타법인증권취득자금(원)",
    "fdpp_etc": "자금조달목적 기타자금(원)",
    "ic_mthn": "증자방식",
    "ssl_at": "공매도 해당여부",
    "ssl_bgd": "공매도 시작일",
    "ssl_edd": "공매도 종료일"
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
