# Architectural Plan: Physical AI & Humanoid Robotics MVP

## 1. Scope and Dependencies
- **In Scope**:
  - Docusaurus site with 4 course modules.
  - FastAPI backend for RAG and Chat History.
  - GitHub Pages for frontend hosting.
  - Neon Postgres for user chat history, metadata, and user context.
  - Qdrant Cloud for vector embeddings of the textbook.
- **Out of Scope**: Personalization logic (Phase 2), Urdu translation (Phase 2).
- **External Dependencies**: OpenAI SDK for Agentic workflow, Gemini API for models integration, Neon Console, Qdrant Cloud Console.

## 2. Key Decisions and Rationale
- **Frontend Hosting**: **GitHub Pages**. Chosen for simplicity and integration with the repository. Requires a static build of the Docusaurus site.
- **Data Persistence (Neon)**: Used for `chat_history` and `user_context`. This ensures that even in an MVP, we can recall previous interactions and store user-specific preferences (e.g., software/hardware background) as requested in the hackathon brief.
- **Vector Search (Qdrant)**: High-performance vector database to store embeddings of the MDX files from the Docusaurus site.

## 3. Interfaces and API Contracts

### 3.1. Chat API (`/api/chat`)
- **POST**: `/v1/chat`
  - **Input**: `{ user_id: string, message: string }`
  - **Logic**:
    1. Fetch `user_context` and recent `chat_history` from **Neon**.
    2. Query **Qdrant** for relevant textbook snippets.
    3. Construct prompt: `Context: [Qdrant Snippets] + [User History] | Query: [Message]`.
    4. Generate response via LLM.
    5. Save new interaction to **Neon**.
  - **Output**: `{ response: string }`

## 4. Data Management
- **Neon Schema**:
  - `users`: `id`, `name`, `hardware_bg`, `software_bg`, `created_at`.
  - `messages`: `id`, `user_id`, `role` (user/bot), `content`, `timestamp`.
- **Qdrant Collection**:
  - `textbook_segments`: `vector`, `payload` (text, chapter_title, url).

## 5. Deployment Strategy
- **Frontend**: `npm run build` -> `gh-pages` branch -> GitHub Pages.
- **Backend**: FastAPI app deployed to Vercel/Render (to handle dynamic API calls).
- **Database**: Neon (Cloud) + Qdrant (Cloud).

## 6. Risk Analysis
1. **GitHub Pages Latency**: Static site is fast, but initial API call to a "cold" serverless backend might lag. *Mitigation: Simple loading states in UI.*
2. **Context Window**: Storing too much history in Neon might exceed LLM limits. *Mitigation: Implement a "sliding window" for history retrieval.*

## 7. Architectural Decision Records (ADR)
- **ADR-001**: Use Neon for Chat History and User Context (Hybrid RAG).

---

### 📋 Architectural decision detected: Use Neon for Chat History and User Context
This decision centralizes user-specific data in Postgres while keeping the knowledge base in Qdrant. 
Document reasoning and tradeoffs? Run `/sp.adr data-storage-strategy`.
