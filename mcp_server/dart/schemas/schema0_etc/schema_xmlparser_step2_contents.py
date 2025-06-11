from pydantic import BaseModel, Field

class Schema_xmlparser_step2_contents(BaseModel):
   path_xml: str = Field(
       description = "the path of xml file that you want to analysis"
   )
   title_tags: list = Field(
      description = "List of tag names to treat as titles, obtained from xmlparser_step1_structure"
   )
   section_tags: list = Field(
      description = "List of tag names to treat as sections, obtained from xmlparser_step1_structure"
   )