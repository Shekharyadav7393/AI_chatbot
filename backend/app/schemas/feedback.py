import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class FeedbackRequest(BaseModel):
    message_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None

class FeedbackResponse(BaseModel):
    id: uuid.UUID
    message_id: uuid.UUID
    user_id: uuid.UUID
    rating: int
    comment: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
