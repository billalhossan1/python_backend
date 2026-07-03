from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class StandardResponse(BaseModel,Generic[T]):
    """Standardized wrapper structure for all API responses."""
    success: bool
    message: str
    meta: Optional[dict[str, Any]] = None
    data: Optional[T] = None
