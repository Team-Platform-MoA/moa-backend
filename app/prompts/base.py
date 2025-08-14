"""
프롬프트 기본 클래스
"""
from abc import ABC, abstractmethod


class BasePrompt(ABC):
    """프롬프트 기본 클래스"""
    
    @abstractmethod
    def generate(self, **kwargs) -> str:
        """
        프롬프트를 생성합니다.
        
        Args:
            **kwargs: 프롬프트 생성에 필요한 매개변수들
            
        Returns:
            str: 생성된 프롬프트
        """
        pass
    
    @abstractmethod
    def get_expected_format(self) -> str:
        """
        기대하는 응답 형식을 반환합니다.
        
        Returns:
            str: 응답 형식 (json, text 등)
        """
        pass 