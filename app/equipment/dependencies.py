from __future__ import annotations

from functools import lru_cache

from app.equipment.repository import EquipmentRepository
from app.equipment.service import EquipmentService


@lru_cache(maxsize=1)
def _get_equipment_repository() -> EquipmentRepository:
    """Returns a single shared EquipmentRepository instance (application lifetime)."""
    return EquipmentRepository()


def get_equipment_service() -> EquipmentService:
    """FastAPI dependency that provides a fully wired EquipmentService."""
    return EquipmentService(repository=_get_equipment_repository())
