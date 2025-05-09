from dataclasses import dataclass

@dataclass
class Docstring_update_corplist:
    docstring = """download corp_list, that contains corp_code/corp_name, for using other APIs. 

Args:
    key(str): API Key for DART system. Ask to user to get this.
Return:
    response(str): answering corp_code or questioning candidates
"""