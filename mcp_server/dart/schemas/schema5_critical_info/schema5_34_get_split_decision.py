from pydantic import BaseModel, Field

class Schema_get_split_decision(BaseModel):
   api_key: str = Field(
       description="API authentication key - Issued authentication key (40 characters)"
   )
   corp_code: str = Field(
       description="Unique code - Unique identification code of the company subject to disclosure (8 characters)"
   )
   bgn_de: str = Field(
       description="Start date (initial receipt date) - Search start receipt date (YYYYMMDD) ※ Information provided from 2015 onwards"
   )
   end_de: str = Field(
       description="End date (initial receipt date) - Search end receipt date (YYYYMMDD) ※ Information provided from 2015 onwards"
   )