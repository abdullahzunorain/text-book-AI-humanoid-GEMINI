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

### Core Features

- **📖 Interactive Textbook**: Modern, responsive documentation site built with Docusaurus
- **🤖 AI Chatbot**: RAG-powered teaching assistant embedded in the site
- **🎯 Smart Search**: Semantic search across all textbook content
- **💬 Context-Aware**: Remembers conversation history for better responses
- **📊 User Personalization**: Tracks learning progress and preferences

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
             │   Neon      │  │  Qdrant   │  │   Gemini    │
             │  Postgres   │  │  Vector   │  │     AI      │
             │  (Chat)     │  │    DB     │  │  (Embeddings)│
             └─────────────┘  └───────────┘  └─────────────┘
```

## 📦 Tech Stack

### Frontend
- **Docusaurus 3** - Documentation framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Vanilla CSS** - Styling with CSS modules

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Neon** - Serverless PostgreSQL
- **Qdrant** - Vector database
- **Gemini API** - AI embeddings and generation

## 📖 Course Modules

1. **Module 1: The Robotic Nervous System (ROS 2)**
   - ROS 2 Nodes, Topics, and Services
   - Python with rclpy
   - URDF robot descriptions

2. **Module 2: The Digital Twin (Gazebo & Unity)**
   - Physics simulation
   - Sensor simulation (LiDAR, IMU)
   - Human-robot interaction

3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)**
   - Isaac Sim & SDK
   - Perception pipelines
   - Reinforcement learning

4. **Module 4: Vision-Language-Action (VLA)**
   - LLMs for planning
   - Voice-to-action with Whisper
   - Autonomous humanoid capstone

## 🛠️ Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd book-project
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
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
python init_db.py        # Initialize Neon
python init_qdrant.py    # Initialize Qdrant
python ingest_textbook.py # Ingest textbook content
```

### 5. Run Servers

```bash
# Option 1: Use startup script
./start-dev.sh  # or start-dev.bat on Windows

# Option 2: Run separately
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2 - Frontend
cd frontend && npm start
```

## 📝 Documentation

- **[Integration Guide](INTEGRATION.md)** - Complete setup and testing guide
- **[Backend README](backend/README.md)** - Backend API documentation
- **[Chat Component](frontend/src/components/Chat/README.md)** - Chat UI documentation

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Test RAG components
python test_rag.py --query "What is ROS 2?"

# Test API (open Swagger UI)
# Navigate to http://localhost:8000/docs
```

### Frontend Tests

```bash
cd frontend

# Type check
npm run typecheck

# Build test
npm run build
```

## 📊 API Endpoints

### Health Check
```
GET /health
```

### User Management
```
POST /users/?name=John&email=john@example.com
GET /users/{user_id}
```

### Chat (RAG-powered)
```
POST /chat/?user_id=1&message=What is ROS 2?&session_id=session123
GET /chat/history/{user_id}?limit=20
```

## 🚀 Deployment

### Frontend (GitHub Pages)

```bash
cd frontend
npm run build
GIT_USER=yourusername npm run deploy
```

### Backend (Render/Railway)

1. Connect repository to hosting platform
2. Set environment variables
3. Deploy automatically on push

See [INTEGRATION.md](INTEGRATION.md) for detailed deployment instructions.

## 🎯 Development Workflow

This project uses **Spec-Driven Development (SDD)** with SpecifyPlus:

- `/sp.specify` - Create feature specifications
- `/sp.plan` - Generate architecture plans
- `/sp.tasks` - Break into tasks
- `/sp.phr` - Record prompt history
- `/sp.adr` - Document architectural decisions

## 📁 Project Structure

```
book-project/
├── backend/                 # FastAPI backend
│   ├── main.py             # API routes
│   ├── database.py         # Database connection
│   ├── models.py           # SQLAlchemy models
│   ├── crud_*.py           # CRUD operations
│   ├── rag_service.py      # RAG chat service
│   ├── ingest_textbook.py  # Content ingestion
│   └── requirements.txt    # Python dependencies
├── frontend/               # Docusaurus frontend
│   ├── docs/              # Textbook content
│   ├── src/
│   │   ├── components/    # React components
│   │   │   └── Chat/      # Chat component
│   │   └── theme/         # Custom theme
│   │       └── Layout.tsx # Layout with chat
│   └── docusaurus.config.ts
├── specs/                  # Feature specifications
│   └── mvp/               # MVP spec
├── history/               # Prompt history records
│   └── prompts/
├── .specify/              # SpecifyPlus config
├── INTEGRATION.md         # Integration guide
├── start-dev.sh           # Dev startup (Linux/macOS)
└── start-dev.bat          # Dev startup (Windows)
```

## ✅ Implementation Status

- [x] Task 1.1: Initialize Docusaurus
- [x] Task 1.2: Structure Course Modules
- [x] Task 1.3: Configure GitHub Pages
- [x] Task 2.1: FastAPI Boilerplate
- [x] Task 2.2: Neon Integration
- [x] Task 2.3: Qdrant Integration
- [x] Task 3.1: Textbook Ingestion Script
- [x] Task 3.2: RAG Chat Logic
- [x] Task 4.1: React Chat Component
- [x] Task 4.2: End-to-End Integration
- [ ] Task 5.1: Deployment

## 🔐 Security

- Environment variables for all secrets
- CORS configured for production
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy ORM

## 🤝 Contributing

1. Create feature branch: `git checkout -b 001-feature-name`
2. Make changes following SDD principles
3. Create PHR for significant work
4. Submit pull request

## 📄 License

[Add your license here]

## 👥 Authors

- Abdullah Zunorain

## 🙏 Acknowledgments

- Panaversity Spec-Kit Plus for SDD framework
- Docusaurus team
- FastAPI team
- Qdrant team
- Gemini AI
