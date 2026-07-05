import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .message import MessageResponse

class ChatRequest(BaseModel):
    message: str
    chat_id: uuid.UUID | None = None

class ChatResponse(BaseModel):
    chat_id: uuid.UUID
    message: MessageResponse

class ChatSummary(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int

    model_config = ConfigDict(from_attributes=True)

class ChatHistoryResponse(BaseModel):
    chats: list[ChatSummary]
    total: int

class ChatDetailResponse(BaseModel):
    id: uuid.UUID
    title: str
    messages: list[MessageResponse]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
