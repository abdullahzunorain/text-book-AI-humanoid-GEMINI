from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    hardware_background: Optional[str] = None
    software_background: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    hardware_background: Optional[str] = None
    software_background: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
