# Execution Tasks: Physical AI & Humanoid Robotics MVP

## Phase 1: Docusaurus & Frontend Scaffolding
- [ ] **Task 1.1: Initialize Docusaurus**
  - **Action**: Run `npx create-docusaurus@latest . classic --typescript` (in a subfolder `frontend/` or root).
  - **Success Criteria**: `npm start` runs locally.
- [ ] **Task 1.2: Structure Course Modules**
  - **Action**: Create folders in `docs/` for Module 1-4. Add placeholder `index.md` files for each.
  - **Success Criteria**: Sidebar shows all 4 modules correctly.
- [ ] **Task 1.3: Configure GitHub Pages**
  - **Action**: Update `docusaurus.config.ts` with `url`, `baseUrl`, `organizationName`, and `projectName`.
  - **Success Criteria**: Project can build and is ready for `gh-pages` deployment.

## Phase 2: Backend Infrastructure (FastAPI)
- [ ] **Task 2.1: FastAPI Boilerplate**
  - **Action**: Initialize a Python environment and create a basic FastAPI app.
  - **Success Criteria**: `/docs` endpoint is accessible.
- [ ] **Task 2.2: Neon Integration**
  - **Action**: Setup `psycopg2` or `SQLAlchemy` to connect to Neon. Create `users` and `messages` tables.
  - **Success Criteria**: Backend can write a test row to Neon.
- [ ] **Task 2.3: Qdrant Integration**
  - **Action**: Setup `qdrant-client`. Initialize a collection for the textbook.
  - **Success Criteria**: Backend can ping Qdrant Cloud.

## Phase 3: RAG Pipeline
- [ ] **Task 3.1: Textbook Ingestion Script**
  - **Action**: Create a script to read MDX files, chunk them, and upsert vectors to Qdrant.
  - **Success Criteria**: Qdrant collection is populated with textbook segments.
- [ ] **Task 3.2: Retrieval & Chat Logic**
  - **Action**: Implement `/v1/chat` endpoint. It must fetch history from Neon and context from Qdrant.
  - **Success Criteria**: LLM response incorporates retrieved textbook context and previous chat history.

## Phase 4: Chat UI Integration
- [ ] **Task 4.1: React Chat Component**
  - **Action**: Build a simple Chat UI component in Docusaurus.
  - **Success Criteria**: UI allows typing and displays messages.
- [ ] **Task 4.2: End-to-End Integration**
  - **Action**: Connect the React component to the FastAPI `/v1/chat` endpoint.
  - **Success Criteria**: Users can chat with the book directly from the Docusaurus site.

## Phase 5: Validation & Deployment
- [ ] **Task 5.1: Final Deployment**
  - **Action**: Deploy Frontend to GitHub Pages and Backend to a hosting provider.
  - **Success Criteria**: The public URL works and the chatbot is functional.
