
from openai import OpenAI
import tempfile
import os
import hashlib
import logging
from google.cloud import storage
from app.core.config import settings
from app.core.constants import STT_MODEL, STT_LANGUAGE, STT_TEMPERATURE, ErrorMessages
from app.utils.common import parse_gcs_uri, format_message

logger = logging.getLogger(__name__)


class SpeechToTextService:
    """OpenAI STT를 사용한 음성-텍스트 변환 서비스"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.storage_client = storage.Client()
        self.bucket_name = settings.GCP_BUCKET_NAME

    def transcribe_audio(self, gcs_uri: str) -> str:
        """GCS에 저장된 오디오 파일을 텍스트로 변환"""
        try:
            logger.info(f"🎤 음성 변환 시작: {gcs_uri}")

            bucket_name, blob_name = parse_gcs_uri(gcs_uri)
            
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            temp_file_path = self._create_temp_file(blob_name)
            blob.download_to_filename(temp_file_path)
            
            self._log_file_info(temp_file_path, gcs_uri)

            try:
                transcribed_text = self._transcribe_with_openai(temp_file_path)
            finally:
                self._cleanup_temp_file(temp_file_path)

            logger.info(f"✅ 음성 변환 완료: {transcribed_text}")
            return transcribed_text

        except Exception as e:
            error_message = self._handle_transcription_error(str(e))
            logger.error(f"❌ 음성 변환 실패: {error_message}")
            raise Exception(error_message)

    def _create_temp_file(self, blob_name: str) -> str:
        """임시 파일 생성"""
        _, ext = os.path.splitext(blob_name)
        if not ext:
            ext = ".bin"
        
        fd, temp_file_path = tempfile.mkstemp(suffix=ext, dir="/tmp")
        os.close(fd)
        return temp_file_path

    def _log_file_info(self, temp_file_path: str, gcs_uri: str):
        """파일 정보 로깅"""
        file_size = os.path.getsize(temp_file_path)
        
        with open(temp_file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        logger.debug(f"📁 다운로드된 파일 정보:")
        logger.debug(f"   - 크기: {file_size} bytes")
        logger.debug(f"   - 해시: {file_hash}")
        logger.debug(f"   - GCS URI: {gcs_uri}")

    def _transcribe_with_openai(self, temp_file_path: str) -> str:
        """OpenAI로 음성 변환"""
        with open(temp_file_path, "rb") as audio_file:
            resp = self.client.audio.transcriptions.create(
                model=STT_MODEL,
                file=audio_file,
                language=STT_LANGUAGE,
                temperature=STT_TEMPERATURE
            )
        return resp.text

    def _cleanup_temp_file(self, temp_file_path: str):
        """임시 파일 정리"""
        try:
            os.remove(temp_file_path)
        except FileNotFoundError:
            pass

    def _handle_transcription_error(self, error_msg: str) -> str:
        """STT 에러 처리 및 사용자 친화적 메시지 반환"""
        lower_msg = error_msg.lower()
        
        if "not found" in lower_msg or "404" in lower_msg:
            return ErrorMessages.AUDIO_FILE_NOT_FOUND
        if "timeout" in lower_msg:
            return ErrorMessages.STT_TIMEOUT
        if "api key" in lower_msg or "unauthorized" in lower_msg or "invalid api key" in lower_msg:
            return ErrorMessages.INVALID_API_KEY
        if "no connection adapters were found" in lower_msg or "openai.audio" in lower_msg:
            return "OpenAI SDK 사용 방식이 오래되었거나 입력 URL 형식이 잘못되었습니다."
        
        return format_message(ErrorMessages.STT_CONVERSION_FAILED, error=error_msg)


speech_to_text_service = SpeechToTextService()

def get_speech_to_text_service() -> SpeechToTextService:
    return speech_to_text_service