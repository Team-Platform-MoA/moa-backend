"""
AI 클라이언트 팩토리
"""
import logging
from typing import Optional

from app.external.ai.base import AIClient
from app.external.ai.gemini import GeminiClient

logger = logging.getLogger(__name__)


class AIClientFactory:
    """AI 클라이언트 팩토리"""
    
    _instance: Optional[AIClient] = None
    
    @classmethod
    def get_client(cls, client_type: str = "gemini") -> AIClient:
        """
        AI 클라이언트 인스턴스를 반환합니다.
        
        Args:
            client_type (str): 클라이언트 타입 (현재는 "gemini"만 지원)
            
        Returns:
            AIClient: AI 클라이언트 인스턴스
        """
        if cls._instance is None:
            if client_type == "gemini":
                cls._instance = GeminiClient()
            else:
                raise ValueError(f"지원하지 않는 AI 클라이언트 타입: {client_type}")
        
        return cls._instance
    
    @classmethod
    def reset_client(cls):
        """클라이언트 인스턴스를 리셋합니다. (테스트용)"""
        cls._instance = None


# 편의 함수
def get_ai_client() -> AIClient:
    """
    기본 AI 클라이언트를 반환합니다.
    
    Returns:
        AIClient: AI 클라이언트 인스턴스
    """
    return AIClientFactory.get_client() 