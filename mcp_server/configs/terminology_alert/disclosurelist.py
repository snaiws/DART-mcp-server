from dataclasses import dataclass, field

from .base import Terminology  # 별도 파일에 선언된 dataclass



@dataclass    
class TerminologyDisclosureList(Terminology):
    corp_cls: str = "법인구분(Y(유가), K(코스닥), N(코넥스), E(기타))"
    corp_name: str = "법인명"
    corp_code: str = "공시대상회사의 고유번호(8자리)"
    stock_code: str = "상장회사의 종목코드(6자리)"
    report_nm: str = "보고서명"
    rcept_no: str = "접수번호(14자리)"
    flr_nm: str = "공시 제출인명"
    rcept_dt: str = "공시 접수일자"
#     rm: tuple = field(default_factory=lambda: ("비고",{
#             "유" : "본 공시사항은 한국거래소 유가증권시장본부 소관임",
#             "코" : "본 공시사항은 한국거래소 코스닥시장본부 소관임",
#             "채" : "본 문서는 한국거래소 채권상장법인 공시사항임",
#             "넥" : "본 문서는 한국거래소 코넥스시장 소관임",
#             "공" : "본 공시사항은 공정거래위원회 소관임",
#             "연" : "본 보고서는 연결부분을 포함한 것임",
#             "정" : "본 보고서 제출 후 정정신고가 있으니 관련 보고서를 참조하시기 바람",
#             "철" : "본 보고서는 철회(간주)되었으니 관련 철회신고서(철회간주안내)를 참고하시기 바람"
#     }))