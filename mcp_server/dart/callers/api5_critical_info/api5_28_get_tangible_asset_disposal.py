from apimanager import HttpxAPIManager



async def get_tangible_asset_disposal(
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
        "ast_sen": "자산구분",
        "ast_nm": "자산명",
        "trfdtl_trfprc": "양도내역(양도금액(원))",
        "trfdtl_tast": "양도내역(자산총액(원))",
        "trfdtl_tast_vs": "양도내역(자산총액대비(%))",
        "trf_pp": "양도목적",
        "trf_af": "양도영향",
        "trf_prd_ctr_cnsd": "양도예정일자(계약체결일)",
        "trf_prd_trf_std": "양도예정일자(양도기준일)",
        "trf_prd_rgs_prd": "양도예정일자(등기예정일)",
        "dlptn_cmpnm": "거래상대방(회사명(성명))",
        "dlptn_cpt": "거래상대방(자본금(원))",
        "dlptn_mbsn": "거래상대방(주요사업)",
        "dlptn_hoadd": "거래상대방(본점소재지(주소))",
        "dlptn_rl_cmpn": "거래상대방(회사와의 관계)",
        "dl_pym": "거래대금지급",
        "exevl_atn": "외부평가에 관한 사항(외부평가 여부)",
        "exevl_bs_rs": "외부평가에 관한 사항(근거 및 사유)",
        "exevl_intn": "외부평가에 관한 사항(외부평가기관의 명칭)",
        "exevl_pd": "외부평가에 관한 사항(외부평가 기간)",
        "exevl_op": "외부평가에 관한 사항(외부평가 의견)",
        "gmtsck_spd_atn": "주주총회 특별결의 여부",
        "gmtsck_prd": "주주총회 예정일자",
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

        results = await get_tangible_asset_disposal(
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