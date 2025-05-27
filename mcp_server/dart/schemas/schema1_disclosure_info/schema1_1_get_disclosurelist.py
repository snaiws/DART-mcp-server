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
       description="(optional) Disclosure type (A, B, C, D, E, F, G, H, I, J)"
   )
   pblntf_detail_ty: str = Field(
       default=None,
       description="(optional) Detailed disclosure type"
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