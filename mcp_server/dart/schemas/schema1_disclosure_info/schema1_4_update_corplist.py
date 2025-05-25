from pydantic import BaseModel, Field

class Schema_update_corplist(BaseModel):
   api_key: str = Field(
       description="API Key for DART system. Ask to user to get this."
   )