from typing import List, Dict
from fastapi import HTTPException

from app.models.models import Conversation

class UserService:
    """사용자 관련 서비스"""
    
    async def get_user_history(self, user_id: str, limit: int = 10) -> Dict:
        """
        사용자의 대화 기록 조회
        
        Args:
            user_id (str): 사용자 ID
            limit (int): 조회할 최대 개수
            
        Returns:
            Dict: 사용자 기록
        """
        try:
            conversations = await Conversation.find(
                Conversation.user_id == user_id
            ).sort(-Conversation.user_timestamp).limit(limit).to_list()
            
            return {
                "user_id": user_id,
                "total_count": len(conversations),
                "conversations": [
                    {
                        "id": str(conv.id),
                        "user_message": conv.user_message,
                        "user_timestamp": conv.user_timestamp,
                        "ai_sentiment": conv.ai_sentiment,
                        "ai_score": conv.ai_score,
                        "ai_comfort_message": conv.ai_comfort_message,
                        "ai_timestamp": conv.ai_timestamp
                    }
                    for conv in conversations
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"기록 조회 중 오류가 발생했습니다: {str(e)}")

user_service = UserService()

def get_user_service() -> UserService:
    """사용자 서비스 인스턴스 반환"""
    return user_service
