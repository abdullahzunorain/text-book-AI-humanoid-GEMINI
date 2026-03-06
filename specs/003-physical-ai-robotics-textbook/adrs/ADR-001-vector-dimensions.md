# ADR-001: Vector Dimension Synchronization

**Status**: Accepted  
**Date**: 2026-03-05

## Context
The codebase had a discrepancy between the vector dimension defined in `vector_store.py` (3072) and the embedding model used in `embeddings.py` (`gemini-embedding-001`, which outputs 768 dimensions). This would lead to failed upsert operations in Qdrant.

## Decision
We will synchronize the vector dimension to **768** across the entire stack to ensure compatibility with the `gemini-embedding-001` model.

## Rationale
- `gemini-embedding-001` is the mandated embedding model for the Flash model family.
- 768 dimensions provide sufficient semantic depth for textbook content while minimizing storage and latency in the Qdrant free tier.

## Consequences
- Qdrant collection must be initialized with `size=768`.
- Any existing collection with 3072 dimensions must be recreated.
