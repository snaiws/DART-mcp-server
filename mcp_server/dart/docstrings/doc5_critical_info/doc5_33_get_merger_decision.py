from dataclasses import dataclass

@dataclass
class Docstring_get_merger_decision:
    docstring = """Get infomation of a company's capital status from it's periodic disclosure in DART system.(증자/감자 현황)
    
Args:
    api_key (str): API authentication key - Issued authentication key (40 characters)
    corp_code (str): Unique code - Unique identification code of the company subject to disclosure (8 characters)
    bgn_de (str): Start date (initial receipt date) - Search start receipt date (YYYYMMDD) ※ Information provided from 2015 onwards
    end_de (str): End date (initial receipt date) - Search end receipt date (YYYYMMDD) ※ Information provided from 2015 onwards
Return:
    response (str): a message including information
"""