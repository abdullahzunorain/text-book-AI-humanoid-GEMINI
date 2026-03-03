# Physical AI & Humanoid Robotics Textbook

An AI-native textbook platform with integrated RAG (Retrieval-Augmented Generation) chatbot for the "Physical AI & Humanoid Robotics" course.

## 🚀 Quick Start

### Run Development Servers

**Linux/macOS:**
```bash
./start-dev.sh
```

**Windows:**
```bash
start-dev.bat
```

This will:
- Set up backend virtual environment
- Install dependencies
- Start FastAPI backend (http://localhost:8000)
- Start Docusaurus frontend (http://localhost:3000)

## 📚 Project Overview

This project creates a comprehensive textbook for the Physical AI & Humanoid Robotics course with an AI-powered teaching assistant that can answer questions based on the textbook content.

### Core Features & Hackathon Requirements

- **📖 Interactive Textbook**: Modern, responsive documentation site built with Docusaurus.
- **🤖 AI Chatbot (OpenAI SDK + Gemini)**: RAG-powered teaching assistant embedded in the site. It uses the OpenAI SDK configured to talk to the Gemini API (`gemini-2.0-flash`).
- **💬 Context & Text-Selection Aware**: Answers questions about the textbook, and optionally uses **only user-selected text** if the user highlights text before sending a message.
- **👤 User Personalization (Bonus)**: Logged-in users can personalize chapter content to their hardware/software background via a click of a button in the UI. 
- **🌐 Urdu Translation (Bonus)**: Instantly translate any chapter content to Urdu while preserving technical terms.
- **🔐 Better-Auth Integration (Bonus)**: Signup and Signin flow intended to capture software/hardware background to feed the personalization agent. *(Note: Since Docusaurus is static, a simulated flow has been prepared via the FastAPI user endpoints; in a full stack scenario, deploy `better-auth` on an Express edge server).*

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│  (Docusaurus)   │◄───────►│   (FastAPI)     │
│  React + TS     │         │   Python        │
└─────────────────┘         └────────┬────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
             ┌──────▼──────┐  ┌─────▼─────┐  ┌──────▼──────┐
             │   Neon      │  │  Qdrant   │  │ OpenAI SDK  │
             │  Postgres   │  │  Vector   │  │  + Gemini   │
             │  (Chat)     │  │    DB     │  │  (LLM API)  │
             └─────────────┘  └───────────┘  └─────────────┘
```

## 📦 Tech Stack

### Frontend
- **Docusaurus 3** - Documentation framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Vanilla CSS** - Styling with CSS modules
- **React-Markdown** - Rendering transformed/translated content dynamically

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Neon** - Serverless PostgreSQL
- **Qdrant** - Vector database
- **uv** - Python package manager
- **OpenAI SDK** - Connecting to Gemini (`base_url="https://generativelanguage.googleapis.com/v1beta/openai/"`)

## 🛠️ Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd book-project
```

### 2. Backend Setup

```bash
cd backend

# Use uv for package management (WSL/Linux recommended)
uv init
uv add fastapi uvicorn python-dotenv pydantic psycopg2-binary sqlalchemy qdrant-client openai requests

# Configure environment
cp .env.example .env
# Edit .env with your credentials (NEON_DB_URL, QDRANT_URL, QDRANT_API_KEY, GEMINI_API_KEY)
# NOTE: The project requires GEMINI_API_KEY to be set!
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Initialize Databases

```bash
# In backend directory
uv run python init_db.py        # Initialize Neon
uv run python init_qdrant.py    # Initialize Qdrant
uv run python ingest_textbook.py # Ingest textbook content
```

### 5. Run Servers

```bash
# Terminal 1 - Backend
cd backend && uv run uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && npm start
```

## 📊 API Endpoints

### Chat & RAG
- `POST /chat/`: Generates a response using RAG.
  - Parameters: `user_id`, `message`, `session_id` (optional), `selected_text` (optional). If `selected_text` is passed, the chatbot restricts its answer to the provided text context only!

### Personalize & Translate (Bonus Features)
- `POST /personalize/`: Takes `user_id` and `content`. Uses Gemini to rewrite the content making it relatable to the user's software/hardware background.
- `POST /translate/`: Takes `content` and returns the Urdu translation.

### User Management
- `POST /users/`: Register user (name, email, `hardware_background`, `software_background`).
- `GET /users/{user_id}`: Fetch user context.

## 🎯 Development Workflow

This project is developed using **Spec-Driven Development (SDD)** with SpecifyPlus tools. 
- You can find the development specifications and plans in the `specs/` directory.
- Prompt histories are stored in `history/prompts/`.
- Executed using the `gemini` CLI and OpenAI SDK integrations.

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature-name`
2. Make changes following SDD principles
3. Create PHR for significant work
4. Submit pull request

