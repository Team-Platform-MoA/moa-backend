"""
리포트 관련 스키마
"""
from pydantic import BaseModel, Field


class ConversationReportEmotion(BaseModel):
    """감정 분석 데이터"""
    stress: int = Field(..., ge=0, le=100, description="스트레스 수준 (0-100)")
    resilience: int = Field(..., ge=0, le=100, description="회복 탄력성 (0-100)")
    stability: int = Field(..., ge=0, le=100, description="정서 안정성 (0-100)")


class ConversationReport(BaseModel):
    """사용자 대화에 대한 레포트"""
    emotion_score: int = Field(..., ge=1, le=100, description="종합 감정 점수 (1-100)")
    daily_summary: str 
    emotion_analysis: ConversationReportEmotion
    letter: str
