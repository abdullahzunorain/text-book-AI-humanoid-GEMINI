# ADR-003: Textbook Content Structure for RAG

**Status**: Accepted  
**Date**: 2026-03-05

## Context
The "Physical AI & Humanoid Robotics" course covers 4 modules over 13 weeks. The structure affects both user navigation and the granularity of RAG context retrieval.

## Decision
We will implement a **Module-based Landing Page + 13 Weekly Sub-pages** (Option C).

## Rationale
- Provides a clear hierarchical structure for students.
- Weekly chapters (approx. 2000-5000 words each) provide ideal chunk sizes for RAG ingestion.
- Docusaurus sidebars can easily represent this 4x13 hierarchy.
- Metadata (chapter, module) can be easily attached to Qdrant payloads for granular citations.

## Consequences
- The `docs/` directory will be organized into 4 module folders.
- Each module folder will contain an `index.md` and weekly `.md` chapters.
- RAG ingestion script must be configured to process this structure.
