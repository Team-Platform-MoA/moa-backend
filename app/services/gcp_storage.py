import uuid
import logging
import asyncio
from google.cloud import storage
from fastapi import UploadFile

from app.core.config import settings

logger = logging.getLogger(__name__)


class GCPStorageService:
    """GCP Cloud Storage 관리 서비스"""
    
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = settings.GCP_BUCKET_NAME
        self.bucket = self.client.bucket(self.bucket_name)
    
    async def upload_audio_file(self, audio_file: UploadFile, user_id: str) -> str:
        """
        오디오 파일을 GCP Storage에 업로드
        
        Args:
            audio_file: 업로드할 오디오 파일
            user_id: 사용자 ID
            
        Returns:
            str: 업로드된 파일의 GCS URI
        """
        try:
            file_extension = audio_file.filename.split('.')[-1] if '.' in audio_file.filename else 'wav'
            unique_filename = f"audio/{user_id}/{uuid.uuid4()}.{file_extension}"
            
            # 파일 전체를 메모리에 올리지 않고 스트리밍 업로드
            audio_file.file.seek(0)
            blob = self.bucket.blob(unique_filename)
            await asyncio.to_thread(
                blob.upload_from_file,
                audio_file.file,
                content_type=audio_file.content_type,
            )

            gcs_uri = f"gs://{self.bucket_name}/{unique_filename}"
            logger.info(f"✅ 오디오 파일 업로드 완료: {gcs_uri}")
            
            return gcs_uri
            
        except Exception as e:
            logger.error(f"❌ 오디오 파일 업로드 실패: {e}")
            raise e
    
    def get_public_url(self, gcs_uri: str) -> str:
        """GCS URI를 공개 URL로 변환"""
        blob_name = gcs_uri.replace(f"gs://{self.bucket_name}/", "")
        blob = self.bucket.blob(blob_name)
        return blob.public_url


gcp_storage_service = GCPStorageService()

def get_gcp_storage_service() -> GCPStorageService:
    """GCP Storage 서비스 인스턴스 반환"""
    return gcp_storage_service
