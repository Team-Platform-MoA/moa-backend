from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class FamilyMemberResponse(BaseModel):
    """가족 구성원 응답"""
    nickname: str
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

class AudioAnswerResponse(BaseModel):
    """오디오 답변 처리 응답"""
    success: bool
    conversation_id: str = None
    question_number: int
    question_text: str = None
    message: str = None
    
    audio_uri_1: Optional[str] = None
    audio_uri_2: Optional[str] = None
    audio_uri_3: Optional[str] = None
    
    user_message: Optional[str] = None
    
    user_id: str
    error: str = None

class ConversationItem(BaseModel):
    """대화 기록 아이템"""
    id: str
    conversation_date: str
    user_message: str
    user_timestamp: datetime
    ai_sentiment: str
    ai_score: float
    ai_comfort_message: str
    ai_timestamp: datetime
    audio_uri_1: Optional[str] = None
    audio_uri_2: Optional[str] = None
    audio_uri_3: Optional[str] = None

class UserHistoryResponse(BaseModel):
    """사용자 기록 응답"""
    user_id: str
    total_count: int
    conversations: List[ConversationItem]