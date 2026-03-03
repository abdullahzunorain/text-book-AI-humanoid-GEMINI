@echo off
REM Startup script for AI Humanoid Textbook platform (Windows)
REM Runs both backend and frontend development servers

echo ======================================
echo AI Humanoid Textbook Platform
echo ======================================
echo.

cd /d "%~dp0"

echo Checking backend setup...
if not exist "backend\venv" (
    echo Backend virtual environment not found. Creating...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

echo Checking frontend setup...
if not exist "frontend\node_modules" (
    echo Frontend dependencies not found. Installing...
    cd frontend
    call npm install
    cd ..
)

if not exist "backend\.env" (
    echo backend\.env not found. Copying from .env.example...
    copy backend\.env.example backend\.env
    echo Please edit backend\.env with your credentials before continuing.
    echo Press any key to continue or Ctrl+C to cancel...
    pause >nul
)

echo.
echo Setup complete!
echo.
echo Starting development servers...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all servers
echo.

REM Start backend in background
cd backend
call venv\Scripts\activate
echo Starting backend...
start /B python main.py
cd ..

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend
cd frontend
echo Starting frontend...
start /B npm start
cd ..

echo.
echo Both servers started!
echo Press any key to exit this window...
pause >nul
