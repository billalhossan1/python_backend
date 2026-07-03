from __future__ import annotations

import uuid
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

    async def get_by_id(self, equipment_id: uuid.UUID) -> Equipment:
        equipment = await self._repo.get_by_id(equipment_id)
        if equipment is None:
            raise NotFoundException(resource="Equipment", identifier=equipment_id)
        return equipment

    # ── Mutation operations ────────────────────────────────────────────────────

    async def create(self, payload: EquipmentCreate) -> Equipment:
        # Check if equipment with the same serial_number already exists
        existing = await self._repo.get_by_serial_number(payload.serial_number)
        if existing is not None:
            raise ConflictException(
                f"Equipment with serial number '{payload.serial_number}' already exists."
            )
        

        equipment = await self._repo.create(
            serial_number=payload.serial_number,
            name=payload.name,
            category=payload.category,
            status=payload.status,
            purchase_date=payload.purchase_date,
        )
        await self._repo.session.commit()
        return equipment

    async def update(self, equipment_id: uuid.UUID, payload: EquipmentUpdate) -> Equipment:
        equipment = await self.get_by_id(equipment_id)
        equipment.apply_update(
            name=payload.name,
            category=payload.category,
            status=payload.status,
            purchase_date=payload.purchase_date,
        )
        updated = await self._repo.update(equipment)
        await self._repo.session.commit()
        return updated

    async def delete(self, equipment_id: uuid.UUID) -> None:
        equipment = await self.get_by_id(equipment_id)
        await self._repo.delete(equipment)
        await self._repo.session.commit()
