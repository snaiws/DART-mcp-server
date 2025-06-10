from apimanager import HttpxAPIManager

async def get_disclosurelist(
    base_url:str,
    endpoint:str,
    api_key:str,
    corp_code:str=None,
    bgn_de:str=None,
    end_de:str=None,
    last_reprt_at:str=None,
    pblntf_ty:str=None,
    pblntf_detail_ty:str=None,
    corp_cls:str=None,
    sort:str=None,
    sort_mth:str=None,
    page_no:int=None,
    page_count:int=None
    ) -> list:
    # 요청 파라미터 설정
    params = {
        'crtfc_key': api_key
    }
    
    # 선택적 파라미터 추가
    if corp_code:
        params['corp_code'] = corp_code
    if bgn_de:
        params['bgn_de'] = bgn_de
    if end_de:
        params['end_de'] = end_de
    if last_reprt_at:
        params['last_reprt_at'] = last_reprt_at
    if pblntf_ty:
        params['pblntf_ty'] = pblntf_ty
    if pblntf_detail_ty:
        params['pblntf_detail_ty'] = pblntf_detail_ty
    if corp_cls:
        params['corp_cls'] = corp_cls
    if sort:
        params['sort'] = sort
    if sort_mth:
        params['sort_mth'] = sort_mth
    if page_no:
        params['page_no'] = page_no
    if page_count:
        params['page_count'] = page_count
        
    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()


    transform1 = {
        "corp_cls": "법인구분",
        "corp_name": "법인명",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "stock_code": "상장회사의 종목코드(6자리)",
        "report_nm": "보고서명",
        "rcept_no": "접수번호(14자리)",
        "flr_nm": "공시 제출인명",
        "rcept_dt": "공시 접수일자",
    }
    transform2 = {
        "Y":"유가",
        "K":"코스닥",
        "N":"코넥스",
        "E":"기타",
    }
    transform3 = {
        "유" : "본 공시사항은 한국거래소 유가증권시장본부 소관임",
        "코" : "본 공시사항은 한국거래소 코스닥시장본부 소관임",
        "채" : "본 문서는 한국거래소 채권상장법인 공시사항임",
        "넥" : "본 문서는 한국거래소 코넥스시장 소관임",
        "공" : "본 공시사항은 공정거래위원회 소관임",
        "연" : "본 보고서는 연결부분을 포함한 것임",
        "정" : "본 보고서 제출 후 정정신고가 있으니 관련 보고서를 참조하시기 바람",
        "철" : "본 보고서는 철회(간주)되었으니 관련 철회신고서(철회간주안내)를 참고하시기 바람"
    }

    result = []
    for datum in data['list']:
        # 비고처리
        rm = datum.pop('rm')
        rm = [f"비고{i+1}: {transform3[x]}" for i, x in enumerate(rm)]
        # 법인구분처리
        datum['corp_cls'] = transform2[datum['corp_cls']]
        datum = [f"{transform1[k]}: {datum[k]}" for k in transform1 if datum.get(k,"")] + rm
        datum = "\n".join(datum)
        result.append(datum)
    return result


    
# 사용 예시
if __name__ == "__main__":
    # uv run -m dart.callers.api1_disclosure_info.api1_1_search_report
    import os
    import asyncio

    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    async def test():
        base_url = "https://opendart.fss.or.kr/api"
        endpoint = "/list.json"
        API_KEY = os.getenv("DART_API_KEY")
        corp_code = "00126380"
        bgn_de="20240101"
        end_de="20241231"
        print(API_KEY)

        results = await get_disclosurelist(
            base_url = base_url,
            endpoint = endpoint,
            api_key = API_KEY,
            corp_code = corp_code,  # 삼성전자 고유번호
            bgn_de = bgn_de,
            end_de = end_de
        )

        for result in results:
            print("---")
            print(result)
        
    asyncio.run(test())