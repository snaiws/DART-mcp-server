from pydantic import BaseModel, Field

class Schema_xmlparser_step3_query(BaseModel):
   path_xml: str = Field(
       description = "the path of xml file that you want to analysis"
   )
   selector: str = Field(
      description = "CSS selector or tag name to search for (e.g., 'TABLE', 'div table', '.class-name')"
   )
   limit: int = Field(
      description = "Maximum number of results to show (default: 5)"
   )