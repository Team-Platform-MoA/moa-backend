"""공통 유틸리티 함수들"""

from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo
from app.core.constants import KOREA_TIMEZONE, FileFormats

def get_korea_now() -> datetime:
    """한국 시간 기준 현재 시간 반환"""
    return datetime.now(ZoneInfo(KOREA_TIMEZONE))

def get_korea_today() -> str:
    """한국 시간 기준 오늘 날짜 반환 (YYYY-MM-DD 형식)"""
    return get_korea_now().strftime(FileFormats.DATE_FORMAT)


def format_date_for_display(date: datetime) -> str:
    """
    날짜를 한국어 표시 형식으로 변환합니다.
    크로스 플랫폼 호환성을 위해 strftime의 플랫폼별 차이를 해결합니다.
    """
    if not date:
        return ""

    # 월과 일에서 앞의 0을 제거
    month = str(date.month).lstrip('0') or '1'
    day = str(date.day).lstrip('0') or '1'

    return f"{month}월 {day}일"


def format_date_for_database(date: datetime) -> str:
    """
    날짜를 데이터베이스 저장용 문자열 형식으로 변환합니다.
    """
    if not date:
        return ""

    return date.strftime("%Y-%m-%d")

def format_message(template: str, **kwargs) -> str:
    """메시지 템플릿 포맷팅"""
    return template.format(**kwargs)

def create_success_response(
    conversation_id: str,
    question_number: int,
    question_text: str,
    message: str,
    user_id: str,
    **additional_fields
) -> Dict[str, Any]:
    """공통 성공 응답 생성"""
    response = {
        "success": True,
        "conversation_id": conversation_id,
        "question_number": question_number,
        "question_text": question_text,
        "message": message,
        "user_id": user_id
    }
    response.update(additional_fields)
    return response

def create_error_response(
    error: str,
    question_number: int = None,
    user_id: str = None,
    **additional_fields
) -> Dict[str, Any]:
    """공통 에러 응답 생성"""
    response = {
        "success": False,
        "error": error
    }
    if question_number is not None:
        response["question_number"] = question_number
    if user_id is not None:
        response["user_id"] = user_id
    response.update(additional_fields)
    return response

def parse_gcs_uri(gcs_uri: str) -> tuple[str, str]:
    """GCS URI를 bucket과 blob으로 파싱"""
    if not gcs_uri.startswith("gs://"):
        raise ValueError(f"잘못된 GCS URI 형식: {gcs_uri}")
    
    uri_body = gcs_uri[5:]
    bucket_name, blob_name = uri_body.split("/", 1)
    return bucket_name, blob_name

def truncate_text(text: str, max_length: int) -> str:
    """텍스트를 지정된 길이로 자르기"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def safe_get_error_message(error: Exception) -> str:
    """안전한 에러 메시지 추출"""
    return str(error) if str(error) else f"{type(error).__name__}: {repr(error)}"
