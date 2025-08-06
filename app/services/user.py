from typing import Dict
from fastapi import HTTPException
from datetime import datetime
import uuid

from app.models.models import Conversation, User
from app.schemas.requests import OnboardingRequest

class UserService:
    """사용자 관련 서비스"""
    
    async def create_user_onboarding(self, onboarding_data: OnboardingRequest) -> Dict:
        """
        사용자 온보딩 정보 저장
        
        Args:
            onboarding_data (OnboardingRequest): 온보딩 데이터
            
        Returns:
            Dict: 생성된 사용자 정보
        """
        try:
            # 새로운 사용자 ID 생성
            user_id = str(uuid.uuid4())
            
            # 사용자 정보 생성
            user = User(
                user_id=user_id,
                name=onboarding_data.name,
                age=onboarding_data.age,
                caregiver_type=onboarding_data.caregiver_type,  # Enum 직접 저장
                caregiver_age=onboarding_data.caregiver_age,
                is_onboarded=True,
                created_at=datetime.now(),
                last_active=datetime.now()
            )
            
            await user.insert()
            
            return {
                "user_id": user_id,
                "name": user.name,
                "age": user.age,
                "caregiver_type": user.caregiver_type.value if user.caregiver_type else None,  # API 응답용으로 문자열 변환
                "caregiver_age": user.caregiver_age,
                "is_onboarded": user.is_onboarded,
                "message": "온보딩이 성공적으로 완료되었습니다."
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"온보딩 처리 중 오류가 발생했습니다: {str(e)}")

    async def get_user_onboarding_status(self, user_id: str) -> Dict:
        """
        사용자 온보딩 상태 조회

        Args:
            user_id (str): 사용자 ID

        Returns:
            Dict: 사용자 온보딩 정보
        """
        try:
            user = await User.find_one(User.user_id == user_id)

            if not user:
                raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

            return {
                "user_id": user.user_id,
                "name": user.name,
                "age": user.age,
                "caregiver_type": user.caregiver_type.value if user.caregiver_type else None,  # API 응답용으로 문자열 변환
                "caregiver_age": user.caregiver_age,
                "is_onboarded": user.is_onboarded,
                "message": "온보딩 완료" if user.is_onboarded else "온보딩 미완료"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"온보딩 상태 조회 중 오류가 발생했습니다: {str(e)}")
    
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
