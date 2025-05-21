from apimanager import HttpxAPIManager



async def get_split_merger_decision(
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
        "rcept_no": "접수번호",
        "corp_cls": "법인구분",
        "corp_code": "고유번호",
        "corp_name": "회사명",
        "dvmg_mth": "분할합병 방법",
        "dvmg_impef": "분할합병의 중요영향 및 효과",
        "dv_trfbsnprt_cn": "분할에 관한 사항(분할로 이전할 사업 및 재산의 내용)",
        "atdv_excmp_cmpnm": "분할에 관한 사항(분할 후 존속회사(회사명))",
        "atdvfdtl_tast": "분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자산총계)))",
        "atdvfdtl_tdbt": "분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(부채총계)))",
        "atdvfdtl_teqt": "분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자본총계)))",
        "atdvfdtl_cpt": "분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자본금)))",
        "atdvfdtl_std": "분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(현재기준)))",
        "atdv_excmp_exbsn_rsl": "분할에 관한 사항(분할 후 존속회사(존속사업부문 최근 사업연도매출액(원)))",
        "atdv_excmp_mbsn": "분할에 관한 사항(분할 후 존속회사(주요사업))",
        "atdv_excmp_atdv_lstmn_atn": "분할에 관한 사항(분할 후 존속회사(분할 후 상장유지 여부))",
        "dvfcmp_cmpnm": "분할에 관한 사항(분할설립 회사(회사명))",
        "ffdtl_tast": "분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자산총계)))",
        "ffdtl_tdbt": "분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(부채총계)))",
        "ffdtl_teqt": "분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자본총계)))",
        "ffdtl_cpt": "분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자본금)))",
        "ffdtl_std": "분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(현재기준)))",
        "dvfcmp_nbsn_rsl": "분할에 관한 사항(분할설립 회사(신설사업부문 최근 사업연도 매출액(원)))",
        "dvfcmp_mbsn": "분할에 관한 사항(분할설립 회사(주요사업))",
        "dvfcmp_atdv_lstmn_at": "분할에 관한 사항(분할설립 회사(분할후 상장유지여부))",
        "abcr_crrt": "분할에 관한 사항(감자에 관한 사항(감자비율(%)))",
        "abcr_osprpd_bgd": "분할에 관한 사항(감자에 관한 사항(구주권 제출기간(시작일)))",
        "abcr_osprpd_edd": "분할에 관한 사항(감자에 관한 사항(구주권 제출기간(종료일)))",
        "abcr_trspprpd_bgd": "분할에 관한 사항(감자에 관한 사항(매매거래정지 예정기간(시작일)))",
        "abcr_trspprpd_edd": "분할에 관한 사항(감자에 관한 사항(매매거래정지 예정기간(종료일)))",
        "abcr_nstkascnd": "분할에 관한 사항(감자에 관한 사항(신주배정조건))",
        "abcr_shstkcnt_rt_at_rs": "분할에 관한 사항(감자에 관한 사항(주주 주식수 비례여부 및 사유))",
        "abcr_nstkasstd": "분할에 관한 사항(감자에 관한 사항(신주배정기준일))",
        "abcr_nstkdlprd": "분할에 관한 사항(감자에 관한 사항(신주권교부예정일))",
        "abcr_nstklstprd": "분할에 관한 사항(감자에 관한 사항(신주의 상장예정일))",
        "mg_stn": "합병에 관한 사항(합병형태)",
        "mgptncmp_cmpnm": "합병에 관한 사항(합병상대 회사(회사명))",
        "mgptncmp_mbsn": "합병에 관한 사항(합병상대 회사(주요사업))",
        "mgptncmp_rl_cmpn": "합병에 관한 사항(합병상대 회사(회사와의 관계))",
        "rbsnfdtl_tast": "합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자산총계)))",
        "rbsnfdtl_tdbt": "합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(부채총계)))",
        "rbsnfdtl_teqt": "합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자본총계)))",
        "rbsnfdtl_cpt": "합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자본금)))",
        "rbsnfdtl_sl": "합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(매출액)))",
        "rbsnfdtl_nic": "합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(당기순이익)))",
        "eadtat_intn": "합병에 관한 사항(합병상대 회사(외부감사 여부(기관명)))",
        "eadtat_op": "합병에 관한 사항(합병상대 회사(외부감사 여부(감사의견)))",
        "dvmgnstk_ostk_cnt": "합병에 관한 사항(분할합병신주의 종류와 수(주)(보통주식))",
        "dvmgnstk_cstk_cnt": "합병에 관한 사항(분할합병신주의 종류와 수(주)(종류주식))",
        "nmgcmp_cmpnm": "합병에 관한 사항(합병신설 회사(회사명))",
        "nmgcmp_cpt": "합병에 관한 사항(합병신설 회사(자본금(원)))",
        "nmgcmp_mbsn": "합병에 관한 사항(합병신설 회사(주요사업))",
        "nmgcmp_rlst_atn": "합병에 관한 사항(합병신설 회사(재상장신청 여부))",
        "dvmg_rt": "분할합병비율",
        "dvmg_rt_bs": "분할합병비율 산출근거",
        "exevl_atn": "외부평가에 관한 사항(외부평가 여부)",
        "exevl_bs_rs": "외부평가에 관한 사항(근거 및 사유)",
        "exevl_intn": "외부평가에 관한 사항(외부평가기관의 명칭)",
        "exevl_pd": "외부평가에 관한 사항(외부평가 기간)",
        "exevl_op": "외부평가에 관한 사항(외부평가 의견)",
        "dvmgsc_dvmgctrd": "분할합병일정(분할합병계약일)",
        "dvmgsc_shddstd": "분할합병일정(주주확정기준일)",
        "dvmgsc_shclspd_bgd": "분할합병일정(주주명부 폐쇄기간(시작일))",
        "dvmgsc_shclspd_edd": "분할합병일정(주주명부 폐쇄기간(종료일))",
        "dvmgsc_dvmgop_rcpd_bgd": "분할합병일정(분할합병반대의사통지 접수기간(시작일))",
        "dvmgsc_dvmgop_rcpd_edd": "분할합병일정(분할합병반대의사통지 접수기간(종료일))",
        "dvmgsc_gmtsck_prd": "분할합병일정(주주총회예정일자)",
        "dvmgsc_aprskh_expd_bgd": "분할합병일정(주식매수청구권 행사기간(시작일))",
        "dvmgsc_aprskh_expd_edd": "분할합병일정(주식매수청구권 행사기간(종료일))",
        "dvmgsc_cdobprpd_bgd": "분할합병일정(채권자 이의 제출기간(시작일))",
        "dvmgsc_cdobprpd_edd": "분할합병일정(채권자 이의 제출기간(종료일))",
        "dvmgsc_dvmgdt": "분할합병일정(분할합병기일)",
        "dvmgsc_ergmd": "분할합병일정(종료보고 총회일)",
        "dvmgsc_dvmgrgsprd": "분할합병일정(분할합병등기예정일)",
        "bdlst_atn": "우회상장 해당 여부",
        "otcpr_bdlst_sf_atn": "타법인의 우회상장 요건 충족여부",
        "aprskh_exrq": "주식매수청구권에 관한 사항(행사요건)",
        "aprskh_plnprc": "주식매수청구권에 관한 사항(매수예정가격)",
        "aprskh_ex_pc_mth_pd_pl": "주식매수청구권에 관한 사항(행사절차, 방법, 기간, 장소)",
        "aprskh_pym_plpd_mth": "주식매수청구권에 관한 사항(지급예정시기, 지급방법)",
        "aprskh_lmt": "주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용)",
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
    

    result = []
    for datum in data['list']:
        # dict to string
        datum = [f"{transform1[k]}: {datum[k]}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result

    
    
# 사용 예시
if __name__ == "__main__":
    # uv run -m dart.callers.api2_periodic_disclosure_main.api2_1_capital
    import os
    import asyncio

    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        base_url = "https://opendart.fss.or.kr/api"
        endpoint = "/irdsSttus.json"
        API_KEY = os.getenv("DART_API_KEY")
        corp_code = "00126380"
        bgn_de = "2024"
        end_de = "11013"
        print(API_KEY)

        results = await get_split_merger_decision(
            base_url = base_url,
            endpoint = endpoint,
            api_key = API_KEY,
            corp_code = corp_code,  # 삼성전자 고유번호
            bgn_de = bgn_de,
            end_de = end_de
        )

        for result in results:
            print("---")
            print(result)
        
    asyncio.run(test())