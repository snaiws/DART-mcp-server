from pydantic import BaseModel, Field

class Schema_get_disclosurelist(BaseModel):
   corp_code: str = Field(
       description="(optional) a unique code of a company, which is used in DART system.(8 lengths)"
   )
   bgn_de: str = Field(
       description="(optional) Start date for search (YYYYMMDD)"
   )
   end_de: str = Field(
       description="(optional) End date for search (YYYYMMDD)"
   )
   last_reprt_at: str = Field(
       default="N",
       description="(optional) Search only final reports (Y or N, default: N)"
   )
   pblntf_ty: str = Field(
       default=None,
       description="""(optional) Disclosure type 
       A : 정기공시
        B : 주요사항보고
        C : 발행공시
        D : 지분공시
        E : 기타공시
        F : 외부감사관련
        G : 펀드공시
        H : 자산유동화
        I : 거래소공시
        J : 공정위공시
       """
   )
   pblntf_detail_ty: str = Field(
       default=None,
       description="""(optional) Detailed disclosure type
            "A001": "사업보고서",
            "A002": "반기보고서",
            "A003": "분기보고서",
            "A004": "등록법인결산서류(자본시장법이전)",
            "A005": "소액공모법인결산서류",
            "B001": "주요사항보고서",
            "B002": "주요경영사항신고(자본시장법 이전)",
            "B003": "최대주주등과의거래신고(자본시장법 이전)",
            "C001": "증권신고(지분증권)",
            "C002": "증권신고(채무증권)",
            "C003": "증권신고(파생결합증권)",
            "C004": "증권신고(합병등)",
            "C005": "증권신고(기타)",
            "C006": "소액공모(지분증권)",
            "C007": "소액공모(채무증권)",
            "C008": "소액공모(파생결합증권)",
            "C009": "소액공모(합병등)",
            "C010": "소액공모(기타)",
            "C011": "호가중개시스템을통한소액매출",
            "D001": "주식등의대량보유상황보고서",
            "D002": "임원ㆍ주요주주특정증권등소유상황보고서",
            "D003": "의결권대리행사권유",
            "D004": "공개매수",
            "E001": "자기주식취득/처분",
            "E002": "신탁계약체결/해지",
            "E003": "합병등종료보고서",
            "E004": "주식매수선택권부여에관한신고",
            "E005": "사외이사에관한신고",
            "E006": "주주총회소집공고",
            "E007": "시장조성/안정조작",
            "E008": "합병등신고서(자본시장법 이전)",
            "E009": "금융위등록/취소(자본시장법 이전)",
            "F001": "감사보고서",
            "F002": "연결감사보고서",
            "F003": "결합감사보고서",
            "F004": "회계법인사업보고서",
            "F005": "감사전재무제표미제출신고서",
            "G001": "증권신고(집합투자증권-신탁형)",
            "G002": "증권신고(집합투자증권-회사형)",
            "G003": "증권신고(집합투자증권-합병)",
            "H001": "자산유동화계획/양도등록",
            "H002": "사업/반기/분기보고서",
            "H003": "증권신고(유동화증권등)",
            "H004": "채권유동화계획/양도등록",
            "H005": "수시보고",
            "H006": "주요사항보고서",
            "I001": "수시공시",
            "I002": "공정공시",
            "I003": "시장조치/안내",
            "I004": "지분공시",
            "I005": "증권투자회사",
            "I006": "채권공시",
            "J001": "대규모내부거래관련",
            "J002": "대규모내부거래관련(구)",
            "J004": "기업집단현황공시",
            "J005": "비상장회사중요사항공시",
            "J006": "기타공정위공시"
       """
   )
   corp_cls: str = Field(
       default=None,
       description="(optional) Corporation classification (Y: KOSPI, K: KOSDAQ, N: KONEX, E: Etc)"
   )
   sort: str = Field(
       default="date",
       description="(optional) Sort field (date: Filing date, crp: Company name, rpt: Report name, default: date)"
   )
   sort_mth: str = Field(
       default="desc",
       description="(optional) Sort order (asc: Ascending, desc: Descending, default: desc)"
   )
   page_no: int = Field(
       default=1,
       description="(optional) Page number (1~n, default: 1)"
   )
   page_count: int = Field(
       default=10,
       description="(optional) Number of items per page (1~100, default: 10, max: 100)"
   )