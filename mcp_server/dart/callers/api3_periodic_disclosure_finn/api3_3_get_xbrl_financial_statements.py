import os
import io
import zipfile
import logging

from apimanager import HttpxAPIManager


logger = logging.getLogger()


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
                logger.info(file_info.filename)
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
import os
import io
import zipfile
import logging
import asyncio

from apimanager import HttpxAPIManager


logger = logging.getLogger()


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
                logger.info(file_info.filename)
                if '.xbrl' in file_info.filename:
                    xml_content = z.read(file_info.filename)
                
                    path_finstat = os.path.join(path_corp_finstat, file_info.filename)
                    
                    with open(path_finstat, 'wb') as f:
                        f.write(xml_content)
                    
                    result.append(f"path: {path_finstat}")
                    break  # 첫 번째 .xbrl 파일만 처리하고 종료
                
        if not result:
            result.append("재무제표원본없음")
    else:
        result.append(f"status : {response.status_code}")
    return result


async def main():
    """테스트 함수"""
    # 설정값들 (실제 값으로 변경 필요)
    base_url = "https://opendart.fss.or.kr/api/"
    endpoint = "/fnlttXbrl.xml"
    path_finstats = "."  # 저장할 디렉토리
    api_key = "bcd77770130250d342683f56fca017ae9310860d"  # 실제 API 키로 변경
    corp_code = "00126380"  # 삼성전자 예시
    rcept_no = "20190401004781"  # 예시 접수번호
    reprt_code = "11011"  # 사업보고서
    
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    
    try:
        result = await get_xbrl_financial_statements(
            base_url=base_url,
            endpoint=endpoint,
            path_finstats=path_finstats,
            api_key=api_key,
            corp_code=corp_code,
            rcept_no=rcept_no,
            reprt_code=reprt_code
        )
        
        print("결과:")
        for item in result:
            print(f"  {item}")
            
    except Exception as e:
        print(f"오류 발생: {e}")
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())