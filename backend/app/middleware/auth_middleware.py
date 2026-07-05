from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database.session import get_db
from app.models.user import User, UserRole
from app.utils.security import verify_token
from app.utils.exceptions import AuthenticationError, AuthorizationError
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = verify_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise AuthenticationError("Could not validate credentials")
        user_id = uuid.UUID(user_id_str)
    except Exception:
        raise AuthenticationError("Could not validate credentials")
        
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if user is None:
        raise AuthenticationError("User not found")
    if not user.is_active:
        raise AuthenticationError("Inactive user")
        
    return user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise AuthorizationError("The user doesn't have enough privileges")
    return current_user
