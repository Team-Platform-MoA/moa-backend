from datetime import datetime
from beanie import Document
from typing import Optional
from app.schemas.common import CaregiverType

class Conversation(Document):
    """대화 기록 모델 - 사용자 메시지와 AI 응답을 하나로 관리"""
    user_id: str
    
    user_message: str
    user_timestamp: datetime = datetime.now()
    
    ai_sentiment: str  # positive, neutral, negative
    ai_score: float  # -1.0 ~ 1.0
    ai_comfort_message: str
    ai_timestamp: datetime = datetime.now()
    
    is_processed: bool = True  
    
    class Settings:
        name = "conversations"

class User(Document):
    """사용자 정보 모델"""
    user_id: str
    name: str
    age: Optional[int] = None
    caregiver_type: Optional[CaregiverType] = None  # Enum 타입으로 변경
    caregiver_age: Optional[int] = None
    created_at: datetime = datetime.now()
    last_active: datetime = datetime.now()
    total_conversations: int = 0
    is_onboarded: bool = False  # 온보딩 완료 여부
    
    class Settings:
        name = "users"
