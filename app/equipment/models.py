from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Equipment(Base):
    """SQLAlchemy model for equipment records with UUID primary key."""

    __tablename__ = "equipment"

    # UUID type with python-side fallback default.
    # Postgres will automatically generate a UUID on insert if gen_random_uuid is supported.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    serial_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="", server_default="")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
    purchase_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    def apply_update(
        self,
        name: Optional[str],
        category: Optional[str],
        status: Optional[str],
        purchase_date: Optional[date],
    ) -> None:
        """Mutate this equipment's fields in-place (only provided values are changed)."""
        
        if name is not None:
            self.name = name
        if category is not None:
            self.category = category
        if status is not None:
            self.status = status
        if purchase_date is not None:
            self.purchase_date = purchase_date
