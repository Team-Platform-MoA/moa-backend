import os
import uuid
import logging
from typing import Optional
from google.cloud import storage
from fastapi import UploadFile
import tempfile

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
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                content = await audio_file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            blob = self.bucket.blob(unique_filename)
            blob.upload_from_filename(temp_file_path)
            
            os.unlink(temp_file_path)

            gcs_uri = f"gs://{self.bucket_name}/{unique_filename}"
            logger.info(f"✅ 오디오 파일 업로드 완료: {gcs_uri}")
            
            return gcs_uri
            
        except Exception as e:
            logger.error(f"❌ 오디오 파일 업로드 실패: {e}")
            if 'temp_file_path' in locals():
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
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
