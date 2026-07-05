import uuid
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.session import Session
from app.repositories.base_repository import BaseRepository

class SessionRepository(BaseRepository[Session]):
    def __init__(self, db: AsyncSession):
        super().__init__(Session, db)

    async def get_by_refresh_token(self, token: str) -> Session | None:
        stmt = select(self.model).where(self.model.refresh_token == token)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def revoke_session(self, session_id: uuid.UUID) -> bool:
        db_obj = await self.get_by_id(session_id)
        if not db_obj:
            return False
        db_obj.is_revoked = True
        await self.db.commit()
        return True

    async def revoke_all_user_sessions(self, user_id: uuid.UUID) -> int:
        stmt = delete(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount

    async def cleanup_expired(self) -> int:
        now = datetime.now(timezone.utc)
        stmt = delete(self.model).where(self.model.expires_at < now)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
