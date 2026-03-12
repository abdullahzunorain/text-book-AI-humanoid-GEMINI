from pydantic import BaseModel
from typing import Optional, Any


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
