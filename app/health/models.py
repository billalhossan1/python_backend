from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HealthRecord:
    """
    Domain model for a Health Record.

    This is a plain Python dataclass — no ORM, no HTTP concern.
    Swap this out with an SQLAlchemy model when you add a database.
    """

    id: int
    patient_name: str
    diagnosis: str
    severity: str = "low"  # low, medium, high, critical
    notes: str = ""
    recorded_at: Optional[datetime] = None

    def apply_update(
        self,
        patient_name: Optional[str],
        diagnosis: Optional[str],
        severity: Optional[str],
        notes: Optional[str],
    ) -> None:
        if patient_name is not None:
            self.patient_name = patient_name
        if diagnosis is not None:
            self.diagnosis = diagnosis
        if severity is not None:
            self.severity = severity
        if notes is not None:
            self.notes = notes
