import io
import zipfile

import httpx



async def update_corplist(client, url:str, api_key:str, path_corplist:str)->str:
    # API 요청 URL
    url = url.format(api_key=api_key)
    path_zip_corplist = "CORPCODE.xml"

    # GET 요청 보내기
    response = await client.get(url)
    
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
                
    return response



# 사용 예시
if __name__ == "__main__":
    import os
    import asyncio

    import httpx
    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    url = "https://opendart.fss.or.kr/api/list.json"
    API_KEY = os.getenv("DART_API_KEY")
    client = httpx.Client()
    asyncio.run(update_corplist(
            client = client,
            url = url,
            api_key=API_KEY
    ))