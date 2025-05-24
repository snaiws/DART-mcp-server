from pydantic import BaseModel, Field

class Schema_get_corpinfo(BaseModel):
   api_key: str = Field(
       description="API Key for DART system. Ask to user to get this."
   )
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )