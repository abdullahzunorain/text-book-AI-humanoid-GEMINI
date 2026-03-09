"""
Test script for RAG components (manual/integration use).
Not part of the automated pytest suite — requires live API keys.

Usage:
    cd backend && uv run python tests/test_rag.py --query "your test query"
"""
import argparse
import sys

from src.services.vector_store import get_qdrant_client
from src.services.embeddings import get_embedding
from src.db.crud_vectors import search_textbook_content, get_collection_stats


def test_embeddings():
    print("\nTesting Embeddings Generation...")
    test_queries = [
        "What is ROS 2?",
        "How to create a node in Python?",
        "Explain digital twin simulation",
    ]
    for query in test_queries:
        try:
            embedding = get_embedding(query)
            print(f"  OK '{query}' dim={len(embedding)}")
        except Exception as e:
            print(f"  FAIL '{query}' - {e}")
            return False
    return True


def test_qdrant_connection():
    print("\nTesting Qdrant Connection...")
    client = get_qdrant_client()
    if not client:
        print("  FAIL: could not create client")
        return False
    try:
        cols = client.get_collections()
        print(f"  OK: {len(cols.collections)} collections")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_vector_search(query: str = "What is ROS 2?"):
    print(f"\nTesting Vector Search: '{query}'")
    client = get_qdrant_client()
    if not client:
        print("  SKIP: no Qdrant client")
        return True

    stats = get_collection_stats(client)
    if stats.get("vectors_count", 0) == 0:
        print("  SKIP: no vectors in collection")
        return True

    results = search_textbook_content(client=client, query=query, limit=3)
    print(f"  OK: {len(results)} results")
    for i, r in enumerate(results, 1):
        print(f"    [{i}] score={r['score']:.4f} chapter={r['chapter_title']}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Test RAG components")
    parser.add_argument("--query", type=str, default=None)
    args = parser.parse_args()

    ok_embed = test_embeddings()
    ok_qdrant = test_qdrant_connection()
    ok_search = test_vector_search(args.query or "What is ROS 2?")

    all_ok = ok_embed and ok_qdrant and ok_search
    print(f"\nOverall: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
