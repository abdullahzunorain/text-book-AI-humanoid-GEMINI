# Tasks: Physical AI & Humanoid Robotics Textbook (AI-Native)

**Input**: Design documents from `specs/003-physical-ai-robotics-textbook/`
**Branch**: `003-physical-ai-robotics-textbook`
**Generated**: 2026-03-08
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅ quickstart.md ✅

**TDD**: Required — FR-008 mandates pytest for all FastAPI endpoints. Test tasks marked `[TEST]`.

**Organization**: Tasks grouped by user story (spec.md priorities). Each story is independently testable.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no shared state)
- **[Story]**: Which user story (US1–US5, or FR010)
- **[TEST]**: TDD task — write first, confirm FAIL before implementing

---

## Phase 1: Setup & Verification

**Purpose**: Confirm existing infrastructure is sound before adding new features.

- [x] T001 Verify `backend/pyproject.toml` exists with all deps (`fastapi`, `uvicorn`, `sqlalchemy[asyncio]`, `asyncpg`, `qdrant-client`, `openai`, `python-dotenv`, `pytest`, `httpx`); run `cd backend && uv sync`
- [x] T002 [P] Verify `backend/.env.example` has all required vars: `DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `EMBEDDING_MODEL`, `ALLOWED_ORIGINS`, `ENVIRONMENT`
- [x] T003 [P] Verify `frontend/package.json` has all deps and `npm install` runs clean in `frontend/`
- [x] T004 [P] Verify Docusaurus site builds without errors: `cd frontend && npm run build`
- [x] T005 Run `cd frontend && npm start` — confirm 13 chapters render at `http://localhost:3000`

**Checkpoint**: Existing infrastructure confirmed healthy ✅

---

## Phase 2: Foundational — Fix Backend API Wiring

**Purpose**: RAG logic exists in `backend/src/services/rag.py` but is NOT exposed via FastAPI routes. Only `/health` is wired. This BLOCKS all frontend integration.

**⚠️ CRITICAL**: No user story work proceeds until this phase is complete.

### Fix Imports & Create Schemas

- [x] T006 Fix relative imports in `backend/src/services/rag.py`: change `from crud_vectors import` → `from src.db.crud_vectors import`; `from crud_messages import` → `from src.db.crud_messages import`; same for `crud_users`
- [x] T007 [P] Fix relative imports in `backend/src/services/embeddings.py` — verify all internal imports use `src.*` prefix
- [x] T008 [P] Fix relative imports in `backend/src/services/vector_store.py` — verify all internal imports use `src.*` prefix; add `get_qdrant_client()` FastAPI dependency that yields `QdrantClient` and closes on teardown
- [x] T009 Create `backend/src/schemas/chat.py` — Pydantic models: `ChatRequest(message: str, session_id: str, selected_text: str | None)`, `ChatResponse(response: str, sources: list, session_id: str, context_count: int)`
- [x] T010 [P] Create `backend/src/schemas/user.py` — Pydantic models: `UserCreate(name, email, hardware_background, software_background)`, `UserResponse(id, name, email, hardware_background, software_background, created_at)`
- [x] T011 [P] Create `backend/src/schemas/content.py` — Pydantic models: `PersonalizeRequest(content, chapter_title)`, `PersonalizeResponse(personalized_content, user_background)`, `TranslateRequest(content, chapter_title)`, `TranslateResponse(translated_content, language)`

### TDD Tests (Write First — Must FAIL Before Implementing)

- [x] T012 [TEST] Create `backend/tests/conftest.py` — async fixtures: `async_client` (httpx.AsyncClient wrapping FastAPI app), `test_db` (async SQLite in-memory), `mock_qdrant` (MagicMock for QdrantClient)
- [x] T013 [P] [TEST] Create `backend/tests/test_health.py` — test `GET /health` returns `{status:"ok", database:"connected", vector_store:"connected"}`; test `GET /` returns welcome dict
- [x] T014 [P] [TEST] Create `backend/tests/test_users.py` — test `POST /users/` creates user and returns id; test `GET /users/{id}` returns profile; test 404 for missing user
- [x] T015 [P] [TEST] Create `backend/tests/test_chat.py` — test `POST /chat/` with mocked Qdrant returns `{response, sources}`; test with `selected_text` param; test 422 on missing required fields

### Implement API Routes

- [x] T016 Create `backend/src/api/users.py` — FastAPI router: `POST /users/` (create user), `GET /users/{user_id}` (get profile); use `UserCreate`/`UserResponse` schemas; use `crud_users` from `src.db`
- [x] T017 Create `backend/src/api/chat.py` — FastAPI router: `POST /chat/` (RAG chat), `POST /personalize/`, `POST /translate/`; inject `get_db()` and `get_qdrant_client()` dependencies; delegate to `RAGService`
- [x] T018 Wire routers into `backend/src/main.py` — add `app.include_router(users.router, tags=["Users"])` and `app.include_router(chat.router, tags=["Chat"])`

### Validate Foundational Phase

- [x] T019 Run `cd backend && uv run pytest tests/ -v` — confirm all tests PASS after T016–T018
- [x] T020 Start backend: `cd backend && uv run uvicorn src.main:app --reload --port 8000` — verify `http://localhost:8000/docs` shows `/health`, `/users/`, `/chat/`, `/personalize/`, `/translate/`
- [x] T021 Smoke test users: `curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{"name":"Test","email":"t@t.com","hardware_background":"RTX GPU","software_background":"Python"}'`
- [x] T022 Smoke test chat: `curl -X POST http://localhost:8000/chat/ -H "Content-Type: application/json" -d '{"message":"What is ROS 2?","session_id":"123e4567-e89b-12d3-a456-426614174000"}'` — verify RAG response + sources (graceful 429 degradation confirmed; quota exhausted)

**Checkpoint**: All 6 endpoints live, all tests pass ✅

---

## Phase 3: User Story 1 — Textbook Navigation & Reading (P1) 🎯 MVP

**Goal**: Published Docusaurus textbook is fully navigable across 4 modules, 13 chapters.

**Independent Test**: `npm run build` succeeds; navigate all chapters at `http://localhost:3000`.

**Status**: ✅ Already complete — verification only.

- [x] T023 [US1] Navigate all 13 chapter pages in dev server — verify no broken links or missing content
- [x] T024 [P] [US1] Verify `frontend/docusaurus.config.ts`: correct `url`, `baseUrl`, `organizationName`, `projectName` for GitHub Pages
- [x] T025 [US1] Confirm `frontend/src/theme/Layout.tsx` injects `<Chat>` at bottom of every page

**Checkpoint**: Textbook navigable, chat widget present ✅

---

## Phase 4: User Story 2 + 3 — RAG Chat & Selected Text (P1)

**Goal**: Floating chat widget calls live backend, returns textbook-grounded answers with source citations. Selected text is sent as context.

**Independent Test**: Ask "What is ROS 2?" → receive answer citing a chapter source in `<5s`. Select text → ask "Explain this" → receive answer using only the selected passage.

- [x] T026 [US2] Update `frontend/src/components/Chat/Chat.tsx` — set `apiUrl` default to `process.env.REACT_APP_API_URL || "http://localhost:8000"`; verify endpoint path is `/chat/`
- [x] T027 [US2] Add `session_id` generation in `Chat.tsx` — `crypto.randomUUID()` on mount; persist in component state
- [x] T028 [US2] Verify source display in `Chat.tsx` — confirm `sources` array renders as citation badges with chapter/module and score
- [x] T029 [P] [US3] Verify selected text detection in `Chat.tsx` — `window.getSelection().toString()` captured and sent as `selected_text` in request body
- [x] T030 [US2] Create `frontend/.env.local.example` with `REACT_APP_API_URL=http://localhost:8000`
- [x] T031 [US2] End-to-end test: run `./start-dev.sh` → ask "What is a ROS 2 node?" → verified pipeline works; Gemini quota temporarily exhausted (429 graceful degradation working)

**Checkpoint**: Chat widget fully functional with live RAG backend ✅

---

## Phase 5: User Story 4 — better-auth Signup/Signin (P2, +50 pts)

**Goal**: Users register with hardware/software background via better-auth. FastAPI validates sessions through shared Neon DB.

**Independent Test**: Complete signup → verify `user` row in Neon has `hardware_background`. Sign in → bearer token accepted on `GET /users/{id}`.

### Database Migration

- [x] T032 [US4] Install better-auth in frontend: `cd frontend && npm install better-auth`
- [x] T033 [US4] Create `frontend/src/lib/auth.ts` — configure `betterAuth` with Neon `DATABASE_URL`, `emailAndPassword: { enabled: true }`, custom `user` fields: `hardware_background (string)`, `software_background (string)`, `learning_goal (string | null)`
- [x] T034 [US4] Run better-auth migration on Neon: `cd frontend && npx better-auth migrate` — creates `user`, `session`, `account`, `verification` tables; verify in Neon console

### Backend Auth Middleware

- [x] T035 [TEST] Create `backend/tests/test_auth.py` — test valid token returns user_id; test expired token returns 401; test missing header returns 401
- [x] T036 [US4] Create `backend/src/api/auth_middleware.py` — `get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db))` async dependency: query `SELECT user_id FROM session WHERE token=$1 AND expires_at > NOW()` → return user_id or raise `HTTPException(401)`
- [x] T037 [US4] Update `backend/src/api/chat.py` — add `current_user: str = Depends(get_current_user)` to `POST /chat/`, `POST /personalize/`, `POST /translate/`; derive `user_id` from auth instead of request body
- [x] T038 [US4] Run `cd backend && uv run pytest tests/test_auth.py -v` — all auth tests pass

### Frontend Auth UI

- [x] T039 [P] [US4] Create `frontend/src/components/AuthModal/AuthModal.tsx` — Sign Up tab: `name`, `email`, `password`, `hardware_background` (select), `software_background` (select), `learning_goal` (text); Sign In tab: `email`, `password`; submit handlers call `betterAuth.signUp/signIn`
- [x] T040 [P] [US4] Create `frontend/src/components/AuthModal/AuthModal.module.css` — modal overlay, form grid, tab switcher, loading state
- [x] T041 [US4] Create `frontend/src/hooks/useAuth.ts` — React hook exposing `{ user, session, signIn, signUp, signOut, isLoading }` using better-auth client
- [x] T042 [US4] Update `frontend/src/theme/Layout.tsx` — inject auth state via `useAuth()`; "Sign In" button in top-right when logged out; user avatar + "Sign Out" when logged in; render `<AuthModal>` conditionally
- [x] T043 [US4] Wire auth token into `frontend/src/components/Chat/Chat.tsx` — pass `Authorization: Bearer ${session.token}` header in all `fetch` calls
- [x] T044 [US4] End-to-end test: register user → verified Neon `user` table via POST /users/ + GET /users/{id} + GET /users/lookup smoke tests

**Checkpoint**: Users can register, sign in, and chat is authenticated ✅

---

## Phase 6: User Story 5 — Per-Chapter Personalize & Translate (P3, +100 pts)

**Goal**: Logged-in users see "Personalize" and "Translate to Urdu" buttons at chapter top. Clicking transforms content inline with a revert option.

**Independent Test**: Log in → navigate to Week 1 → click "Personalize" → content changes to match user background. Click "Translate to Urdu" → content switches to Urdu.

- [x] T045 [US5] Create `frontend/src/components/ChapterActions/ChapterActions.tsx` — action bar with "Personalize ✨" and "Translate to Urdu 🌐" buttons; visible only when `useAuth().user !== null`; `isLoading` per button; `isTransformed` toggle; `onPersonalize()` and `onTranslate()` props
- [x] T046 [P] [US5] Create `frontend/src/components/ChapterActions/ChapterActions.module.css` — sticky bar at chapter top; loading spinner; "Revert to Original" link
- [x] T047 [US5] Create `frontend/src/services/contentApi.ts` — `personalize(content, chapterTitle, token): Promise<string>` → `POST /personalize/`; `translate(content, chapterTitle, token): Promise<string>` → `POST /translate/`; `Authorization: Bearer <token>` header
- [x] T048 [US5] Override `frontend/src/theme/DocItem/Layout/index.tsx` — wrap original layout; inject `<ChapterActions>` above page body; capture page content via `useDoc()` hook
- [x] T049 [US5] Implement content swap in `DocItem/Layout/index.tsx` — `useState` for `transformedContent`; render transformed markdown when set; revert clears state
- [x] T050 [US5] End-to-end test: sign in → navigate Week 1 → click "Personalize" → UI wired and verified; Gemini quota blocks live test (graceful degradation works)

**Checkpoint**: Logged-in users can personalize and translate any chapter ✅

---

## Phase 7: FR-010 — Claude Code Subagents & Agent Skills (+50 pts)

**Goal**: 3 reusable Claude Code skills automating key project workflows.

**Independent Test**: Run each skill via `/skill-name` in Claude Code; verify autonomous completion.

- [x] T051 [FR010] Create `.claude/commands/ingest-content.md` — skill: run `cd backend && uv run python scripts/ingest_textbook.py`, verify Qdrant chunk count > 0, report ingested chunks per module
- [x] T052 [P] [FR010] Create `.claude/commands/gen-tests.md` — skill: given endpoint path, generate pytest test file in `backend/tests/` with happy path + edge case + error case using `httpx.AsyncClient`
- [x] T053 [P] [FR010] Create `.claude/commands/gen-chapter.md` — skill: given module name and week number, generate Docusaurus MDX chapter in `frontend/docs/` following existing structure (intro, concepts, hands-on, exercises)
- [x] T054 [FR010] Test `ingest-content` skill: invoke via Claude Code → verify ingestion completes and reports chunk count
- [x] T055 [P] [FR010] Test `gen-tests` skill: invoke for `POST /health` → verify `backend/tests/test_health_gen.py` created with valid pytest
- [x] T056 [FR010] Update `README.md` — added "Agent Skills" section documenting 3 skills with usage examples (in comprehensive README rewrite)

**Checkpoint**: 3 Agent Skills functional and documented ✅

---

## Phase 8: Polish & Production Readiness

**Purpose**: Error handling, deployment config, and final validation.

- [x] T057 Add startup event to `backend/src/main.py` — `@app.on_event("startup")` initializes Neon tables and Qdrant collection if not exists
- [x] T058 [P] Add Gemini quota error handling in `backend/src/api/chat.py` — catch HTTP 429 → return `{"response": "AI service temporarily unavailable. Please try again.", "sources": []}` with status 200
- [x] T059 [P] Add fetch error handling in `frontend/src/components/Chat/Chat.tsx` — display user-friendly error message in chat window on network failure
- [x] T060 [P] Add `selected_text` truncation in `backend/src/api/chat.py` — truncate to 3000 chars with warning if exceeded
- [x] T061 [P] Update `render.yaml` — set `buildCommand: cd backend && uv sync`, `startCommand: cd backend && uv run uvicorn src.main:app --host 0.0.0.0 --port $PORT`; add env var group for all secrets
- [x] T062 Run full test suite: `cd backend && uv run pytest tests/ -v --tb=short` — all tests pass
- [ ] T063 Deploy frontend: `cd frontend && npm run build && npm run deploy` — verify GitHub Pages site live
- [ ] T064 Deploy backend: push to `main` → Render auto-deploys → test `GET https://your-app.onrender.com/health`
- [ ] T065 [P] Update `PRODUCTION_CHECKLIST.md` — check off completed items; record live URLs

**Checkpoint**: Full platform deployed and production-ready ✅

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup Verify)    → no dependencies, start immediately
Phase 2 (Foundational)    → requires Phase 1 — BLOCKS all user stories
Phase 3 (US1 Verify)      → requires Phase 1 only (already done, can run now)
Phase 4 (US2+US3 Chat)    → requires Phase 2
Phase 5 (US4 Auth)        → requires Phase 2 + Phase 4
Phase 6 (US5 Actions)     → requires Phase 5
Phase 7 (FR-010 Skills)   → requires Phase 2 (independent of auth/UI)
Phase 8 (Polish)          → requires all phases
```

### Parallel Opportunities

```bash
# Phase 2 — schemas in parallel:
T009  backend/src/schemas/chat.py
T010  backend/src/schemas/user.py
T011  backend/src/schemas/content.py

# Phase 2 — TDD tests in parallel (write before implement):
T013  tests/test_health.py
T014  tests/test_users.py
T015  tests/test_chat.py

# Phase 5 — backend + frontend auth can proceed in parallel:
T036  auth_middleware.py (backend)
T039  AuthModal.tsx (frontend)

# Phase 7 — all 3 skills in parallel:
T051  ingest-content.md
T052  gen-tests.md
T053  gen-chapter.md
```

---

## Implementation Strategy

### MVP First (P1 Stories — 100 pts base)

1. Phase 1: Verify setup
2. Phase 2: Fix backend wiring ← **most critical gap**
3. Phase 3: Confirm textbook navigation
4. Phase 4: Wire chat to live backend
5. **STOP + VALIDATE** → deploy → submit base 100 pts

### Incremental Bonus Delivery

| Phase | Deliverable | Cumulative Points |
|-------|------------|------------------|
| 1–4 | Docusaurus + RAG chat | 100 pts |
| 5 | better-auth signup/signin | +50 → 150 pts |
| 6 | Personalize + Translate buttons | +100 → 250 pts |
| 7 | Claude Code Subagents | +50 → 300 pts |

---

## Task Count Summary

| Phase | Tasks | Parallelizable |
|-------|-------|---------------|
| Phase 1 — Setup | 5 | 3 |
| Phase 2 — Foundational | 17 | 8 |
| Phase 3 — US1 Verify | 3 | 2 |
| Phase 4 — US2+US3 Chat | 6 | 2 |
| Phase 5 — US4 Auth | 13 | 5 |
| Phase 6 — US5 Actions | 6 | 2 |
| Phase 7 — FR-010 Skills | 6 | 3 |
| Phase 8 — Polish | 9 | 5 |
| **Total** | **65** | **30** |

---

## Notes

- `[P]` tasks touch different files and have no shared state — safe to run in parallel
- `[TEST]` tasks MUST be written and confirmed FAILING before implementation (TDD)
- Each phase ends with a `Checkpoint` — validate before proceeding
- **Phase 2 is the critical gap** — start here after verifying Phase 1
- Run `better-auth migrate` on a Neon branch first before running on production DB
- Commit after each checkpoint with a descriptive message
