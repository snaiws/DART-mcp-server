from apimanager import HttpxAPIManager



async def get_split_decision(
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
        "dv_mth": "분할방법",
        "dv_impef": "분할의 중요영향 및 효과",
        "dv_rt": "분할비율",
        "dv_trfbsnprt_cn": "분할로 이전할 사업 및 재산의 내용",
        "atdv_excmp_cmpnm": "분할 후 존속회사(회사명)",
        "atdvfdtl_tast": "분할 후 존속회사(분할후 재무내용(원)(자산총계))",
        "atdvfdtl_tdbt": "분할 후 존속회사(분할후 재무내용(원)(부채총계))",
        "atdvfdtl_teqt": "분할 후 존속회사(분할후 재무내용(원)(자본총계))",
        "atdvfdtl_cpt": "분할 후 존속회사(분할후 재무내용(원)(자본금))",
        "atdvfdtl_std": "분할 후 존속회사(분할후 재무내용(원)(현재기준))",
        "atdv_excmp_exbsn_rsl": "분할 후 존속회사(존속사업부문 최근 사업연도매출액(원))",
        "atdv_excmp_mbsn": "분할 후 존속회사(주요사업)",
        "atdv_excmp_atdv_lstmn_atn": "분할 후 존속회사(분할 후 상장유지 여부)",
        "dvfcmp_cmpnm": "분할설립회사(회사명)",
        "ffdtl_tast": "분할설립회사(설립시 재무내용(원)(자산총계))",
        "ffdtl_tdbt": "분할설립회사(설립시 재무내용(원)(부채총계))",
        "ffdtl_teqt": "분할설립회사(설립시 재무내용(원)(자본총계))",
        "ffdtl_cpt": "분할설립회사(설립시 재무내용(원)(자본금))",
        "ffdtl_std": "분할설립회사(설립시 재무내용(원)(현재기준))",
        "dvfcmp_nbsn_rsl": "분할설립회사(신설사업부문 최근 사업연도 매출액(원))",
        "dvfcmp_mbsn": "분할설립회사(주요사업)",
        "dvfcmp_rlst_atn": "분할설립회사(재상장신청 여부)",
        "abcr_crrt": "감자에 관한 사항(감자비율(%))",
        "abcr_osprpd_bgd": "감자에 관한 사항(구주권 제출기간(시작일))",
        "abcr_osprpd_edd": "감자에 관한 사항(구주권 제출기간(종료일))",
        "abcr_trspprpd_bgd": "감자에 관한 사항(매매거래정지 예정기간(시작일))",
        "abcr_trspprpd_edd": "감자에 관한 사항(매매거래정지 예정기간(종료일))",
        "abcr_nstkascnd": "감자에 관한 사항(신주배정조건)",
        "abcr_shstkcnt_rt_at_rs": "감자에 관한 사항(주주 주식수 비례여부 및 사유)",
        "abcr_nstkasstd": "감자에 관한 사항(신주배정기준일)",
        "abcr_nstkdlprd": "감자에 관한 사항(신주권교부예정일)",
        "abcr_nstklstprd": "감자에 관한 사항(신주의 상장예정일)",
        "gmtsck_prd": "주주총회 예정일",
        "cdobprpd_bgd": "채권자 이의제출기간(시작일)",
        "cdobprpd_edd": "채권자 이의제출기간(종료일)",
        "dvdt": "분할기일",
        "dvrgsprd": "분할등기 예정일",
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

    