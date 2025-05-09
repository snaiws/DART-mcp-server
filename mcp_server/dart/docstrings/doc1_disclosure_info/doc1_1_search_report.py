from dataclasses import dataclass

@dataclass
class Docstring_get_disclosurelist:
    docstring = """Get list of disclosure of a company. you can narrow the result by optional inputs.

Args:
    key (str): API Key for DART system. Ask to user to get this.
    corp_code(str) : a unique code of a company, which is used in DART system.(8 lengths)
    bgn_de (str): Start date for search (YYYYMMDD)
    end_de (str): End date for search (YYYYMMDD)
    last_reprt_at (str, optional): Search only final reports (Y or N, default: N)  
    pblntf_ty (str, optional): Disclosure type (A, B, C, D, E, F, G, H, I, J)  
    pblntf_detail_ty (str, optional): Detailed disclosure type  
    corp_cls (str, optional): Corporation classification (Y: KOSPI, K: KOSDAQ, N: KONEX, E: Etc)
    sort (str, optional): Sort field (date: Filing date, crp: Company name, rpt: Report name, default: date)
    sort_mth (str, optional): Sort order (asc: Ascending, desc: Descending, default: desc)  
    page_no (int, optional): Page number (1~n, default: 1)  
    page_count (int, optional): Number of items per page (1~100, default: 10, max: 100)  
Return:
    response(str): a message including information()
"""