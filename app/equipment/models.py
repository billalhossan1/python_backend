from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Equipment(Base):
    """SQLAlchemy model for equipment records."""

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="", server_default="")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
    purchase_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    def apply_update(
        self,
        name: Optional[str],
        serial_number: Optional[str],
        category: Optional[str],
        status: Optional[str],
        purchase_date: Optional[date],
    ) -> None:
        """Mutate this equipment's fields in-place (only provided values are changed)."""
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
