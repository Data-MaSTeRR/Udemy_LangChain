from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description="summary") # 요약
    facts: List[str] = Field(description="interesting facts about them") # 흥미로운 사실들

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)


