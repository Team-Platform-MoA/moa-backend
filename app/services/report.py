import uuid
from datetime import datetime
from fastapi import HTTPException
from typing import Dict, Optional
import logging

from app.external.ai.client import get_ai_client
from app.models import Conversation
from app.models.models import ConversationSummary
from app.prompts.report import EmotionReportPrompt
from app.core.constants import ErrorMessages
from app.utils.common import format_message

logger = logging.getLogger(__name__)


class ReportService:
    """감정 리포트 생성 서비스"""
    
    def __init__(self):
        self.ai_client = get_ai_client()
        self.report_prompt = EmotionReportPrompt()
    
    async def generate_emotion_report(
        self, 
        user_answers: str, 
        user_id: Optional[str] = None
    ) -> Dict:
        """
        감정 리포트를 생성합니다.
        
        Args:
            user_answers: Q&A 형식의 사용자 답변 텍스트
                예: "Q1: 질문\nA1: 답변\nQ2: 질문\nA2: 답변..."
            user_id: 사용자 ID (선택사항)
            
        Returns:
            Dict: 리포트 생성 결과
                - user_id: 사용자 ID
                - report_data: 생성된 리포트 데이터 (성공시)
                - error: 오류 메시지 (실패시)
                - generated_at: 생성 시간 (ISO 형식)
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
            logger.error(format_message(ErrorMessages.REPORT_SERVICE_GENERATION_ERROR, error=e))
            logger.exception(ErrorMessages.REPORT_SERVICE_GENERATION_EXCEPTION)
            
            if not user_id:
                user_id = str(uuid.uuid4())
            
            return {
                "user_id": user_id,
                "error": ErrorMessages.REPORT_SERVICE_FALLBACK_ERROR,
                "generated_at": datetime.now().isoformat()
            }

    async def get_user_reports(
            self,
            user_id: str,
            year: int,
            month: int
    ) -> dict:
        try:
            start = datetime(year, month, 1)
            if month == 12:
                end = datetime(year + 1, 1, 1)
            else:
                end = datetime(year, month + 1, 1)

            query = {
                "user_id": user_id,
                "user_timestamp": {"$gte": start, "$lt": end}
            }

            rows: list[ConversationSummary] = (
                await Conversation.find(query)
                .sort(-Conversation.conversation_date)
                .project(ConversationSummary)
                .to_list()
            )

            summaries = [
                {
                    "report_id": str(r.id),
                    "report_date": r.conversation_date.strftime("%-m월 %-d일")
                    if r.conversation_date else ""
                }
                for r in rows
            ]

            return {
                "total_count": len(rows),
                "reports": summaries,
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=format_message(ErrorMessages.HISTORY_QUERY_ERROR, error=str(e)),
            )


# 의존성 주입을 위한 함수
def get_report_service() -> ReportService:
    """ReportService 인스턴스를 반환합니다."""
    return ReportService()