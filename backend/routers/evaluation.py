"""
ECHO — Evaluation Router (Evon v3.3 Reasoning Architecture)
FastAPI endpoints for joint bilingual evaluation and articulation matrix generation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from services.evon_reasoning import evon_engine

router = APIRouter(prefix="/api/reasoning", tags=["Reasoning & Evaluation"])

class EvaluateAnswerRequest(BaseModel):
    questionId: str = Field(..., description="ID of question being evaluated")
    nativeLanguage: str = Field(default="te-IN", description="Candidate's mother tongue code")
    nativeTranscript: str = Field(..., description="Transcript of native language explanation")
    englishTranscript: str = Field(..., description="Transcript of English explanation")
    geminiApiKey: Optional[str] = Field(default=None, description="Optional Google Gemini API Key")

class FinalReportRequest(BaseModel):
    candidateName: Optional[str] = "Candidate"
    targetRole: Optional[str] = "Software Engineer"
    nativeLanguage: Optional[str] = "Telugu"
    jobDescription: Optional[str] = ""
    customInstructions: Optional[str] = ""
    evaluations: List[Dict[str, Any]] = []

@router.post("/evaluate")
def evaluate_bilingual_answer(payload: EvaluateAnswerRequest):
    """
    Jointly evaluates both answers to calculate Concept Score, Fluency Score,
    the Articulation Gap, Semantic Delta, and the Golden English Bridge.
    Supports Dual Mode, English-only, or Mother Tongue-only.
    """
    native = (payload.nativeTranscript or "").strip()
    english = (payload.englishTranscript or "").strip()

    if not native and not english:
        native = "Candidate explained concept."
        english = "Candidate explained concept."
    elif not native:
        native = english
    elif not english:
        english = native

    report = evon_engine.evaluate_bilingual_answer(
        question_id=payload.questionId,
        native_language=payload.nativeLanguage,
        native_transcript=native,
        english_transcript=english,
        gemini_api_key=payload.geminiApiKey
    )

    return report

@router.post("/final-report")
def generate_final_report(payload: FinalReportRequest):
    """
    Generates a comprehensive diagnostic report aggregating all question
    evaluations across the session with executive hire recommendation.
    """
    final_report = evon_engine.generate_final_diagnostic_report(payload.dict())
    return final_report

