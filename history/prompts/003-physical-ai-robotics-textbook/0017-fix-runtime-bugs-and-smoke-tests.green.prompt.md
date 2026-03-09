---
id: "0017"
title: "Fix Runtime Bugs and Smoke Tests"
stage: green
date: 2026-03-09
surface: agent
model: claude-opus-4-6
feature: 003-physical-ai-robotics-textbook
branch: 003-physical-ai-robotics-textbook
user: zunorain
command: /sp.implement
labels: ["bugfix", "smoke-test", "database", "qdrant", "embeddings"]
links:
  spec: specs/003-physical-ai-robotics-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/db/database.py
  - backend/src/db/init_db.py
  - backend/src/db/crud_vectors.py
  - backend/src/services/embeddings.py
  - backend/src/api/chat.py
  - backend/.env
  - specs/003-physical-ai-robotics-textbook/tasks.md
tests:
  - backend/tests/test_auth.py (4 PASS)
  - backend/tests/test_chat.py (3 PASS)
  - backend/tests/test_health.py (2 PASS)
  - backend/tests/test_rag.py (3 PASS)
  - backend/tests/test_users.py (3 PASS)
---

## Prompt

/sp.implement (no user input — resume implementation, fix runtime bugs discovered during smoke testing)

## Response snapshot

Fixed 4 critical runtime bugs preventing the backend from starting and serving live requests:

1. **init_db.py import error**: Changed `from src.models import user, message` to `from src.models.models import User, Message, UserContext` — old modules were renamed to .bak in previous session.

2. **asyncpg sslmode error**: Neon connection string contains `sslmode=require&channel_binding=require` which asyncpg doesn't accept as URL params. Added URL parsing in database.py to strip these params and pass SSL via `connect_args={"ssl": ssl_context}`. Guarded with `"asyncpg" in DATABASE_URL` to avoid mangling SQLite test URLs.

3. **Qdrant client.search() removed**: qdrant-client v1.12+ replaced `search()` with `query_points()`. Updated `crud_vectors.py` to use `client.query_points()` with `query_response.points` iteration.

4. **Embedding dimension mismatch**: `gemini-embedding-001` defaults to 3072 dimensions but Qdrant collection uses 768. Added `output_dimensionality=EMBEDDING_DIMENSIONS` (default 768) to all `embed_content` calls.

Smoke test results:
- GET /health: `{"status":"ok","database":"connected","vector_store":"connected"}`
- POST /users/: Created user id=24 in Neon
- GET /users/24 + GET /users/lookup?email=: Both return correct data
- POST /chat/: Gemini API returns 429 (quota exhausted) — graceful degradation working correctly
- All 15 pytest tests pass, frontend builds clean

## Outcome

- Impact: Backend fully starts, connects to Neon + Qdrant, serves all endpoints. RAG pipeline blocked only by Gemini quota (not code bugs).
- Tests: 15/15 PASS
- Files: 6 files modified, 1 task file updated
- Next prompts: Wait for Gemini quota reset, then re-run T022/T031 live chat test; deploy to Render
- Reflection: Runtime bugs only surface when connecting to live services (Neon, Qdrant Cloud, Gemini). Unit tests with mocks passed but masked 4 integration issues.

## Evaluation notes (flywheel)

- Failure modes observed: Module-level code in database.py runs at import time — URL parsing must handle both asyncpg (production) and aiosqlite (test) URLs gracefully.
- Graders run and results (PASS/FAIL): pytest 15/15 PASS, smoke tests 4/5 PASS (1 blocked by quota)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add integration test that validates database.py URL parsing for both asyncpg and aiosqlite URL formats
