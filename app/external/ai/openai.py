"""
OpenAI GPT 클라이언트 구현
"""
import json
import re
import logging
import asyncio
from typing import Dict, Any

from openai import OpenAI

from app.core.config import settings
from app.external.ai.base import AIClient

logger = logging.getLogger(__name__)


class OpenAIClient(AIClient):
    """OpenAI GPT 클라이언트"""
    
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        try:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self._available = True
        except Exception as e:
            logger.error(f"OpenAI 클라이언트 초기화 실패: {e}")
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
                raise Exception("OpenAI 서비스를 사용할 수 없습니다.")
            
            loop = asyncio.get_running_loop()
            
            # 동기 호출을 executor로 비동기화
            response = await loop.run_in_executor(None, self._sync_generate_content, prompt)
            
            if not response or not response.choices:
                raise Exception("AI 응답이 비어있습니다.")
            
            response_text = response.choices[0].message.content
            logger.info(f"OpenAI 응답 생성 완료: {len(response_text)} 문자")
            return response_text
            
        except Exception as e:
            logger.error(f"OpenAI 응답 생성 실패: {e}")
            raise
    
    def _sync_generate_content(self, prompt: str):
        """동기적으로 OpenAI API를 호출합니다."""
        print("🔵 OpenAI generate_content 시작")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in JSON format when requested. Always return complete, valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        print("🟢 OpenAI 응답 수신 완료")
        return response
    
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
        OpenAI 서비스 사용 가능 여부를 확인합니다.
        
        Returns:
            bool: 사용 가능 여부
        """
        return self._available and bool(settings.OPENAI_API_KEY)
    
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