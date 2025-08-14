import uuid
from datetime import datetime
from typing import Dict

from app.external.ai.client import get_ai_client
from app.prompts.report import EmotionReportPrompt

import logging

logger = logging.getLogger(__name__)


class ReportService:
    """감정 리포트 생성 서비스"""
    
    def __init__(self):
        self.ai_client = get_ai_client()
        self.report_prompt = EmotionReportPrompt()
    
    async def generate_emotion_report(self, user_answers: Dict, user_id: str = None) -> Dict:
        """
        감정 리포트를 생성합니다.
        
        Args:
            user_answers (dict): {
                "memorable_moment": "오늘 부양하면서 가장 기억에 남는 순간",
                "current_emotion": "지금 이 순간 가장 큰 감정",
                "message_to_self": "나 자신에게 해주고 싶은 말"
            }
            user_id (str, optional): 사용자 ID
            
        Returns:
            Dict: 리포트 생성 결과
        """
        try:
            if not user_id:
                user_id = str(uuid.uuid4())
            
            # 프롬프트 생성
            prompt = self.report_prompt.generate(user_answers=user_answers)
            
            # AI 응답 생성
            result_data = await self.ai_client.generate_structured_content(prompt)
            
            return {
                "user_id": user_id,
                "report_data": result_data,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"리포트 생성 오류: {e}")
            
            if not user_id:
                user_id = str(uuid.uuid4())
            
            return {
                "user_id": user_id,
                "error": "리포트 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
                "generated_at": datetime.now().isoformat()
            }


# 의존성 주입을 위한 함수
def get_report_service() -> ReportService:
    """ReportService 인스턴스를 반환합니다."""
    return ReportService()