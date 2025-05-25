from dataclasses import dataclass

@dataclass
class Docstring_get_tangible_asset_disposal:
    docstring = """Provides key information of Decision on Tangible Asset Transfer, within the Major Matters Report
    
Args:
    api_key (str): API authentication key - Issued authentication key (40 characters)
    corp_code (str): Unique code - Unique identification code of the company subject to disclosure (8 characters)
    bgn_de (str): Start date (initial receipt date) - Search start receipt date (YYYYMMDD) ※ Information provided from 2015 onwards
    end_de (str): End date (initial receipt date) - Search end receipt date (YYYYMMDD) ※ Information provided from 2015 onwards
Return:
    response (str): a message including information
"""