@echo off
echo ============================================================
echo  Vehicle Health ^& Diagnostics - Backend Server
echo ============================================================
echo.

:: Check if pip dependencies are installed
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo Starting FastAPI server on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server.
echo ============================================================

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
