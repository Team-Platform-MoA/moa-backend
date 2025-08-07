from datetime import datetime
from beanie import Document
from app.schemas.common import Gender, DementiaStage, FamilyRelationship

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
    """사용자 정보 모델 (부양자 + 부양받는 가족 정보 포함)"""
    user_id: str
    name: str
    birth_year: int
    gender: Gender
    family_relationship: FamilyRelationship
    daily_care_hours: int
    
    # 부양받는 가족 정보
    family_member_name: str
    family_member_birth_year: int
    family_member_gender: Gender
    family_member_dementia_stage: DementiaStage
    
    created_at: datetime = datetime.now()
    last_active: datetime = datetime.now()
    total_conversations: int = 0
    is_onboarded: bool = False  # 온보딩 완료 여부
    
    class Settings:
        name = "users"
