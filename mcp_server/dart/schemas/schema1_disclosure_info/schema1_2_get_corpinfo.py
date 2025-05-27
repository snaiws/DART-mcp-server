from pydantic import BaseModel, Field

class Schema_get_corpinfo(BaseModel):
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )