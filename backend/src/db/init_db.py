"""
Database initialization script to create tables in Neon Postgres.
"""
import asyncio
import sys
import os

# Add src to path if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.database import engine, Base
from src.models.models import User, Message, UserContext  # Import models to register with Base

async def init_db():
    print("⏳ Initializing database...")
    async with engine.begin() as conn:
        # For development, you might want to drop all tables first
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
