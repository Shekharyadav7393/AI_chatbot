from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import SignupRequest, LoginRequest, RefreshTokenRequest
from app.schemas.common import SuccessResponse
from app.services.auth_service import AuthService

class AuthController:
    @staticmethod
    async def signup(request: SignupRequest, db: AsyncSession):
        service = AuthService(db)
        tokens = await service.signup(request)
        return SuccessResponse(message="User registered successfully", data=tokens)

    @staticmethod
    async def login(request: LoginRequest, db: AsyncSession):
        service = AuthService(db)
        tokens = await service.login(request)
        return SuccessResponse(message="Login successful", data=tokens)

    @staticmethod
    async def refresh(request: RefreshTokenRequest, db: AsyncSession):
        service = AuthService(db)
        tokens = await service.refresh_token(request)
        return SuccessResponse(message="Token refreshed successfully", data=tokens)

    @staticmethod
    async def logout(request: RefreshTokenRequest, db: AsyncSession):
        service = AuthService(db)
        await service.logout(request.refresh_token)
        return SuccessResponse(message="Logged out successfully")
