from apimanager import HttpxAPIManager



async def get_treasury_stock_acquisition(
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
        "aqpln_stk_ostk": "취득예정주식수(보통주식)",
        "aqpln_stk_estk": "취득예정주식수(기타주식)",
        "aqpln_prc_ostk": "취득예정금액(보통주식)(원)",
        "aqpln_prc_estk": "취득예정금액(기타주식)(원)",
        "aqexpd_bgd": "취득예상기간 시작일",
        "aqexpd_edd": "취득예상기간 종료일",
        "hdexpd_bgd": "보유예상기간 시작일",
        "hdexpd_edd": "보유예상기간 종료일",
        "aq_pp": "취득목적",
        "aq_mth": "취득방법",
        "cs_iv_bk": "위탁투자중개업자",
        "aq_wtn_div_ostk": "취득 전 자기주식 보유현황(배당가능이익 범위 내)(보통주식)",
        "aq_wtn_div_ostk_rt": "취득 전 자기주식 보유현황(배당가능이익 범위 내)(보통주식 비율%)",
        "aq_wtn_div_estk": "취득 전 자기주식 보유현황(배당가능이익 범위 내)(기타주식)",
        "aq_wtn_div_estk_rt": "취득 전 자기주식 보유현황(배당가능이익 범위 내)(기타주식 비율%)",
        "eaq_ostk": "취득 전 자기주식 보유현황(기타취득)(보통주식)",
        "eaq_ostk_rt": "취득 전 자기주식 보유현황(기타취득)(보통주식 비율%)",
        "eaq_estk": "취득 전 자기주식 보유현황(기타취득)(기타주식)",
        "eaq_estk_rt": "취득 전 자기주식 보유현황(기타취득)(기타주식 비율%)",
        "aq_dd": "취득결정일",
        "od_a_at_t": "사외이사 참석자 수",
        "od_a_at_b": "사외이사 불참자 수",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
        "d1_prodlm_ostk": "1일 매수 주문수량 한도(보통주식)",
        "d1_prodlm_estk": "1일 매수 주문수량 한도(기타주식)"
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
