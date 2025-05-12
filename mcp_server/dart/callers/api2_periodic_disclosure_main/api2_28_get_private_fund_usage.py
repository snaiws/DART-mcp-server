from apimanager import HttpxAPIManager



async def get_private_fund_usage(
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
        "se_nm": "구분",
        "tm": "회차",
        "pay_de": "납입일",
        "pay_amount": "납입금액",
        "cptal_use_plan": "자금사용 계획",
        "real_cptal_use_sttus": "실제 자금사용 현황",
        "mtrpt_cptal_use_plan_useprps": "주요사항보고서의 자금사용 계획(사용용도)",
        "mtrpt_cptal_use_plan_prcure_amount": "주요사항보고서의 자금사용 계획(조달금액)",
        "real_cptal_use_dtls_cn": "실제 자금사용 내역(내용)",
        "real_cptal_use_dtls_amount": "실제 자금사용 내역(금액)",
        "dffrnc_occrrnc_resn": "차이발생 사유 등",
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
        datum = [f"{transform1[k]}: {datum[k]}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result

    
    
# 사용 예시
if __name__ == "__main__":
    # uv run -m dart.callers.api2_periodic_disclosure_main.api2_28_get_private_fund_usage
    import os
    import asyncio

    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        base_url = "https://opendart.fss.or.kr/api"
        endpoint = "/prvsrpCptalUseDtls.json"
        API_KEY = os.getenv("DART_API_KEY")
        corp_code = "00126380"
        bsns_year = "2024"
        reprt_code = "11013"
        print(API_KEY)

        results = await get_private_fund_usage(
            base_url = base_url,
            endpoint = endpoint,
            api_key = API_KEY,
            corp_code = corp_code,  # 삼성전자 고유번호
            bsns_year = bsns_year,
            reprt_code = reprt_code
        )

        for result in results:
            print("---")
            print(result)
        
    asyncio.run(test())