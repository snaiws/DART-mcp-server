from apimanager import HttpxAPIManager



async def get_employees(
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
        "corp_name": "법인명",
        "fo_bbm": "사업부문",
        "sexdstn": "성별(남, 여)",
        "reform_bfe_emp_co_rgllbr": "개정 전 직원 수 정규직",
        "reform_bfe_emp_co_cnttk": "개정 전 직원 수 계약직",
        "reform_bfe_emp_co_etc": "개정 전 직원 수 기타",
        "rgllbr_co": "정규직 수",
        "rgllbr_abacpt_labrr_co": "정규직 단시간 근로자 수",
        "cnttk_co": "계약직 수",
        "cnttk_abacpt_labrr_co": "계약직 단시간 근로자 수",
        "sm": "합계",
        "avrg_cnwk_sdytrn": "평균 근속 연수",
        "fyer_salary_totamt": "연간 급여 총액",
        "jan_salary_am": "1인평균 급여 액",
        "rm": "비고",
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
        datum = [f"{transform1[k]}: {datum[k]}" for k in transform1 if datum.get(k,"")]
        datum = "\n".join(datum)
        result.append(datum)
    return result

    
    