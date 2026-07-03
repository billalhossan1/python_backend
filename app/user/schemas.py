from datetime import date 

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
        name: str
        email: str
        password: str
        date_of_birth: date
        role: str

 

class UserProfileResponse(BaseModel):
    """Response schema returned to the client."""

    id: uuid.UUID
    name: str
    email: str 
    date_of_birth: date
    role: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
