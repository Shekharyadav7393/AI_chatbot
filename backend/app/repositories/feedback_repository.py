import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.feedback import Feedback
from app.repositories.base_repository import BaseRepository

class FeedbackRepository(BaseRepository[Feedback]):
    def __init__(self, db: AsyncSession):
        super().__init__(Feedback, db)

    async def get_by_message(self, message_id: uuid.UUID) -> Feedback | None:
        stmt = select(self.model).where(self.model.message_id == message_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[Feedback]:
        stmt = select(self.model).where(self.model.user_id == user_id).order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_average_rating(self) -> float:
        stmt = select(func.avg(self.model.rating))
        result = await self.db.execute(stmt)
        return result.scalar() or 0.0

    async def get_recent(self, limit: int = 10) -> list[Feedback]:
        stmt = select(self.model).order_by(self.model.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
