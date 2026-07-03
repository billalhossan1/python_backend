from __future__ import annotations

import uuid
from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.equipment.models import Equipment


class EquipmentRepository:
    """SQLAlchemy implementation of the Equipment repository using UUIDs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> Sequence[Equipment]:
        result = await self.session.execute(select(Equipment))
        return result.scalars().all()

    async def get_by_id(self, equipment_id: uuid.UUID) -> Optional[Equipment]:
        return await self.session.get(Equipment, equipment_id)

    async def get_by_serial_number(self, serial_number: str) -> Optional[Equipment]:
        result = await self.session.execute(
            select(Equipment).where(Equipment.serial_number == serial_number)
        )
        return result.scalars().first()

    async def create(
        self,
        serial_number: str,
        name: str,
        category: str,
        status: str,
        purchase_date: Optional[date],
    ) -> Equipment:
        equipment = Equipment(
            serial_number=serial_number,
            name=name,
            category=category,
            status=status,
            purchase_date=purchase_date,
        )
        self.session.add(equipment)
        await self.session.flush()  # Generates the UUID
        return equipment

    async def update(self, equipment: Equipment) -> Equipment:
        self.session.add(equipment)
        await self.session.flush()
        return equipment

    async def delete(self, equipment: Equipment) -> None:
        await self.session.delete(equipment)
        await self.session.flush()
