@echo off
cd /d "%~dp0backend"
echo ========================================================
echo Starting ECHO Technical Interview Server on port 8000...
echo Open http://127.0.0.1:8000 in your browser
echo ========================================================
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause

