from fastapi import APIRouter, Depends, status
from app.services.user import get_user_service, UserService
from app.schemas.requests import CompleteOnboardingRequest
from app.schemas.responses import OnboardingResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/onboarding", response_model=OnboardingResponse, status_code=status.HTTP_201_CREATED)
async def create_onboarding(
    onboarding_data: CompleteOnboardingRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    완전한 온보딩 정보 저장 (사용자 + 가족 정보)
    """
    return await user_service.create_complete_onboarding(onboarding_data)

@router.get("/{user_id}/onboarding")
async def get_onboarding_status(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    사용자 온보딩 상태 조회
    """
    return await user_service.get_user_onboarding_status(user_id)