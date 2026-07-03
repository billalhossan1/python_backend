from app.core.exceptions import ConflictException
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.schemas import StandardResponse
from app.equipment.router import router as equipment_router
from app.health.router import router as health_router


from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: runs setup before startup and teardown on shutdown."""
    # ── startup ──────────────────────────────────────────────
    print(f"🚀  {settings.app_name} v{settings.app_version} starting up...")
    
    # Import models here to ensure they are registered on Base
    from app.equipment.models import Equipment
    from app.health.models import HealthRecord

    # Automatically create tables in database (not recommended for production, use Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    # ── shutdown ─────────────────────────────────────────────
    print("👋  Shutting down...")


def create_app() -> FastAPI:
    """Application factory — returns a fully configured FastAPI instance."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Mount feature routers
    # (Primary keys have been changed to MongoDB-like ObjectIDs)
    app.include_router(equipment_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")

    @app.get("/", response_model=StandardResponse[dict], tags=["App"])
    @app.get("/{id}", response_model=StandardResponse[dict], tags=["App"])
    def health_check(id: int = 1) -> StandardResponse[dict]:
        if id == 101:
            raise ConflictException("Conflict")
        return StandardResponse(
            success=True,
            message="Application is healthy",
            data={"status": "ok", "app": settings.app_name, "version": settings.app_version},
        )

    return app
