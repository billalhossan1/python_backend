
 
from datetime import date
from app.user.models import Role 
from typing import Optional
import uuid
from sqlalchemy import select
from app.user.models import User
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
class UserRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, id: uuid.UUID ) -> Optional[User]:
        return await self.session.get(User, id)
        
    

    async def create(self,
    name: str,
    email: str,
    password: str,
    dateOfBirth: date,
    role: Role,
    ) -> User:
        record = User(
            name=name,
            email=email,
            password=password,
            date_of_birth=dateOfBirth,
            role=role, 
        )
        self.session.add(record)
        await self.session.flush() 
        return record

    async def update(self, record: User) -> User:
        self.session.add(record)
        await self.session.flush()
        return record

    async def delete(self, record: User) -> None:
        await self.session.delete(record)
        await self.session.flush()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()