from pydantic import BaseModel, Field

class Schema_get_single_company_accounts(BaseModel):
   corp_code: str = Field(
       description="Unique code - Unique identification code of the company subject to disclosure (8 characters) ※ Refer to Development Guide > Disclosure Information > Unique Number"
   )
   bsns_year: str = Field(
       description="Business year - Business year (4 characters) ※ Information provided from 2015 onwards"
   )
   reprt_code: str = Field(
       description="Report code - Report code (5 characters) 1st quarter report: 11013, Semi-annual report: 11012, 3rd quarter report: 11014, Business report: 11011"
   )