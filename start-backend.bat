@echo off
echo ====================================================
echo   Starting Search-Want Python FastAPI Backend...
echo   API URL:     http://localhost:8000
echo   Swagger UI:  http://localhost:8000/docs
echo ====================================================
cd /d "%~dp0backend"
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

