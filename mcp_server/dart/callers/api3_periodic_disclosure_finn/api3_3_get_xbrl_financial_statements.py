import os
import io
import zipfile

from apimanager import HttpxAPIManager



async def get_xbrl_financial_statements(
    base_url:str,
    endpoint:str,
    path_finstats:str,
    api_key:str,
    corp_code:str,
    rcept_no:str,
    reprt_code:str
    )->list:

    # API 요청 URL
    params = {
        "crtfc_key":api_key,
        "rcept_no":rcept_no,
        "reprt_code":reprt_code
    }


    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    path_corp_finstat = os.path.join(path_finstats, corp_code)
    os.makedirs(path_corp_finstat, exist_ok=True)

    result = []
    # 응답 확인
    if response.status_code == 200:
        # 응답이 성공적인 경우 압축 파일 처리
        zip_file = io.BytesIO(response.content)
        # 압축 해제
        with zipfile.ZipFile(zip_file) as z:
            print("압축파일 내 파일 목록:")
            for file_info in z.filelist:
                if '.xbrl' in file_info.filename:
                    xml_content = z.read(file_info.filename)
                
                    path_finstat = os.path.join(path_corp_finstat, file_info.filename)
                    # XML 파일 저장 (선택사항)
                    with open(path_finstat, 'wb') as f:
                        f.write(xml_content)
                    break
                
                result.append(f"path: {path_finstat}")
            if not result:
                result.append("재무제표원본없음")
    else:
        result.append(f"status : {response.status_code}")
    return result
    