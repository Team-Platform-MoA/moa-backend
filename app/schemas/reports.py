"""
리포트 관련 스키마
"""
from pydantic import BaseModel


class ConversationReportEmotion(BaseModel):
    """감정 분석 데이터"""
    stress: int
    resilience: int
    stability: int


class ConversationReport(BaseModel):
    """사용자 대화에 대한 레포트"""
    emotion_score: int
    daily_summary: str
    emotion_analysis: ConversationReportEmotion
    letter: str
