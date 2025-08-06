import json
import uuid
from fastapi import APIRouter, WebSocket, Depends
from app.services.analysis import get_analysis_service, AnalysisService
import logging 

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    await websocket.accept()
    logger.info("📡 Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"🎤 Received: {data}")
            
            try:
                message_data = json.loads(data)
                if isinstance(message_data, dict) and "message" in message_data:
                    user_id = message_data.get("user_id", str(uuid.uuid4()))
                    message = message_data["message"]
                else:
                    user_id = str(uuid.uuid4())
                    message = data
            except json.JSONDecodeError:
                user_id = str(uuid.uuid4())
                message = data
            
            result = await analysis_service.analyze_text(message, user_id)
            await websocket.send_text(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        logger.error("❌ Error:", e)
    finally:
        logger.info("🔌 Client disconnected")
        await websocket.close()
