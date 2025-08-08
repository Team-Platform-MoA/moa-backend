"""
AI 클라이언트 팩토리
"""
import logging
from typing import Optional

from app.external.ai.base import AIClient
from app.external.ai.gemini import GeminiClient
from app.external.ai.openai import OpenAIClient

logger = logging.getLogger(__name__)


class AIClientFactory:
    """AI 클라이언트 팩토리"""
    
    _instances: dict = {}
    
    @classmethod
    def get_client(cls, client_type: str = "openai") -> AIClient:
        """
        AI 클라이언트 인스턴스를 반환합니다.
        
        Args:
            client_type (str): 클라이언트 타입 ("openai", "gemini")
            
        Returns:
            AIClient: AI 클라이언트 인스턴스
        """
        if client_type not in cls._instances:
            if client_type == "openai":
                cls._instances[client_type] = OpenAIClient()
            elif client_type == "gemini":
                cls._instances[client_type] = GeminiClient()
            else:
                raise ValueError(f"지원하지 않는 AI 클라이언트 타입: {client_type}")
        
        return cls._instances[client_type]
    
    @classmethod
    def reset_clients(cls):
        """클라이언트 인스턴스들을 리셋합니다. (테스트용)"""
        cls._instances = {}


# 편의 함수
def get_ai_client(client_type: str = "openai") -> AIClient:
    """
    기본 AI 클라이언트를 반환합니다.
    
    Args:
        client_type (str): 클라이언트 타입 (기본값: "openai")
        
    Returns:
        AIClient: AI 클라이언트 인스턴스
    """
    return AIClientFactory.get_client(client_type) 