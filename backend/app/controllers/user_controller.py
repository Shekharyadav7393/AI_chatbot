from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserUpdateRequest
from app.schemas.common import SuccessResponse
from app.services.user_service import UserService

class UserController:
    @staticmethod
    async def get_profile(current_user: User, db: AsyncSession):
        service = UserService(db)
        profile = await service.get_profile(current_user.id)
        return SuccessResponse(data=profile)

    @staticmethod
    async def update_profile(request: UserUpdateRequest, current_user: User, db: AsyncSession):
        service = UserService(db)
        updated_profile = await service.update_profile(current_user.id, request)
        return SuccessResponse(message="Profile updated successfully", data=updated_profile)
