from pydantic import BaseModel, Field

class Schema_get_disclosurelist(BaseModel):
   api_key: str = Field(
       description="API Key for DART system. Ask to user to get this."
   )
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )
   bgn_de: str = Field(
       description="Start date for search (YYYYMMDD)"
   )
   end_de: str = Field(
       description="End date for search (YYYYMMDD)"
   )
   last_reprt_at: str = Field(
       default="N",
       description="Search only final reports (Y or N, default: N)"
   )
   pblntf_ty: str = Field(
       default=None,
       description="Disclosure type (A, B, C, D, E, F, G, H, I, J)"
   )
   pblntf_detail_ty: str = Field(
       default=None,
       description="Detailed disclosure type"
   )
   corp_cls: str = Field(
       default=None,
       description="Corporation classification (Y: KOSPI, K: KOSDAQ, N: KONEX, E: Etc)"
   )
   sort: str = Field(
       default="date",
       description="Sort field (date: Filing date, crp: Company name, rpt: Report name, default: date)"
   )
   sort_mth: str = Field(
       default="desc",
       description="Sort order (asc: Ascending, desc: Descending, default: desc)"
   )
   page_no: int = Field(
       default=1,
       description="Page number (1~n, default: 1)"
   )
   page_count: int = Field(
       default=10,
       description="Number of items per page (1~100, default: 10, max: 100)"
   )