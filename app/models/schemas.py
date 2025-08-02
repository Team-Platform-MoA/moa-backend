from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
