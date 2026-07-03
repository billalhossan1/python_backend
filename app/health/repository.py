from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.health.models import HealthRecord


class HealthRecordRepository:
    """
    In-memory storage for HealthRecord domain objects.

    Replace the `_store` dict with actual DB calls (SQLAlchemy, motor, etc.)
    without touching any layer above this one.
    """

    def __init__(self) -> None:
        self._store: dict[int, HealthRecord] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[HealthRecord]:
        return list(self._store.values())

    def get_by_id(self, record_id: int) -> Optional[HealthRecord]:
        return self._store.get(record_id)

    def create(
        self,
        patient_name: str,
        diagnosis: str,
        severity: str,
        notes: str,
    ) -> HealthRecord:
        new_id = self._next_id()
        record = HealthRecord(
            id=new_id,
            patient_name=patient_name,
            diagnosis=diagnosis,
            severity=severity,
            notes=notes,
            recorded_at=datetime.now(),
        )
        self._store[new_id] = record
        return record

    def update(self, record: HealthRecord) -> HealthRecord:
        """Persist an already-mutated HealthRecord back to the store."""
        self._store[record.id] = record
        return record

    def delete(self, record_id: int) -> bool:
        if record_id in self._store:
            del self._store[record_id]
            return True
        return False
