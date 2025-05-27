from pydantic import BaseModel, Field

class Schema_get_stock_exchange_transfer_decision(BaseModel):
   corp_code: str = Field(
       description="Unique code - Unique identification code of the company subject to disclosure (8 characters)"
   )
   bgn_de: str = Field(
       description="Start date (initial receipt date) - Search start receipt date (YYYYMMDD) ※ Information provided from 2015 onwards"
   )
   end_de: str = Field(
       description="End date (initial receipt date) - Search end receipt date (YYYYMMDD) ※ Information provided from 2015 onwards"
   )