from typing import Dict
from fastapi import UploadFile, HTTPException
import logging

from app.models.models import Conversation, User
from app.services.gcp_storage import get_gcp_storage_service
from app.services.speech_to_text import get_speech_to_text_service
from app.services.question import get_question_service
from app.utils.common import (
    get_korea_now, get_korea_today, format_message, 
    create_success_response, create_error_response
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
            
            question_text = self.question_service.get_question_text(question_number)
            await self._ensure_user_exists(user_id)
            
            gcs_uri = await self.gcp_storage_service.upload_audio_file(audio_file, user_id)
            conversation = await self._find_or_create_conversation(user_id)
            await self._save_audio_uri(conversation, question_number, gcs_uri)
            
            if question_number == FINAL_QUESTION_NUMBER:
                await self._process_all_audio_to_text(conversation)
                
                conversation = await Conversation.find_one(
                    Conversation.user_id == user_id,
                    Conversation.conversation_date == get_korea_today()
                )
                
                return create_success_response(
                    conversation_id=str(conversation.id),
                    question_number=question_number,
                    question_text=question_text,
                    message=Messages.ALL_ANSWERS_COMPLETE,
                    user_id=user_id,
                    user_message=conversation.user_message,
                    audio_uri_1=conversation.audio_uri_1,
                    audio_uri_2=conversation.audio_uri_2,
                    audio_uri_3=conversation.audio_uri_3
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
            logger.error(format_message(Messages.AUDIO_PROCESSING_FAILED, error=e))
            return create_error_response(
                error=str(e),
                question_number=question_number,
                user_id=user_id
            )
    
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
        today = get_korea_today()
        
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
    
    async def _process_all_audio_to_text(self, conversation: Conversation):
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
                    question_text = self.question_service.get_question_text(question_num)
                    transcribed_text = await self.speech_to_text_service.transcribe_audio(audio_uri)
                    
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
                    question_text = self.question_service.get_question_text(question_num)
                    if question_text:
                        message_parts.extend([
                            f"Q{question_num}: {question_text}",
                            f"A{question_num}: 음성 변환 실패: {str(e)}"
                        ])
            
            conversation.user_message = '\n'.join(message_parts)
            
            await self._update_user_last_active(conversation.user_id)
            await conversation.save()
            logger.info(Messages.STT_COMPLETE)
            
        except Exception as e:
            logger.error(format_message(Messages.STT_FAILED, error=e))
            raise e
    
    def _collect_audio_uris(self, conversation: Conversation) -> list[tuple[int, str]]:
        """Conversation에서 오디오 URI들을 수집"""
        audio_uris = []
        for i in range(1, 4):
            audio_uri = getattr(conversation, f"audio_uri_{i}")
            if audio_uri:
                audio_uris.append((i, audio_uri))
        return audio_uris
    
    async def _update_user_last_active(self, user_id: str):
        """사용자 마지막 활동 시간 업데이트"""
        user = await User.find_one(User.user_id == user_id)
        if user:
            user.last_active = get_korea_now()
            await user.save()


answer_service = AnswerService()

def get_answer_service() -> AnswerService:
    """Answer 서비스 인스턴스 반환"""
    return answer_service
