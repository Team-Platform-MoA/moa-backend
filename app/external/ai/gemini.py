"""
Gemini AI 클라이언트 구현
"""
import json
import re
import logging
from typing import Dict, Any

import google.generativeai as genai

from app.core.config import settings
from app.external.ai.base import AIClient

logger = logging.getLogger(__name__)


class GeminiClient(AIClient):
    """Gemini AI 클라이언트"""
    
    def __init__(self):
        """Gemini 클라이언트 초기화"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-pro")
            self._available = True
        except Exception as e:
            logger.error(f"Gemini 클라이언트 초기화 실패: {e}")
            self._available = False
    
    async def generate_content(self, prompt: str) -> str:
        """
        프롬프트를 받아 AI 응답을 생성합니다.
        
        Args:
            prompt (str): AI에게 전달할 프롬프트
            
        Returns:
            str: AI 응답 텍스트
        """
        try:
            if not self.is_available():
                raise Exception("Gemini 서비스를 사용할 수 없습니다.")
            
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("AI 응답이 비어있습니다.")
            
            logger.info(f"Gemini 응답 생성 완료: {len(response.text)} 문자")
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini 응답 생성 실패: {e}")
            raise
    
    async def generate_structured_content(self, prompt: str, expected_format: str = "json") -> Dict[str, Any]:
        """
        구조화된 응답을 생성합니다.
        
        Args:
            prompt (str): AI에게 전달할 프롬프트
            expected_format (str): 기대하는 응답 형식 (현재는 json만 지원)
            
        Returns:
            Dict[str, Any]: 구조화된 응답 데이터
        """
        try:
            response_text = await self.generate_content(prompt)
            return self._extract_json_from_response(response_text)
            
        except Exception as e:
            logger.error(f"구조화된 응답 생성 실패: {e}")
            raise
    
    def is_available(self) -> bool:
        """
        Gemini 서비스 사용 가능 여부를 확인합니다.
        
        Returns:
            bool: 사용 가능 여부
        """
        return self._available and bool(settings.GEMINI_API_KEY)
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        AI 응답에서 JSON을 추출하고 파싱합니다.
        
        Args:
            response_text (str): AI 응답 텍스트
            
        Returns:
            Dict[str, Any]: 파싱된 JSON 데이터
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        try:
            # JSON 패턴 매칭
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, response_text, re.DOTALL)
            
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
                    
        except Exception:
            pass
        
        try:
            # 코드 블록에서 JSON 추출
            json_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            match = re.search(json_block_pattern, response_text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
        except Exception:
            pass
        
        logger.warning(f"JSON 추출 실패. 원본 응답: {response_text[:200]}...")
        raise ValueError("AI 응답에서 유효한 JSON을 추출할 수 없습니다.") 