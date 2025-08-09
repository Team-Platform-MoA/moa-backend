from datetime import datetime
from typing import Optional
from beanie import Document
from app.schemas.common import Gender, DementiaStage, FamilyRelationship
from app.utils.common import get_korea_now
from app.core.constants import Defaults

class Conversation(Document):
    """대화 기록 모델 - 사용자 메시지와 AI 응답을 하나로 관리"""
    user_id: str
    conversation_date: str
    
    user_message: str
    user_timestamp: datetime = get_korea_now()
    
    ai_sentiment: str
    ai_score: float
    ai_comfort_message: str
    ai_timestamp: datetime = get_korea_now()
    
    is_processed: bool = Defaults.CONVERSATION_PROCESSED_STATUS
    
    audio_uri_1: Optional[str] = None
    audio_uri_2: Optional[str] = None
    audio_uri_3: Optional[str] = None
    
    class Settings:
        name = "conversations"

class User(Document):
    """사용자 정보 모델 (부양자 + 부양받는 가족 정보 포함)"""
    user_id: str
    name: str
    birth_year: int
    gender: Gender
    family_relationship: FamilyRelationship
    daily_care_hours: int
    
    family_member_nickname: str
    family_member_birth_year: int
    family_member_gender: Gender
    family_member_dementia_stage: DementiaStage
    
    created_at: datetime = get_korea_now()
    last_active: datetime = get_korea_now()
    total_conversations: int = Defaults.USER_CONVERSATIONS_COUNT
    is_onboarded: bool = Defaults.USER_ONBOARDED_STATUS
    
    class Settings:
        name = "users"
