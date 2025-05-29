from pydantic import BaseModel, Field

class Schema_get_executive_major_shareholders_reports(BaseModel):
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )