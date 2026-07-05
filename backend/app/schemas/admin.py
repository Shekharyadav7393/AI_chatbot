import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.user import UserRole

class ActivityItem(BaseModel):
    type: str
    description: str
    timestamp: datetime

class DashboardResponse(BaseModel):
    total_users: int
    total_documents: int
    total_chats: int
    total_messages: int
    total_feedback: int
    avg_rating: float
    recent_activity: list[ActivityItem]

class AdminUserUpdate(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None
