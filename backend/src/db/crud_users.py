"""
CRUD operations for user management (async).
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.models import User, UserContext
from datetime import datetime
from typing import Optional, List


async def create_user(
    db: AsyncSession,
    name: str,
    email: Optional[str] = None,
    hardware_background: Optional[str] = None,
    software_background: Optional[str] = None,
) -> User:
    db_user = User(
        name=name,
        email=email,
        hardware_background=hardware_background,
        software_background=software_background,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user_id: int, **kwargs) -> Optional[User]:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    for key, value in kwargs.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    db_user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_or_update_user_context(
    db: AsyncSession,
    user_id: int,
    current_module: Optional[str] = None,
    current_chapter: Optional[str] = None,
    learning_pace: Optional[str] = None,
    preferred_detail_level: Optional[str] = None,
    topics_mastered: Optional[List[str]] = None,
    topics_in_progress: Optional[List[str]] = None,
) -> UserContext:
    result = await db.execute(
        select(UserContext).where(UserContext.user_id == user_id)
    )
    user_context = result.scalar_one_or_none()

    if not user_context:
        user_context = UserContext(user_id=user_id)
        db.add(user_context)

    if current_module is not None:
        user_context.current_module = current_module
    if current_chapter is not None:
        user_context.current_chapter = current_chapter
    if learning_pace is not None:
        user_context.learning_pace = learning_pace
    if preferred_detail_level is not None:
        user_context.preferred_detail_level = preferred_detail_level
    if topics_mastered is not None:
        user_context.topics_mastered = ",".join(topics_mastered)
    if topics_in_progress is not None:
        user_context.topics_in_progress = ",".join(topics_in_progress)

    await db.commit()
    await db.refresh(user_context)
    return user_context


async def get_user_context(db: AsyncSession, user_id: int) -> Optional[UserContext]:
    result = await db.execute(
        select(UserContext).where(UserContext.user_id == user_id)
    )
    return result.scalar_one_or_none()
