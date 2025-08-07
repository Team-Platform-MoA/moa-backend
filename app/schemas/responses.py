from pydantic import BaseModel
from datetime import datetime
from typing import List

class FamilyMemberResponse(BaseModel):
    """가족 구성원 응답"""
    name: str
    birth_year: int
    gender: str
    dementia_stage: str

class OnboardingResponse(BaseModel):
    """온보딩 완료 응답"""
    user_id: str
    user_name: str
    user_birth_year: int
    user_gender: str
    family_relationship: str
    daily_care_hours: int
    family_member: FamilyMemberResponse
    is_onboarded: bool
    message: str

class AnalysisResponse(BaseModel):
    """감정 분석 응답"""
    sentiment: str
    score: float
    comfort_message: str

class ConversationItem(BaseModel):
    """대화 기록 아이템"""
    id: str
    user_message: str
    user_timestamp: datetime
    ai_sentiment: str
    ai_score: float
    ai_comfort_message: str
    ai_timestamp: datetime

class UserHistoryResponse(BaseModel):
    """사용자 기록 응답"""
    user_id: str
    total_count: int
    conversations: List[ConversationItem] 