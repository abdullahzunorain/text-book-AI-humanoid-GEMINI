# Technical Plan: Physical AI & Humanoid Robotics Textbook

**Feature**: `003-physical-ai-robotics-textbook`  
**Created**: 2026-03-03
**Status**: Draft

## 1. Architecture Overview
This project uses a standard web architecture:
- **Frontend**: A Docusaurus (React) single-page application for the textbook content.
- **Backend**: A FastAPI (Python) server providing the RAG, personalization, and translation APIs.
- **Database**: Neon Serverless Postgres for user and chat history.
- **Vector Store**: Qdrant Cloud for storing and searching textbook embeddings.
- **AI Services**: Gemini API via the OpenAI SDK for embeddings, chat generation, and content transformation.

## 2. File Structure
The key files for this implementation are:

- `frontend/src/theme/DocItem/Layout/index.tsx`: Wraps every textbook page to add bonus feature buttons.
- `frontend/src/components/Chat/Chat.tsx`: The RAG chat UI.
- `backend/main.py`: The main FastAPI application with all API endpoints.
- `backend/rag_service.py`: Contains all the core AI logic (chat, personalize, translate).
- `backend/embeddings.py`: Handles vector embedding generation via the Gemini API.
- `backend/crud_*.py`: Manages database interactions for users and messages.

## 3. Tech Stack
- **Frontend**: Docusaurus, React, TypeScript
- **Backend**: FastAPI, Python, SQLAlchemy, `uv`
- **Database**: Neon (Postgres)
- **Vector DB**: Qdrant
- **AI SDK**: OpenAI Python SDK (configured for Gemini)

## 4. API Contracts
- **`POST /chat/`**: 
  - Request: `{ "user_id": int, "message": str, "selected_text": Optional[str] }`
  - Response: `{ "response": str, "sources": List }`
- **`POST /personalize/`**: 
  - Request: `{ "user_id": int, "content": str }`
  - Response: `{ "content": str }`
- **`POST /translate/`**: 
  - Request: `{ "content": str }`
  - Response: `{ "content": str }`

## 5. Implementation Strategy
The core functionality is already in place. This implementation will focus on ensuring the bonus features and RAG selection work as intended. We will:
1.  Verify that the `Chat.tsx` component correctly captures and sends selected text.
2.  Ensure the `DocItem/Layout/index.tsx` wrapper correctly fetches the active chapter content and sends it to the backend for personalization/translation.
3.  Add unit or integration tests to validate the backend endpoints.
4.  Update the documentation to reflect the final state.
