"""
AI 클라이언트 기본 추상 클래스
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AIClient(ABC):
    """AI 서비스 클라이언트 기본 클래스"""
    
    @abstractmethod
    async def generate_content(self, prompt: str) -> str:
        """
        프롬프트를 받아 AI 응답을 생성합니다.
        
        Args:
            prompt (str): AI에게 전달할 프롬프트
            
        Returns:
            str: AI 응답 텍스트
        """
        pass
    
    @abstractmethod
    async def generate_structured_content(self, prompt: str, expected_format: str = "json") -> Dict[str, Any]:
        """
        구조화된 응답을 생성합니다.
        
        Args:
            prompt (str): AI에게 전달할 프롬프트
            expected_format (str): 기대하는 응답 형식 (json, xml 등)
            
        Returns:
            Dict[str, Any]: 구조화된 응답 데이터
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        AI 서비스 사용 가능 여부를 확인합니다.
        
        Returns:
            bool: 사용 가능 여부
        """
        pass 