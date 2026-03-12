# Quickstart: AI Humanoid Textbook (AI-Native)

## 1. Prerequisites (WSL2)
- Python 3.13 (via `uv`)
- Node.js 20+ & npm
- Neon Cloud account (Postgres)
- Qdrant Cloud account (Vector DB)
- Google Gemini API Key

## 2. Backend Setup
```bash
cd backend
cp .env.example .env
# Edit .env with Neon, Qdrant, and Gemini credentials

uv sync                          # Install dependencies
uv run python src/db/init_db.py  # Create Postgres tables
uv run python scripts/init_qdrant.py          # Create Qdrant collection
uv run python scripts/ingest_textbook.py      # Index textbook content

# Run TDD tests
uv run pytest tests/ -v
```

## 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with credentials and API_BASE_URL
```

## 4. Run Development Servers
```bash
./start-dev.sh
```

## 5. Deploy
- **Frontend**: `cd frontend && npm run deploy` (Deploys to GitHub Pages)
- **Backend**: Push to `main` branch (Render auto-deploys via Dockerfile)
