from dataclasses import dataclass

@dataclass
class Docstring_get_multi_company_accounts:
    docstring = """[정기보고서 재무정보 - 다중회사 주요계정]
    Provides major account items (statement of financial position, income statement) \
    from XBRL financial statements within periodic disclosures \
    submitted by listed corporations (securities and KOSDAQ) \
    and major unlisted corporations (subject to business report submission & IFRS application).
    (Multiple companies inquiry available)
    """