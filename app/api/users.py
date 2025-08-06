from fastapi import APIRouter, Depends
from app.models.schemas import UserHistoryResponse
from app.services.user import get_user_service, UserService

router = APIRouter(prefix="/users", tags=["사용자"])

@router.get("/{user_id}/history", response_model=UserHistoryResponse)
async def get_user_history(
    user_id: str,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service)
):
    """사용자의 분석 기록 조회"""
    result = await user_service.get_user_history(user_id, limit)
    return UserHistoryResponse(**result)
