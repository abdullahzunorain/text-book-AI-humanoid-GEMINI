# Physical AI & Humanoid Robotics — AI-Native Interactive Textbook

An AI-powered interactive textbook platform for learning Physical AI and Humanoid Robotics. Built with **Docusaurus 3** (frontend) and **FastAPI** (backend), featuring **RAG-based AI chat**, **content personalization**, and **Urdu translation** — all powered by **Google Gemini 2.0 Flash** and **Qdrant** vector search.

---

## Table of Contents

- [What Is This Application?](#what-is-this-application)
- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up External Services](#2-set-up-external-services)
  - [3. Backend Setup](#3-backend-setup)
  - [4. Frontend Setup](#4-frontend-setup)
  - [5. Ingest Textbook Content](#5-ingest-textbook-content)
  - [6. Run Development Servers](#6-run-development-servers)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Deploy Frontend (GitHub Pages)](#deploy-frontend-github-pages)
  - [Deploy Backend (Render.com)](#deploy-backend-rendercom)
- [Course Content](#course-content)
- [Claude Code Agent Skills](#claude-code-agent-skills)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## What Is This Application?

This is a **full-stack, AI-native educational platform** designed for a 13-week university course on **Physical AI & Humanoid Robotics**. It combines a beautifully structured static textbook with powerful AI features:

1. **Interactive Textbook** — A Docusaurus 3 site with 4 modules and 13 weekly chapters covering ROS 2, digital twins, NVIDIA Isaac, and Vision-Language-Action (VLA) models.

2. **RAG Chat Assistant** — A floating AI chatbot on every page that answers questions using textbook content as context. It retrieves relevant passages from a Qdrant vector database and generates responses using Google Gemini 2.0 Flash.

3. **Selected Text Q&A** — Select any text on the page, then ask a question. The AI answers based *only* on the selected passage.

4. **Content Personalization** — Logged-in users get AI-rewritten content tailored to their hardware and software background (e.g., "RTX GPU" + "Intermediate Python").

5. **Urdu Translation** — Any chapter can be translated to Urdu with one click, making the content accessible to a wider audience.

6. **User Authentication** — Sign up with your learning background. The system uses your profile to personalize AI responses and content.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **RAG Chat** | Semantic search over textbook content + Gemini LLM responses with source citations |
| **Selected Text Mode** | Highlight text on any page and ask questions about it specifically |
| **Personalization** | AI rewrites chapter content based on your hardware/software background |
| **Urdu Translation** | One-click translation of any chapter to Urdu |
| **User Profiles** | Register with background info for personalized learning |
| **13 Chapters** | Structured across 4 modules: ROS 2, Digital Twin, NVIDIA Isaac, VLA |
| **Dark Mode** | Automatic light/dark theme based on system preferences |
| **Source Citations** | Every AI response includes chapter and module source references with relevance scores |
| **Agent Skills** | 3 Claude Code automation skills for content ingestion, test generation, and chapter creation |

---

## Architecture Overview

```
                          GitHub Pages                    Render.com
                        ┌─────────────┐              ┌──────────────┐
                        │  Docusaurus  │   REST API   │   FastAPI    │
  User ──────────────── │  (React 19)  │ ──────────── │  (Python)    │
                        │  Static Site │              │  RAG Service │
                        └─────────────┘              └──────┬───────┘
                                                           │
                                              ┌────────────┼────────────┐
                                              │            │            │
                                        ┌─────┴─────┐ ┌───┴───┐ ┌─────┴─────┐
                                        │   Neon     │ │Qdrant │ │  Gemini   │
                                        │  Postgres  │ │ Cloud │ │ 2.0 Flash │
                                        │  (Users,   │ │(768-d │ │  (LLM +   │
                                        │  Messages) │ │vectors│ │ Embeddings│
                                        └───────────┘ └───────┘ └───────────┘
```

**How it works:**

1. The **Docusaurus frontend** serves the textbook as a static site. A floating chat widget and chapter action buttons are injected into every page.
2. When a user asks a question, the **frontend sends a POST request** to the FastAPI backend with the message and session ID.
3. The **RAG service** generates an embedding for the query using `gemini-embedding-001` (768 dimensions), searches the **Qdrant vector database** for relevant textbook chunks, and builds a context-aware prompt.
4. **Gemini 2.0 Flash** generates a response grounded in the retrieved textbook content.
5. The response is returned with **source citations** (chapter, module, relevance score).
6. For **personalization**, the backend fetches the user's hardware/software background and instructs Gemini to rewrite content accordingly.
7. For **translation**, the backend sends content to Gemini with a translation prompt.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Docusaurus 3 + React 19 + TypeScript | Static textbook site |
| **Backend** | FastAPI + Python 3.13 | REST API + RAG pipeline |
| **Package Manager** | `uv` (Python), `npm` (Node.js) | Dependency management |
| **Relational DB** | Neon Serverless Postgres | Users, messages, sessions |
| **Vector DB** | Qdrant Cloud | Textbook embeddings (768-dim) |
| **LLM** | Google Gemini 2.0 Flash | Chat, personalization, translation |
| **Embedding Model** | gemini-embedding-001 | 768-dimensional text embeddings |
| **Auth** | better-auth + custom middleware | User registration and sessions |
| **ORM** | SQLAlchemy (async) + asyncpg | Database operations |
| **Testing** | pytest + httpx + aiosqlite | Async endpoint testing with in-memory DB |
| **Frontend Deploy** | GitHub Pages | Static site hosting |
| **Backend Deploy** | Render.com (Docker) | API hosting |

---

## Project Structure

```
HACK-I-CLAUDE/
├── backend/                        # FastAPI backend
│   ├── src/
│   │   ├── main.py                 # App entry point, lifespan, CORS, routers
│   │   ├── api/
│   │   │   ├── health.py           # GET /health — liveness check
│   │   │   ├── users.py            # POST /users/, GET /users/{id}, GET /users/lookup
│   │   │   ├── chat.py             # POST /chat/, /personalize/, /translate/
│   │   │   └── auth_middleware.py   # Bearer token auth dependency
│   │   ├── services/
│   │   │   ├── rag.py              # RAG pipeline (retrieve → prompt → generate)
│   │   │   ├── embeddings.py       # Gemini embedding generation
│   │   │   └── vector_store.py     # Qdrant client + collection management
│   │   ├── db/
│   │   │   ├── database.py         # Async SQLAlchemy engine + session factory
│   │   │   ├── init_db.py          # Table creation script
│   │   │   ├── crud_users.py       # User CRUD operations
│   │   │   ├── crud_messages.py    # Message/chat history CRUD
│   │   │   └── crud_vectors.py     # Qdrant search + upsert operations
│   │   ├── models/
│   │   │   └── models.py           # SQLAlchemy models (User, Message, UserContext)
│   │   └── schemas/
│   │       ├── chat.py             # Chat request/response Pydantic models
│   │       ├── user.py             # User request/response models
│   │       └── content.py          # Personalize/translate models
│   ├── scripts/
│   │   ├── ingest_textbook.py      # Markdown → Qdrant ingestion pipeline
│   │   └── init_qdrant.py          # Qdrant collection initialization
│   ├── tests/
│   │   ├── conftest.py             # Test fixtures (in-memory DB, mock Qdrant)
│   │   ├── test_health.py          # Health endpoint tests
│   │   ├── test_users.py           # User CRUD tests
│   │   ├── test_chat.py            # Chat endpoint tests (mocked Gemini)
│   │   ├── test_auth.py            # Auth middleware tests
│   │   └── test_rag.py             # RAG integration tests
│   ├── pyproject.toml              # Python dependencies (uv-managed)
│   ├── Dockerfile                  # Production Docker image
│   ├── .env.example                # Environment variable template
│   └── .dockerignore               # Docker build excludes
│
├── frontend/                       # Docusaurus 3 frontend
│   ├── docs/                       # Textbook content (13 chapters)
│   │   ├── intro.md
│   │   ├── module-1-ros2/          # Weeks 1-4: ROS 2 fundamentals
│   │   ├── module-2-digital-twin/  # Weeks 5-7: Simulation & digital twins
│   │   ├── module-3-nvidia-isaac/  # Weeks 8-10: NVIDIA Isaac platform
│   │   └── module-4-vla/           # Weeks 11-13: VLA models & deployment
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/               # Floating RAG chat widget
│   │   │   ├── AuthModal/          # Sign up / sign in modal
│   │   │   └── ChapterActions/     # Personalize + Translate buttons
│   │   ├── theme/
│   │   │   ├── Layout.tsx          # Global layout (chat + auth injection)
│   │   │   └── DocItem/Layout/     # Per-chapter action bar injection
│   │   ├── hooks/
│   │   │   └── useAuth.ts          # Authentication React hook
│   │   ├── services/
│   │   │   └── contentApi.ts       # Personalize/translate API client
│   │   └── lib/
│   │       └── auth.ts             # better-auth client config
│   ├── package.json
│   ├── docusaurus.config.ts
│   └── .env.local.example
│
├── .claude/commands/               # Claude Code agent skills
│   ├── ingest-content.md           # Skill: run RAG ingestion pipeline
│   ├── gen-tests.md                # Skill: scaffold pytest tests
│   └── gen-chapter.md              # Skill: generate textbook chapter
│
├── render.yaml                     # Render.com deployment config
├── start-dev.sh                    # Dev server startup script
└── .gitignore
```

---

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

| Requirement | Version | Check Command |
|-------------|---------|--------------|
| **Python** | 3.13+ | `python --version` |
| **uv** | Latest | `uv --version` |
| **Node.js** | 20+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **Git** | Any | `git --version` |

### Install uv (Python package manager)

```bash
# macOS / Linux / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### External Service Accounts (Free Tier)

You will need accounts on these services (all have free tiers):

1. **[Neon](https://neon.tech)** — Serverless Postgres database
2. **[Qdrant Cloud](https://cloud.qdrant.io)** — Vector database
3. **[Google AI Studio](https://aistudio.google.com)** — Gemini API key

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/abdullahzunorain/text-book-AI-humanoid.git
cd text-book-AI-humanoid
```

### 2. Set Up External Services

#### Neon Postgres

1. Go to [neon.tech](https://neon.tech) and create a free account.
2. Create a new project (any name, e.g., `ai-textbook`).
3. Copy the **connection string** from the dashboard. It looks like:
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```
4. Keep this — you'll need it for `DATABASE_URL`.

#### Qdrant Cloud

1. Go to [cloud.qdrant.io](https://cloud.qdrant.io) and create a free account.
2. Create a new cluster (Free tier, any region).
3. Once created, copy the **Cluster URL** (e.g., `https://abc123-xxx.aws.cloud.qdrant.io`) and **API Key**.
4. Keep these — you'll need them for `QDRANT_URL` and `QDRANT_API_KEY`.

#### Google Gemini API Key

1. Go to [aistudio.google.com](https://aistudio.google.com).
2. Click **"Get API Key"** in the top right.
3. Create a key and copy it.
4. Keep this — you'll need it for `GEMINI_API_KEY`.

### 3. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Copy the environment template
cp .env.example .env
```

Now open `backend/.env` in your text editor and fill in your credentials:

```env
# Paste your Neon connection string (add +asyncpg after postgresql)
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.neon.tech/dbname?sslmode=require

# Paste your Qdrant credentials
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=textbook_chunks

# Paste your Gemini API key
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
EMBEDDING_MODEL=gemini-embedding-001

# CORS origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
SECRET_KEY=any-random-string-here
```

> **Important:** Make sure your `DATABASE_URL` uses `postgresql+asyncpg://` (not just `postgresql://`). The system auto-converts it, but it's cleaner to set it correctly from the start.

Now install dependencies and initialize the database:

```bash
# Install Python dependencies
uv sync

# Create database tables in Neon
uv run python src/db/init_db.py

# Initialize Qdrant collection (768-dim vectors)
uv run python scripts/init_qdrant.py
```

You should see:

```
✅ Collection 'textbook_chunks' created.
```

### 4. Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Copy the environment template
cp .env.local.example .env.local
```

Edit `frontend/.env.local` if you need to change the API URL (default is fine for local development):

```env
REACT_APP_API_URL=http://localhost:8000
```

### 5. Ingest Textbook Content

This step reads all 14 chapter markdown files, chunks them, generates embeddings using Gemini, and stores them in Qdrant for semantic search.

```bash
# From the backend directory
cd backend
uv run python scripts/ingest_textbook.py
```

Expected output:

```
🔧 Starting textbook ingestion...
📚 Found 14 markdown files
   Processing: intro.md...
      → 3 segments
   Processing: week-1-intro-physical-ai.md...
      → 12 segments
   ...
📤 Upserting segments to Qdrant...
✅ Ingestion complete!
   Files processed: 14
   Segments created: ~150
```

> **Note:** This step requires a valid `GEMINI_API_KEY` and `QDRANT_URL` because it generates real embeddings and stores them in Qdrant.

### 6. Run Development Servers

You need **two terminals** — one for the backend, one for the frontend.

**Terminal 1 — Backend:**

```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

The API is now running at **http://localhost:8000**. Verify it:
- Health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs

**Terminal 2 — Frontend:**

```bash
cd frontend
npm start
```

The textbook is now running at **http://localhost:3000**.

You should see:
- The textbook with all 13 chapters in the sidebar
- A floating **"AI Textbook Assistant"** chat widget in the bottom-right corner
- A **"Sign In"** button in the top-right corner

**Try it out:**
1. Click the chat widget and type: **"What is ROS 2?"**
2. You should receive an AI response with source citations from the textbook.
3. Click **"Sign In"** → **"Sign Up"** → Register with your background info.
4. Navigate to any chapter → You'll see **"Personalize"** and **"Translate to Urdu"** buttons at the top of the chapter.

---

## API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | None | Welcome message |
| `GET` | `/health` | None | Health check (DB + Qdrant status) |
| `POST` | `/users/` | None | Register a new user |
| `GET` | `/users/lookup` | None | Find user by email (`?email=...`) |
| `GET` | `/users/{id}` | None | Get user profile by ID |
| `POST` | `/chat/` | Optional | RAG chat (message + session_id) |
| `POST` | `/personalize/` | Optional | Personalize chapter content |
| `POST` | `/translate/` | None | Translate content to Urdu |

### Example: Send a Chat Message

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is a ROS 2 node?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Example Response

```json
{
  "response": "A ROS 2 node is a fundamental building block in the Robot Operating System 2...",
  "sources": [
    {
      "chapter": "Week 3: Nodes, Topics & Services",
      "module": "module-1-ros2",
      "score": 0.92
    }
  ],
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "context_count": 3,
  "context_used": true
}
```

### Example: Register a User

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Abdullah",
    "email": "abdullah@example.com",
    "hardware_background": "NVIDIA RTX Series",
    "software_background": "Intermediate Python"
  }'
```

### Example: Personalize Content

```bash
curl -X POST http://localhost:8000/personalize/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 1" \
  -d '{
    "content": "ROS 2 uses DDS for communication...",
    "chapter_title": "Week 2: ROS 2 Architecture"
  }'
```

### Interactive API Documentation

Once the backend is running, visit **http://localhost:8000/docs** for the full Swagger UI with all endpoints, request/response schemas, and a "Try it out" button for each endpoint.

---

## Testing

The backend has a comprehensive test suite using `pytest` with async support, in-memory SQLite, and mocked external services. **No API keys or external services are needed to run tests.**

```bash
cd backend

# Run all tests with verbose output
uv run pytest tests/ -v

# Run a specific test file
uv run pytest tests/test_chat.py -v

# Run with short traceback on failures
uv run pytest tests/ -v --tb=short
```

### Test Coverage

| File | Tests | What It Tests |
|------|-------|---------------|
| `test_health.py` | 2 | Root endpoint (`/`) + health check (`/health`) |
| `test_users.py` | 3 | Create user, get user by ID, 404 for missing user |
| `test_chat.py` | 3 | Missing fields (422), mocked RAG chat, selected text mode |
| `test_auth.py` | 4 | Unauthenticated fallback, valid auth token, email lookup, 404 |
| `test_rag.py` | 3 | Embedding generation, Qdrant connection, vector search |

**Total: 15 tests** — all run against an in-memory SQLite database with mocked Qdrant and Gemini.

---

## Deployment

### Deploy Frontend (GitHub Pages)

The Docusaurus site is pre-configured for GitHub Pages deployment.

**Step 1:** Update `frontend/docusaurus.config.ts` with your GitHub info:

```typescript
url: 'https://YOUR-USERNAME.github.io',
baseUrl: '/YOUR-REPO-NAME/',
organizationName: 'YOUR-USERNAME',
projectName: 'YOUR-REPO-NAME',
```

**Step 2:** Build and deploy:

```bash
cd frontend
npm run build
npm run deploy
```

Your textbook is now live at `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`.

### Deploy Backend (Render.com)

The repository includes a `render.yaml` for easy Render deployment:

1. Push your code to the `main` branch on GitHub.
2. Go to [render.com](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Render will auto-detect the `render.yaml` configuration.
5. Add your environment variables in the Render dashboard:
   - `DATABASE_URL` — your Neon connection string
   - `QDRANT_URL` — your Qdrant cluster URL
   - `QDRANT_API_KEY` — your Qdrant API key
   - `GEMINI_API_KEY` — your Gemini API key
   - `ALLOWED_ORIGINS` — your GitHub Pages URL (e.g., `https://user.github.io`)
6. Click Deploy.

**Alternative: Docker deployment**

```bash
cd backend
docker build -t ai-textbook-backend .
docker run -p 8000:8000 --env-file .env ai-textbook-backend
```

> **After deploying the backend**, update your frontend's `REACT_APP_API_URL` environment variable to point to the Render URL before building the frontend for production.

---

## Course Content

The textbook is organized into **4 modules** with **13 weekly chapters**:

### Module 1: ROS 2 — The Robotic Nervous System

| Week | Chapter |
|------|---------|
| 1 | Introduction to Physical AI |
| 2 | ROS 2 Architecture |
| 3 | Nodes, Topics & Services |
| 4 | ROS 2 Packages with Python |

### Module 2: Digital Twin — Simulation & Modeling

| Week | Chapter |
|------|---------|
| 5 | Gazebo Basics |
| 6 | Unity Robotics |
| 7 | Sim-to-Real Transfer |

### Module 3: NVIDIA Isaac — GPU-Accelerated Robotics

| Week | Chapter |
|------|---------|
| 8 | Isaac Sim Introduction |
| 9 | Isaac ROS Bridge |
| 10 | Advanced Simulation |

### Module 4: VLA — Vision-Language-Action Models

| Week | Chapter |
|------|---------|
| 11 | VLA Architecture |
| 12 | Training VLA Models |
| 13 | Deploying Humanoid Robots |

---

## Claude Code Agent Skills

This project includes 3 reusable [Claude Code](https://claude.ai/code) agent skills (found in `.claude/commands/`):

### `/ingest-content`

Runs the full RAG ingestion pipeline: reads textbook markdown files, chunks them, generates Gemini embeddings, and upserts to Qdrant. Reports chunk count per module.

### `/gen-tests`

Given an endpoint path (e.g., `POST /chat/`), generates a complete pytest test file with happy path, edge case, and error case tests using `httpx.AsyncClient` and the existing conftest fixtures.

### `/gen-chapter`

Given a module name and week number, generates a complete Docusaurus chapter following the existing textbook structure: introduction, core concepts, hands-on exercises, and review questions.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | Neon Postgres connection string (`postgresql+asyncpg://...`) |
| `QDRANT_URL` | Yes | — | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Yes | — | Qdrant Cloud API key |
| `QDRANT_COLLECTION_NAME` | No | `textbook_chunks` | Vector collection name |
| `GEMINI_API_KEY` | Yes | — | Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-2.0-flash` | Chat/personalization LLM model |
| `EMBEDDING_MODEL` | No | `gemini-embedding-001` | Text embedding model (768-dim) |
| `ALLOWED_ORIGINS` | No | `http://localhost:3000` | CORS origins (comma-separated) |
| `ENVIRONMENT` | No | `development` | `development` or `production` |
| `SECRET_KEY` | No | — | Secret key for session signing |

### Frontend (`frontend/.env.local`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REACT_APP_API_URL` | No | `http://localhost:8000` | Backend API base URL |

---

## Troubleshooting

### "GEMINI_API_KEY environment variable is not set"

Make sure `backend/.env` exists and has a valid `GEMINI_API_KEY`. The file must be in the `backend/` directory (not the project root).

### Tests fail with "no such table"

Run tests from the `backend/` directory so the correct conftest.py is picked up:

```bash
cd backend
uv run pytest tests/ -v
```

### Chat returns "connection refused"

The frontend expects the backend at `http://localhost:8000`. Make sure the backend is running:

```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

### Qdrant "collection not found"

Initialize the collection and ingest content:

```bash
cd backend
uv run python scripts/init_qdrant.py
uv run python scripts/ingest_textbook.py
```

### Frontend build warnings about broken links

These are cosmetic warnings about cross-module sidebar links. They work correctly on the deployed site. The `onBrokenLinks: 'warn'` setting in `docusaurus.config.ts` prevents them from blocking the build.

### "uv: command not found"

Install uv first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal or run `source ~/.bashrc` (or `~/.zshrc`).

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run backend tests: `cd backend && uv run pytest tests/ -v`
5. Build the frontend: `cd frontend && npm run build`
6. Commit your changes: `git commit -m "Add my feature"`
7. Push to your fork: `git push origin feature/my-feature`
8. Open a Pull Request

This project uses **Spec-Driven Development (SDD)** with SpecifyPlus tools. Development specifications, plans, and task breakdowns are in the `specs/` directory. Prompt history records are in `history/prompts/`.

---

## License

This project was built for the **Hackathon I** at the **Governor Sindh IT Initiative - Generative AI Quarter**. All course content is educational material for the Physical AI & Humanoid Robotics program.

---

Built with Docusaurus, FastAPI, Gemini AI, Qdrant, and Neon Postgres.
