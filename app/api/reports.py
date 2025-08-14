from fastapi import APIRouter, Depends, Header
from app.core.constants import Defaults
from app.services.user import get_user_service, UserService
from app.schemas.responses import ReportsListResponse

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=ReportsListResponse)
async def list_reports(
    limit: int = Defaults.HISTORY_LIMIT,
    user_id: str = Header(..., alias="X-User-Id"),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_history(user_id, limit)