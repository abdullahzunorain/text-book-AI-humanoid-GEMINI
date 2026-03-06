from src.db.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    
    # Custom fields for Physical AI textbook
    hardware_background = Column(String(100), nullable=True)
    software_background = Column(String(100), nullable=True)
    learning_goal = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="user")
