import os
import io
import zipfile

from apimanager import HttpxAPIManager



async def get_disclosure(
    base_url:str,
    endpoint:str,
    path_disclosures:str,
    api_key:str, 
    corp_code:str,
    rcept_no:str,
    )->list:

    # API 요청 URL
    params = {
        "crtfc_key":api_key,
        "rcept_no":rcept_no,
    }
    path_disclosure_corp = os.path.join(path_disclosures, corp_code)
    os.makedirs(path_disclosure_corp, exist_ok=True)

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)

    result = []
    result.append(f"status[{response.status_code}]")
    # 응답 확인
    if response.status_code == 200:
        # 응답이 성공적인 경우 압축 파일 처리
        zip_file = io.BytesIO(response.content)
        # 압축 해제
        with zipfile.ZipFile(zip_file) as z:
            xml_content = z.read(f"{rcept_no}.xml")
            
            path_disclosure = os.path.join(path_disclosure_corp, f"{rcept_no}.xml")
            # XML 파일 저장 (선택사항)
            with open(path_disclosure, 'wb') as f:
                f.write(xml_content)
        result.append(f"path: {path_disclosure}")
        
    return result



# 사용 예시
if __name__ == "__main__":
    # uv run -m dart.callers.api1_disclosure_info.api1_3_get_disclosure
    import os
    import asyncio

    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        base_url = "https://opendart.fss.or.kr/api"
        endpoint = "/document.xml"
        path_disclosures = "."
        API_KEY = os.getenv("DART_API_KEY")
        corp_code = "00000000"
        rcept_no = "20190401004781"
        print(API_KEY)

        results = await get_disclosure(
            base_url = base_url,
            endpoint = endpoint,
            path_disclosures = path_disclosures,
            api_key = API_KEY,
            corp_code = corp_code,
            rcept_no = rcept_no
        )

        for result in results:
            print("---")
            print(result)
        
    asyncio.run(test())