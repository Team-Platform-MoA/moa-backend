from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api import users, websocket

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    await connect_to_mongo()
    yield
    await close_mongo_connection()

def create_app() -> FastAPI:
    """FastAPI 애플리케이션 생성"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users.router, prefix="/api")
    app.include_router(websocket.router)

    @app.get("/")
    async def root():
        return {
            "message": "MoA Backend API",
            "version": settings.VERSION,
            "description": settings.DESCRIPTION
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()
