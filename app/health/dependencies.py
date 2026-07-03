from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.health.repository import HealthRecordRepository
from app.health.service import HealthRecordService


def get_health_service(
    session: AsyncSession = Depends(get_db_session),
) -> HealthRecordService:
    """FastAPI dependency that provides a fully wired HealthRecordService instance per request."""
    repository = HealthRecordRepository(session=session)
    return HealthRecordService(repository=repository)
