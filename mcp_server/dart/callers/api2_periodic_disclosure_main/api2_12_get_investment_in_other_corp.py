from apimanager import HttpxAPIManager



async def get_investment_in_other_corp(
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
        "inv_prm": "법인명",
        "frst_acqs_de": "최초 취득 일자",
        "invstmnt_purps": "출자 목적(자회사 등)",
        "frst_acqs_amount": "최초 취득 금액",
        "bsis_blce_qy": "기초 잔액 수량",
        "bsis_blce_qota_rt": "기초 잔액 지분 율",
        "bsis_blce_acntbk_amount": "기초 잔액 장부 가액",
        "incrs_dcrs_acqs_dsps_qy": "증가 감소 취득 처분 수량",
        "incrs_dcrs_acqs_dsps_amount": "증가 감소 취득 처분 금액",
        "incrs_dcrs_evl_lstmn": "증가 감소 평가 손액",
        "trmend_blce_qy": "기말 잔액 수량",
        "trmend_blce_qota_rt": "기말 잔액 지분 율",
        "trmend_blce_acntbk_amount": "기말 잔액 장부 가액",
        "recent_bsns_year_fnnr_sttus_tot_assets": "최근 사업 연도 재무 현황 총 자산",
        "recent_bsns_year_fnnr_sttus_thstrm_ntpf": "최근 사업 연도 재무 현황 당기 순이익",
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

    