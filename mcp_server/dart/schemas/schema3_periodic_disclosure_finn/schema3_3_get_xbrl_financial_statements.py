from pydantic import BaseModel, Field

class Schema_get_xbrl_financial_statements(BaseModel):
   corp_code: str = Field(
       description="a unique code of a company, which is used in DART system.(8 lengths)"
   )
   rcept_no	: str = Field(
       description="a unique code of disclosure, you can get this by the tool 'get_disclosurelist'"
   )
   reprt_code: str = Field(
       description="a unique code of a period(1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011)"
   )