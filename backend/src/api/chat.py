from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.db.database import get_db
from src.services.vector_store import get_qdrant_client
from src.services.rag import RAGService
from src.schemas.chat import ChatRequest, ChatResponse
from src.schemas.content import (
    PersonalizeRequest,
    PersonalizeResponse,
    TranslateRequest,
    TranslateResponse,
)
from src.api.auth_middleware import get_current_user_optional

router = APIRouter()


@router.post("/chat/", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    qdrant=Depends(get_qdrant_client),
    current_user: Optional[int] = Depends(get_current_user_optional),
):
    user_id = current_user or 1  # fallback for unauthenticated users
    try:
        service = RAGService(db, qdrant)
        result = await service.chat(
            user_id=user_id,
            message=req.message,
            session_id=req.session_id,
            selected_text=req.selected_text,
        )
        return ChatResponse(
            response=result["response"],
            sources=result.get("sources", []),
            session_id=result.get("session_id", req.session_id),
            context_count=result.get("context_count", 0),
            context_used=result.get("context_used", False),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import logging
        logging.error(f"Chat error: {type(e).__name__}: {e}")
        if "429" in str(e) or "quota" in str(e).lower() or "rate" in str(e).lower():
            return ChatResponse(
                response="AI service temporarily unavailable. Please try again later.",
                sources=[],
                session_id=req.session_id,
                context_count=0,
                context_used=False,
            )
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personalize/", response_model=PersonalizeResponse)
async def personalize(
    req: PersonalizeRequest,
    db: AsyncSession = Depends(get_db),
    qdrant=Depends(get_qdrant_client),
    current_user: Optional[int] = Depends(get_current_user_optional),
):
    user_id = current_user or 1
    try:
        service = RAGService(db, qdrant)
        personalized = await service.personalize_content(
            user_id=user_id,
            content=req.content,
        )
        return PersonalizeResponse(personalized_content=personalized)
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            return PersonalizeResponse(
                personalized_content="AI service temporarily unavailable. Please try again later."
            )
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate/", response_model=TranslateResponse)
async def translate(
    req: TranslateRequest,
    db: AsyncSession = Depends(get_db),
    qdrant=Depends(get_qdrant_client),
):
    try:
        service = RAGService(db, qdrant)
        translated = await service.translate_content(content=req.content)
        return TranslateResponse(translated_content=translated)
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            return TranslateResponse(
                translated_content="AI service temporarily unavailable. Please try again later."
            )
        raise HTTPException(status_code=500, detail=str(e))
