from fastapi import APIRouter, Depends, Header, Query
from app.services.report import ReportService, get_report_service
from app.schemas.responses import ReportsListResponse

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=ReportsListResponse)
async def list_reports(
    year: int = Query(..., description="조회할 연도 (예: 2025)"),
    month: int = Query(..., ge=1, le=12, description="조회할 월 (1~12)"),
    x_user_id: str = Header(..., alias="X-User-Id"),
    report_service: ReportService = Depends(get_report_service)
):
    return await report_service.get_user_reports(
        user_id=x_user_id,
        year=year,
        month=month
    )