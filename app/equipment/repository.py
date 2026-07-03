from __future__ import annotations

from datetime import date
from typing import Optional

from app.equipment.models import Equipment


class EquipmentRepository:
    """
    In-memory storage for Equipment domain objects.

    Replace the `_store` dict with actual DB calls (SQLAlchemy, motor, etc.)
    without touching any layer above this one.
    """

    def __init__(self) -> None:
        self._store: dict[int, Equipment] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[Equipment]:
        return list(self._store.values())

    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        return self._store.get(equipment_id)

    def create(
        self,
        name: str,
        serial_number: str,
        category: str,
        status: str,
        purchase_date: Optional[date],
    ) -> Equipment:
        new_id = self._next_id()
        equipment = Equipment(
            id=new_id,
            name=name,
            serial_number=serial_number,
            category=category,
            status=status,
            purchase_date=purchase_date,
        )
        self._store[new_id] = equipment
        return equipment

    def update(self, equipment: Equipment) -> Equipment:
        """Persist an already-mutated Equipment back to the store."""
        self._store[equipment.id] = equipment
        return equipment

    def delete(self, equipment_id: int) -> bool:
        if equipment_id in self._store:
            del self._store[equipment_id]
            return True
        return False
