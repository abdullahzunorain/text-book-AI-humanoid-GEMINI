"""
CRUD operations for user management.
"""
from sqlalchemy.orm import Session
from models import User, UserContext
from datetime import datetime
from typing import Optional, List


def create_user(db: Session, name: str, email: Optional[str] = None,
                hardware_background: Optional[str] = None,
                software_background: Optional[str] = None) -> User:
    """
    Create a new user in the database.
    
    Args:
        db: Database session
        name: User's name
        email: User's email (optional)
        hardware_background: Hardware experience description (optional)
        software_background: Software experience description (optional)
    
    Returns:
        Created User object
    """
    db_user = User(
        name=name,
        email=email,
        hardware_background=hardware_background,
        software_background=software_background
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by their ID.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by their email.
    
    Args:
        db: Database session
        email: User's email
    
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    """
    Update user information.
    
    Args:
        db: Database session
        user_id: User ID
        **kwargs: Fields to update (name, email, hardware_background, software_background)
    
    Returns:
        Updated User object or None if not found
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def create_or_update_user_context(db: Session, user_id: int,
                                   current_module: Optional[str] = None,
                                   current_chapter: Optional[str] = None,
                                   learning_pace: Optional[str] = None,
                                   preferred_detail_level: Optional[str] = None,
                                   topics_mastered: Optional[List[str]] = None,
                                   topics_in_progress: Optional[List[str]] = None) -> UserContext:
    """
    Create or update user context for personalized learning.
    
    Args:
        db: Database session
        user_id: User ID
        current_module: Current module being studied
        current_chapter: Current chapter being studied
        learning_pace: User's preferred learning pace
        preferred_detail_level: User's preferred detail level
        topics_mastered: List of topic IDs the user has mastered
        topics_in_progress: List of topic IDs the user is currently studying
    
    Returns:
        UserContext object
    """
    user_context = db.query(UserContext).filter(UserContext.user_id == user_id).first()
    
    if not user_context:
        user_context = UserContext(user_id=user_id)
        db.add(user_context)
    
    # Update fields if provided
    if current_module:
        user_context.current_module = current_module
    if current_chapter:
        user_context.current_chapter = current_chapter
    if learning_pace:
        user_context.learning_pace = learning_pace
    if preferred_detail_level:
        user_context.preferred_detail_level = preferred_detail_level
    if topics_mastered:
        user_context.topics_mastered = ",".join(topics_mastered)
    if topics_in_progress:
        user_context.topics_in_progress = ",".join(topics_in_progress)
    
    db.commit()
    db.refresh(user_context)
    return user_context


def get_user_context(db: Session, user_id: int) -> Optional[UserContext]:
    """
    Get user context by user ID.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        UserContext object or None if not found
    """
    return db.query(UserContext).filter(UserContext.user_id == user_id).first()
