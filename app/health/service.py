from __future__ import annotations

from app.core.exceptions import NotFoundException
from app.health.models import HealthRecord
from app.health.repository import HealthRecordRepository
from app.health.schemas import HealthRecordCreate, HealthRecordUpdate


class HealthRecordService:
    """
    Business logic layer for Health Records.

    Sits between the HTTP router and the data repository.
    All domain rules live here — keeps routers thin.
    """

    def __init__(self, repository: HealthRecordRepository) -> None:
        self._repo = repository

    # ── Query operations ───────────────────────────────────────────────────────

    def get_all(self) -> list[HealthRecord]:
        return self._repo.get_all()

    def get_by_id(self, record_id: int) -> HealthRecord:
        record = self._repo.get_by_id(record_id)
        if record is None:
            raise NotFoundException(resource="HealthRecord", identifier=record_id)
        return record

    # ── Mutation operations ────────────────────────────────────────────────────

    def create(self, payload: HealthRecordCreate) -> HealthRecord:
        return self._repo.create(
            patient_name=payload.patient_name,
            diagnosis=payload.diagnosis,
            severity=payload.severity,
            notes=payload.notes,
        )

    def update(self, record_id: int, payload: HealthRecordUpdate) -> HealthRecord:
        record = self.get_by_id(record_id)
        record.apply_update(
            patient_name=payload.patient_name,
            diagnosis=payload.diagnosis,
            severity=payload.severity,
            notes=payload.notes,
        )
        return self._repo.update(record)

    def delete(self, record_id: int) -> None:
        if not self._repo.delete(record_id):
            raise NotFoundException(resource="HealthRecord", identifier=record_id)
