from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class EquipmentCreate(BaseModel):
    """Payload required to create a new equipment record."""

    name: str = Field(..., min_length=1, max_length=100, description="Equipment name")
    serial_number: str = Field(..., min_length=1, max_length=50, description="Unique serial number")
    category: str = Field(default="", max_length=100, description="Equipment category")
    status: str = Field(default="active", description="Status: active, maintenance, retired")
    purchase_date: Optional[date] = Field(default=None, description="Date of purchase")


class EquipmentUpdate(BaseModel):
    """Partial-update payload — all fields are optional."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    serial_number: Optional[str] = Field(default=None, min_length=1, max_length=50)
    category: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default=None)
    purchase_date: Optional[date] = Field(default=None)


class EquipmentResponse(BaseModel):
    """Response schema returned to the client."""

    id: int
    name: str
    serial_number: str
    category: str
    status: str
    purchase_date: Optional[date]

    model_config = {"from_attributes": True}
