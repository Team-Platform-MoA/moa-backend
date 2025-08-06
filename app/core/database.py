from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.models import Conversation, User
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    
db = Database()

async def connect_to_mongo():
    """MongoDB 연결"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        database = db.client[settings.MONGODB_DATABASE]
        
        await init_beanie(
            database=database,
            document_models=[Conversation, User]
        )
        
        logger.info("✅ MongoDB 연결 성공")
        
    except Exception as e:
        logger.error(f"❌ MongoDB 연결 실패: {e}")

async def close_mongo_connection():
    """MongoDB 연결 종료"""
    if db.client:
        db.client.close()
        logger.info("🔌 MongoDB 연결 종료")

def get_database():
    """데이터베이스 인스턴스 반환"""
    return db.client[settings.MONGODB_DATABASE]
