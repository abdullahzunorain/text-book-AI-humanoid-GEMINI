"""
CRUD operations for message/chat history management (async).
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.models import Message
from datetime import datetime
from typing import Optional, List


async def create_message(
    db: AsyncSession,
    user_id: int,
    role: str,
    content: str,
    session_id: Optional[str] = None,
) -> Message:
    db_message = Message(
        user_id=user_id,
        role=role,
        content=content,
        session_id=session_id,
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


async def get_messages_by_user(
    db: AsyncSession, user_id: int, limit: int = 50
) -> List[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.user_id == user_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_messages_by_session(
    db: AsyncSession, session_id: str, limit: int = 50
) -> List[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.timestamp.asc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_recent_chat_history(
    db: AsyncSession,
    user_id: int,
    session_id: Optional[str] = None,
    limit: int = 10,
) -> List[Message]:
    stmt = select(Message).where(Message.user_id == user_id)
    if session_id:
        stmt = stmt.where(Message.session_id == session_id)
    stmt = stmt.order_by(Message.timestamp.desc()).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def delete_messages_by_user(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(select(Message).where(Message.user_id == user_id))
    messages = result.scalars().all()
    count = len(messages)
    for msg in messages:
        await db.delete(msg)
    await db.commit()
    return count
