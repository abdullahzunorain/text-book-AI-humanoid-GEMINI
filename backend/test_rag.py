"""
Test script for RAG components.
Tests embeddings generation and vector search functionality.

Usage:
    python test_rag.py --query "your test query"
"""
import argparse
from vector_store import get_qdrant_client, check_qdrant_connection
from embeddings import get_embedding, get_embedding_dimension
from crud_vectors import search_textbook_content, get_collection_stats


def test_embeddings():
    """
    Test embedding generation.
    """
    print("\n🧪 Testing Embeddings Generation...")
    
    test_queries = [
        "What is ROS 2?",
        "How to create a node in Python?",
        "Explain digital twin simulation"
    ]
    
    for query in test_queries:
        try:
            embedding = get_embedding(query)
            print(f"   ✓ '{query}'")
            print(f"      Dimension: {len(embedding)}")
            print(f"      First 5 values: {[round(v, 4) for v in embedding[:5]]}")
        except Exception as e:
            print(f"   ❌ '{query}' - Error: {e}")
            return False
    
    return True


def test_qdrant_connection():
    """
    Test Qdrant connection.
    """
    print("\n🧪 Testing Qdrant Connection...")
    
    status = check_qdrant_connection()
    
    if status["status"] == "connected":
        print(f"   ✓ Connected to Qdrant")
        print(f"   Collections: {status.get('collections_count', 0)}")
        for col in status.get("collections", []):
            print(f"      - {col}")
        return True
    else:
        print(f"   ❌ Connection failed: {status.get('error', 'Unknown error')}")
        return False


def test_vector_search(query: str = None):
    """
    Test vector search functionality.
    
    Args:
        query: Search query (optional)
    """
    print("\n🧪 Testing Vector Search...")
    
    if not query:
        query = "What is ROS 2?"
    
    print(f"   Query: '{query}'")
    
    try:
        client = get_qdrant_client()
        
        # Get collection stats
        stats = get_collection_stats(client)
        if stats["status"] == "ok":
            print(f"   Collection stats:")
            print(f"      Vectors: {stats.get('vectors_count', 0)}")
            print(f"      Points: {stats.get('points_count', 0)}")
        
        if stats.get("vectors_count", 0) == 0:
            print(f"   ⚠️  No vectors in collection. Run ingest_textbook.py first.")
            return True
        
        # Perform search
        results = search_textbook_content(
            client=client,
            query=query,
            limit=3
        )
        
        if not results:
            print(f"   ⚠️  No results found")
            return True
        
        print(f"   ✓ Found {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"\n   Result {i} (score: {result['score']:.4f}):")
            print(f"      Chapter: {result['chapter_title']}")
            print(f"      Module: {result['module_name']}")
            print(f"      Text: {result['text'][:200]}...")
        
        return True
    
    except Exception as e:
        print(f"   ❌ Search failed: {e}")
        return False


def main():
    """
    Run all tests.
    """
    parser = argparse.ArgumentParser(description="Test RAG components")
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Custom search query for testing"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RAG Component Tests")
    print("=" * 60)
    
    # Test embeddings
    embeddings_ok = test_embeddings()
    
    # Test Qdrant connection
    qdrant_ok = test_qdrant_connection()
    
    # Test vector search
    search_ok = test_vector_search(args.query)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"   Embeddings: {'✅ PASS' if embeddings_ok else '❌ FAIL'}")
    print(f"   Qdrant Connection: {'✅ PASS' if qdrant_ok else '❌ FAIL'}")
    print(f"   Vector Search: {'✅ PASS' if search_ok else '❌ FAIL'}")
    
    all_ok = embeddings_ok and qdrant_ok and search_ok
    print(f"\n   Overall: {'✅ ALL TESTS PASSED' if all_ok else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
