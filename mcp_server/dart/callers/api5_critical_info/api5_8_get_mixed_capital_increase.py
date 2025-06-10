from apimanager import HttpxAPIManager



async def get_mixed_capital_increase(
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
        "piic_nstk_ostk_cnt": "유상증자 신주의 종류와 수(보통주식) (주)",
        "piic_nstk_estk_cnt": "유상증자 신주의 종류와 수(기타주식) (주)",
        "piic_fv_ps": "유상증자 1주당 액면가액 (원)",
        "piic_bfic_tisstk_ostk": "유상증자 증자전 발행주식총수(보통주식) (주)",
        "piic_bfic_tisstk_estk": "유상증자 증자전 발행주식총수(기타주식) (주)",
        "piic_fdpp_fclt": "유상증자 자금조달목적(시설자금) (원)",
        "piic_fdpp_bsninh": "유상증자 자금조달목적(영업양수자금) (원)(2019년 12월 9일부터 추가됨)",
        "piic_fdpp_op": "유상증자 자금조달목적(운영자금) (원)",
        "piic_fdpp_dtrp": "유상증자 자금조달목적(채무상환자금) (원)(2019년 12월 9일부터 추가됨)",
        "piic_fdpp_ocsa": "유상증자 자금조달목적(타법인 증권 취득자금) (원)",
        "piic_fdpp_etc": "유상증자 자금조달목적(기타자금) (원)",
        "piic_ic_mthn": "유상증자 증자방식",
        "fric_nstk_ostk_cnt": "무상증자 신주의 종류와 수(보통주식) (주)",
        "fric_nstk_estk_cnt": "무상증자 신주의 종류와 수(기타주식) (주)",
        "fric_fv_ps": "무상증자 1주당 액면가액 (원)",
        "fric_bfic_tisstk_ostk": "무상증자 증자전 발행주식총수(보통주식) (주)",
        "fric_bfic_tisstk_estk": "무상증자 증자전 발행주식총수(기타주식) (주)",
        "fric_nstk_asstd": "무상증자 신주배정기준일",
        "fric_nstk_ascnt_ps_ostk": "무상증자 1주당 신주배정 주식수(보통주식) (주)",
        "fric_nstk_ascnt_ps_estk": "무상증자 1주당 신주배정 주식수(기타주식) (주)",
        "fric_nstk_dividrk": "무상증자 신주의 배당기산일",
        "fric_nstk_dlprd": "무상증자 신주권교부예정일",
        "fric_nstk_lstprd": "무상증자 신주의 상장 예정일",
        "fric_bddd": "무상증자 이사회결의일(결정일)",
        "fric_od_a_at_t": "무상증자 사외이사 참석여부(참석) (명)",
        "fric_od_a_at_b": "무상증자 사외이사 참석여부(불참) (명)",
        "fric_adt_a_atn": "무상증자 감사(감사위원)참석 여부",
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

    