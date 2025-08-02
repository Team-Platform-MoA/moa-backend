from fastapi import APIRouter, Depends
from app.models.schemas import MessageRequest, AnalysisResponse
from app.services.analysis import get_analysis_service, AnalysisService

router = APIRouter(prefix="/analysis", tags=["분석"])

@router.post("/", response_model=AnalysisResponse)
async def analyze_message(
    request: MessageRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """메시지 감정 분석"""
    result = await analysis_service.analyze_text(request.message, request.user_id)
    return AnalysisResponse(**result)
