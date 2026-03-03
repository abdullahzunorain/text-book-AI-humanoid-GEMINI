from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

from database import engine, get_db, Base
from models import User, Message, UserContext
from crud_users import create_user, get_user_by_id, get_user_context, create_or_update_user_context
from crud_messages import create_message, get_recent_chat_history
from vector_store import get_qdrant_client
from rag_service import RAGService

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Humanoid Textbook API")

# Configure CORS for Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Humanoid Textbook API is running"}


@app.get("/health")
async def health(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies database connectivity.
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.post("/users/", response_model=dict)
async def register_user(
    name: str,
    email: str = None,
    hardware_background: str = None,
    software_background: str = None,
    db: Session = Depends(get_db)
):
    """
    Register a new user in the system.
    
    - **name**: User's display name (required)
    - **email**: User's email (optional)
    - **hardware_background**: Hardware experience (optional)
    - **software_background**: Software experience (optional)
    """
    user = create_user(
        db=db,
        name=name,
        email=email,
        hardware_background=hardware_background,
        software_background=software_background
    )
    
    # Create default user context
    create_or_update_user_context(db=db, user_id=user.id)
    
    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": str(user.created_at)
    }


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user information by ID.
    """
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "hardware_background": user.hardware_background,
        "software_background": user.software_background,
        "created_at": str(user.created_at)
    }


@app.post("/chat/")
async def chat(
    user_id: int,
    message: str,
    session_id: str = None,
    selected_text: str = None,
    db: Session = Depends(get_db)
):
    """
    Send a message and get a RAG-powered response from the AI chatbot.
    """
    try:
        # Initialize RAG service
        qdrant_client = get_qdrant_client()
        rag_service = RAGService(db, qdrant_client)
        
        # Generate RAG response
        result = rag_service.chat(
            user_id=user_id,
            message=message,
            session_id=session_id,
            selected_text=selected_text
        )
        
        bot_response = result["response"]
        
    except Exception as e:
        # Fallback if RAG fails
        bot_response = f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"
        result = {
            "context_used": False,
            "context_count": 0,
            "sources": []
        }
    
    # Save user message
    create_message(
        db=db,
        user_id=user_id,
        role="user",
        content=message,
        session_id=session_id
    )
    
    # Save bot response
    create_message(
        db=db,
        user_id=user_id,
        role="bot",
        content=bot_response,
        session_id=session_id
    )
    
    return {
        "response": bot_response,
        "context_used": result.get("context_used", False),
        "context_count": result.get("context_count", 0),
        "sources": result.get("sources", []),
        "user_id": user_id
    }


@app.get("/chat/history/{user_id}")
async def get_chat_history(
    user_id: int,
    session_id: str = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a user.
    """
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = get_recent_chat_history(
        db=db,
        user_id=user_id,
        session_id=session_id,
        limit=limit
    )
    
    return {
        "user_id": user_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": str(msg.timestamp),
                "session_id": msg.session_id
            }
            for msg in messages
        ],
        "count": len(messages)
    }


class ContentRequest(BaseModel):
    user_id: int
    content: str

@app.post("/personalize/")
async def personalize(
    req: ContentRequest,
    db: Session = Depends(get_db)
):
    try:
        qdrant_client = get_qdrant_client()
        rag_service = RAGService(db, qdrant_client)
        personalized = rag_service.personalize_content(req.user_id, req.content)
        return {"content": personalized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TranslateRequest(BaseModel):
    content: str

@app.post("/translate/")
async def translate(
    req: TranslateRequest,
    db: Session = Depends(get_db)
):
    try:
        qdrant_client = get_qdrant_client()
        rag_service = RAGService(db, qdrant_client)
        translated = rag_service.translate_content(req.content)
        return {"content": translated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
