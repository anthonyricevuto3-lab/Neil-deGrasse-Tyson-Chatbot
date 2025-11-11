@echo off
echo Starting Neil deGrasse Tyson Chatbot Server...
echo.
uvicorn backend.app:app --port 8000
pause
