from dataclasses import dataclass



@dataclass
class Docstring_get_private_fund_usage:
    docstring = """Get information of a company's capital status from its periodic disclosure in DART system.(증자/감자 현황)

Args:
    key(str): API Key for DART system. Ask to user to get this.
    corp_code(str): A unique code of a company, which is used in DART system (8 lengths).
    bsns_year(str): Business year for which capital status is reported (4 lengths, available after 2015).
    reprt_code(str): A unique code of a period (1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011).

Return:
    response(dict): A dictionary containing the following information:
        - rcept_no(str): 접수번호 - 14-digit receipt number. Used for connection to disclosure viewer (e.g., PC: https://dart.fss.or.kr/dsaf001/main.do?rcpNo=접수번호)
        - corp_cls(str): 법인구분 - Corporation classification: Y(유가), K(코스닥), N(코넥스), E(기타)
        - corp_code(str): 고유번호 - Unique company code (8 digits)
        - corp_name(str): 회사명 - Company name
        - se_nm(str): 구분 - Classification
        - tm(str): 회차 - Round/Sequence (added since December 9, 2019)
        - pay_de(str): 납입일 - Payment date
        - pay_amount(str): 납입금액 - Payment amount (9,999,999,999 format, used until January 18, 2018)
        - cptal_use_plan(str): 자금사용 계획 - Capital usage plan (used until January 18, 2018)
        - real_cptal_use_sttus(str): 실제 자금사용 현황 - Actual capital usage status (used until January 18, 2018)
        - mtrpt_cptal_use_plan_useprps(str): 주요사항보고서의 자금사용 계획(사용용도) - Major issue report's capital usage plan (purpose) (added since January 19, 2018)
        - mtrpt_cptal_use_plan_prcure_amount(str): 주요사항보고서의 자금사용 계획(조달금액) - Major issue report's capital usage plan (procurement amount) (9,999,999,999 format, added since January 19, 2018)
        - real_cptal_use_dtls_cn(str): 실제 자금사용 내역(내용) - Actual capital usage details (content) (added since January 19, 2018)
        - real_cptal_use_dtls_amount(str): 실제 자금사용 내역(금액) - Actual capital usage details (amount) (9,999,999,999 format, added since January 19, 2018)
        - dffrnc_occrrnc_resn(str): 차이발생 사유 등 - Reason for differences
        - stlm_dt(str): 결산기준일 - Settlement reference date (YYYY-MM-DD format)
"""