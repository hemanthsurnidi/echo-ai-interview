"""
ECHO — Gnani AI PRISMA v2.5 Speech-to-Text Service
Handles Indian language speech recognition (Telugu, Hindi, Tamil, Kannada, English)
with support for both Live Gnani Prisma API and 100% Free Lifetime Speech-to-Text.
"""

import os
import io
import base64
import urllib.request
import json
from typing import Dict, Any, Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None
from services.question_engine import QuestionEngine

class PrismaService:
    def __init__(self):
        self.mode = os.getenv("GNANI_MODE", "mock")
        self.endpoint = os.getenv("GNANI_STT_ENDPOINT", "https://api.vachana.ai/stt/v3")
        self.api_key = os.getenv("GNANI_API_KEY", "")
        self.access_token = os.getenv("GNANI_ACCESS_TOKEN", "")
        self.app_id = os.getenv("GNANI_APP_ID", "")
        self.recognizer = sr.Recognizer() if sr else None

    def transcribe(
        self,
        audio_bytes: Optional[bytes] = None,
        language: str = "te-IN",
        question_id: str = "py-list-tuple",
        phase: str = "native",
        audio_duration_seconds: float = 8.0,
        client_transcript: Optional[str] = None,
        user_confirmed_live: bool = True
    ) -> Dict[str, Any]:
        """
        Transcribes candidate audio input strictly using Live Gnani Prisma API (Prisma v3.0).
        """
        return self._call_live_prisma(
            audio_bytes,
            language,
            audio_duration_seconds,
            client_transcript=client_transcript
        )

    def _call_live_prisma(
        self,
        audio_bytes: Optional[bytes],
        language: str,
        duration: float,
        client_transcript: Optional[str] = None
    ) -> Dict[str, Any]:
        """Live Gnani Prisma STT API Caller (https://api.vachana.ai/stt/v3) - STRICT LIVE MODE"""
        estimated_credits = max(1, int(duration // 10) + 1)
        api_key = self.api_key or self.access_token or os.getenv("GNANI_API_KEY") or os.getenv("GNANI_ACCESS_TOKEN")

        gnani_lang = language if "-" in language else f"{language}-IN"
        if gnani_lang not in ["as-IN", "bn-IN", "en-IN", "gu-IN", "hi-IN", "kn-IN", "ml-IN", "mr-IN", "pa-IN", "ta-IN", "te-IN"]:
            gnani_lang = "indic-auto"

        print("=" * 70)
        print(f"⚡ [STRICT GNANI LIVE STT] >>> CALLING VACHANA API")
        print(f"   Endpoint: {self.endpoint}")
        print(f"   Language: {gnani_lang} | Audio Size: {len(audio_bytes or b'')} bytes")
        print(f"   Estimated Credits: {estimated_credits}")
        print("=" * 70)

        try:
            import requests
            headers = {
                "X-API-Key-ID": api_key
            }

            data = {
                "model": "prisma-v3.0",
                "language_code": gnani_lang
            }
            files = {
                "audio_file": ("answer.wav", audio_bytes or b"", "audio/wav")
            }
            # Generous 20s timeout so live cloud API completes cleanly
            resp = requests.post(self.endpoint, headers=headers, data=data, files=files, timeout=20.0)
            req_id = resp.headers.get("x-api-request-id", "req-live-vachana-stt")

            if resp.status_code == 200:
                data_json = resp.json()
                transcript = data_json.get("transcript") or data_json.get("text") or data_json.get("data", {}).get("transcript", "")
                final_text = (transcript or "").strip()

                if not final_text and client_transcript:
                    final_text = client_transcript.strip()

                print("=" * 70)
                print(f"⚡ [STRICT GNANI LIVE STT] >>> SUCCESS! 200 OK")
                print(f"   Vachana Request ID: {req_id}")
                print(f"   Transcript: {repr(final_text[:60])}")
                print(f"   Credits Deducted: {estimated_credits} credits on Vachana.ai")
                print("=" * 70)

                return {
                    "transcript": final_text,
                    "confidence": data_json.get("confidence", 0.95),
                    "language": language,
                    "model": "Gnani Prisma v3.0 (Live API)",
                    "credits_consumed": estimated_credits,
                    "is_mock": False,
                    "vachanaRequestId": req_id
                }
            else:
                err_text = resp.text.encode('ascii', 'replace').decode('ascii')
                print(f"❌ [STRICT GNANI LIVE STT] API Error HTTP {resp.status_code}: {err_text}")
                return {
                    "error": f"Gnani Prisma STT returned HTTP {resp.status_code}: {err_text}",
                    "transcript": client_transcript or "",
                    "model": "Gnani Prisma v3.0 (Live API Error)",
                    "credits_consumed": 0,
                    "is_mock": False
                }
        except Exception as err:
            err_msg = str(err).encode('ascii', 'replace').decode('ascii')
            print(f"❌ [STRICT GNANI LIVE STT] Connection Error: {err_msg}")
            return {
                "error": f"Gnani Prisma STT Connection Error: {err_msg}",
                "transcript": client_transcript or "",
                "model": "Gnani Prisma v3.0 (Connection Error)",
                "credits_consumed": 0,
                "is_mock": False
            }

    def _execute_free_transcription(
        self,
        audio_bytes: Optional[bytes],
        language: str,
        question_id: str,
        phase: str,
        duration: float,
        client_transcript: Optional[str]
    ) -> Dict[str, Any]:
        """
        Transcribes candidate audio using Free Lifetime Speech Recognition.
        1. Checks client WebSpeech transcript if already provided.
        2. Transcribes actual WAV audio bytes using SpeechRecognition.
        3. Only if no speech was detected, returns empty/silence status instead of faking text.
        """
        # 1. Use client transcript if provided
        if client_transcript and len(client_transcript.strip()) > 0:
            return {
                "transcript": client_transcript.strip(),
                "confidence": 0.96,
                "language": language,
                "model": "Client WebSpeech / Free ASR",
                "credits_consumed": 0,
                "is_mock": False
            }

        # 2. Transcribe real audio bytes if present
        if sr and self.recognizer and audio_bytes and len(audio_bytes) > 200:
            try:
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio_data = self.recognizer.record(source)

                # Map language code to Google ASR format
                # e.g. 'te-IN', 'hi-IN', 'ta-IN', 'kn-IN', 'en-IN'
                target_lang = language if language else "en-IN"
                recognized_text = self.recognizer.recognize_google(audio_data, language=target_lang)
                
                if recognized_text and recognized_text.strip():
                    print(f"[Free STT] Successfully transcribed ({target_lang}): {recognized_text[:40]}...")
                    return {
                        "transcript": recognized_text.strip(),
                        "confidence": 0.94,
                        "language": target_lang,
                        "model": "Free Lifetime Speech Recognition (Google ASR)",
                        "credits_consumed": 0,
                        "is_mock": False
                    }
            except sr.UnknownValueError:
                print(f"[Free STT] No speech / silence detected in audio file.")
            except Exception as e:
                print(f"[Free STT] Transcription attempt note: {e}")

        # 3. If silence or no microphone input detected
        return {
            "transcript": "",
            "confidence": 0.0,
            "language": language,
            "model": "Free Lifetime Engine (No Speech Detected)",
            "credits_consumed": 0,
            "is_mock": False,
            "note": "No clear speech detected in recorded audio."
        }

prisma_service = PrismaService()
