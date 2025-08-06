"""
MoA Backend - 치매 부양자를 위한 감정 분석 및 위로 메시지 제공 서비스
"""

import uvicorn
from app.core.config import settings

def main():
    """애플리케이션 실행"""
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        reload_dirs=["./app"] if settings.DEBUG else None
    )

if __name__ == "__main__":
    main()
