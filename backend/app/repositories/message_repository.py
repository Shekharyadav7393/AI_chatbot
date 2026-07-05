import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.repositories.base_repository import BaseRepository

class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)

    async def get_by_chat(self, chat_id: uuid.UUID, skip: int = 0, limit: int = 50) -> list[Message]:
        stmt = select(self.model).where(self.model.chat_id == chat_id).order_by(self.model.created_at.asc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_recent_by_chat(self, chat_id: uuid.UUID, limit: int = 10) -> list[Message]:
        stmt = select(self.model).where(self.model.chat_id == chat_id).order_by(self.model.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        messages = list(result.scalars().all())
        messages.reverse() # return in chronological order
        return messages
