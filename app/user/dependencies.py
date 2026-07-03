from app.user.repository import UserRepository
from app.user.service import UserService
from app.core.database import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

def get_user_service(
    session: AsyncSession = Depends(get_db_session),
) -> UserService:
    """FastAPI dependency that provides a fully wired HealthRecordService instance per request."""
    repository = UserRepository(session=session)
    return UserService(repository=repository)
