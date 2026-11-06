"""
ECHO — Questions Router
FastAPI endpoints for question generation and playlist management.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from services.question_engine import QuestionEngine

router = APIRouter(prefix="/api/questions", tags=["Questions"])

class GenerateSessionRequest(BaseModel):
    role: str = Field(default="python_backend")
    experience_level: Optional[str] = Field(default="fresher")
    count: Optional[int] = Field(default=None)
    question_count: Optional[int] = Field(default=None)
    duration_minutes: Optional[int] = Field(default=15)
    interview_type: Optional[str] = Field(default="technical")
    language: Optional[str] = Field(default=None)
    candidate_profile: Optional[Dict[str, Any]] = None

@router.get("")
def list_questions():
    """Retrieve full curated question bank with Indian language translations"""
    return QuestionEngine.get_all_questions()

@router.get("/{question_id}")
def get_question(question_id: str):
    """Retrieve a single question by ID with expected concepts and rubrics"""
    q = QuestionEngine.get_question_by_id(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

@router.post("/generate-session")
def generate_interview_session_questions(payload: GenerateSessionRequest):
    """
    Generates a personalized question playlist based on the candidate's
    target role, experience level, and optional resume/project evidence.
    """
    profile = payload.candidate_profile or {}
    duration = payload.duration_minutes or profile.get("duration_minutes") or 15
    itype = payload.interview_type or profile.get("interview_type") or "technical"

    playlist = QuestionEngine.generate_session_questions(
        role=payload.role,
        experience_level=payload.experience_level or "fresher",
        candidate_profile=profile,
        duration_minutes=duration,
        interview_type=itype,
        count=payload.question_count or payload.count
    )
    return {
        "success": True,
        "question_count": len(playlist),
        "playlist": playlist,
        "questions": playlist
    }
