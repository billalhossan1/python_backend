from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class Equipment:
    """
    Domain model  for a piece of Equipment.

    This is a plain Python dataclass — no ORM, no HTTP concern.
    Swap this out with an SQLAlchemy model when you add a database.
    """

    id: int
    name: str
    serial_number: str
    category: str = ""
    status: str = "active"  # active, maintenance, retired
    purchase_date: Optional[date] = None

    def apply_update(
        self,
        name: Optional[str],
        serial_number: Optional[str],
        category: Optional[str],
        status: Optional[str],
        purchase_date: Optional[date],
    ) -> None:
        if name is not None:
            self.name = name
        if serial_number is not None:
            self.serial_number = serial_number
        if category is not None:
            self.category = category
        if status is not None:
            self.status = status
        if purchase_date is not None:
            self.purchase_date = purchase_date
