from apimanager import HttpxAPIManager



async def get_business_suspension(
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
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "bsnsp_rm": "영업정지 분야",
        "bsnsp_amt": "영업정지금액",
        "rsl": "최근매출총액",
        "sl_vs": "매출액 대비",
        "ls_atn": "대규모법인여부",
        "krx_stt_atn": "거래소 의무공시 해당 여부",
        "bsnsp_cn": "영업정지 내용",
        "bsnsp_rs": "영업정지사유",
        "ft_ctp": "향후대책",
        "bsnsp_af": "영업정지영향",
        "bsnspd": "영업정지일자",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석",
        "od_a_at_b": "사외이사 불참",
        "adt_a_atn": "감사(감사위원) 참석여부"
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

    