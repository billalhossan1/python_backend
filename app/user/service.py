from argon2 import _password_hasher
from argon2 import _password_hasher
from argon2 import _password_hasher
import uuid
from typing import Optional, Sequence
from datetime import date

from app.core.exceptions import NotFoundException
from app.user.models import Role, User
from app.user.repository import UserRepository
from app.user.schemas import UserProfileCreate
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_all(self) -> Sequence[User]:
        return await self.repository.get_all()

    async def get_by_id(self, record_id: uuid.UUID) -> User:
        record = await self.repository.get_by_id(record_id)
        if record is None:
            raise NotFoundException(resource="User", identifier=record_id)
        return record

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def create(self, payload: UserProfileCreate) -> User:
        record = await self.repository.create(
            name=payload.name,
            email=payload.email,
            password=password_hash.hash(payload.password),
            dateOfBirth=payload.date_of_birth,
            role=Role(payload.role),
        )
        await self.repository.session.commit()
        return record

    async def update(self, record_id: uuid.UUID, payload: UserProfileCreate) -> User:
        record = await self.get_by_id(record_id)
        record.name = payload.name
        record.email = payload.email
        record.password = password_hash.hash(payload.password)
        record.date_of_birth = payload.date_of_birth
        record.role = Role(payload.role)
        updated = await self.repository.update(record)
        await self.repository.session.commit()
        return updated

    async def delete(self, record_id: uuid.UUID) -> None:
        record = await self.get_by_id(record_id)
        await self.repository.delete(record)
        await self.repository.session.commit()