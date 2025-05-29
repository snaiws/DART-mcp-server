from pydantic import BaseModel, Field

class Schema_get_public_fund_usage(BaseModel):
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )
   bsns_year: str = Field(
       description="business year for which capital status is reported(4 lengths, available after of 2015)"
   )
   reprt_code: str = Field(
       description="a unique code of a period(1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011)"
   )