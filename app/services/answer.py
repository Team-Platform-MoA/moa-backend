from typing import Dict, List, Tuple
from fastapi import UploadFile, HTTPException
import logging

from app.models.models import Conversation, User
from app.schemas.reports import ConversationReport
from app.services.gcp_storage import get_gcp_storage_service
from app.services.speech_to_text import get_speech_to_text_service
from app.services.question import get_question_service
from app.services.report import get_report_service
from app.utils.common import (
    get_korea_now, format_message,
    create_success_response, create_error_response, safe_get_error_message, get_korea_today_date
)
from app.core.constants import (
    FINAL_QUESTION_NUMBER, Messages, ErrorMessages, 
    Defaults, DEFAULT_AI_SENTIMENT, DEFAULT_AI_SCORE
)

logger = logging.getLogger(__name__)


class AnswerService:
    """답변 처리 서비스"""
    
    def __init__(self):
        self.gcp_storage_service = get_gcp_storage_service()
        self.speech_to_text_service = get_speech_to_text_service()
        self.question_service = get_question_service()
        self.report_service = get_report_service()
    
    async def process_audio_answer(
        self, 
        audio_file: UploadFile, 
        question_number: int, 
        user_id: str
    ) -> Dict:
        """오디오 파일을 처리하여 답변을 저장"""
        try:
            if not self.question_service.is_valid_question_number(question_number):
                raise HTTPException(
                    status_code=400,
                    detail=format_message(
                        ErrorMessages.INVALID_QUESTION_NUMBER,
                        max_questions=self.question_service.get_total_questions()
                    )
                )
            
            user = await self._ensure_user_exists(user_id)
            question_text = self.question_service.get_question_text(question_number, user)
            gcs_uri = await self.gcp_storage_service.upload_audio_file(audio_file, user_id)
            conversation = await self._find_or_create_conversation(user_id)
            # 디버깅: 이미 확보한 인스턴스 확인
            logger.debug(f"최종 처리 대상 conversation 확인: id={conversation.id}, date={conversation.conversation_date}")

            await self._save_audio_uri(conversation, question_number, gcs_uri)
            
            if question_number == FINAL_QUESTION_NUMBER:
                await self._process_all_audio_to_text(conversation, user)
                report_response = None

                try:
                    report_response = await self.report_service.generate_emotion_report(
                        user_answers=conversation.user_message, 
                        user_id=conversation.user_id
                    )
                    await self._save_report(conversation, report_response)
                    logger.info(format_message(Messages.REPORT_GENERATION_SUCCESS, user_id=user_id))
                except Exception as report_error:
                    logger.error(format_message(ErrorMessages.REPORT_GENERATION_FAILED, error=report_error))
                    logger.exception(ErrorMessages.REPORT_GENERATION_EXCEPTION)

                report_obj = None
                if report_response and report_response.get("report_data"):
                    try:
                        report_obj = ConversationReport(**report_response.get("report_data"))
                    except Exception as e:
                        logger.error(f"리포트 객체 변환 실패: {e}")
                        report_obj = None

                return create_success_response(
                    conversation_id=str(conversation.id),
                    question_number=question_number,
                    question_text=question_text,
                    message=Messages.ALL_ANSWERS_COMPLETE,
                    user_id=user_id,
                    user_message=conversation.user_message,
                    audio_uri_1=conversation.audio_uri_1,
                    audio_uri_2=conversation.audio_uri_2,
                    audio_uri_3=conversation.audio_uri_3,
                    report=report_obj
                )
            else:
                return create_success_response(
                    conversation_id=str(conversation.id),
                    question_number=question_number,
                    question_text=question_text,
                    message=format_message(Messages.AUDIO_UPLOAD_SUCCESS, question_number=question_number),
                    user_id=user_id,
                    audio_uri_1=conversation.audio_uri_1,
                    audio_uri_2=conversation.audio_uri_2,
                    audio_uri_3=conversation.audio_uri_3
                )
            
        except HTTPException:
            raise
        except Exception as e:
            error_msg = safe_get_error_message(e)
            logger.error(format_message(Messages.AUDIO_PROCESSING_FAILED, error=error_msg))
            logger.exception(ErrorMessages.AUDIO_PROCESSING_EXCEPTION)  # 스택 트레이스도 로깅
            return create_error_response(
                error=error_msg,
                question_number=question_number,
                user_id=user_id
            )

    async def _save_report(self, conversation: Conversation, report_response: Dict):
        """리포트 저장"""
        try:
            if report_response and report_response.get("report_data"):
                report_data = report_response.get("report_data")

                if report_response and report_response.get("report_data"):
                    report_data = report_response.get("report_data")

                if not isinstance(report_data.get("actions"), str) or not report_data["actions"].strip():
                    report_data["actions"] = (
                        "오늘 하루를 마무리하며 자신을 돌보는 시간을 가져보세요. "
                        "10분 정도 깊게 호흡하고 따뜻한 차 한 잔을 마시며 "
                        "스스로에게 '오늘도 정말 수고했어'라고 말해보세요."
                    )

                if not isinstance(report_data.get("letter"), str) or not report_data["letter"].strip():
                    report_data["letter"] = (
                        "오늘도 최선을 다한 당신, 정말 수고하셨어요. "
                        "스스로를 조금 더 따뜻하게 돌보는 시간을 가져보길 바라요."
                    )

                report_obj = ConversationReport(**report_data)
                conversation.report = report_obj
                await conversation.save()
                logger.info("리포트 저장 완료")

        except Exception as e:
            logger.error(f"리포트 저장 실패: {e}")
            raise e
    
    async def _ensure_user_exists(self, user_id: str) -> User:
        """사용자가 존재하는지 확인하고, 없으면 오류 발생"""
        user = await User.find_one(User.user_id == user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=ErrorMessages.USER_NOT_FOUND
            )
        return user
    
    async def _find_or_create_conversation(self, user_id: str) -> Conversation:
        """사용자의 오늘 날짜 Conversation 찾기 또는 새로 생성"""
        today = get_korea_today_date()
        
        conversation = await Conversation.find_one(
            Conversation.user_id == user_id,
            Conversation.conversation_date == today
        )
        
        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                conversation_date=today,
                user_message=Defaults.USER_MESSAGE_EMPTY,
                ai_sentiment=DEFAULT_AI_SENTIMENT,
                ai_score=DEFAULT_AI_SCORE,
                ai_comfort_message=Messages.DEFAULT_COMFORT_MESSAGE
            )
            await conversation.save()
            logger.info(format_message(Messages.CONVERSATION_CREATED, user_id=user_id, date=today))
        return conversation
    
    async def _save_audio_uri(self, conversation: Conversation, question_number: int, audio_uri: str):
        """오디오 URI 저장"""
        try:
            audio_field = f"audio_uri_{question_number}"
            setattr(conversation, audio_field, audio_uri)
            await conversation.save()
            logger.info(format_message(
                Messages.AUDIO_URI_SAVE_SUCCESS, 
                question_number=question_number, 
                audio_uri=audio_uri
            ))
        except Exception as e:
            logger.error(format_message(Messages.AUDIO_URI_SAVE_FAILED, error=e))
            raise e
    
    async def _process_all_audio_to_text(self, conversation: Conversation, user: User):
        """모든 오디오 파일을 STT 처리하여 통합된 텍스트로 변환"""
        try:
            logger.info(Messages.STT_START)
            
            audio_uris = self._collect_audio_uris(conversation)
            
            if not audio_uris:
                logger.warning(Messages.STT_NO_FILES)
                return
            
            logger.info(format_message(Messages.STT_PROCESSING, count=len(audio_uris)))
            
            message_parts = []
            
            for question_num, audio_uri in audio_uris:
                try:
                    question_text = self.question_service.get_question_text(question_num, user)
                    transcribed_text = self.speech_to_text_service.transcribe_audio(audio_uri)
                    
                    if question_text and transcribed_text:
                        message_parts.extend([
                            f"Q{question_num}: {question_text}",
                            f"A{question_num}: {transcribed_text}"
                        ])
                    
                    logger.info(format_message(
                        Messages.STT_QUESTION_SUCCESS,
                        question_num=question_num,
                        text=transcribed_text[:Defaults.TEXT_PREVIEW_LENGTH]
                    ))
                    
                except Exception as e:
                    logger.error(format_message(Messages.STT_QUESTION_FAILED, question_num=question_num, error=e))
                    question_text = self.question_service.get_question_text(question_num, user)
                    if question_text:
                        message_parts.extend([
                            f"Q{question_num}: {question_text}",
                            f"A{question_num}: {format_message(ErrorMessages.STT_CONVERSION_FAILED_ANSWER, error=str(e))}"
                        ])
            
            conversation.user_message = '\n'.join(message_parts)
            
            await self._update_user_last_active(conversation.user_id)
            await conversation.save()
            logger.info(Messages.STT_COMPLETE)
            
        except Exception as e:
            logger.error(format_message(Messages.STT_FAILED, error=e))
            raise e
    
    def _collect_audio_uris(self, conversation: Conversation) -> List[Tuple[int, str]]:
        """Conversation에서 오디오 URI들을 수집"""
        audio_uris = []
        for i in range(1, FINAL_QUESTION_NUMBER + 1):
            audio_uri = getattr(conversation, f"audio_uri_{i}")
            if audio_uri:
                audio_uris.append((i, audio_uri))
        return audio_uris
    
    async def _update_user_last_active(self, user_id: str) -> None:
        """사용자 마지막 활동 시간 업데이트"""
        try:
            user = await User.find_one(User.user_id == user_id)
            if user:
                user.last_active = get_korea_now()
                await user.save()
                logger.debug(format_message(Messages.USER_LAST_ACTIVE_DEBUG, user_id=user_id))
        except Exception as e:
            logger.error(format_message(ErrorMessages.USER_LAST_ACTIVE_UPDATE_FAILED, error=e))


answer_service = AnswerService()

def get_answer_service() -> AnswerService:
    """Answer 서비스 인스턴스 반환"""
    return answer_service
