import uuid
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat import Chat
from app.repositories.base_repository import BaseRepository

class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chat, db)

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[Chat]:
        stmt = select(self.model).where(self.model.user_id == user_id).order_by(self.model.updated_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_with_messages(self, chat_id: uuid.UUID) -> Chat | None:
        stmt = select(self.model).options(selectinload(self.model.messages)).where(self.model.id == chat_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def delete_all_by_user(self, user_id: uuid.UUID) -> int:
        stmt = delete(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
