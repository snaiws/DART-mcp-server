async def get_corpinfo(client, url:str, api_key:str, corp_code:str)->str:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code
    }

    # GET 요청 보내기
    response = await client.get(url, params = params)
        
    data = response.json()
    return data


    
# 사용 예시
if __name__ == "__main__":
    import os
    import asyncio

    import httpx
    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    url = "https://opendart.fss.or.kr/api/company.json"
    API_KEY = os.getenv("DART_API_KEY")
    client = httpx.Client()
    print(API_KEY)

    result = asyncio.run(get_corpinfo(
        client = client,
        url = url,
        api_key=API_KEY,
        corp_code="00126380",  # 삼성전자 고유번호
    ))

    print(result)