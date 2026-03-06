"""
CRUD operations for message/chat history management.
"""
from sqlalchemy.orm import Session
from models import Message
from datetime import datetime
from typing import Optional, List


def create_message(db: Session, user_id: int, role: str, content: str,
                   session_id: Optional[str] = None) -> Message:
    """
    Create a new message (user or bot) in the database.
    
    Args:
        db: Database session
        user_id: User ID
        role: 'user' or 'bot'
        content: Message content
        session_id: Optional session identifier for grouping conversations
    
    Returns:
        Created Message object
    """
    db_message = Message(
        user_id=user_id,
        role=role,
        content=content,
        session_id=session_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_by_user(db: Session, user_id: int, limit: int = 50) -> List[Message]:
    """
    Get recent messages for a user.
    
    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of messages to return
    
    Returns:
        List of Message objects, ordered by timestamp (most recent first)
    """
    return db.query(Message)\
        .filter(Message.user_id == user_id)\
        .order_by(Message.timestamp.desc())\
        .limit(limit)\
        .all()


def get_messages_by_session(db: Session, session_id: str, limit: int = 50) -> List[Message]:
    """
    Get messages from a specific chat session.
    
    Args:
        db: Database session
        session_id: Session identifier
        limit: Maximum number of messages to return
    
    Returns:
        List of Message objects, ordered by timestamp
    """
    return db.query(Message)\
        .filter(Message.session_id == session_id)\
        .order_by(Message.timestamp.asc())\
        .limit(limit)\
        .all()


def get_recent_chat_history(db: Session, user_id: int, session_id: Optional[str] = None,
                            limit: int = 10) -> List[Message]:
    """
    Get recent chat history for a user, optionally filtered by session.
    Implements sliding window for context retrieval.
    
    Args:
        db: Database session
        user_id: User ID
        session_id: Optional session identifier
        limit: Number of recent messages to retrieve
    
    Returns:
        List of Message objects (alternating user/bot pairs)
    """
    query = db.query(Message).filter(Message.user_id == user_id)
    
    if session_id:
        query = query.filter(Message.session_id == session_id)
    
    return query\
        .order_by(Message.timestamp.desc())\
        .limit(limit)\
        .all()


def delete_messages_by_user(db: Session, user_id: int) -> int:
    """
    Delete all messages for a user.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        Number of messages deleted
    """
    deleted = db.query(Message).filter(Message.user_id == user_id).delete()
    db.commit()
    return deleted


def delete_messages_by_session(db: Session, session_id: str) -> int:
    """
    Delete all messages in a session.
    
    Args:
        db: Database session
        session_id: Session identifier
    
    Returns:
        Number of messages deleted
    """
    deleted = db.query(Message).filter(Message.session_id == session_id).delete()
    db.commit()
    return deleted
