from dataclasses import dataclass

@dataclass
class Docstring_get_capitalstatus:
    docstring = """Get infomation of a company's capital status from it's periodic disclosure in DART system.(증자/감자 현황)

Args:
    key(str): API Key for DART system. Ask to user to get this.
    corp_code(str) : a unique code of a company, which is used in DART system.(8 lengths)
    bsns_year(str) : business year for which capital status is reported(4 lengths, available after of 2015)
    reprt_code(str) : a unique code of a period(1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011)
Return:
    response(str): a message including information()
"""