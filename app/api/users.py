from fastapi import APIRouter, Depends
from app.schemas.responses import UserHistoryResponse, OnboardingResponse
from app.schemas.requests import OnboardingRequest
from app.services.user import get_user_service, UserService

router = APIRouter(prefix="/users", tags=["사용자"])

@router.post("/onboarding", response_model=OnboardingResponse)
async def create_user_onboarding(
    onboarding_data: OnboardingRequest,
    user_service: UserService = Depends(get_user_service)
):
    """사용자 온보딩 정보 저장"""
    result = await user_service.create_user_onboarding(onboarding_data)
    return OnboardingResponse(**result)

@router.get("/{user_id}/onboarding", response_model=OnboardingResponse)
async def get_user_onboarding_status(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """사용자 온보딩 상태 조회"""
    result = await user_service.get_user_onboarding_status(user_id)
    return OnboardingResponse(**result)

@router.get("/{user_id}/history", response_model=UserHistoryResponse)
async def get_user_history(
    user_id: str,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service)
):
    """사용자의 분석 기록 조회"""
    result = await user_service.get_user_history(user_id, limit)
    return UserHistoryResponse(**result)
