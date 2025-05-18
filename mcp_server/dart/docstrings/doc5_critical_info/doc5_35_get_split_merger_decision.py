from dataclasses import dataclass

@dataclass
class Docstring_get_split_merger_decision:
    docstring = """Provides key information within the Major Issue Report (Decision on Company Split-Merger).

    Args:
        crtfc_key(str): API authentication key (40 characters) issued by DART system.
        corp_code(str): Unique company code used in DART system (8 characters).
        bgn_de(str): Start date (initial receipt date) in format YYYYMMDD. Information available from 2015 onwards.
        end_de(str): End date (initial receipt date) in format YYYYMMDD. Information available from 2015 onwards.
    
    Return:
        response(str): A message including information about stock exchange and transfer decisions.
    """