from apimanager import HttpxAPIManager



async def get_corpinfo(
        base_url:str,
        endpoint:str,
        api_key:str, 
        corp_code:str
        )->list:
    
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
        
    data = response.json()

    # 후처리
    transform1 = {
        "corp_name": "정식회사명칭",
        "corp_name_eng": "영문정식회사명칭",
        "stock_name": "종목명(상장사) 또는 약식명칭(기타법인)",
        "stock_code": "상장회사인 경우 주식의 종목코드(6자리)",
        "ceo_nm": "대표자명",
        "corp_cls": "법인구분",
        "jurir_no": "법인등록번호",
        "bizr_no": "사업자등록번호",
        "adres": "주소",
        "hm_url": "홈페이지",
        "ir_url": "IR홈페이지",
        "phn_no": "전화번호",
        "fax_no": "팩스번호",
        "induty_code": "업종코드",
        "est_dt": "설립일",
        "acc_mt": "결산월"
    }

    transform2 = {
        "Y":"유가",
        "K":"코스닥",
        "N":"코넥스",
        "E":"기타",
    }
    # 법인구분 처리
    data['corp_cls'] = transform2[data['corp_cls']]
    # dict to string
    result = [f"{transform1[k]}: {data[k]}" for k in transform1]
    result = "\n".join(result)

    return [result]


    
# 사용 예시
if __name__ == "__main__":
    import os
    import asyncio

    import httpx
    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        url = "https://opendart.fss.or.kr/api/company.json"
        API_KEY = os.getenv("DART_API_KEY")
        print(API_KEY)
        async with httpx.AsyncClient() as client:

            result = await get_corpinfo(
                client = client,
                url = url,
                api_key=API_KEY,
                corp_code="00126380",  # 삼성전자 고유번호
            )

        print(result)
        
    asyncio.run(test())