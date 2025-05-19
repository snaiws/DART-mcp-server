from apimanager import HttpxAPIManager



async def get_capitalstatus(
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
        "corp_name": "법인명",
        "isu_dcrs_de": "주식발행 감소일자",
        "isu_dcrs_stle": "발행 감소 형태",
        "isu_dcrs_stock_knd": "발행 감소 주식 종류",
        "isu_dcrs_qy": "발행 감소 수량",
        "isu_dcrs_mstvdv_fval_amount": "발행 감소 주당 액면 가액",
        "isu_dcrs_mstvdv_amount": "발행 감소 주당 가액",
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
        bsns_year = "2024"
        reprt_code = "11013"
        print(API_KEY)

        results = await get_capitalstatus(
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