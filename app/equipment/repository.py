from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.equipment.models import Equipment


class EquipmentRepository:
    """SQLAlchemy implementation of the Equipment repository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> Sequence[Equipment]:
        result = await self.session.execute(select(Equipment))
        return result.scalars().all()

    async def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        return await self.session.get(Equipment, equipment_id)

    async def create(
        self,
        name: str,
        serial_number: str,
        category: str,
        status: str,
        purchase_date: Optional[date],
    ) -> Equipment:
        equipment = Equipment(
            name=name,
            serial_number=serial_number,
            category=category,
            status=status,
            purchase_date=purchase_date,
        )
        self.session.add(equipment)
        await self.session.flush()  # Populates auto-generated ID
        return equipment

    async def update(self, equipment: Equipment) -> Equipment:
        self.session.add(equipment)
        await self.session.flush()
        return equipment

    async def delete(self, equipment: Equipment) -> None:
        await self.session.delete(equipment)
        await self.session.flush()
