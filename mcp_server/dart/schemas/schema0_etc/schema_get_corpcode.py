from pydantic import BaseModel, Field

class Schema_get_corpcode(BaseModel):
   corp_name: str = Field(
       description="a corp name that user requested. Korean or English name available."
   )