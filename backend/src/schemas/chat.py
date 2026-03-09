from pydantic import BaseModel, Field
from typing import List, Optional, Any


class Source(BaseModel):
    chapter: str
    module: str
    score: float


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=2000)
    session_id: str = Field(..., description="UUID for conversation grouping")
    selected_text: Optional[str] = Field(None, max_length=3000)


class ChatResponse(BaseModel):
    response: str
    sources: List[Source] = []
    session_id: str
    context_count: int = 0
    context_used: bool = False


class PersonalizeRequest(BaseModel):
    content: str
    chapter_title: str


class PersonalizeResponse(BaseModel):
    personalized_content: str
    user_background: Optional[Any] = None


class TranslateRequest(BaseModel):
    content: str
    chapter_title: str


class TranslateResponse(BaseModel):
    translated_content: str
    language: str = "Urdu"
