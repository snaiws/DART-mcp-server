import io
import zipfile

from apimanager import HttpxAPIManager



async def update_corplist(
    base_url:str,
    endpoint:str,
    api_key:str, 
    path_corplist:str
    )->list:

    # API 요청 URL
    endpoint = endpoint.format(api_key=api_key)
    path_zip_corplist = "CORPCODE.xml"

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint)
    
    # 응답 확인
    if response.status_code == 200:
        # 응답이 성공적인 경우 압축 파일 처리
        zip_file = io.BytesIO(response.content)
        
        # 압축 해제
        with zipfile.ZipFile(zip_file) as z:
            xml_content = z.read(path_zip_corplist)
            
            # XML 파일 저장 (선택사항)
            with open(path_corplist, 'wb') as f:
                f.write(xml_content)
                
    return [f"status[{response.status_code}]"]



# 사용 예시
if __name__ == "__main__":
    import os
    import asyncio

    import httpx
    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        url = "https://opendart.fss.or.kr/api/list.json"
        API_KEY = os.getenv("DART_API_KEY")
        print(API_KEY)
        async with httpx.AsyncClient() as client:

            result = await update_corplist(
                client = client,
                url = url,
                api_key=API_KEY
            )

        print(result)
        
    asyncio.run(test())