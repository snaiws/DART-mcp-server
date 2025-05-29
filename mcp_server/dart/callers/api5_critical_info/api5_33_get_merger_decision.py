from apimanager import HttpxAPIManager



async def get_merger_decision(
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
    
    transform1 = transform2 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "mg_mth": "합병방법",
        "mg_stn": "합병형태",
        "mg_pp": "합병목적",
        "mg_rt": "합병비율",
        "mg_rt_bs": "합병비율 산출근거",
        "exevl_atn": "외부평가에 관한 사항(외부평가 여부)",
        "exevl_bs_rs": "외부평가에 관한 사항(근거 및 사유)",
        "exevl_intn": "외부평가에 관한 사항(외부평가기관의 명칭)",
        "exevl_pd": "외부평가에 관한 사항(외부평가 기간)",
        "exevl_op": "외부평가에 관한 사항(외부평가 의견)",
        "mgnstk_ostk_cnt": "합병신주의 종류와 수(주)(보통주식)",
        "mgnstk_cstk_cnt": "합병신주의 종류와 수(주)(종류주식)",
        "mgptncmp_cmpnm": "합병상대회사(회사명)",
        "mgptncmp_mbsn": "합병상대회사(주요사업)",
        "mgptncmp_rl_cmpn": "합병상대회사(회사와의 관계)",
        "rbsnfdtl_tast": "합병상대회사(최근 사업연도 재무내용(원)(자산총계))",
        "rbsnfdtl_tdbt": "합병상대회사(최근 사업연도 재무내용(원)(부채총계))",
        "rbsnfdtl_teqt": "합병상대회사(최근 사업연도 재무내용(원)(자본총계))",
        "rbsnfdtl_cpt": "합병상대회사(최근 사업연도 재무내용(원)(자본금))",
        "rbsnfdtl_sl": "합병상대회사(최근 사업연도 재무내용(원)(매출액))",
        "rbsnfdtl_nic": "합병상대회사(최근 사업연도 재무내용(원)(당기순이익))",
        "eadtat_intn": "합병상대회사(외부감사 여부(기관명))",
        "eadtat_op": "합병상대회사(외부감사 여부(감사의견))",
        "nmgcmp_cmpnm": "신설합병회사(회사명)",
        "ffdtl_tast": "신설합병회사(설립시 재무내용(원)(자산총계))",
        "ffdtl_tdbt": "신설합병회사(설립시 재무내용(원)(부채총계))",
        "ffdtl_teqt": "신설합병회사(설립시 재무내용(원)(자본총계))",
        "ffdtl_cpt": "신설합병회사(설립시 재무내용(원)(자본금))",
        "ffdtl_std": "신설합병회사(설립시 재무내용(원)(현재기준))",
        "nmgcmp_nbsn_rsl": "신설합병회사(신설사업부문 최근 사업연도 매출액(원))",
        "nmgcmp_mbsn": "신설합병회사(주요사업)",
        "nmgcmp_rlst_atn": "신설합병회사(재상장신청 여부)",
        "mgsc_mgctrd": "합병일정(합병계약일)",
        "mgsc_shddstd": "합병일정(주주확정기준일)",
        "mgsc_shclspd_bgd": "합병일정(주주명부 폐쇄기간(시작일))",
        "mgsc_shclspd_edd": "합병일정(주주명부 폐쇄기간(종료일))",
        "mgsc_mgop_rcpd_bgd": "합병일정(합병반대의사통지 접수기간(시작일))",
        "mgsc_mgop_rcpd_edd": "합병일정(합병반대의사통지 접수기간(종료일))",
        "mgsc_gmtsck_prd": "합병일정(주주총회예정일자)",
        "mgsc_aprskh_expd_bgd": "합병일정(주식매수청구권 행사기간(시작일))",
        "mgsc_aprskh_expd_edd": "합병일정(주식매수청구권 행사기간(종료일))",
        "mgsc_osprpd_bgd": "합병일정(구주권 제출기간(시작일))",
        "mgsc_osprpd_edd": "합병일정(구주권 제출기간(종료일))",
        "mgsc_trspprpd_bgd": "합병일정(매매거래 정지예정기간(시작일))",
        "mgsc_trspprpd_edd": "합병일정(매매거래 정지예정기간(종료일))",
        "mgsc_cdobprpd_bgd": "합병일정(채권자이의 제출기간(시작일))",
        "mgsc_cdobprpd_edd": "합병일정(채권자이의 제출기간(종료일))",
        "mgsc_mgdt": "합병일정(합병기일)",
        "mgsc_ergmd": "합병일정(종료보고 총회일)",
        "mgsc_mgrgsprd": "합병일정(합병등기예정일자)",
        "mgsc_nstkdlprd": "합병일정(신주권교부예정일)",
        "mgsc_nstklstprd": "합병일정(신주의 상장예정일)",
        "bdlst_atn": "우회상장 해당 여부",
        "otcpr_bdlst_sf_atn": "타법인의 우회상장 요건 충족여부",
        "aprskh_plnprc": "주식매수청구권에 관한 사항(매수예정가격)",
        "aprskh_pym_plpd_mth": "주식매수청구권에 관한 사항(지급예정시기, 지급방법)",
        "aprskh_ctref": "주식매수청구권에 관한 사항(계약에 미치는 효력)",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사참석여부(참석(명))",
        "od_a_at_b": "사외이사참석여부(불참(명))",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
        "popt_ctr_atn": "풋옵션 등 계약 체결여부",
        "popt_ctr_cn": "계약내용",
        "rs_sm_atn": "증권신고서 제출대상 여부",
        "ex_sm_r": "제출을 면제받은 경우 그 사유"
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

    