import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.message import MessageRole

class MessageResponse(BaseModel):
    id: uuid.UUID
    role: MessageRole
    content: str
    sources: list | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
