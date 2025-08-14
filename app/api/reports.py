from fastapi import APIRouter, Depends, Header
from app.core.constants import Defaults
from app.services.report import ReportService, get_report_service
from app.schemas.responses import ReportsListResponse

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=ReportsListResponse)
async def list_reports(
    limit: int = Defaults.HISTORY_LIMIT,
    user_id: str = Header(..., alias="X-User-Id"),
    report_service: ReportService = Depends(get_report_service())
):
    return await report_service.get_user_reports(user_id, limit)