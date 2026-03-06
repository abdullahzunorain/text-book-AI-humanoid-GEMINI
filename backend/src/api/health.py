from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.db.database import get_db
from src.services.vector_store import get_qdrant_client

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Check Database
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Qdrant
    qdrant_status = "connected"
    client = get_qdrant_client()
    if not client:
        qdrant_status = "error: could not initialize client"
    else:
        try:
            client.get_collections()
        except Exception as e:
            qdrant_status = f"error: {str(e)}"
            
    return {
        "status": "ok",
        "database": db_status,
        "vector_store": qdrant_status
    }
