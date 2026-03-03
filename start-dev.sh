#!/bin/bash

# Startup script for AI Humanoid Textbook platform
# Runs both backend and frontend development servers

set -e

echo "======================================"
echo "AI Humanoid Textbook Platform"
echo "======================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is set up
echo -e "${BLUE}Checking backend setup...${NC}"
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}Backend virtual environment not found. Creating...${NC}"
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Check if frontend is set up
echo -e "${BLUE}Checking frontend setup...${NC}"
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Frontend dependencies not found. Installing...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Check .env file
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}backend/.env not found. Copying from .env.example...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${YELLOW}Please edit backend/.env with your credentials before continuing.${NC}"
    echo "Press any key to continue or Ctrl+C to cancel..."
    read -n 1
fi

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Starting development servers..."
echo ""
echo -e "${BLUE}Backend:${NC} http://localhost:8000"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
echo -e "${GREEN}Starting backend...${NC}"
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
cd frontend
echo -e "${GREEN}Starting frontend...${NC}"
npm start &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait
