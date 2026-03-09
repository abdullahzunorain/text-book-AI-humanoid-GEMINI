"""
CRUD operations for vector store (Qdrant).
Handles textbook content indexing and retrieval.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime

from src.services.vector_store import get_qdrant_client, TEXTBOOK_COLLECTION
from src.services.embeddings import get_embedding


def upsert_textbook_segment(
    client: QdrantClient,
    text: str,
    chapter_title: str,
    module_name: str,
    url: str,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Upsert a textbook segment into the vector store.
    
    Args:
        client: Qdrant client
        text: Text content of the segment
        chapter_title: Title of the chapter
        module_name: Name of the module
        url: URL/Path to the content
        metadata: Additional metadata (optional)
    
    Returns:
        Point ID of the upserted segment
    """
    # Generate embedding
    embedding = get_embedding(text)
    
    # Create metadata payload
    payload = {
        "text": text,
        "chapter_title": chapter_title,
        "module_name": module_name,
        "url": url,
        "created_at": datetime.utcnow().isoformat(),
        **(metadata or {})
    }
    
    # Generate unique ID
    point_id = str(uuid.uuid4())
    
    # Create point
    point = PointStruct(
        id=point_id,
        vector=embedding,
        payload=payload
    )
    
    # Upsert to Qdrant
    client.upsert(
        collection_name=TEXTBOOK_COLLECTION,
        points=[point]
    )
    
    return point_id


def upsert_textbook_segments_batch(
    client: QdrantClient,
    segments: List[Dict[str, Any]]
) -> List[str]:
    """
    Upsert multiple textbook segments in batch.
    
    Args:
        client: Qdrant client
        segments: List of segment dicts with keys:
            - text: str
            - chapter_title: str
            - module_name: str
            - url: str
            - metadata: Dict (optional)
    
    Returns:
        List of point IDs
    """
    points = []
    point_ids = []
    
    for segment in segments:
        # Generate embedding
        embedding = get_embedding(segment["text"])
        
        # Create metadata payload
        payload = {
            "text": segment["text"],
            "chapter_title": segment["chapter_title"],
            "module_name": segment["module_name"],
            "url": segment["url"],
            "created_at": datetime.utcnow().isoformat(),
            **(segment.get("metadata", {}))
        }
        
        # Generate unique ID
        point_id = str(uuid.uuid4())
        point_ids.append(point_id)
        
        # Create point
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload=payload
        )
        points.append(point)
    
    # Upsert batch to Qdrant
    client.upsert(
        collection_name=TEXTBOOK_COLLECTION,
        points=points
    )
    
    return point_ids


def search_textbook_content(
    client: QdrantClient,
    query: str,
    limit: int = 5,
    module_filter: Optional[str] = None,
    score_threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Search textbook content using semantic search.
    
    Args:
        client: Qdrant client
        query: Search query text
        limit: Maximum number of results
        module_filter: Optional module name to filter by
        score_threshold: Minimum similarity score
    
    Returns:
        List of search results with scores and metadata
    """
    # Generate query embedding
    query_embedding = get_embedding(query)
    
    # Build filter if module specified
    search_filter = None
    if module_filter:
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="module_name",
                    match=MatchValue(value=module_filter)
                )
            ]
        )
    
    # Search using query_points (qdrant-client v1.12+)
    query_response = client.query_points(
        collection_name=TEXTBOOK_COLLECTION,
        query=query_embedding,
        query_filter=search_filter,
        limit=limit,
        score_threshold=score_threshold,
    )

    # Format results
    formatted_results = []
    for result in query_response.points:
        formatted_results.append({
            "score": result.score,
            "text": result.payload.get("text", ""),
            "chapter_title": result.payload.get("chapter_title", ""),
            "module_name": result.payload.get("module_name", ""),
            "url": result.payload.get("url", ""),
            "metadata": {k: v for k, v in result.payload.items() 
                        if k not in ["text", "chapter_title", "module_name", "url"]}
        })
    
    return formatted_results


def get_segment_by_id(
    client: QdrantClient,
    point_id: str
) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific segment by its ID.
    
    Args:
        client: Qdrant client
        point_id: Point ID to retrieve
    
    Returns:
        Segment data or None if not found
    """
    points = client.retrieve(
        collection_name=TEXTBOOK_COLLECTION,
        ids=[point_id],
        with_payload=True,
        with_vectors=False
    )
    
    if not points:
        return None
    
    point = points[0]
    return {
        "id": point.id,
        "text": point.payload.get("text", ""),
        "chapter_title": point.payload.get("chapter_title", ""),
        "module_name": point.payload.get("module_name", ""),
        "url": point.payload.get("url", ""),
        "metadata": {k: v for k, v in point.payload.items() 
                    if k not in ["text", "chapter_title", "module_name", "url"]}
    }


def delete_segment(
    client: QdrantClient,
    point_id: str
) -> bool:
    """
    Delete a segment by its ID.
    
    Args:
        client: Qdrant client
        point_id: Point ID to delete
    
    Returns:
        True if deleted, False otherwise
    """
    try:
        client.delete(
            collection_name=TEXTBOOK_COLLECTION,
            points_selector=[point_id]
        )
        return True
    except Exception:
        return False


def get_collection_stats(client: QdrantClient) -> Dict[str, Any]:
    """
    Get statistics about the textbook collection.
    
    Args:
        client: Qdrant client
    
    Returns:
        Dictionary with collection statistics
    """
    try:
        info = client.get_collection(TEXTBOOK_COLLECTION)
        
        return {
            "status": "ok",
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "indexed_vectors_count": info.indexed_vectors_count
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def clear_collection(client: QdrantClient) -> bool:
    """
    Clear all points from the collection.
    
    Args:
        client: Qdrant client
    
    Returns:
        True if successful
    """
    try:
        client.clear_payload(
            collection_name=TEXTBOOK_COLLECTION
        )
        return True
    except Exception:
        return False
