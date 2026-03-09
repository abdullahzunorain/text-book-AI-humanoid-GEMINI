---
id: "0004"
title: "Implement E2E Testing and Bug Resolution"
stage: green
date: 2026-03-09
surface: agent
model: claude-opus-4-6
feature: 004-e2e-testing-bugfix
branch: 004-e2e-testing-bugfix
user: zunorain
command: /sp.implement
labels: ["e2e", "playwright", "testing", "bugfix", "implementation"]
links:
  spec: specs/004-e2e-testing-bugfix/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/playwright.config.ts
  - frontend/e2e/homepage.spec.ts
  - frontend/e2e/chat.spec.ts
  - frontend/e2e/auth.spec.ts
  - frontend/e2e/actions.spec.ts
  - frontend/src/components/Chat/Chat.tsx
  - frontend/src/hooks/useAuth.ts
  - frontend/src/services/contentApi.ts
  - frontend/src/lib/auth.ts
  - backend/src/schemas/user.py
  - backend/src/api/users.py
  - .gitignore
  - specs/004-e2e-testing-bugfix/tasks.md
  - specs/004-e2e-testing-bugfix/plan.md
tests:
  - backend/tests/ (15/15 PASS)
  - frontend/e2e/ (12/12 PASS via Playwright headed mode)
---

## Prompt

implement properly and carefully

## Response snapshot

Executed all 55 tasks across 7 phases for feature 004-e2e-testing-bugfix:

**Phase 1 (Setup)**: Verified .env, uv sync, npm install, init_db, pytest 15/15, frontend build — all PASS.

**Phase 2 (Playwright Install)**: Installed @playwright/test and Chromium. Created playwright.config.ts with headed mode (slowMo: 500) and webServer config for both backend/frontend. Created e2e/ directory.

**Phase 3 (API Endpoint Validation)**: Tested all 7 endpoints via live curl requests. Found bug: POST /users/ accepted missing email (200 instead of 422). Fixed by making email required in UserCreate schema.

**Phase 4 (Playwright E2E)**: Created 4 test files (12 tests total):
- homepage.spec.ts: Title check, module links (4+), navigation to chapter
- chat.spec.ts: Chat widget visibility, send message + receive response
- auth.spec.ts: Modal tabs, sign up, sign out + sign in
- actions.spec.ts: Personalize/Translate visible when logged in, loading states, revert, hidden when logged out

Found and fixed 6 bugs during Playwright testing:
1. `process.env` not available in Docusaurus browser (replaced with hardcoded URL in 4 files)
2. POST /users/ missing email validation (made email required)
3. Duplicate email returns 500 (added IntegrityError -> 409 handler)
4. Playwright `goto('/')` ignores baseURL (changed to `goto('./')`)
5. Auth modal tab persistence (explicitly click Sign In tab)
6. slowMo TypeScript error (moved to launchOptions)

**Phase 5 (Stability)**: pytest 15/15, frontend build SUCCESS, Playwright 12/12 PASS.

**Phase 6 (AI Verification)**: Confirmed OpenAI SDK with Gemini chat.completions for all 3 features. GEMINI_MODEL configurable. output_dimensionality=768 correct. Graceful 429 degradation verified.

**Phase 7 (Polish)**: Updated .gitignore with test-results/. Verified .env.example. Updated plan.md completion criteria (7/7 PASS).

## Outcome

- Impact: Full E2E test coverage for the platform — 15 backend unit tests + 12 Playwright browser tests + 7 live API endpoint validations. 6 bugs found and fixed.
- Tests: pytest 15/15 PASS, Playwright 12/12 PASS (non-headless), frontend build SUCCESS
- Files: 14 files created/modified
- Next prompts: /sp.git.commit_pr to commit and create PR
- Reflection: The biggest time sink was debugging Playwright selector issues — the `process.env` crash caused blank pages, and the baseURL path resolution was non-obvious. The scoped modal selectors (to avoid chat input collision) was a key insight. Running tests with 1 worker prevents race conditions on shared backend state.

## Evaluation notes (flywheel)

- Failure modes observed: process.env crash in browser, Playwright baseURL path resolution, selector collisions between modal and chat inputs, duplicate email race conditions with parallel workers
- Graders run and results (PASS/FAIL): pytest 15/15 PASS, Playwright 12/12 PASS, frontend build PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
