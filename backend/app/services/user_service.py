import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse, UserUpdateRequest
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import NotFoundError, ConflictError

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_profile(self, user_id: uuid.UUID) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserResponse.model_validate(user)

    async def update_profile(self, user_id: uuid.UUID, data: UserUpdateRequest) -> UserResponse:
        # Check uniqueness if updating email
        if data.email:
            existing = await self.user_repo.get_by_email(data.email)
            if existing and existing.id != user_id:
                raise ConflictError("Email already in use")
                
        # Check uniqueness if updating username
        if data.username:
            existing = await self.user_repo.get_by_username(data.username)
            if existing and existing.id != user_id:
                raise ConflictError("Username already in use")
                
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_profile(user_id)
            
        updated_user = await self.user_repo.update(user_id, update_data)
        return UserResponse.model_validate(updated_user)
