from dataclasses import dataclass

@dataclass
class Docstring_get_corp_candidates:
    docstring = """Use this when user-requested-corp-name is not exactly matching official corp-names.
if a company reveals twice in the result, select recent one using modify_date.
Args:
    corp_name_input(str): a corp name that user requested. Korean or English name available.
    n(int) : number of candidates
Return:
    response(str): corp candidates that is similar to user-request
"""