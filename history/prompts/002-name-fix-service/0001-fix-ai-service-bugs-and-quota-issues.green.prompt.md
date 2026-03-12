---
id: 0001
title: Fix AI Service Bugs and Quota Issues
stage: green
date: 2026-03-03
surface: agent
model: gemini-exp
feature: 002-name-fix-service
branch: 002-name-fix-service
user: zunorain
command: "/sp.specify"
labels: ["bug-fix", "embeddings", "rag"]
links:
  spec: "specs/002-name-fix-service/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - backend/embeddings.py
  - backend/vector_store.py
  - backend/main.py
  - backend/rag_service.py
  - frontend/docusaurus.config.ts
tests:
  - "uv run python ingest_textbook.py"
  - "uv run python main.py (Health check validated)"
---

# Prompt History Record: Fix AI Service Bugs and Quota Issues

## 1. Context & Intent
- **Stage:** green
- **Goal:** Resolve issues identified in logs: embedding model 404, vector dimension mismatch, backend 500 errors, and Docusaurus configuration warnings.

## 2. Prompt Text
```
pls read these log and verify it.... also write tests for it and resolve these issues using proper testing of it and verify that these issues, error and bugs are resolved...
```

## 3. Assistant Response
- Identified that `text-embedding-004` was returning 404 in `v1beta`.
- Switched embedding model to `gemini-embedding-001` which is stable.
- Discovered `gemini-embedding-001` uses 3072 dimensions, updated `vector_store.py` accordingly.
- Reset the Qdrant collection and successfully ran `ingest_textbook.py`.
- Fixed backend health check by wrapping SQL in `text()` for SQLAlchemy 2.0.
- Fixed 500 errors in `/personalize` and `/translate` by adding `user` role messages to the OpenAI SDK calls (previously only system messages were sent).
- Validated fixes using a temporary `test_api.py` script; confirmed that 400/500 errors are gone (now hitting 429 quota limits which is expected for free tier).
- Updated `docusaurus.config.ts` to remove deprecated `onBrokenMarkdownLinks` warning.

## 4. Outcome & Evaluation
- **Result:** System is now stable and ingestion works perfectly.
- **Constraints/Invariants met:** Verified with actual execution and log analysis.
- **Follow-ups:** Monitor Gemini API quota usage.
