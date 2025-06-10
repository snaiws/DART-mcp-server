from apimanager import HttpxAPIManager



async def get_treasury_stock_disposal(
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
        "dppln_stk_ostk": "처분예정주식수(보통주식)",
        "dppln_stk_estk": "처분예정주식수(기타주식)",
        "dpstk_prc_ostk": "처분 대상 주식가격(보통주식, 원)",
        "dpstk_prc_estk": "처분 대상 주식가격(기타주식, 원)",
        "dppln_prc_ostk": "처분예정금액(보통주식, 원)",
        "dppln_prc_estk": "처분예정금액(기타주식, 원)",
        "dpprpd_bgd": "처분예정기간 시작일",
        "dpprpd_edd": "처분예정기간 종료일",
        "dp_pp": "처분목적",
        "dp_m_mkt": "처분방법(시장을 통한 매도, 주)",
        "dp_m_ovtm": "처분방법(시간외대량매매, 주)",
        "dp_m_otc": "처분방법(장외처분, 주)",
        "dp_m_etc": "처분방법(기타, 주)",
        "cs_iv_bk": "위탁투자중개업자",
        "aq_wtn_div_ostk": "처분 전 자기주식 보유현황(배당가능이익 범위 내 취득, 보통주식)",
        "aq_wtn_div_ostk_rt": "처분 전 자기주식 보유현황(배당가능이익 범위 내 취득 비율, 보통주식, %)",
        "aq_wtn_div_estk": "처분 전 자기주식 보유현황(배당가능이익 범위 내 취득, 기타주식)",
        "aq_wtn_div_estk_rt": "처분 전 자기주식 보유현황(배당가능이익 범위 내 취득 비율, 기타주식, %)",
        "eaq_ostk": "처분 전 자기주식 보유현황(기타취득, 보통주식)",
        "eaq_ostk_rt": "처분 전 자기주식 보유현황(기타취득 비율, 보통주식, %)",
        "eaq_estk": "처분 전 자기주식 보유현황(기타취득, 기타주식)",
        "eaq_estk_rt": "처분 전 자기주식 보유현황(기타취득 비율, 기타주식, %)",
        "dp_dd": "처분결정일",
        "od_a_at_t": "사외이사 참석자 수",
        "od_a_at_b": "사외이사 불참자 수",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
        "d1_slodlm_ostk": "1일 매도 주문수량 한도(보통주식)",
        "d1_slodlm_estk": "1일 매도 주문수량 한도(기타주식)"
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

    
    