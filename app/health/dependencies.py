from __future__ import annotations

from functools import lru_cache

from app.health.repository import HealthRecordRepository
from app.health.service import HealthRecordService


@lru_cache(maxsize=1)
def _get_health_repository() -> HealthRecordRepository:
    """Returns a single shared HealthRecordRepository instance (application lifetime)."""
    return HealthRecordRepository()


def get_health_service() -> HealthRecordService:
    """FastAPI dependency that provides a fully wired HealthRecordService."""
    return HealthRecordService(repository=_get_health_repository())
