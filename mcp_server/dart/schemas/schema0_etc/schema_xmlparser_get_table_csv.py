from pydantic import BaseModel, Field

class Schema_xmlparser_get_table_csv(BaseModel):
   path_xml: str = Field(
       description = "the path of xml file that you want to analysis"
   )
   table_index: int = Field(
      description = "Index of the table to extract (1-based indexing)"
   )