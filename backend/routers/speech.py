"""
ECHO — Speech & Voice Router (Prisma v2.5 STT & Timbre v2.5 TTS)
FastAPI endpoints for speech recognition, voice synthesis, and credit estimations.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from services.prisma_service import prisma_service
from services.timbre_service import timbre_service

router = APIRouter(prefix="/api/gnani", tags=["Speech & Voice"])

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize")
    language: str = Field(default="te-IN", description="Language code")
    voice: str = Field(default="female", description="Voice gender")
    userConfirmedLive: bool = Field(default=False, description="Explicit approval for live credits")
    gnaniApiKey: Optional[str] = Field(default=None, description="Optional Gnani API key")
    gnaniAppId: Optional[str] = Field(default=None, description="Optional Gnani App ID")

class EstimateRequest(BaseModel):
    service: str = Field(default="tts", description="'stt' or 'tts'")
    text: Optional[str] = Field(default="")
    durationSeconds: Optional[float] = Field(default=10.0)

@router.post("/stt")
async def transcribe_speech(
    audioFile: Optional[UploadFile] = File(None),
    language: str = Form("te-IN"),
    questionId: str = Form("py-list-tuple"),
    phase: str = Form("native"),
    audioDuration: float = Form(8.0),
    clientTranscript: Optional[str] = Form(None),
    userConfirmedLive: bool = Form(False),
    gnaniApiKey: Optional[str] = Form(None),
    gnaniAppId: Optional[str] = Form(None)
):
    """
    Transcribes audio using Gnani AI Prisma v2.5 or Free Lifetime Engine.
    """
    if gnaniApiKey:
        prisma_service.api_key = gnaniApiKey
        prisma_service.mode = "live"
    if gnaniAppId:
        prisma_service.app_id = gnaniAppId

    audio_bytes = None
    if audioFile:
        audio_bytes = await audioFile.read()

    result = prisma_service.transcribe(
        audio_bytes=audio_bytes,
        language=language,
        question_id=questionId,
        phase=phase,
        audio_duration_seconds=audioDuration,
        client_transcript=clientTranscript,
        user_confirmed_live=userConfirmedLive
    )

    return result

@router.post("/tts")
def synthesize_speech(payload: TTSRequest):
    """
    Synthesizes speech using Gnani AI Timbre v2.5 or Free Lifetime Neural Engine.
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if payload.gnaniApiKey:
        timbre_service.api_key = payload.gnaniApiKey
        timbre_service.mode = "live"
    if payload.gnaniAppId:
        timbre_service.app_id = payload.gnaniAppId

    result = timbre_service.synthesize(
        text=payload.text,
        language=payload.language,
        voice=payload.voice,
        user_confirmed_live=payload.userConfirmedLive
    )

    return result

class SetModeRequest(BaseModel):
    mode: str = Field(..., description="'live' for Gnani AI Models, or 'mock' for Free Neural Models")

@router.get("/mode")
def get_gnani_mode():
    """Returns current active model engine mode"""
    return {
        "status": "success",
        "gnaniMode": "live",
        "isLive": True,
        "modelName": "Gnani AI Models (Timbre v2.5 & Prisma v3.0) — Strict Live"
    }

@router.post("/mode")
def set_gnani_mode(payload: SetModeRequest):
    """Enforces Gnani AI Live Models strictly"""
    import os
    os.environ["GNANI_MODE"] = "live"
    timbre_service.mode = "live"
    prisma_service.mode = "live"
    return {
        "status": "success",
        "gnaniMode": "live",
        "isLive": True,
        "modelName": "Gnani AI Models (Timbre v2.5 & Prisma v3.0)"
    }

@router.post("/estimate")
def preflight_credit_estimate(payload: EstimateRequest):
    """
    Pre-flight credit safety estimator before executing real Gnani calls.
    """
    if payload.service == "tts":
        return timbre_service.estimate_cost(payload.text or "")
    else:
        duration = payload.durationSeconds or 10.0
        credits_est = max(1, int(duration // 10) + 1)
        return {
            "service": "Prisma v2.5 (STT)",
            "duration_seconds": duration,
            "estimated_credits": credits_est,
            "basis": f"Estimated based on ~{duration}s audio duration"
        }
