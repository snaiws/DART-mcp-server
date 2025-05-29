from apimanager import HttpxAPIManager



async def get_major_holding_reports(
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
        "rcept_no": "접수번호",
        "rcept_dt": "공시 접수일자(YYYYMMDD)",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사의 종목명(상장사) 또는 법인명(기타법인)",
        "report_tp": "주식등의 대량보유상황 보고구분",
        "repror": "대표보고자",
        "stkqy": "보유주식등의 수",
        "stkqy_irds": "보유주식등의 증감",
        "stkrt": "보유비율",
        "stkrt_irds": "보유비율 증감",
        "ctr_stkqy": "주요체결 주식등의 수",
        "ctr_stkrt": "주요체결 보유비율",
        "report_resn": "보고사유"
    }

    result = []
    for datum in data['list']:
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)

    return result