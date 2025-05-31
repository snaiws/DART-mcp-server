from dataclasses import dataclass

@dataclass
class Docstring_get_corp_candidates:
    docstring = """Use this when user-requested-corp-name is not exactly matching official corp-names.
if a company reveals twice in the result, select recent one using modify_date."""