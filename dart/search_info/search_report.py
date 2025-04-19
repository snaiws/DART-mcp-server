async def get_disclosurelist(
    client,
    url:str,
    api_key:str,
    corp_code:str,
    bgn_de:str,
    end_de:str,
    last_reprt_at:str='N',
    pblntf_ty:str=None,
    pblntf_detail_ty:str=None,
    corp_cls:str=None,
    sort:str='date',
    sort_mth:str='desc',
    page_no:int=1,
    page_count:int=10
):
    """
    DART 시스템에서 공시 정보 목록을 가져오는 함수 (httpx 사용)
    corp_code를 필수로 제한(목적상)
    bgn_de, end_de가 없으면 검색결과가 있어도 안나올 수 있으므로 필수로 제한
    
    Args:
        api_key (str): 발급받은 API 인증키 (40자리)
        corp_code (str): 공시대상회사의 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (YYYYMMDD)
        end_de (str): 검색종료 접수일자 (YYYYMMDD)
        last_reprt_at (str, optional): 최종보고서만 검색여부 (Y or N, 기본값: N)
        pblntf_ty (str, optional): 공시유형 (A, B, C, D, E, F, G, H, I, J)
        pblntf_detail_ty (str, optional): 공시상세유형
        corp_cls (str, optional): 법인구분 (Y: 유가, K: 코스닥, N: 코넥스, E: 기타)
        sort (str, optional): 정렬 기준 (date: 접수일자, crp: 회사명, rpt: 보고서명, 기본값: date)
        sort_mth (str, optional): 정렬방법 (asc: 오름차순, desc: 내림차순, 기본값: desc)
        page_no (int, optional): 페이지 번호 (1~n, 기본값: 1)
        page_count (int, optional): 페이지당 건수 (1~100, 기본값: 10, 최대값: 100)
    
    Returns:
        dict: API 응답 결과
    """
    # 요청 파라미터 설정
    params = {
        'crtfc_key': api_key,
        'last_reprt_at': last_reprt_at,
        'sort': sort,
        'sort_mth': sort_mth,
        'page_no': page_no,
        'page_count': page_count
    }
    
    # 선택적 파라미터 추가
    if corp_code:
        params['corp_code'] = corp_code
    if bgn_de:
        params['bgn_de'] = bgn_de
    if end_de:
        params['end_de'] = end_de
    if pblntf_ty:
        params['pblntf_ty'] = pblntf_ty
    if pblntf_detail_ty:
        params['pblntf_detail_ty'] = pblntf_detail_ty
    if corp_cls:
        params['corp_cls'] = corp_cls
    
    # 클라이언트로 API 요청 보내기
    response = await client.get(url, params=params)
    
    data = response.json()

    return data


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
    print(API_KEY)
    
    result = asyncio.run(get_disclosurelist(
        client = client,
        url = url,
        api_key=API_KEY,
        corp_code="00126380",  # 삼성전자 고유번호
        bgn_de="20240101",
        end_de="20241231",
    ))
    print(result)