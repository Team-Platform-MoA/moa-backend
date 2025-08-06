from pydantic import BaseModel
from typing import List
from datetime import datetime

class OnboardingResponse(BaseModel):
    user_id: str
    name: str
    age: int
    dependent_type: str
    dependent_age: int
    is_onboarded: bool
    message: str

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