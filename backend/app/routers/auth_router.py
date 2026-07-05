from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, RefreshTokenRequest, TokenResponse
from app.schemas.common import SuccessResponse
from app.controllers.auth_controller import AuthController
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
alias_router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=SuccessResponse[TokenResponse])
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.signup(request, db)

@router.post("/login", response_model=SuccessResponse[TokenResponse])
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(request, db)

@router.post("/refresh", response_model=SuccessResponse[TokenResponse])
async def refresh(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.refresh(request, db)

@router.post("/logout", response_model=SuccessResponse)
async def logout(
    request: RefreshTokenRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AuthController.logout(request, db)


@alias_router.post("/signup", response_model=SuccessResponse[TokenResponse])
async def signup_alias(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.signup(request, db)


@alias_router.post("/login", response_model=SuccessResponse[TokenResponse])
async def login_alias(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(request, db)


@alias_router.post("/logout", response_model=SuccessResponse)
async def logout_alias(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AuthController.logout(request, db)
