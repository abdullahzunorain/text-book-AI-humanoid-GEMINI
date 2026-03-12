# Tasks: End-to-End Testing & Bug Resolution

**Input**: Design documents from `specs/004-e2e-testing-bugfix/`
**Branch**: `004-e2e-testing-bugfix`
**Generated**: 2026-03-09
**Prerequisites**: plan.md ✅ spec.md ✅

**Tests**: Required — FR-013 mandates Playwright E2E tests; FR-015 mandates pytest passing.

**Organization**: Tasks grouped by user story (spec.md priorities). Each story is independently testable.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no shared state)
- **[Story]**: Which user story (US1–US4)
- **[TEST]**: Test task

---

## Phase 1: Setup & Environment Verification

**Purpose**: Confirm all services are running and dependencies are installed before testing.

- [x] T001 Verify `backend/.env` has all required vars: `DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY`, `GEMINI_API_KEY`, `EMBEDDING_MODEL`
- [x] T002 [P] Run `cd backend && uv sync` — verify all Python dependencies install cleanly
- [x] T003 [P] Run `cd frontend && npm install` — verify all Node dependencies install cleanly
- [x] T004 Run `cd backend && uv run python src/db/init_db.py` — verify database tables created successfully
- [x] T005 Run `cd backend && uv run pytest tests/ -v` — verify all 15 existing tests pass (15/15 PASS)
- [x] T006 Run `cd frontend && npm run build` — verify frontend builds with zero errors (SUCCESS)

**Checkpoint**: All dependencies installed, DB initialized, tests pass, frontend builds ✅

---

## Phase 2: Foundational — Install Playwright

**Purpose**: Playwright is NOT installed. This BLOCKS all browser E2E testing (US2).

- [x] T007 Install Playwright test runner: `cd frontend && npm install -D @playwright/test`
- [x] T008 Install Playwright browser binary: `cd frontend && npx playwright install chromium`
- [x] T009 Create `frontend/playwright.config.ts` — configure: `baseURL: 'http://localhost:3000'`, `headless: false`, `slowMo: 500`, screenshot on failure, `webServer` for both backend (port 8000) and frontend (port 3000)
- [x] T010 Create `frontend/e2e/` directory and verify Playwright runs with a minimal smoke test (navigate to `/`, assert page title)

**Checkpoint**: Playwright installed, configured non-headless, minimal test runs ✅

---

## Phase 3: User Story 1 — Backend API Endpoint Validation (P1)

**Goal**: All 7 FastAPI endpoints respond correctly to live HTTP requests with proper status codes, schemas, and error handling.

**Independent Test**: Start backend, issue curl requests to each endpoint, verify responses.

### Start Backend Server

- [x] T011 [US1] Start backend: `cd backend && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000` — verify `http://localhost:8000/docs` shows all endpoints

### Health & Root

- [x] T012 [US1] Test `GET /` — verify returns `{"message": "Welcome to the AI Humanoid Textbook API"}`
- [x] T013 [US1] Test `GET /health` — verify returns `{"status": "ok", "database": "connected", "vector_store": "connected"}`

### User Endpoints

- [x] T014 [US1] Test `POST /users/` with valid data `{"name":"Test","email":"e2e@test.com","hardware_background":"RTX GPU","software_background":"Python"}` — verify returns user with `id` field
- [x] T015 [P] [US1] Test `GET /users/{id}` with the created user ID — verify returns full user profile
- [x] T016 [P] [US1] Test `GET /users/lookup?email=e2e@test.com` — verify returns matching user
- [x] T017 [US1] Test `GET /users/lookup?email=nonexistent@test.com` — verify returns 404
- [x] T018 [US1] Test `GET /users/99999` — verify returns 404 for missing user
- [x] T019 [US1] Test `POST /users/` with missing required fields — verify returns 422

### Chat Endpoint

- [x] T020 [US1] Test `POST /chat/` with `{"message":"What is ROS 2?","session_id":"e2e-test-session"}` — verify returns response with `response`, `sources`, `session_id`, `context_count` fields
- [x] T021 [US1] Test `POST /chat/` with missing `message` field — verify returns 422
- [x] T022 [P] [US1] Test `POST /chat/` with `selected_text` parameter — verify selected text is used as context

### Content Endpoints

- [x] T023 [US1] Test `POST /personalize/` with `{"content":"ROS 2 is a robotics framework.","chapter_title":"Week 1"}` — verify returns personalized content or graceful 429 message
- [x] T024 [P] [US1] Test `POST /translate/` with `{"content":"ROS 2 is a robotics framework.","chapter_title":"Week 1"}` — verify returns translated content or graceful 429 message

### Auth Middleware

- [x] T025 [US1] Test `POST /chat/` with `Authorization: Bearer {user_id}` header — verify auth middleware accepts valid token
- [x] T026 [P] [US1] Test `POST /chat/` without auth header — verify falls back to anonymous user (no 401)

### Fix Any Bugs Found

- [x] T027 [US1] Bug found: POST /users/ accepted missing email (200 instead of 422). Fix: Made `email` required in UserCreate schema (schemas/user.py). Re-tested: 422 confirmed. pytest 15/15 PASS.

**Checkpoint**: All 7 endpoints validated with correct responses and error handling ✅

---

## Phase 4: User Story 2 — Frontend Browser Testing with Playwright (P1)

**Goal**: Playwright tests verify the complete user journey in a real non-headless browser.

**Independent Test**: Run `npx playwright test --headed` against running frontend+backend.

### Homepage & Navigation

- [x] T028 [US2] Create `frontend/e2e/homepage.spec.ts` — test: navigate to `/`, verify page title contains "Physical AI" or textbook name, verify at least 4 module links are visible
- [x] T029 [US2] Add navigation test in `homepage.spec.ts` — click first module link, verify chapter page loads with content

### Chat Widget

- [x] T030 [US2] Create `frontend/e2e/chat.spec.ts` — test: navigate to a chapter page, locate the chat widget toggle button, click to open chat panel
- [x] T031 [US2] Add chat interaction test — type "What is ROS 2?" in the chat input, press Enter, wait for response to appear in the chat window (or verify loading state appears)

### Authentication Flow

- [x] T032 [US2] Create `frontend/e2e/auth.spec.ts` — test: find and click "Sign In" button, verify authentication modal opens with two tabs (Sign In / Sign Up)
- [x] T033 [US2] Add sign up test — switch to Sign Up tab, fill in name, email (unique timestamp-based), password, select hardware and software backgrounds, submit form, verify user is logged in (Sign In button changes to user name + Sign Out)
- [x] T034 [US2] Add sign out + sign in test — click Sign Out, click Sign In, fill email and password in Sign In tab, submit, verify logged back in

### Chapter Actions (Auth-Gated)

- [x] T035 [US2] Create `frontend/e2e/actions.spec.ts` — test: while logged in, navigate to a chapter page, verify "Personalize" and "Translate to Urdu" buttons are visible
- [x] T036 [US2] Add personalize test — click "Personalize" button, verify loading state appears, wait for content change or graceful error message
- [x] T037 [US2] Add translate test — click "Translate to Urdu" button, verify loading state appears, wait for content change or graceful error message
- [x] T038 [US2] Add revert test — after content transformation, click "Revert to Original", verify original content is restored
- [x] T039 [US2] Add logged-out test — sign out, navigate to chapter page, verify Personalize and Translate buttons are NOT visible

### Fix Any Bugs Found

- [x] T040 [US2] Bugs found and fixed: (1) `process.env` not available in Docusaurus browser — replaced with hardcoded localhost in 4 files. (2) Playwright baseURL path resolution — changed `goto('/')` to `goto('./')`. (3) Auth modal tab persistence — explicitly click Sign In tab on re-open. (4) Duplicate email 500 error — added IntegrityError handler returning 409.

**Checkpoint**: Full user journey tested in non-headless browser ✅

---

## Phase 5: User Story 3 — Bug Resolution & Application Stability (P1)

**Goal**: All bugs found during testing are resolved. Application is fully stable.

- [x] T041 [US3] Run full backend test suite: `cd backend && uv run pytest tests/ -v` — confirm 15/15 pass after all fixes
- [x] T042 [P] [US3] Run frontend build: `cd frontend && npm run build` — confirm zero errors after all fixes
- [x] T043 [US3] Run full Playwright suite: `cd frontend && npx playwright test --headed` — confirm all 12 E2E tests pass
- [x] T044 [US3] Bug summary documented below and in plan.md
- [x] T045 [US3] Verify no regressions: pytest 15/15 PASS after all changes

**Checkpoint**: Zero critical bugs, all tests pass, application stable ✅

---

## Phase 6: User Story 4 — OpenAI SDK + Gemini Integration Verification (P2)

**Goal**: Confirm the AI service uses the OpenAI SDK with Gemini models through chat.completions.

- [x] T046 [US4] Verify `backend/src/services/rag.py` uses `from openai import OpenAI` and `chat.completions.create()` for RAG chat
- [x] T047 [P] [US4] Verify `backend/src/services/rag.py` uses `chat.completions.create()` for personalization
- [x] T048 [P] [US4] Verify `backend/src/services/rag.py` uses `chat.completions.create()` for translation
- [x] T049 [US4] Verify `backend/src/services/embeddings.py` uses `output_dimensionality=768` to match Qdrant collection
- [x] T050 [US4] Verify model name is configurable via `GEMINI_MODEL` env var (not hardcoded)
- [x] T051 [US4] Test graceful degradation: POST /chat/ returns "AI service temporarily unavailable" with status 200 when Gemini quota exhausted

**Checkpoint**: OpenAI SDK + Gemini integration verified and documented ✅

---

## Phase 7: Polish & Final Verification

**Purpose**: Full end-to-end verification and documentation.

- [x] T052 Run complete test execution workflow: pytest 15/15 PASS → all 7 API endpoints validated → frontend build SUCCESS → Playwright 12/12 PASS
- [x] T053 [P] Verify `.gitignore` includes `backend/.env`, `node_modules/`, `.venv/`, `frontend/test-results/` — added test-results and playwright-report
- [x] T054 [P] Verify `backend/.env.example` lists all required environment variables with descriptions — 11 vars documented
- [x] T055 Update `specs/004-e2e-testing-bugfix/plan.md` completion criteria

**Checkpoint**: Full platform tested end-to-end, all verified, documentation complete ✅

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)          → no dependencies, start immediately
Phase 2 (Playwright)     → requires Phase 1 (npm install)
Phase 3 (US1 API Tests)  → requires Phase 1 (backend running)
Phase 4 (US2 Playwright) → requires Phase 2 (Playwright installed) + Phase 1 (both servers)
Phase 5 (US3 Bug Fix)    → runs after Phases 3-4 (bugs discovered)
Phase 6 (US4 AI Verify)  → requires Phase 3 (API endpoints working)
Phase 7 (Polish)         → requires all phases complete
```

### Parallel Opportunities

```bash
# Phase 1 — setup tasks in parallel:
T002  backend uv sync
T003  frontend npm install

# Phase 3 — independent endpoint tests:
T015  GET /users/{id}
T016  GET /users/lookup
T022  POST /chat/ with selected_text
T024  POST /translate/
T026  POST /chat/ without auth

# Phase 4 — independent Playwright test files:
T028  homepage.spec.ts (after T010)
T030  chat.spec.ts (after T010)
T032  auth.spec.ts (after T010)

# Phase 5 — independent verification:
T041  pytest suite
T042  frontend build

# Phase 6 — independent AI checks:
T047  personalization verification
T048  translation verification
```

---

## Implementation Strategy

### MVP First (US1 + US2 — P1 Stories)

1. Phase 1: Verify setup
2. Phase 2: Install Playwright
3. Phase 3: Test all API endpoints (US1)
4. Phase 4: Playwright browser tests (US2)
5. **STOP + VALIDATE** → fix all bugs found

### Incremental Completion

| Phase | Deliverable | Status |
|-------|------------|--------|
| 1-2 | Setup + Playwright installed | Ready to test |
| 3 | All API endpoints validated | Backend verified |
| 4 | All browser flows tested | Frontend verified |
| 5 | All bugs fixed | Application stable |
| 6 | AI integration verified | SDK compliance confirmed |
| 7 | Final verification | Feature complete |

---

## Task Count Summary

| Phase | Tasks | Parallelizable |
|-------|-------|---------------|
| Phase 1 — Setup | 6 | 2 |
| Phase 2 — Playwright Install | 4 | 0 |
| Phase 3 — US1 API Tests | 17 | 5 |
| Phase 4 — US2 Playwright E2E | 13 | 3 |
| Phase 5 — US3 Bug Fix | 5 | 1 |
| Phase 6 — US4 AI Verify | 6 | 2 |
| Phase 7 — Polish | 4 | 2 |
| **Total** | **55** | **15** |
