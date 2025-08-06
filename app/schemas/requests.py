from pydantic import BaseModel, Field
from typing import Optional
from .common import DependentType

class OnboardingRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="사용자 이름")
    age: int = Field(..., ge=1, le=120, description="사용자 나이")
    dependent_type: DependentType = Field(..., description="부양자 유형")
    dependent_age: int = Field(..., ge=1, le=120, description="부양자 나이")

class MessageRequest(BaseModel):
    user_id: str
    message: str

class WebSocketMessage(BaseModel):
    message: str
    user_id: Optional[str] = None 