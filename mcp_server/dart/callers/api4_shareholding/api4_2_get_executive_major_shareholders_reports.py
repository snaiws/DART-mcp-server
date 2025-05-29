
from apimanager import HttpxAPIManager



async def get_executive_major_shareholders_reports(
        base_url:str,
        endpoint:str,
        api_key:str, 
        corp_code:str
        )->list:
    
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
        
    # 후처리
    data = response.json()

    transform1 = {
        "rcept_no": "접수번호(14자리)",
        "rcept_dt": "공시 접수일자(YYYY-MM-DD)",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "회사명",
        "repror": "보고자명",
        "isu_exctv_rgist_at": "발행회사 관계 임원 등기여부(등기임원, 비등기임원 등)",
        "isu_exctv_ofcps": "발행회사 관계 임원 직위(대표이사, 이사, 전무 등)",
        "isu_main_shrholdr": "발행회사 관계 주요주주(10%이상주주 등)",
        "sp_stock_lmp_cnt": "특정증권 등 소유수량",
        "sp_stock_lmp_irds_cnt": "특정증권 등 소유 증감수량",
        "sp_stock_lmp_rate": "특정증권 등 소유비율(%)",
        "sp_stock_lmp_irds_rate": "특정증권 등 소유 증감비율(%)"
    }

    result = []
    for datum in data['list']:
        # dict to string
        datum = [f"{transform1[k]}: {datum[k]}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)

    return result