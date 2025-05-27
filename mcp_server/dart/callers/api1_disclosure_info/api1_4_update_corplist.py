import os
import io
import zipfile

from apimanager import HttpxAPIManager



async def update_corplist(
    base_url:str,
    endpoint:str,
    api_key:str, 
    path_base:str
    )->list:

    # API 요청 URL
    params = {
        "crtfc_key":api_key
    }
    os.makedirs(path_base, exist_ok=True)
    filename = "CORPCODE.xml"
    path_corplist = os.path.join(path_base, filename)

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 응답 확인
    if response.status_code == 200:
        # 응답이 성공적인 경우 압축 파일 처리
        zip_file = io.BytesIO(response.content)
        
        # 압축 해제
        with zipfile.ZipFile(zip_file) as z:
            xml_content = z.read(filename)
            
            # XML 파일 저장 (선택사항)
            with open(path_corplist, 'wb') as f:
                f.write(xml_content)
                
    return [f"status[{response.status_code}]"]

    
    
# 사용 예시
if __name__ == "__main__":
    # uv run -m dart.callers.api1_disclosure_info.api1_4_request_corplist
    import os
    import asyncio

    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        base_url = "https://opendart.fss.or.kr/api"
        endpoint = "/corpCode.xml"
        API_KEY = os.getenv("DART_API_KEY")
        path_corplist = "CORPCODE.xml"
        print(API_KEY)

        results = await update_corplist(
            base_url = base_url,
            endpoint = endpoint,
            api_key = API_KEY,
            path_corplist = path_corplist
        )

        for result in results:
            print("---")
            print(result)
        
    asyncio.run(test())