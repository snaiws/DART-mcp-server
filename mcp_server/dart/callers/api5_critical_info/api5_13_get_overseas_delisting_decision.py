from apimanager import HttpxAPIManager



async def get_overseas_delisting_decision(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bgn_de:str, 
    end_de:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': bgn_de,
        'end_de': end_de
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()
    
    transform1 = {
        "rcept_no": "접수번호",
        "corp_cls": "법인구분",
        "corp_code": "고유번호",
        "corp_name": "회사명",
        "dlststk_ostk_cnt": "상장폐지 보통주식 수 (단위: 주)",
        "dlststk_estk_cnt": "상장폐지 기타주식 수 (단위: 주)",
        "lstex_nt": "상장거래소 소재 국가",
        "dlstrq_prd": "폐지 신청 예정일자",
        "dlst_prd": "폐지 예정일자",
        "dlst_rs": "상장폐지 사유",
        "bddd": "이사회 결의일 또는 확인일",
        "od_a_at_t": "사외이사 참석 인원수",
        "od_a_at_b": "사외이사 불참 인원수",
        "adt_a_atn": "감사 또는 감사위원 참석 여부"
    }


    transform2 = {
        "Y":"유가",
        "K":"코스닥",
        "N":"코넥스",
        "E":"기타",
    }
    

    result = []
    for datum in data['list']:
        # 법인구분처리
        datum['corp_cls'] = transform2[datum['corp_cls']]
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result

    