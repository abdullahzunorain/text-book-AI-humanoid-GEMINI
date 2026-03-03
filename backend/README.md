# Backend - AI Humanoid Textbook API

FastAPI backend for the Physical AI & Humanoid Robotics textbook with RAG chatbot capabilities.

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Database Configuration (Neon Postgres)
DATABASE_URL=postgresql://user:password@host:5432/database_name

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Application Configuration
APP_ENV=development
SECRET_KEY=your_secret_key_here
```

**Getting a Neon Database:**
1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project
3. Copy the connection string from the dashboard

**Getting a Qdrant Database:**
1. Go to [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a new cluster
3. Get your API key and cluster URL
4. For local development, you can run Qdrant with Docker:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

### 4. Initialize Database

```bash
python init_db.py
```

This creates the following tables:
- `users` - User profiles and preferences
- `messages` - Chat history
- `user_contexts` - Personalized learning context

### 5. Initialize Qdrant Vector Database

```bash
python init_qdrant.py
```

This creates the `textbook_segments` collection for storing textbook embeddings.

### 6. Ingest Textbook Content

Run the ingestion script to process markdown files and create embeddings:

```bash
python ingest_textbook.py
```

Options:

```bash
# Custom docs directory
python ingest_textbook.py --docs-dir /path/to/docs

# Adjust chunking parameters
python ingest_textbook.py --chunk-size 1000 --chunk-overlap 100

# Clear existing data before ingestion
python ingest_textbook.py --clear-existing
```

### 7. Test RAG Components

Run the test script to verify embeddings and search:

```bash
python test_rag.py
```

With custom query:

```bash
python test_rag.py --query "What is ROS 2?"
```

### 8. Run the Server

```bash
python main.py
```

Or with auto-reload for development:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Register User

```bash
POST /users/?name=John&email=john@example.com&hardware_background=Beginner&software_background=Python developer
```

Response:
```json
{
  "user_id": 1,
  "name": "John",
  "email": "john@example.com",
  "created_at": "2026-03-03T10:00:00"
}
```

### Get User

```bash
GET /users/{user_id}
```

### Chat (RAG-powered)

```bash
POST /chat/?user_id=1&message=What is ROS 2?&session_id=session123
```

Response:
```json
{
  "response": "ROS 2 is a robotic middleware...",
  "context_used": true,
  "context_count": 3,
  "sources": [
    {
      "chapter": "Introduction to ROS 2",
      "module": "module-1-ros2",
      "score": 0.89
    }
  ],
  "user_id": 1
}
```

### Get Chat History

```bash
GET /chat/history/{user_id}?session_id=session123&limit=20
```

## Testing with cURL

### Register a user:
```bash
curl -X POST "http://localhost:8000/users/?name=Test%20User&email=test@example.com"
```

### Send a chat message:
```bash
curl -X POST "http://localhost:8000/chat/?user_id=1&message=Hello&session_id=test1"
```

### Get chat history:
```bash
curl "http://localhost:8000/chat/history/1?session_id=test1&limit=10"
```

## Testing with FastAPI Docs

Open your browser and navigate to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── crud_users.py        # User CRUD operations
├── crud_messages.py     # Message CRUD operations
├── crud_vectors.py      # Vector store CRUD operations
├── vector_store.py      # Qdrant client configuration
├── embeddings.py        # Gemini embeddings generation
├── rag_service.py       # RAG chat service
├── ingest_textbook.py   # Textbook content ingestion script
├── test_rag.py          # RAG component testing script
├── init_db.py           # Database initialization script
├── init_qdrant.py       # Qdrant initialization script
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Database Schema

### Users Table
- `id` - Primary key
- `name` - User's display name
- `email` - Unique email (optional)
- `hardware_background` - Hardware experience
- `software_background` - Software experience
- `created_at` - Timestamp
- `updated_at` - Last update timestamp

### Messages Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `role` - 'user' or 'bot'
- `content` - Message text
- `timestamp` - Message timestamp
- `session_id` - Conversation grouping (optional)

### User Contexts Table
- `id` - Primary key
- `user_id` - Foreign key to users (unique)
- `current_module` - Current study module
- `current_chapter` - Current chapter
- `learning_pace` - slow/standard/fast
- `preferred_detail_level` - beginner/intermediate/advanced
- `topics_mastered` - Comma-separated topic IDs
- `topics_in_progress` - Comma-separated topic IDs

## Next Steps

- [x] Task 2.2: Neon Integration - **COMPLETED**
- [x] Task 2.3: Qdrant Integration - **COMPLETED**
- [x] Task 3.1: Textbook Ingestion Script - **COMPLETED**
- [x] Task 3.2: RAG Chat Logic Implementation - **COMPLETED**
- [ ] Task 4.1: React Chat Component
- [ ] Task 4.2: Frontend Integration
