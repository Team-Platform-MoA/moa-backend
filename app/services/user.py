import uuid
from datetime import datetime
from typing import Dict, Optional
from fastapi import HTTPException
from app.models.models import User, Conversation
from app.schemas.requests import CompleteOnboardingRequest
from app.schemas.common import Gender, DementiaStage, FamilyRelationship

class UserService:
    """사용자 관련 서비스"""

    def _safe_enum_value(self, enum_value, field_name: str) -> str:
        """
        Enum 값을 안전하게 추출하는 헬퍼 함수
        
        Args:
            enum_value: Enum 인스턴스
            field_name: 필드명 (에러 메시지용)
            
        Returns:
            str: Enum 값
            
        Raises:
            HTTPException: Enum이 None이거나 잘못된 경우
        """
        if enum_value is None:
            raise HTTPException(
                status_code=400, 
                detail=f"데이터 검증 실패: {field_name}이(가) 설정되지 않았습니다."
            )
        
        try:
            return enum_value.value
        except AttributeError:
            raise HTTPException(
                status_code=400, 
                detail=f"데이터 검증 실패: {field_name}이(가) 올바른 Enum 타입이 아닙니다."
            )

    async def create_complete_onboarding(self, onboarding_data: CompleteOnboardingRequest) -> Dict:
        """
        완전한 온보딩 정보 저장 (사용자 + 가족 정보)

        Args:
            onboarding_data (CompleteOnboardingRequest): 온보딩 데이터

        Returns:
            Dict: 온보딩 완료 정보
        """
        try:
            # 새로운 사용자 ID 생성
            user_id = str(uuid.uuid4())
            
            # 사용자 정보 생성 (부양자 + 가족 정보 포함)
            user = User(
                user_id=user_id,
                name=onboarding_data.user_name,
                birth_year=onboarding_data.user_birth_year,
                gender=onboarding_data.user_gender,
                family_relationship=onboarding_data.family_relationship,
                daily_care_hours=onboarding_data.daily_care_hours,
                # 부양받는 가족 정보
                family_member_nickname=onboarding_data.family_member.nickname,
                family_member_birth_year=onboarding_data.family_member.birth_year,
                family_member_gender=onboarding_data.family_member.gender,
                family_member_dementia_stage=onboarding_data.family_member.dementia_stage,
                is_onboarded=True,
                created_at=datetime.now(),
                last_active=datetime.now()
            )
            
            # 데이터베이스에 저장
            await user.insert()
            
            return {
                "user_id": user_id,
                "user_name": user.name,
                "user_birth_year": user.birth_year,
                "user_gender": self._safe_enum_value(user.gender, "사용자 성별"),
                "family_relationship": self._safe_enum_value(user.family_relationship, "가족 관계"),
                "daily_care_hours": user.daily_care_hours,
                "family_member": {
                    "nickname": user.family_member_nickname,
                    "birth_year": user.family_member_birth_year,
                    "gender": self._safe_enum_value(user.family_member_gender, "가족 성별"),
                    "dementia_stage": self._safe_enum_value(user.family_member_dementia_stage, "치매 정도")
                },
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

            response = {
                "user_id": user.user_id,
                "user_name": user.name,
                "user_birth_year": user.birth_year,
                "user_gender": self._safe_enum_value(user.gender, "사용자 성별"),
                "family_relationship": self._safe_enum_value(user.family_relationship, "가족 관계"),
                "daily_care_hours": user.daily_care_hours,
                "family_member": {
                    "nickname": user.family_member_nickname,
                    "birth_year": user.family_member_birth_year,
                    "gender": self._safe_enum_value(user.family_member_gender, "가족 성별"),
                    "dementia_stage": self._safe_enum_value(user.family_member_dementia_stage, "치매 정도")
                },
                "is_onboarded": user.is_onboarded,
                "message": "온보딩 완료" if user.is_onboarded else "온보딩 미완료"
            }
            
            return response
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
