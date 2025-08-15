import uuid
from typing import Dict
from fastapi import HTTPException
from app.core.constants import Defaults, ErrorMessages, Messages
from app.models.models import User, Conversation
from app.schemas.requests import CompleteOnboardingRequest
from app.utils.common import format_message, get_korea_now

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
                 detail=format_message(ErrorMessages.ENUM_VALIDATION_MISSING, field_name=field_name)
            )
        
        try:
            return enum_value.value
        except AttributeError:
            raise HTTPException(
                status_code=400, 
               detail=format_message(ErrorMessages.ENUM_VALIDATION_INVALID, field_name=field_name)
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
            user_id = str(uuid.uuid4())
            
            user = User(
                user_id=user_id,
                name=onboarding_data.user_name,
                birth_year=onboarding_data.user_birth_year,
                gender=onboarding_data.user_gender,
                family_relationship=onboarding_data.family_relationship,
                daily_care_hours=onboarding_data.daily_care_hours,
                family_member_nickname=onboarding_data.family_member.nickname,
                family_member_birth_year=onboarding_data.family_member.birth_year,
                family_member_gender=onboarding_data.family_member.gender,
                family_member_dementia_stage=onboarding_data.family_member.dementia_stage,
                is_onboarded=True,
                created_at=get_korea_now(),
                last_active=get_korea_now()
            )
            
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
                "message": Messages.ONBOARDING_SUCCESS
            }
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=format_message(ErrorMessages.ONBOARDING_PROCESSING_ERROR, error=str(e))
            )

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
                                raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)

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
                "message": Messages.ONBOARDING_COMPLETE if user.is_onboarded else Messages.ONBOARDING_INCOMPLETE
            }
            
            return response
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=format_message(ErrorMessages.ONBOARDING_STATUS_ERROR, error=str(e))
            )

user_service = UserService()

def get_user_service() -> UserService:
    """사용자 서비스 인스턴스 반환"""
    return user_service
