from __future__ import annotations

from typing import Sequence

from app.core.exceptions import ConflictException, NotFoundException
from app.equipment.models import Equipment
from app.equipment.repository import EquipmentRepository
from app.equipment.schemas import EquipmentCreate, EquipmentUpdate


class EquipmentService:
    """
    Business logic layer for Equipment.

    Sits between the HTTP router and the data repository.
    All domain rules live here — keeps routers thin.
    """

    def __init__(self, repository: EquipmentRepository) -> None:
        self._repo = repository

    # ── Query operations ───────────────────────────────────────────────────────

    async def get_all(self) -> Sequence[Equipment]:
        return await self._repo.get_all()

    async def get_by_id(self, equipment_id: int) -> Equipment:
        equipment = await self._repo.get_by_id(equipment_id)
        if equipment is None:
            raise NotFoundException(resource="Equipment", identifier=equipment_id)
        return equipment

    # ── Mutation operations ────────────────────────────────────────────────────

    async def create(self, payload: EquipmentCreate) -> Equipment:
        # Business rule: no duplicate serial numbers
        existing = await self._repo.get_all()
        if any(e.serial_number == payload.serial_number for e in existing):
            raise ConflictException(
                f"Equipment with serial number '{payload.serial_number}' already exists."
            )

        return await self._repo.create(
            name=payload.name,
            serial_number=payload.serial_number,
            category=payload.category,
            status=payload.status,
            purchase_date=payload.purchase_date,
        )

    async def update(self, equipment_id: int, payload: EquipmentUpdate) -> Equipment:
        equipment = await self.get_by_id(equipment_id)
        equipment.apply_update(
            name=payload.name,
            serial_number=payload.serial_number,
            category=payload.category,
            status=payload.status,
            purchase_date=payload.purchase_date,
        )
        return await self._repo.update(equipment)

    async def delete(self, equipment_id: int) -> None:
        equipment = await self.get_by_id(equipment_id)
        await self._repo.delete(equipment)
