async def get_capitalstatus(client, url:str, api_key:str, corp_code:str, bsns_year:str, reprt_code:str)->str:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code
    }

    # GET 요청 보내기
    response = await client.get(url, params = params)
        
    data = response.json()
    return data


if __name__ == "__main__":
    import os
    import asyncio

    import httpx
    from dotenv import load_dotenv
    load_dotenv(verbose=False)
        
    async def test():
        url = "https://opendart.fss.or.kr/api/irdsSttus.json"
        API_KEY = os.getenv("DART_API_KEY")
        print(API_KEY)
        corp_code = "00126380"
        bsns_year = "2024"
        reprt_code = "11013"
        async with httpx.AsyncClient() as client:

            result = await get_capitalstatus(client, url, API_KEY, corp_code, bsns_year, reprt_code)

        print(result)
        
    asyncio.run(test())