from apimanager import HttpxAPIManager



async def get_private_fund_usage(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bsns_year:str, 
    reprt_code:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()
    
    transform1 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "고유번호(8자리)",
        "corp_name": "회사명",
        "se_nm": "구분",
        "tm": "회차(2019년 12월 9일부터 추가된 사항)",
        "pay_de": "납입일",
        "pay_amount": "납입금액(2018년 1월 18일까지 사용된 사항)",
        "cptal_use_plan": "자금사용 계획(2018년 1월 18일까지 사용된 사항)",
        "real_cptal_use_sttus": "실제 자금사용 현황(2018년 1월 18일까지 사용된 사항)",
        "mtrpt_cptal_use_plan_useprps": "주요사항보고서의 자금사용 계획 사용용도(2018년 1월 19일부터 추가된 사항)",
        "mtrpt_cptal_use_plan_prcure_amount": "주요사항보고서의 자금사용 계획 조달금액(2018년 1월 19일부터 추가된 사항)",
        "real_cptal_use_dtls_cn": "실제 자금사용 내역 내용(2018년 1월 19일부터 추가된 사항)",
        "real_cptal_use_dtls_amount": "실제 자금사용 내역 금액(2018년 1월 19일부터 추가된 사항)",
        "dffrnc_occrrnc_resn": "차이발생 사유 등",
        "stlm_dt": "결산기준일"
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

    
    