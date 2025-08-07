"""
API 스키마 패키지
"""

from .requests import CompleteOnboardingRequest, FamilyMemberInfo, MessageRequest, WebSocketMessage
from .responses import OnboardingResponse, AnalysisResponse, ConversationItem, UserHistoryResponse, FamilyMemberResponse
from .common import Gender, DementiaStage, FamilyRelationship

__all__ = [
    "CompleteOnboardingRequest", "FamilyMemberInfo", "MessageRequest", "WebSocketMessage",
    "OnboardingResponse", "AnalysisResponse", "ConversationItem", "UserHistoryResponse", "FamilyMemberResponse",
    "Gender", "DementiaStage", "FamilyRelationship"
] 