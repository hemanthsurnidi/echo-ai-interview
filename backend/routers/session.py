"""
ECHO — Session Router
FastAPI endpoints for managing the bilingual interview state machine.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from services.interview_session import session_manager

router = APIRouter(prefix="/api/session", tags=["Interview Session"])

class StartSessionRequest(BaseModel):
    role: str = Field(default="python_backend")
    language_mode: str = Field(default="mode_c")
    primary_language: str = Field(default="te-IN")
    candidate_profile: Optional[Dict[str, Any]] = None
    count: int = Field(default=3)

class SubmitAnswerRequest(BaseModel):
    session_id: str
    phase: str  # 'native' or 'english'
    transcript: str

class AdvanceQuestionRequest(BaseModel):
    session_id: str

@router.post("/start")
def start_session(payload: StartSessionRequest):
    """Initializes an interactive interview session with the 7-turn state machine"""
    session = session_manager.create_session(
        role=payload.role,
        language_mode=payload.language_mode,
        primary_language=payload.primary_language,
        candidate_profile=payload.candidate_profile,
        count=payload.count
    )
    return session

@router.get("/{session_id}")
def get_session_status(session_id: str):
    """Retrieve active turn progress and question state"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/submit-answer")
def submit_session_answer(payload: SubmitAnswerRequest):
    """Submits answer for active turn (native or english) and advances turn state"""
    updated = session_manager.submit_answer(
        session_id=payload.session_id,
        phase=payload.phase,
        transcript=payload.transcript
    )
    if "error" in updated:
        raise HTTPException(status_code=400, detail=updated["error"])
    return updated

@router.post("/next-question")
def advance_to_next_question(payload: AdvanceQuestionRequest):
    """Advances session to the next question playlist item"""
    res = session_manager.advance_question(payload.session_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res
