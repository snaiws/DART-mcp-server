from dataclasses import dataclass

@dataclass
class Docstring_get_corpcode:
    docstring = """Get corp_code for using other APIs. 

Args:
    corp_name_input(str): a corp name that user requested. Korean or English name available.
Return:
    response(str): answering corp_code
"""