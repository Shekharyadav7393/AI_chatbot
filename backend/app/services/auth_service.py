import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from app.utils.exceptions import ConflictError, AuthenticationError
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.session_repo = SessionRepository(db)

    async def signup(self, data: SignupRequest) -> TokenResponse:
        # Check if email exists
        if await self.user_repo.get_by_email(data.email):
            raise ConflictError("Email already registered")
        
        # Check if username exists
        if await self.user_repo.get_by_username(data.username):
            raise ConflictError("Username already taken")
        
        # Create user (first user is admin)
        total_users = await self.user_repo.count()
        role = UserRole.admin if total_users == 0 else UserRole.user
        
        user_data = {
            "email": data.email,
            "username": data.username,
            "hashed_password": hash_password(data.password),
            "role": role
        }
        user = await self.user_repo.create(user_data)
        
        return await self._create_tokens_for_user(user.id)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
            
        return await self._create_tokens_for_user(user.id)

    async def refresh_token(self, data: RefreshTokenRequest) -> TokenResponse:
        try:
            payload = verify_token(data.refresh_token)
            if payload.get("type") != "refresh":
                raise AuthenticationError("Invalid token type")
        except Exception:
            raise AuthenticationError("Invalid or expired refresh token")

        # Verify token in DB
        db_session = await self.session_repo.get_by_refresh_token(data.refresh_token)
        if not db_session or db_session.is_revoked:
            raise AuthenticationError("Session revoked or invalid")

        # Revoke old session and create new tokens
        await self.session_repo.revoke_session(db_session.id)
        return await self._create_tokens_for_user(db_session.user_id)

    async def logout(self, refresh_token: str):
        db_session = await self.session_repo.get_by_refresh_token(refresh_token)
        if db_session:
            await self.session_repo.revoke_session(db_session.id)

    async def _create_tokens_for_user(self, user_id: uuid.UUID) -> TokenResponse:
        access_token = create_access_token(data={"sub": str(user_id)})
        refresh_token = create_refresh_token(data={"sub": str(user_id)})
        
        # Decode refresh token to get expiry
        payload = verify_token(refresh_token)
        from datetime import datetime, timezone
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        
        # Save session to DB
        await self.session_repo.create({
            "user_id": user_id,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        })
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
