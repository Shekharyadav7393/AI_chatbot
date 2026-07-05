from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest
from app.schemas.common import SuccessResponse
from app.controllers.user_controller import UserController
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
alias_router = APIRouter(tags=["Users"])

@router.get("/profile", response_model=SuccessResponse[UserResponse])
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await UserController.get_profile(current_user, db)

@router.put("/profile", response_model=SuccessResponse[UserResponse])
async def update_profile(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await UserController.update_profile(request, current_user, db)


@alias_router.get("/profile", response_model=SuccessResponse[UserResponse])
async def get_profile_alias(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await UserController.get_profile(current_user, db)
