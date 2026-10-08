from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    question: str
    history: list[dict] = Field(default_factory=list)


class AIResponse(BaseModel):
    question: str
    answer: str