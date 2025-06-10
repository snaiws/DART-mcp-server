from apimanager import HttpxAPIManager



async def get_contingent_capital_securities_issuance(
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
    "bd_tm": "사채의 종류(회차)",
    "bd_knd": "사채의 종류(종류)",
    "bd_fta": "사채의 권면(전자등록)총액(원)",
    "ovis_fta": "해외발행 권면(전자등록)총액",
    "ovis_fta_crn": "해외발행 권면총액 통화단위",
    "ovis_ster": "해외발행 기준환율등",
    "ovis_isar": "해외발행 발행지역",
    "ovis_mktnm": "해외발행 해외상장시 시장명칭",
    "fdpp_fclt": "자금조달목적 - 시설자금(원)",
    "fdpp_bsninh": "자금조달목적 - 영업양수자금(원)",
    "fdpp_op": "자금조달목적 - 운영자금(원)",
    "fdpp_dtrp": "자금조달목적 - 채무상환자금(원)",
    "fdpp_ocsa": "자금조달목적 - 타법인 증권취득자금(원)",
    "fdpp_etc": "자금조달목적 - 기타자금(원)",
    "bd_intr_sf": "사채 표면이자율(%)",
    "bd_intr_ex": "사채 만기이자율(%)",
    "bd_mtd": "사채만기일",
    "dbtrs_sc": "채무재조정의 범위",
    "sbd": "청약일",
    "pymd": "납입일",
    "rpmcmp": "대표주관회사",
    "grint": "보증기관",
    "bddd": "이사회결의일(결정일)",
    "od_a_at_t": "사외이사 참석인원(명)",
    "od_a_at_b": "사외이사 불참인원(명)",
    "adt_a_atn": "감사(감사위원) 참석여부",
    "rs_sm_atn": "증권신고서 제출대상 여부",
    "ex_sm_r": "증권신고서 제출면제 사유",
    "ovis_ltdtl": "해외발행 연계 대차거래 내역",
    "ftc_stt_atn": "공정거래위원회 신고대상 여부"
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

    