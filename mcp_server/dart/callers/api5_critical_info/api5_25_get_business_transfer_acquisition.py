from apimanager import HttpxAPIManager



async def get_business_transfer_acquisition(
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
        "inh_bsn": "양수영업",
        "inh_bsn_mc": "양수영업 주요내용",
        "inh_prc": "양수가액(원)",
        "absn_inh_atn": "영업전부의 양수 여부",
        "ast_inh_bsn": "재무내용-자산액(양수대상 영업부문)(원)",
        "ast_cmp_all": "재무내용-자산액(당사전체)(원)",
        "ast_rt": "재무내용-자산액 비중(%)",
        "sl_inh_bsn": "재무내용-매출액(양수대상 영업부문)(원)",
        "sl_cmp_all": "재무내용-매출액(당사전체)(원)",
        "sl_rt": "재무내용-매출액 비중(%)",
        "dbt_inh_bsn": "재무내용-부채액(양수대상 영업부문)(원)",
        "dbt_cmp_all": "재무내용-부채액(당사전체)(원)",
        "dbt_rt": "재무내용-부채액 비중(%)",
        "inh_pp": "양수목적",
        "inh_af": "양수영향",
        "inh_prd_ctr_cnsd": "양수예정일자(계약체결일)",
        "inh_prd_inh_std": "양수예정일자(양수기준일)",
        "dlptn_cmpnm": "거래상대방 회사명(성명)",
        "dlptn_cpt": "거래상대방 자본금(원)",
        "dlptn_mbsn": "거래상대방 주요사업",
        "dlptn_hoadd": "거래상대방 본점소재지(주소)",
        "dlptn_rl_cmpn": "거래상대방과 회사와의 관계",
        "inh_pym": "양수대금지급",
        "exevl_atn": "외부평가 여부",
        "exevl_bs_rs": "외부평가 근거 및 사유",
        "exevl_intn": "외부평가기관의 명칭",
        "exevl_pd": "외부평가 기간",
        "exevl_op": "외부평가 의견",
        "gmtsck_spd_atn": "주주총회 특별결의 여부",
        "gmtsck_prd": "주주총회 예정일자",
        "aprskh_plnprc": "주식매수청구권-매수예정가격(원)",
        "aprskh_pym_plpd_mth": "주식매수청구권-지급예정시기 및 지급방법",
        "aprskh_lmt": "주식매수청구권 제한 관련 내용",
        "aprskh_ctref": "주식매수청구권-계약에 미치는 효력",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석(명)",
        "od_a_at_b": "사외이사 불참(명)",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
        "bdlst_atn": "우회상장 해당 여부",
        "n6m_tpai_plann": "향후 6월이내 제3자배정 증자 등 계획",
        "otcpr_bdlst_sf_atn": "타법인의 우회상장 요건 충족여부",
        "ftc_stt_atn": "공정거래위원회 신고대상 여부",
        "popt_ctr_atn": "풋옵션 등 계약 체결여부",
        "popt_ctr_cn": "계약내용"
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

        results = await get_business_transfer_acquisition(
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