from dataclasses import dataclass

@dataclass
class Docstring_get_complete_financial_statements:
    docstring = """[정기보고서 재무정보 - 단일회사 전체 재무제표]
    "Provides  all account items \
    from XBRL financial statements within periodic disclosure \
    submitted by listed corporations (securities and KOSDAQ) and \
    major unlisted corporations (subject to business report submission & IFRS application).

    - 주의사항 - 
    1. 본 tool은 재무상태표, 손익계산서, 포괄손익계산서, 현금흐름표, 자본변동표를 제공합니다.
    2. 공시보고서 검색 결과 같은 기간에 연결재무제표와 개별재무제표 둘 다 있다면 연결 재무제표를 우선시합니다.
    3. 당기금액에 대한 계산은 다음과 같습니다.
        - 1분기보고서 (포괄)손익계산서 당기금액 : 1분기 금액
        - 반기보고서 (포괄)손익계산서 당기금액 : 2분기 금액
        - 3분기보고서 (포괄)손익계산서 당기금액 : 3분기 금액
        - 사업보고서 (포괄)손익계산서 당기금액 : 1,2,3,4분기 금액
        - 1분기보고서 현금흐름표 당기금액 : 1분기 금액
        - 반기보고서 현금흐름표 당기금액 : 1,2분기 금액
        - 3분기보고서 현금흐름표 당기금액 : 3분기 금액
        - 사업보고서 현금흐름표 당기금액 : 1,2,3,4분기 금액
        * 따라서 4분기 당기금액 분석을 위해선 모든 보고서를 참고 후 계산해야합니다.
    4. 비교 분석 시 동일한 기간의 금액을 비교하도록 주의하고 반드시 표를 활용하세요.
    """