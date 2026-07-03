from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class EquipmentCreate(BaseModel):
    """Payload required to create a new equipment record."""

    serial_number: str = Field(..., min_length=1, max_length=50, description="Unique serial number")
    name: str = Field(..., min_length=1, max_length=100, description="Equipment name")
    category: str = Field(default="", max_length=100, description="Equipment category")
    status: str = Field(default="active", description="Status: active, maintenance, retired")
    purchase_date: Optional[date] = Field(default=None, description="Date of purchase")


class EquipmentUpdate(BaseModel):
    """Partial-update payload — all fields are optional. Identifiers cannot be updated."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default=None)
    purchase_date: Optional[date] = Field(default=None)


class EquipmentResponse(BaseModel):
    """Response schema returned to the client."""

    id: uuid.UUID
    serial_number: str
    name: str
    category: str
    status: str
    purchase_date: Optional[date]

    model_config = {"from_attributes": True}
