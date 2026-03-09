"""
Database models for user management and chat history.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.database import Base


class User(Base):
    """
    User model for storing user profile and preferences.
    Used for personalization and chat history tracking.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hardware_background = Column(String(500), nullable=True, default=None)
    software_background = Column(String(500), nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to messages
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Message(Base):
    """
    Message model for storing chat history.
    Each message is linked to a user and has a role (user/bot).
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(10), nullable=False)  # 'user' or 'bot'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(255), nullable=True, index=True)  # For grouping conversations

    # Relationship to user
    user = relationship("User", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, role='{self.role}')>"


class UserContext(Base):
    """
    User context model for storing personalized learning preferences.
    Used to tailor RAG responses based on user's background and progress.
    """
    __tablename__ = "user_contexts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_module = Column(String(100), nullable=True, default="module-1-ros2")
    current_chapter = Column(String(255), nullable=True)
    learning_pace = Column(String(50), nullable=True, default="standard")  # slow, standard, fast
    preferred_detail_level = Column(String(50), nullable=True, default="intermediate")  # beginner, intermediate, advanced
    topics_mastered = Column(Text, nullable=True)  # JSON array of topic IDs
    topics_in_progress = Column(Text, nullable=True)  # JSON array of topic IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to user
    user = relationship("User")

    def __repr__(self):
        return f"<UserContext(id={self.id}, user_id={self.user_id}, current_module='{self.current_module}')>"
