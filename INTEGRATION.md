# End-to-End Integration Guide

This guide walks you through setting up and testing the complete AI Humanoid Textbook platform with RAG chatbot.

## Prerequisites

- Node.js >= 20.0
- Python >= 3.9
- PostgreSQL database (Neon or local)
- Qdrant vector database (Cloud or local via Docker)
- Gemini API key

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Configuration

### Backend (.env)

```env
# Database (Neon Postgres)
DATABASE_URL=postgresql://user:password@host:5432/database_name

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# App
APP_ENV=development
SECRET_KEY=your_secret_key
```

### Frontend

Edit `frontend/src/theme/Layout.tsx` to configure the backend URL:

```tsx
<Chat 
  apiUrl="http://localhost:8000"  // Change for production
  userId={1} 
/>
```

## Running Locally

### Step 1: Start Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Step 2: Initialize Databases

```bash
# In backend directory
python init_db.py        # Initialize Neon tables
python init_qdrant.py    # Initialize Qdrant collection
```

### Step 3: Ingest Textbook Content

```bash
# In backend directory
python ingest_textbook.py
```

This processes all markdown files from `frontend/docs/` and creates embeddings in Qdrant.

### Step 4: Start Frontend

```bash
cd frontend
npm start
```

Frontend will be available at: http://localhost:3000

### Step 5: Test the Integration

1. Open http://localhost:3000 in your browser
2. Look for the chat widget in the bottom-right corner
3. Click to expand the chat
4. Type a question about the textbook content
5. Verify the AI responds with textbook-based answers

## Testing the Full Stack

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/users/?name=Test%20User&email=test@example.com"
```

Save the `user_id` from the response.

### 2. Send a Chat Message

```bash
curl -X POST "http://localhost:8000/chat/?user_id=1&message=What is ROS 2?"
```

### 3. View Chat History

```bash
curl "http://localhost:8000/chat/history/1?limit=10"
```

### 4. Test RAG Components

```bash
# In backend directory
python test_rag.py --query "What is ROS 2?"
```

## Troubleshooting

### Backend Issues

**Database Connection Error:**
```
Error: Could not connect to database
```
- Verify `DATABASE_URL` in `.env`
- Check Neon console for connection string
- Ensure network access is allowed

**Qdrant Connection Error:**
```
Error: Could not connect to Qdrant
```
- Verify `QDRANT_URL` and `QDRANT_API_KEY`
- For local Qdrant: `docker run -p 6333:6333 qdrant/qdrant`
- For cloud: Check API key in Qdrant Cloud console

**Gemini API Error:**
```
Error: Gemini API error: 403
```
- Verify `GEMINI_API_KEY` is correct
- Check API key has proper permissions
- Ensure quota is not exceeded

### Frontend Issues

**Chat Not Appearing:**
- Check browser console for errors
- Verify `Layout.tsx` exists in `src/theme/`
- Ensure no TypeScript compilation errors

**CORS Errors:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```
- Backend CORS is configured for all origins (development)
- For production, update `allow_origins` in `main.py`

**No Response from Backend:**
- Verify backend is running on port 8000
- Check `apiUrl` in `Layout.tsx` matches backend URL
- Test backend directly: http://localhost:8000/health

### Integration Issues

**Empty Responses:**
- Ensure textbook content is ingested: `python ingest_textbook.py`
- Check Qdrant has vectors: `python test_rag.py`
- Verify Gemini API key is set

**Slow Responses:**
- Check network latency to Qdrant/Gemini
- Reduce chunk size in `ingest_textbook.py`
- Optimize search parameters in `rag_service.py`

## Production Deployment

### Frontend (GitHub Pages)

1. Update `docusaurus.config.ts`:
   ```ts
   url: 'https://yourusername.github.io',
   baseUrl: '/your-repo-name/',
   ```

2. Build and deploy:
   ```bash
   npm run build
   GIT_USER=yourusername npm run deploy
   ```

### Backend (Render/Railway/Vercel)

1. Create `requirements-prod.txt`:
   ```
   fastapi
   uvicorn[standard]
   python-dotenv
   psycopg2-binary
   sqlalchemy
   qdrant-client
   requests
   ```

2. Create `Procfile` (for Render):
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. Set environment variables in hosting platform

4. Update frontend `apiUrl` to production backend URL

### Database (Production)

**Neon:**
- Use production connection string
- Enable connection pooling
- Set up backups

**Qdrant Cloud:**
- Use production cluster URL
- Secure API key
- Configure access controls

## Performance Optimization

### Backend

1. **Connection Pooling:**
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=10,
       max_overflow=20
   )
   ```

2. **Caching:**
   Add Redis for caching frequent queries

3. **Batch Processing:**
   Use batch embeddings for ingestion

### Frontend

1. **Code Splitting:**
   Lazy load chat component

2. **Message Pagination:**
   Load chat history in chunks

3. **Optimistic Updates:**
   Show user messages immediately

## Monitoring

### Backend Health

```bash
# Check API health
curl http://localhost:8000/health

# Check Qdrant
python -c "from vector_store import check_qdrant_connection; print(check_qdrant_connection())"

# Check Database
python -c "from database import SessionLocal; db = SessionLocal(); db.execute('SELECT 1'); print('DB OK')"
```

### Logging

Add logging to `main.py`:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Security Considerations

### Production Checklist

- [ ] Use HTTPS for all API calls
- [ ] Implement proper authentication
- [ ] Rate limit API endpoints
- [ ] Sanitize user inputs
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted origins
- [ ] Implement request validation
- [ ] Add error handling and logging

## Next Steps

After successful integration:

1. **Content Enhancement:**
   - Add more textbook content
   - Improve chunking strategy
   - Add metadata for better search

2. **AI Improvements:**
   - Fine-tune prompts
   - Add conversation memory
   - Implement feedback loop

3. **UI/UX:**
   - Add markdown rendering
   - Implement code highlighting
   - Add chat export feature

4. **Analytics:**
   - Track common questions
   - Monitor response quality
   - A/B test improvements

## Support

For issues or questions:
- Check backend logs
- Review API documentation at `/docs`
- Test components individually
- Verify all environment variables
