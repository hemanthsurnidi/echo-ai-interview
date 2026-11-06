"""
ECHO — Python FastAPI Backend Server
Gnani AI Great Indian AI Internship Challenge 2026
"""

import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from dotenv import load_dotenv
# Load environment configuration FIRST before importing services/routers
load_dotenv(Path(__file__).parent.parent / ".env")
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.config import router as config_router
from routers.intelligence import router as intelligence_router
from routers.questions import router as questions_router
from routers.speech import router as speech_router
from routers.session import router as session_router
from routers.evaluation import router as evaluation_router

app = FastAPI(
    title="ECHO Backend API",
    description="AI-powered bilingual interview preparation platform powered by Gnani AI models",
    version="1.0.0"
)

# Register routers
app.include_router(config_router)
app.include_router(intelligence_router)
app.include_router(questions_router)
app.include_router(speech_router)
app.include_router(session_router)
app.include_router(evaluation_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enforce no-cache for static frontend assets to guarantee latest layout
@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path.endswith((".html", ".css", ".js")) or request.url.path == "/":
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# In-memory credit safety state (defaulting to safe mock mode)
GNANI_MODE = os.getenv("GNANI_MODE", "mock")
TOTAL_CREDITS = int(os.getenv("TOTAL_GNANI_CREDITS", "5000"))
CREDITS_CONSUMED = 0

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "server": "FastAPI",
        "python_version": "3.14.5",
        "framework": "FastAPI + Uvicorn"
    }

@app.get("/api/status")
def system_status():
    current_mode = os.getenv("GNANI_MODE", "live")
    return {
        "appName": "ECHO — Think in Your Language. Speak with Confidence.",
        "gnaniMode": current_mode,
        "isLive": current_mode == "live",
        "creditLedger": {
            "initialBalance": TOTAL_CREDITS,
            "creditsConsumed": CREDITS_CONSUMED,
            "creditsRemaining": TOTAL_CREDITS - CREDITS_CONSUMED,
            "mockCreditsSaved": 0
        },
        "supportedModes": [
            {"id": "mode_a", "name": "English Only"},
            {"id": "mode_b", "name": "Single Indian Language"},
            {"id": "mode_c", "name": "Bilingual (Signature Flow)"}
        ],
        "supportedLanguages": [
            {"code": "en-IN", "name": "English", "flag": "🇮🇳"},
            {"code": "te-IN", "name": "Telugu (తెలుగు)", "flag": "🇮🇳"},
            {"code": "hi-IN", "name": "Hindi (हिन्दी)", "flag": "🇮🇳"},
            {"code": "ta-IN", "name": "Tamil (தமிழ்)", "flag": "🇮🇳"},
            {"code": "kn-IN", "name": "Kannada (ಕನ್ನಡ)", "flag": "🇮🇳"}
        ]
    }

# Mount audio cache directory
AUDIO_CACHE_DIR = Path(__file__).parent.parent / "cache" / "audio"
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/cache/audio", StaticFiles(directory=str(AUDIO_CACHE_DIR)), name="audio_cache")

# Mount static frontend files if public folder exists
PUBLIC_DIR = Path(__file__).parent.parent / "public"
if PUBLIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    print(f">> ECHO FastAPI Server running at http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
