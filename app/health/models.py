from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class HealthRecord(Base):
    """SQLAlchemy model for health records."""

    __tablename__ = "health_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    diagnosis: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="low", server_default="low")
    notes: Mapped[str] = mapped_column(Text, default="", server_default="")
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def apply_update(
        self,
        patient_name: Optional[str],
        diagnosis: Optional[str],
        severity: Optional[str],
        notes: Optional[str],
    ) -> None:
        """Mutate this record's fields in-place (only provided values are changed)."""
        if patient_name is not None:
            self.patient_name = patient_name
        if diagnosis is not None:
            self.diagnosis = diagnosis
        if severity is not None:
            self.severity = severity
        if notes is not None:
            self.notes = notes
