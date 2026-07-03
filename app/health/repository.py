from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.health.models import HealthRecord


class HealthRecordRepository:
    """SQLAlchemy implementation of the HealthRecord repository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> Sequence[HealthRecord]:
        result = await self.session.execute(select(HealthRecord))
        return result.scalars().all()

    async def get_by_id(self, record_id: int) -> Optional[HealthRecord]:
        return await self.session.get(HealthRecord, record_id)

    async def create(
        self,
        patient_name: str,
        diagnosis: str,
        severity: str,
        notes: str,
    ) -> HealthRecord:
        record = HealthRecord(
            patient_name=patient_name,
            diagnosis=diagnosis,
            severity=severity,
            notes=notes,
        )
        self.session.add(record)
        await self.session.flush()  # Populates ID
        return record

    async def update(self, record: HealthRecord) -> HealthRecord:
        self.session.add(record)
        await self.session.flush()
        return record

    async def delete(self, record: HealthRecord) -> None:
        await self.session.delete(record)
        await self.session.flush()
