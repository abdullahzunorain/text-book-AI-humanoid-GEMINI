from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from src.api import health, users, chat

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables and Qdrant collection on startup."""
    # Create tables if they don't exist
    from src.db.database import engine, Base
    if engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Initialize Qdrant collection if available
    from src.services.vector_store import get_qdrant_client, init_collection
    client = get_qdrant_client()
    if client:
        init_collection(client)

    yield


app = FastAPI(
    title="AI Humanoid Textbook API",
    version="1.0.0",
    description="RAG-native API for Physical AI textbook.",
    lifespan=lifespan,
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(users.router, tags=["Users"])
app.include_router(chat.router, tags=["Chat"])


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Humanoid Textbook API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
