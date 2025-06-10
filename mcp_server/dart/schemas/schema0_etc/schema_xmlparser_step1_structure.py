from pydantic import BaseModel, Field

class Schema_xmlparser_step1_structure(BaseModel):
   path_xml: str = Field(
       description = "the path of xml file that you want to analysis"
   )
   max_depth: int = Field(
      description = "Maximum depth level to explore (default: 4)"
   )