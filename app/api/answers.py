from fastapi import APIRouter, Depends, Header, UploadFile, File, Form, HTTPException

from app.schemas.responses import AudioAnswerResponse
from app.services.answer import get_answer_service, AnswerService
from app.services.question import get_question_service, QuestionService
from app.core.constants import ALLOWED_AUDIO_TYPES, MAX_AUDIO_FILE_SIZE, ErrorMessages
from app.utils.common import format_message

router = APIRouter(prefix="/answers", tags=["answers"])

@router.get("/questions")
async def get_questions(
     x_user_id: str = Header(..., alias="X-User-Id"),
    question_service: QuestionService = Depends(get_question_service)
):
    """전체 질문 목록 조회"""
    user = None
    if x_user_id:
        from app.models.models import User
        user = await User.find_one(User.user_id == x_user_id)
        
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=format_message(ErrorMessages.USER_NOT_FOUND)
            )
    
    personalized_questions = {}
    for question_number in range(1, question_service.get_total_questions() + 1):
        personalized_questions[question_number] = question_service.get_question_text(question_number, user)
    
    return {
        "total_questions": question_service.get_total_questions(),
        "questions": personalized_questions
    }

@router.get("/questions/{question_number}")
async def get_question(
    question_number: int,
   x_user_id: str = Header(..., alias="X-User-Id"),
    question_service: QuestionService = Depends(get_question_service)
):
    """특정 질문 조회"""
    if not question_service.is_valid_question_number(question_number):
        raise HTTPException(
            status_code=404,
            detail=format_message(ErrorMessages.QUESTION_NOT_FOUND, question_number=question_number)
        )
    
    user = None
    if x_user_id:
        from app.models.models import User
        user = await User.find_one(User.user_id == x_user_id)
        
        if user is None:
            raise HTTPException(
                status_code=404,
               detail=format_message(ErrorMessages.USER_NOT_FOUND)
            )
    
    return {
        "question_number": question_number,
        "question_text": question_service.get_question_text(question_number, user)
    }

@router.post("/audio", response_model=AudioAnswerResponse)
async def upload_audio_answer(
    audio_file: UploadFile = File(..., description="오디오 파일 (wav, mp3, m4a, webm, ogg 등)"),
    question_number: int = Form(..., description="질문 번호 (1-3)"),
    x_user_id: str = Header(..., alias="X-User-Id"),
    answer_service: AnswerService = Depends(get_answer_service)
):
    """오디오 파일로 답변 제출 (한국 시간 기준)"""
    try:
        _validate_audio_file(audio_file)
        
        result = await answer_service.process_audio_answer(
            audio_file=audio_file,
            question_number=question_number,
            user_id=x_user_id
        )
        
        return AudioAnswerResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=format_message(ErrorMessages.AUDIO_ANSWER_PROCESSING_ERROR, error=str(e))
        )

def _validate_audio_file(audio_file: UploadFile):
    """오디오 파일 유효성 검사"""
    if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=format_message(
                ErrorMessages.UNSUPPORTED_AUDIO_FORMAT, 
                formats=', '.join(ALLOWED_AUDIO_TYPES)
            )
        )
    
    audio_file.file.seek(0, 2)
    file_size = audio_file.file.tell()
    audio_file.file.seek(0)
    
    if file_size > MAX_AUDIO_FILE_SIZE:
        max_size_mb = MAX_AUDIO_FILE_SIZE // (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=format_message(ErrorMessages.FILE_SIZE_EXCEEDED, max_size=max_size_mb)
        )