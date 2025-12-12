from pydantic import BaseModel, Field


class ComplaintAnalysis(BaseModel):
    emotion: str = Field(...)
    accused_entities: list[str] = Field(...)
    category: str = Field(...)
    department: str = Field(...)
