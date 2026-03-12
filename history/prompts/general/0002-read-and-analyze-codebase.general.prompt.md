---
id: 2
title: Read and Analyze Codebase
stage: general
date: 2026-03-04
surface: agent
model: gemini-2.0-flash
feature: none
branch: main
user: zunorain
command: "pls read the whole code base"
labels: ["discovery", "architecture", "code-review"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/main.py
  - backend/rag_service.py
  - frontend/src/components/Chat/Chat.tsx
  - backend/models.py
  - backend/vector_store.py
tests_yaml: |
  - none
---

# Prompt
pls read the whole code base

# Response
I analyzed the codebase using `codebase_investigator` and manual file reads. The project is a RAG-powered AI assistant for a robotics textbook. 

Key findings:
1. **Backend:** FastAPI with Neon (PostgreSQL) and Qdrant (Vector DB). Uses Gemini API for RAG.
2. **Frontend:** Docusaurus with a custom React Chat component that supports "selected text" context.
3. **Services:** `RAGService` handles context retrieval and LLM interaction. `ingest_textbook.py` manages the data pipeline.
4. **Architecture:** Clean separation of concerns with standard CRUD patterns for both relational and vector data.

The project is ready for further development or feature enhancement.
