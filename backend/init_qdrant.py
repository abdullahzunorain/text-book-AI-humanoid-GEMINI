"""
Qdrant initialization script.
Sets up the vector database collection for textbook content.

Usage:
    python init_qdrant.py
"""
from vector_store import get_qdrant_client, init_qdrant_collection, check_qdrant_connection
from crud_vectors import get_collection_stats


def init_qdrant():
    """
    Initialize Qdrant vector database.
    """
    print("🔧 Initializing Qdrant vector database...")
    
    # Check connection
    connection_status = check_qdrant_connection()
    
    if connection_status["status"] != "connected":
        print(f"❌ Error: Could not connect to Qdrant")
        print(f"   Error: {connection_status.get('error', 'Unknown error')}")
        print("\nPlease check your QDRANT_URL and QDRANT_API_KEY in .env file")
        return False
    
    print(f"✅ Connected to Qdrant")
    print(f"   Existing collections: {connection_status.get('collections_count', 0)}")
    
    # Initialize textbook collection
    client = get_qdrant_client()
    success = init_qdrant_collection(client)
    
    if not success:
        print("❌ Failed to initialize textbook collection")
        return False
    
    # Get collection stats
    stats = get_collection_stats(client)
    
    if stats["status"] == "ok":
        print(f"\n📊 Collection Statistics:")
        print(f"   Vectors: {stats.get('vectors_count', 0)}")
        print(f"   Points: {stats.get('points_count', 0)}")
    
    print("\n✅ Qdrant initialization complete!")
    return True


if __name__ == "__main__":
    import sys
    success = init_qdrant()
    sys.exit(0 if success else 1)
