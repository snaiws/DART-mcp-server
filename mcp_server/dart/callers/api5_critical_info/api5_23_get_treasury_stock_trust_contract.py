from apimanager import HttpxAPIManager



async def get_treasury_stock_trust_contract(
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
        "ctr_prc": "계약금액(원)",
        "ctr_pd_bgd": "계약기간 시작일",
        "ctr_pd_edd": "계약기간 종료일",
        "ctr_pp": "계약목적",
        "ctr_cns_int": "계약체결기관",
        "ctr_cns_prd": "계약체결 예정일자",
        "aq_wtn_div_ostk": "계약 전 자기주식 보유현황(배당가능범위내 취득 보통주식수)",
        "aq_wtn_div_ostk_rt": "계약 전 자기주식 보유현황(배당가능범위내 취득 보통주식 비율(%))",
        "aq_wtn_div_estk": "계약 전 자기주식 보유현황(배당가능범위내 취득 기타주식수)",
        "aq_wtn_div_estk_rt": "계약 전 자기주식 보유현황(배당가능범위내 취득 기타주식 비율(%))",
        "eaq_ostk": "계약 전 자기주식 보유현황(기타취득 보통주식수)",
        "eaq_ostk_rt": "계약 전 자기주식 보유현황(기타취득 보통주식 비율(%))",
        "eaq_estk": "계약 전 자기주식 보유현황(기타취득 기타주식수)",
        "eaq_estk_rt": "계약 전 자기주식 보유현황(기타취득 기타주식 비율(%))",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석인원수",
        "od_a_at_b": "사외이사 불참인원수",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
        "cs_iv_bk": "위탁투자중개업자"
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

        results = await get_treasury_stock_trust_contract(
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