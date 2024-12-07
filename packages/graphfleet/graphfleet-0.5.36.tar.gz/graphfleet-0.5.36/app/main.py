from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.endpoints import search
from app.core.config import Settings, get_settings
from app.db.init_db import init_db

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="GraphRAG implementation for fleet management",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add API router
    app.include_router(search.router, prefix=f"{settings.API_V1_STR}/search", tags=["search"])

    @app.on_event("startup")
    async def startup_event():
        await init_db()

    @app.get("/", tags=["health"])
    async def root():
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "message": "Welcome to GraphFleet API"
        }

    return app


app = create_app()