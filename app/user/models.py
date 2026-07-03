
 
    
from app.core.database import Base
from enum import Enum
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum as SQLEnum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
 
class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "user"

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        date_of_birth: date,
        role: Role = Role.USER,
    ):
        self.name = name
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.role = role

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(10), nullable=False)

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    role: Mapped[Role] = mapped_column(
        SQLEnum(Role),
        default=Role.USER,
        nullable=False,
    )