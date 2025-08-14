import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """애플리케이션 설정"""
    
    PROJECT_NAME: str = "MoA Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "치매 부양자를 위한 감정 분석 및 위로 메시지 제공 서비스"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "database")
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    GCP_BUCKET_NAME: str = os.getenv("GCP_BUCKET_NAME", "moa-audio-storage")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    class Config:
        case_sensitive = True

settings = Settings()

def get_settings() -> Settings:
    """설정 인스턴스 반환"""
    return settings
