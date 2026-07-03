from __future__ import annotations

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

    def get_all(self) -> list[Equipment]:
        return self._repo.get_all()

    def get_by_id(self, equipment_id: int) -> Equipment:
        equipment = self._repo.get_by_id(equipment_id)
        if equipment is None:
            raise NotFoundException(resource="Equipment", identifier=equipment_id)
        return equipment

    # ── Mutation operations ────────────────────────────────────────────────────

    def create(self, payload: EquipmentCreate) -> Equipment:
        # Business rule: no duplicate serial numbers
        existing = self._repo.get_all()
        if any(e.serial_number == payload.serial_number for e in existing):
            raise ConflictException(
                f"Equipment with serial number '{payload.serial_number}' already exists."
            )

        return self._repo.create(
            name=payload.name,
            serial_number=payload.serial_number,
            category=payload.category,
            status=payload.status,
            purchase_date=payload.purchase_date,
        )

    def update(self, equipment_id: int, payload: EquipmentUpdate) -> Equipment:
        equipment = self.get_by_id(equipment_id)
        equipment.apply_update(
            name=payload.name,
            serial_number=payload.serial_number,
            category=payload.category,
            status=payload.status,
            purchase_date=payload.purchase_date,
        )
        return self._repo.update(equipment)

    def delete(self, equipment_id: int) -> None:
        if not self._repo.delete(equipment_id):
            raise NotFoundException(resource="Equipment", identifier=equipment_id)
