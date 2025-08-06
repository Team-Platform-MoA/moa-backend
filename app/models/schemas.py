from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CaregiverType(str, Enum):
    MOTHER = "어머니"
    FATHER = "아버지"
    HUSBAND = "남편"
    WIFE = "아내"
    RELATIVE = "친척"
    IN_LAWS = "시부모님"

class OnboardingRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="사용자 이름")
    age: int = Field(..., ge=1, le=120, description="사용자 나이")
    caregiver_type: CaregiverType = Field(..., description="부양자 유형")
    caregiver_age: int = Field(..., ge=1, le=120, description="부양자 나이")

class OnboardingResponse(BaseModel):
    user_id: str
    name: str
    age: int
    caregiver_type: str
    caregiver_age: int
    is_onboarded: bool
    message: str

class MessageRequest(BaseModel):
    user_id: str
    message: str

class WebSocketMessage(BaseModel):
    message: str
    user_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    sentiment: str
    score: float
    comfort_message: str
    message_id: str
    user_id: str

class ConversationItem(BaseModel):
    id: str
    user_message: str
    user_timestamp: datetime
    ai_sentiment: str
    ai_score: float
    ai_comfort_message: str
    ai_timestamp: datetime

class UserHistoryResponse(BaseModel):
    user_id: str
    total_count: int
    conversations: List[ConversationItem]
