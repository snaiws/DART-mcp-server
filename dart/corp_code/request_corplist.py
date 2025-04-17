import io
import zipfile

import httpx



async def update_corplist(url:str, key:str, path_corplist:str)->str:
    # API 요청 URL
    url = url.format(key=key)
    path_zip_corplist = "CORPCODE.xml"

    # GET 요청 보내기
    with httpx.Client() as client:
        response = client.get(url)
        
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
                
        return str(response.status_code)
        # print(f"API 요청 실패: {response.status_code}")
        # print(response.text)


if __name__ == "__main__":
    key = ""
    update_corplist(key)