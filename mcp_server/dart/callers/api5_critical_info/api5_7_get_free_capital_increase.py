from apimanager import HttpxAPIManager



async def get_free_capital_increase(
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
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "nstk_ostk_cnt": "신주의 종류와 수(보통주식)",
        "nstk_estk_cnt": "신주의 종류와 수(기타주식)",
        "fv_ps": "1주당 액면가액",
        "bfic_tisstk_ostk": "증자전 발행주식총수(보통주식)",
        "bfic_tisstk_estk": "증자전 발행주식총수(기타주식)",
        "nstk_asstd": "신주배정기준일",
        "nstk_ascnt_ps_ostk": "1주당 신주배정 주식수(보통주식)",
        "nstk_ascnt_ps_estk": "1주당 신주배정 주식수(기타주식)",
        "nstk_dividrk": "신주의 배당기산일",
        "nstk_dlprd": "신주권교부예정일",
        "nstk_lstprd": "신주의 상장 예정일",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석여부(참석)",
        "od_a_at_b": "사외이사 참석여부(불참)",
        "adt_a_atn": "감사(감사위원)참석 여부"
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

    