"""
Qdrant vector database configuration and client.
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
TEXTBOOK_COLLECTION = os.getenv("QDRANT_COLLECTION_NAME", "textbook_chunks")

# ADR-001: Vector dimension synchronized to 768 for gemini-embedding-001
VECTOR_SIZE = 768
DISTANCE_METRIC = Distance.COSINE

def get_qdrant_client():
    """
    Initialize and return a Qdrant client.
    """
    if not QDRANT_URL:
        return None
    
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        return client
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return None

def init_collection(client: QdrantClient):
    """
    Ensure the textbook collection exists with correct parameters.
    """
    try:
        collections = client.get_collections().collections
        exists = any(c.name == TEXTBOOK_COLLECTION for c in collections)
        
        if not exists:
            client.create_collection(
                collection_name=TEXTBOOK_COLLECTION,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=DISTANCE_METRIC
                ),
            )
            return True, f"Collection '{TEXTBOOK_COLLECTION}' created."
        else:
            # Check if dimensions match
            collection_info = client.get_collection(TEXTBOOK_COLLECTION)
            current_size = collection_info.config.params.vectors.size
            if current_size != VECTOR_SIZE:
                return False, f"Collection exists but has wrong dimension ({current_size} != {VECTOR_SIZE}). Re-creation required."
            
            return True, f"Collection '{TEXTBOOK_COLLECTION}' already exists."
    except Exception as e:
        return False, f"Error initializing Qdrant collection: {str(e)}"
