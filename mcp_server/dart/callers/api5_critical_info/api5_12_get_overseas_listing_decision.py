from apimanager import HttpxAPIManager



async def get_overseas_listing_decision(
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
        "lstprstk_ostk_cnt": "상장예정주식 보통주식 수",
        "lstprstk_estk_cnt": "상장예정주식 기타주식 수",
        "tisstk_ostk": "발행주식 총수 보통주식",
        "tisstk_estk": "발행주식 총수 기타주식",
        "psmth_nstk_sl": "공모방법 신주발행",
        "psmth_ostk_sl": "공모방법 구주매출",
        "fdpp": "자금조달 신주발행 목적",
        "lststk_orlst": "상장증권 원주상장",
        "lststk_drlst": "상장증권 DR상장",
        "lstex_nt": "상장거래소 소재국가",
        "lstpp": "해외상장목적",
        "lstprd": "상장예정일자",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석",
        "od_a_at_b": "사외이사 불참",
        "adt_a_atn": "감사(감사위원) 참석여부"
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

    