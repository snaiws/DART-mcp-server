from dataclasses import dataclass

@dataclass
class Docstring_get_corpinfo:
    docstring = """Get rough infomation of a company(기업개황) from DART system.

Args:
    key(str): API Key for DART system. Ask to user to get this.
    corp_code(str) : a unique code of a company, which is used in DART system.(8 lengths)
Return:
    response(str): a message including information()
"""