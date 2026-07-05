import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdateRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
