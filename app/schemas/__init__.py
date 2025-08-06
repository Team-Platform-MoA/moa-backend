"""
API 스키마 패키지
"""

from .requests import OnboardingRequest, MessageRequest, WebSocketMessage
from .responses import OnboardingResponse, AnalysisResponse, ConversationItem, UserHistoryResponse
from .common import CaregiverType

__all__ = [
    "OnboardingRequest", "MessageRequest", "WebSocketMessage",
    "OnboardingResponse", "AnalysisResponse", "ConversationItem", "UserHistoryResponse",
    "CaregiverType"
] 