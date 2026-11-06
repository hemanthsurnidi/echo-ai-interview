"""
ECHO — Interview Configuration Router
Handles 1-Click Onboarding, Role Selection, and Language Modes (A, B, C)
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

router = APIRouter(prefix="/api/config", tags=["Configuration"])

class InterviewConfigRequest(BaseModel):
    role: str = Field(default="python_backend", description="Target job role")
    experience_level: str = Field(default="fresher", description="fresher | intermediate | senior")
    interview_type: str = Field(default="technical", description="technical | behavioral | mixed")
    language_mode: str = Field(default="mode_c", description="mode_a (English) | mode_b (Single) | mode_c (Bilingual)")
    primary_language: str = Field(default="te-IN", description="Mother tongue language code")
    duration_minutes: int = Field(default=15, description="Target interview duration in minutes")
    question_count: int = Field(default=3, description="Number of questions in session")

@router.get("/options")
def get_configuration_options():
    """Return all selectable roles, language modes, and interview types"""
    return {
        "roles": [
            {"id": "python_backend", "title": "Python & Backend Developer", "icon": "🐍", "desc": "APIs, Mutability, Memory, Concurrency, Architecture"},
            {"id": "frontend_react", "title": "Frontend Engineer (React)", "icon": "⚛️", "desc": "Virtual DOM, State Management, Render Cycle, Performance"},
            {"id": "dsa_sde", "title": "Data Structures & Algorithms (SDE)", "icon": "⚡", "desc": "Hash Tables, Tree Traversal, Graphs, Dynamic Programming"},
            {"id": "ai_ml", "title": "AI & Machine Learning Engineer", "icon": "🧠", "desc": "Overfitting, Gradient Descent, Transformers, Evaluation Metrics"},
            {"id": "hr_behavioral", "title": "HR & Behavioral (STAR Method)", "icon": "🤝", "desc": "Difficult Bugs, Team Conflict, Project Ownership, Problem Solving"}
        ],
        "language_modes": [
            {
                "id": "mode_c",
                "name": "Mode C: Bilingual Interview (Signature Mode)",
                "recommended": True,
                "badge": "ECHO Special",
                "description": "Interviewer asks in your mother tongue first, you answer in your native language, then express the exact same concept in English. Evaluates technical depth independently from fluency."
            },
            {
                "id": "mode_b",
                "name": "Mode B: Single Indian Language",
                "recommended": False,
                "badge": "Native Focus",
                "description": "Entire interview conducted in your selected regional Indian language (Telugu, Hindi, Tamil, Kannada)."
            },
            {
                "id": "mode_a",
                "name": "Mode A: English Only",
                "recommended": False,
                "badge": "Standard",
                "description": "Standard English technical interview with real-time fluency scoring and feedback."
            }
        ],
        "supported_languages": [
            {"code": "te-IN", "name": "Telugu (తెలుగు)", "flag": "🇮🇳"},
            {"code": "hi-IN", "name": "Hindi (हिन्दी)", "flag": "🇮🇳"},
            {"code": "ta-IN", "name": "Tamil (தமிழ்)", "flag": "🇮🇳"},
            {"code": "kn-IN", "name": "Kannada (ಕನ್ನಡ)", "flag": "🇮🇳"},
            {"code": "en-IN", "name": "English", "flag": "🇮🇳"}
        ],
        "experience_levels": [
            {"id": "fresher", "label": "College Student / Fresher (0-1 yrs)"},
            {"id": "intermediate", "label": "Junior / Mid-Level (1-3 yrs)"},
            {"id": "senior", "label": "Senior Developer (3+ yrs)"}
        ]
    }

@router.post("/create-session")
def create_interview_session(config: InterviewConfigRequest):
    """Initializes a new customized interview session in seconds without mandatory uploads"""
    session_id = f"echo_{uuid.uuid4().hex[:10]}"
    
    return {
        "success": True,
        "session_id": session_id,
        "config": config.model_dump(),
        "status": "ready",
        "message": f"Session created for {config.role} in {config.language_mode}. Ready to begin immediately."
    }
