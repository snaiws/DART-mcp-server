from dataclasses import dataclass

@dataclass
class Docstring_get_disclosure:
    docstring = """[공시정보 - 공시서류원본파일]
    Download a disclosure of a company by corp_code(고유번호) and rcept_no(접수번호)
    재무제표 원본파일의 경우 get_xbrl_financial_statements를 사용할 것
    """