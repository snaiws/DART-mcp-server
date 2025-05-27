from pydantic import BaseModel, Field

class Schema_get_single_company_key_indicators(BaseModel):
   api_key: str = Field(
       description="API authentication key - Issued authentication key (40 characters)"
   )
   corp_code: str = Field(
       description="Unique code - Unique identification code of the company subject to disclosure (8 characters) ※ Refer to Development Guide > Disclosure Information > Unique Number"
   )
   bsns_year: str = Field(
       description="Business year - Business year (4 characters) ※ Information provided from 3rd quarter of 2023 onwards"
   )
   reprt_code: str = Field(
       description="Report code - Report code (5 characters) 1st quarter report: 11013, Semi-annual report: 11012, 3rd quarter report: 11014, Business report: 11011"
   )
   idx_cl_code: str = Field(
       description="Index classification code - Index classification code (7 characters) Profitability indicators: M210000, Stability indicators: M220000, Growth indicators: M230000, Activity indicators: M240000"
   )