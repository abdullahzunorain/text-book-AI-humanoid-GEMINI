"""
Database initialization script.
Creates all tables and sets up the database schema.

Usage:
    python init_db.py
"""
from database import engine, Base
from models import User, Message, UserContext


def init_database():
    """
    Initialize the database by creating all tables.
    This is safe to run multiple times (idempotent).
    """
    print("🔧 Initializing database...")
    print(f"Database engine: {engine.url}")
    
    # Create all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print("\nCreated tables:")
    print("  - users (User profiles and preferences)")
    print("  - messages (Chat history)")
    print("  - user_contexts (Personalized learning context)")


if __name__ == "__main__":
    init_database()
