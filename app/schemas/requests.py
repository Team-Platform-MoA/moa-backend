from pydantic import BaseModel, Field
from typing import Optional
from .common import Gender, DementiaStage, FamilyRelationship

class FamilyMemberInfo(BaseModel):
    """가족 구성원 정보"""
    name: str = Field(..., min_length=1, max_length=50, description="가족 구성원 이름")
    birth_year: int = Field(..., ge=1900, le=2024, description="출생년도 (4자리)")
    gender: Gender = Field(..., description="성별")
    dementia_stage: DementiaStage = Field(..., description="치매 정도")

class CompleteOnboardingRequest(BaseModel):
    """완전한 온보딩 요청 - 사용자 + 가족 정보"""
    # 사용자 정보 (My Profile Setup)
    user_name: str = Field(..., min_length=1, max_length=50, description="사용자 이름")
    user_birth_year: int = Field(..., ge=1900, le=2024, description="사용자 출생년도 (4자리)")
    user_gender: Gender = Field(..., description="사용자 성별")
    family_relationship: FamilyRelationship = Field(..., description="가족과의 관계")
    daily_care_hours: int = Field(..., ge=1, le=24, description="하루 돌봄 시간 (시간)")
    
    # 가족 정보 (Family Profile Setup)
    family_member: FamilyMemberInfo = Field(..., description="부양해야 할 가족 구성원 정보")

class MessageRequest(BaseModel):
    user_id: str
    message: str

class WebSocketMessage(BaseModel):
    message: str
    user_id: Optional[str] = None 