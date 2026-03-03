"""
Qdrant vector database configuration and client.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Collection name for textbook content
TEXTBOOK_COLLECTION = "textbook_segments"

# Vector dimensions (using Gemini embeddings - 768 dimensions)
VECTOR_SIZE = 768


def get_qdrant_client() -> QdrantClient:
    """
    Get a Qdrant client instance.
    
    Returns:
        QdrantClient instance
    """
    if QDRANT_API_KEY:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=60
        )
    else:
        client = QdrantClient(
            url=QDRANT_URL,
            timeout=60
        )
    
    return client


def init_qdrant_collection(client: QdrantClient = None) -> bool:
    """
    Initialize the textbook collection in Qdrant.
    Creates the collection if it doesn't exist.
    
    Args:
        client: Optional Qdrant client (creates one if not provided)
    
    Returns:
        True if successful, False otherwise
    """
    if client is None:
        client = get_qdrant_client()
    
    try:
        # Check if collection exists
        collections = client.get_collections().collections
        collection_exists = any(col.name == TEXTBOOK_COLLECTION for col in collections)
        
        if not collection_exists:
            # Create collection
            client.create_collection(
                collection_name=TEXTBOOK_COLLECTION,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                ),
                hnsw_config={
                    "m": 16,
                    "ef_construct": 100
                }
            )
            print(f"✅ Created collection: {TEXTBOOK_COLLECTION}")
        else:
            print(f"✓ Collection already exists: {TEXTBOOK_COLLECTION}")
        
        return True
    except Exception as e:
        print(f"❌ Error initializing Qdrant collection: {e}")
        return False


def check_qdrant_connection() -> dict:
    """
    Check Qdrant connection status.
    
    Returns:
        Dict with connection status and info
    """
    try:
        client = get_qdrant_client()
        collections = client.get_collections()
        
        return {
            "status": "connected",
            "collections_count": len(collections.collections),
            "collections": [col.name for col in collections.collections]
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e)
        }


# Convenience function for getting a ready-to-use client
def get_vector_store():
    """
    Get a configured Qdrant client with initialized collection.
    
    Returns:
        Tuple of (client, success_message) or (None, error_message)
    """
    try:
        client = get_qdrant_client()
        success = init_qdrant_collection(client)
        
        if success:
            return client, "Qdrant connection established"
        else:
            return None, "Failed to initialize Qdrant collection"
    except Exception as e:
        return None, f"Qdrant connection error: {str(e)}"
