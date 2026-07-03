from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.equipment.repository import EquipmentRepository
from app.equipment.service import EquipmentService


def get_equipment_service(
    session: AsyncSession = Depends(get_db_session),
) -> EquipmentService:
    """FastAPI dependency that provides a fully wired EquipmentService instance per request."""
    repository = EquipmentRepository(session=session)
    return EquipmentService(repository=repository)
