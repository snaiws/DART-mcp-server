from dataclasses import dataclass

@dataclass
class Docstring_get_stock_exchange_transfer_decision:
    docstring = """Provides key information of The Major Issue Report (Decision on Stock Exchange/Transfer) .

Args:
    api_key(str): API Key for DART system. Ask to user to get this.
    corp_code(str): Unique company code used in DART system (8 characters).
    bgn_de(str): Start date (initial receipt date) in format YYYYMMDD. Information available from 2015 onwards.
    end_de(str): End date (initial receipt date) in format YYYYMMDD. Information available from 2015 onwards.

Return:
    response(str): a message including information()
"""
