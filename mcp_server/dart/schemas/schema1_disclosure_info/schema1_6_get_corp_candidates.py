from pydantic import BaseModel, Field

class Schema_get_corp_candidates(BaseModel):
   corp_name: str = Field(
       description="a corp name that user requested. Korean or English name available."
   )
   n: int = Field(
       description="number of candidates"
   )