import json
import re
import uuid
from datetime import datetime
from typing import Dict

import google.generativeai as genai

from app.core.config import settings
from app.models.models import Conversation, User
from app.utils.prompts import get_emotion_analysis_prompt

import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

class AnalysisService:
    """감정 분석 서비스"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-pro")
    
    def _extract_json_from_response(self, response_text: str) -> Dict:
        """
        AI 응답에서 JSON을 추출하고 파싱합니다.
        
        Args:
            response_text (str): AI 응답 텍스트
            
        Returns:
            Dict: 파싱된 JSON 데이터
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        try:
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
            json_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            match = re.search(json_block_pattern, response_text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
        except Exception:
            pass
        
        logger.info(f"AI 응답 원문: {response_text}")
        return {
            "sentiment": "neutral",
            "score": 0.0,
            "comfort_message": "죄송합니다. 현재 분석이 어려운 상황입니다. 잠시 후 다시 시도해 주세요."
        }
    
    async def analyze_text(self, text: str, user_id: str = None) -> Dict:
        """
        텍스트 감정 분석 및 데이터베이스 저장
        
        Args:
            text (str): 분석할 텍스트
            user_id (str, optional): 사용자 ID
            
        Returns:
            Dict: 분석 결과
        """
        try:
            prompt = get_emotion_analysis_prompt(text)
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("AI 응답이 비어있습니다.")
            
            logger.info(f"AI 원본 응답: {response.text[:200]}...") 
            
            result_data = self._extract_json_from_response(response.text)
            
            required_fields = ["sentiment", "score", "comfort_message"]
            for field in required_fields:
                if field not in result_data:
                    logger.info(f"누락된 필드: {field}")
                    result_data[field] = self._get_default_value(field)
            
            if not user_id:
                user_id = str(uuid.uuid4())
            
            analysis_result = await self._save_analysis_data(text, user_id, result_data)
            
            return {
                "sentiment": result_data["sentiment"],
                "score": float(result_data["score"]),
                "comfort_message": result_data["comfort_message"],
                "message_id": str(analysis_result.id) if analysis_result else None,
                "user_id": user_id
            }
            
        except Exception as e:
            logger.error(f"분석 오류: {e}")
            if not user_id:
                user_id = str(uuid.uuid4())
            
            default_result = {
                "sentiment": "neutral",
                "score": 0.0,
                "comfort_message": "현재 시스템이 불안정합니다. 잠시 후 다시 시도해 주세요.",
                "message_id": None,
                "user_id": user_id
            }
            
            try:
                analysis_result = await self._save_analysis_data(text, user_id, default_result)
                default_result["message_id"] = str(analysis_result.id) if analysis_result else None
            except:
                pass
                
            return default_result
    
    def _get_default_value(self, field: str):
        """필드별 기본값 반환"""
        defaults = {
            "sentiment": "neutral",
            "score": 0.0,
            "comfort_message": "분석 중 오류가 발생했습니다. 다시 시도해 주세요."
        }
        return defaults.get(field, "")
    
    async def _save_analysis_data(self, text: str, user_id: str, result_data: Dict):
        """분석 데이터를 새로운 통합 모델로 저장"""
        try:
            conversation = Conversation(
                user_id=user_id,
                user_message=text,
                ai_sentiment=result_data.get("sentiment", "neutral"),
                ai_score=float(result_data.get("score", 0.0)),
                ai_comfort_message=result_data.get("comfort_message", "분석 중 오류가 발생했습니다.")
            )
            await conversation.save()
            
            user = await User.find_one(User.id == user_id)
            if not user:
                user = User(user_id=user_id, total_conversations=1)
            else:
                user.total_conversations += 1
            user.last_active = datetime.now()
            await user.save()
            
            return conversation
            
        except Exception as e:
            logger.error(f"데이터 저장 오류: {e}")
            return None

analysis_service = AnalysisService()

def get_analysis_service() -> AnalysisService:
    """분석 서비스 인스턴스 반환"""
    return analysis_service
