# Tasks: Physical AI & Humanoid Robotics Textbook (AI-Native)

## Phase 1: Setup
- [x] T001 Initialize backend project structure using uv in `backend/`
- [x] T002 [P] Initialize frontend project structure using Docusaurus 3 in `frontend/`
- [x] T003 Configure environment variables template in `backend/.env.example`
- [x] T004 [P] Configure Docusaurus site metadata in `frontend/docusaurus.config.ts`
- [x] T005 Set up Dockerfile for backend deployment in `backend/Dockerfile`
- [x] T006 [P] Set up GitHub Actions for frontend deployment in `.github/workflows/deploy-frontend.yml`
- [x] T007 [P] Set up GitHub Actions for backend testing in `.github/workflows/test-backend.yml`

## Phase 2: Foundational
- [x] T008 [P] Implement Neon Postgres connection utility in `backend/src/db/database.py`
- [x] T009 [P] Implement Qdrant client utility with VECTOR_SIZE=768 in `backend/src/services/vector_store.py`
- [x] T010 [P] Implement gemini-embedding-001 wrapper in `backend/src/services/embeddings.py`
- [x] T011 Create database initialization script for Neon tables in `backend/src/db/init_db.py`
- [x] T012 Create Qdrant collection initialization script in `backend/scripts/init_qdrant.py`
- [x] T013 Implement basic health check endpoint in `backend/src/api/health.py`
- [x] T014 [P] Create TDD base test configuration and fixtures in `backend/tests/conftest.py`

## Phase 3: User Story 1 - Textbook Navigation and Reading [US1]
- [ ] T015 [US1] Structure course module directories in `frontend/docs/`
- [ ] T016 [US1] Configure Docusaurus sidebar for module/weekly hierarchy in `frontend/sidebars.ts`
- [ ] T017 [US1] Implement textbook ingestion script for chunking and embedding in `backend/scripts/ingest_textbook.py`
- [ ] T018 [US1] Create content generation subagent script for chapter drafts in `scripts/generate_chapter.py`
- [ ] T019 [US1] Author 13 weekly chapter Markdown files in `frontend/docs/`
- [ ] T020 [US1] Run ingestion script to populate Qdrant Cloud collection

## Phase 4: User Story 2 - Integrated RAG Chatbot [US2]
- [ ] T021 [US2] Create Message model for chat history in `backend/src/models/message.py`
- [ ] T022 [US2] Create Pydantic schemas for chat requests/responses in `backend/src/schemas/chat.py`
- [ ] T023 [US2] Implement retrieval service logic in `backend/src/services/rag.py`
- [ ] T024 [US2] Implement chat endpoint with grounded generation in `backend/src/api/chat.py`
- [ ] T025 [US2] Create ChatWidget frontend component in `frontend/src/components/ChatWidget/index.tsx`
- [ ] T026 [US2] Implement useChat hook for interacting with /chat/ endpoint in `frontend/src/components/ChatWidget/useChat.ts`
- [ ] T027 [US2] Add unit tests for RAG retrieval logic in `backend/tests/unit/test_rag.py`
- [ ] T028 [US2] Add integration tests for /chat/ endpoint in `backend/tests/integration/test_chat_endpoint.py`

## Phase 5: User Story 3 - Selected Text Contextual Query [US3]
- [ ] T029 [US3] Update /chat/ endpoint to handle selected_text context in `backend/src/api/chat.py`
- [ ] T030 [US3] Update useChat hook to capture browser selection in `frontend/src/components/ChatWidget/useChat.ts`
- [ ] T031 [US3] Update ChatWidget UI to display selected text context in `frontend/src/components/ChatWidget/index.tsx`
- [ ] T032 [US3] Add integration test for selected text override in `backend/tests/integration/test_chat_endpoint.py`

## Phase 6: User Story 4 - Better-Auth Signup/Signin [US4]
- [ ] T033 [US4] Extend User model with hardware/software background fields in `backend/src/models/user.py`
- [ ] T034 [US4] Define session table schema for shared database validation in `backend/src/models/session.py`
- [ ] T035 [US4] Implement better-auth configuration in `frontend/`
- [ ] T036 [US4] Create custom signup flow with background questionnaire in `frontend/src/components/SignupFlow/`
- [ ] T037 [US4] Implement session validation dependency in `backend/src/api/deps.py`
- [ ] T038 [US4] Wrap frontend with session provider in `frontend/src/theme/Root.tsx`
- [ ] T039 [US4] Add integration tests for auth dependency in `backend/tests/integration/test_auth.py`

## Phase 7: User Story 5 - Personalization & Urdu Translation [US5]
- [ ] T040 [US5] Implement personalization service using user profile in `backend/src/services/personalize.py`
- [ ] T041 [US5] Implement Urdu translation service in `backend/src/services/translate.py`
- [ ] T042 [US5] Implement /personalize/ and /translate/ endpoints in `backend/src/api/`
- [ ] T043 [US5] Create PersonalizeButton and TranslateButton components in `frontend/src/components/ChapterActions/`
- [ ] T044 [US5] Inject transformation buttons into chapter layout in `frontend/src/theme/DocItem/Layout/index.tsx`
- [ ] T045 [US5] Add unit tests for personalization prompt logic in `backend/tests/unit/test_personalize.py`
- [ ] T046 [US5] Add integration tests for personalization and translation endpoints in `backend/tests/integration/test_transformations.py`

## Phase 8: Polish & Cross-Cutting
- [ ] T047 Implement test scaffolding subagent script in `scripts/scaffold_tests.py`
- [ ] T048 Create unified startup script in `start-dev.sh`
- [ ] T049 Optimize Qdrant search parameters for better RAG precision in `backend/src/services/rag.py`
- [ ] T050 Conduct final performance audit of RAG and transformation endpoints

## Dependencies
- Phase 3 [US1] depends on Phase 1 & 2
- Phase 4 [US2] depends on Phase 3 [US1]
- Phase 5 [US3] depends on Phase 4 [US2]
- Phase 6 [US4] depends on Phase 2
- Phase 7 [US5] depends on Phase 6 [US4] and Phase 3 [US1]

## Parallel Execution Opportunities
- T001, T002 (Scaffolding)
- T004, T006, T007 (Config & CI)
- T008, T009, T010 (DB Utilities)
- T015, T016, T018 (Content structure & automation)

## Implementation Strategy
- **MVP**: Complete Phases 1 through 4 to deliver a functional RAG-powered textbook.
- **Incremental**: Add US3 (Selected Text) for improved UX, then US4 (Auth) to enable the US5 (Personalization/Translation) bonuses.
- **TDD**: Tests in each US phase must pass before moving to the next phase.
