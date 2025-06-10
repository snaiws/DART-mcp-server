from apimanager import HttpxAPIManager



async def get_capital_reduction(
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
        "crstk_ostk_cnt": "감자주식의 종류와 수(보통주식) (주)",
        "crstk_estk_cnt": "감자주식의 종류와 수(기타주식) (주)",
        "fv_ps": "1주당 액면가액 (원)",
        "bfcr_cpt": "감자전후 자본금(감자전) (원)",
        "atcr_cpt": "감자전후 자본금(감자후) (원)",
        "bfcr_tisstk_ostk": "감자전후 발행주식수(보통주식)(감자전) (주)",
        "atcr_tisstk_ostk": "감자전후 발행주식수(보통주식)(감자후) (주)",
        "bfcr_tisstk_estk": "감자전후 발행주식수(기타주식)(감자전) (주)",
        "atcr_tisstk_estk": "감자전후 발행주식수(기타주식)(감자후) (주)",
        "cr_rt_ostk": "감자비율(보통주식) (%)",
        "cr_rt_estk": "감자비율(기타주식) (%)",
        "cr_std": "감자기준일",
        "cr_mth": "감자방법",
        "cr_rs": "감자사유",
        "crsc_gmtsck_prd": "감자일정(주주총회 예정일)",
        "crsc_trnmsppd": "감자일정(명의개서정지기간)",
        "crsc_osprpd": "감자일정(구주권 제출기간)(2019년 12월 8일까지 사용됨)",
        "crsc_trspprpd": "감자일정(매매거래 정지예정기간)(2019년 12월 8일까지 사용됨)",
        "crsc_osprpd_bgd": "감자일정(구주권 제출기간 시작일)(2019년 12월 8일까지 추가됨)",
        "crsc_osprpd_edd": "감자일정(구주권 제출기간 종료일)(2019년 12월 8일까지 추가됨)",
        "crsc_trspprpd_bgd": "감자일정(매매거래 정지예정기간 시작일)(2019년 12월 8일까지 추가됨)",
        "crsc_trspprpd_edd": "감자일정(매매거래 정지예정기간 종료일)(2019년 12월 8일까지 추가됨)",
        "crsc_nstkdlprd": "감자일정(신주권교부예정일)",
        "crsc_nstklstprd": "감자일정(신주상장예정일)",
        "cdobprpd_bgd": "채권자 이의제출기간(시작일)",
        "cdobprpd_edd": "채권자 이의제출기간(종료일)",
        "ospr_nstkdl_pl": "구주권제출 및 신주권교부장소",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석여부(참석) (명)",
        "od_a_at_b": "사외이사 참석여부(불참) (명)",
        "adt_a_atn": "감사(감사위원) 참석여부",
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

    