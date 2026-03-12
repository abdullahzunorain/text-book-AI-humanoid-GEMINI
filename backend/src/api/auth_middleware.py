"""
Authentication middleware for FastAPI.
Validates user identity from Authorization header.
For MVP: accepts user_id directly as token.
For production: validates session token against Neon session table.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.db.crud_users import get_user_by_id
from typing import Optional

security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[int]:
    """
    Optional auth dependency. Returns user_id if authenticated, None otherwise.
    """
    if not credentials:
        return None

    token = credentials.credentials
    try:
        user_id = int(token)
    except (ValueError, TypeError):
        return None

    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    return user_id


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> int:
    """
    Required auth dependency. Returns user_id or raises 401.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        user_id = int(token)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
