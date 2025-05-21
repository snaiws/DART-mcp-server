from apimanager import HttpxAPIManager



async def get_stock_exchange_transfer_decision(
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
        "extr_sen": "구분",
        "extr_stn": "교환ㆍ이전 형태",
        "extr_tgcmp_cmpnm": "교환ㆍ이전 대상법인(회사명)",
        "extr_tgcmp_rp": "교환ㆍ이전 대상법인(대표자)",
        "extr_tgcmp_mbsn": "교환ㆍ이전 대상법인(주요사업)",
        "extr_tgcmp_rl_cmpn": "교환ㆍ이전 대상법인(회사와의 관계)",
        "extr_tgcmp_tisstk_ostk": "교환ㆍ이전 대상법인이 발행한 보통주식 총 수(주)",
        "extr_tgcmp_tisstk_cstk": "교환ㆍ이전 대상법인이 발행한 종류주식 총 수(주)",
        "rbsnfdtl_tast": "교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(자산총계))",
        "rbsnfdtl_tdbt": "교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(부채총계))",
        "rbsnfdtl_teqt": "교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(자본총계))",
        "rbsnfdtl_cpt": "교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(자본금))",
        "extr_rt": "교환ㆍ이전 비율",
        "extr_rt_bs": "교환ㆍ이전 비율 산출근거",
        "exevl_atn": "외부평가에 관한 사항(외부평가 여부)",
        "exevl_bs_rs": "외부평가에 관한 사항(근거 및 사유)",
        "exevl_intn": "외부평가에 관한 사항(외부평가기관의 명칭)",
        "exevl_pd": "외부평가에 관한 사항(외부평가 기간)",
        "exevl_op": "외부평가에 관한 사항(외부평가 의견)",
        "extr_pp": "교환ㆍ이전 목적",
        "extrsc_extrctrd": "교환ㆍ이전일정(교환ㆍ이전계약일)",
        "extrsc_shddstd": "교환ㆍ이전일정(주주확정기준일)",
        "extrsc_shclspd_bgd": "교환ㆍ이전일정(주주명부 폐쇄기간(시작일))",
        "extrsc_shclspd_edd": "교환ㆍ이전일정(주주명부 폐쇄기간(종료일))",
        "extrsc_extrop_rcpd_bgd": "교환ㆍ이전일정(주식교환ㆍ이전 반대의사 통지접수기간(시작일))",
        "extrsc_extrop_rcpd_edd": "교환ㆍ이전일정(주식교환ㆍ이전 반대의사 통지접수기간(종료일))",
        "extrsc_gmtsck_prd": "교환ㆍ이전일정(주주총회 예정일자)",
        "extrsc_aprskh_expd_bgd": "교환ㆍ이전일정(주식매수청구권 행사기간(시작일))",
        "extrsc_aprskh_expd_edd": "교환ㆍ이전일정(주식매수청구권 행사기간(종료일))",
        "extrsc_osprpd_bgd": "교환ㆍ이전일정(구주권제출기간(시작일))",
        "extrsc_osprpd_edd": "교환ㆍ이전일정(구주권제출기간(종료일))",
        "extrsc_trspprpd": "교환ㆍ이전일정(매매거래정지예정기간)",
        "extrsc_trspprpd_bgd": "교환ㆍ이전일정(매매거래정지예정기간(시작일))",
        "extrsc_trspprpd_edd": "교환ㆍ이전일정(매매거래정지예정기간(종료일))",
        "extrsc_extrdt": "교환ㆍ이전일정(교환ㆍ이전일자)",
        "extrsc_nstkdlprd": "교환ㆍ이전일정(신주권교부예정일)",
        "extrsc_nstklstprd": "교환ㆍ이전일정(신주의 상장예정일)",
        "atextr_cpcmpnm": "교환ㆍ이전 후 완전모회사명",
        "aprskh_plnprc": "주식매수청구권에 관한 사항(매수예정가격)",
        "aprskh_pym_plpd_mth": "주식매수청구권에 관한 사항(지급예정시기, 지급방법)",
        "aprskh_lmt": "주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용)",
        "aprskh_ctref": "주식매수청구권에 관한 사항(계약에 미치는 효력)",
        "bdlst_atn": "우회상장 해당 여부",
        "otcpr_bdlst_sf_atn": "타법인의 우회상장 요건 충족 여부",
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
    # uv run -m dart.callers.api5_critical_info.api5_36_get_stock_exchange_transfer_decision
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

        results = await get_stock_exchange_transfer_decision(
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