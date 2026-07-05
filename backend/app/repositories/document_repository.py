import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentStatus
from app.repositories.base_repository import BaseRepository

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db: AsyncSession):
        super().__init__(Document, db)

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[Document]:
        stmt = select(self.model).where(self.model.uploaded_by == user_id).order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_user(self, user_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(self.model).where(self.model.uploaded_by == user_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_by_status(self, status: DocumentStatus) -> list[Document]:
        stmt = select(self.model).where(self.model.status == status)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_status(self, id: uuid.UUID, status: DocumentStatus, chunk_count: int | None = None) -> Document | None:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        db_obj.status = status
        if chunk_count is not None:
            db_obj.chunk_count = chunk_count
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
