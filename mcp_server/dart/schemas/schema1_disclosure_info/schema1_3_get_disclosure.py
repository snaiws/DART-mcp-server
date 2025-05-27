from pydantic import BaseModel, Field

class Schema_get_disclosure(BaseModel):
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )
   rcept_no: str = Field(
       description="rcept_no(접수번호) for searching information of disclosure. Use 'get_disclosurelist' to get this."
   )