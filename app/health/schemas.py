from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthRecordCreate(BaseModel):
    """Payload required to create a new health record."""

    patient_name: str = Field(..., min_length=1, max_length=100, description="Patient name")
    diagnosis: str = Field(..., min_length=1, max_length=500, description="Diagnosis description")
    severity: str = Field(default="low", description="Severity: low, medium, high, critical")
    notes: str = Field(default="", max_length=1000, description="Additional notes")


class HealthRecordUpdate(BaseModel):
    """Partial-update payload — all fields are optional."""

    patient_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    diagnosis: Optional[str] = Field(default=None, min_length=1, max_length=500)
    severity: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=1000)


class HealthRecordResponse(BaseModel):
    """Response schema returned to the client."""

    id: uuid.UUID
    patient_name: str
    diagnosis: str
    severity: str
    notes: str
    recorded_at: Optional[datetime]

    model_config = {"from_attributes": True}
