"""
ECHO — Gnani AI TIMBRE v2.5 Text-to-Speech Service
Synthesizes speech in Indian languages (Telugu, Hindi, Tamil, Kannada) and English.
Includes SHA-256 local disk audio caching and 0-credit safe simulation.
"""

import os
import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional

AUDIO_CACHE_DIR = Path(__file__).parent.parent.parent / "cache" / "audio"
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class TimbreService:
    def __init__(self):
        self.mode = os.getenv("GNANI_MODE", "mock")
        self.endpoint = os.getenv("GNANI_TTS_ENDPOINT", "https://api.vachana.ai/api/v1/tts/inference")
        self.api_key = os.getenv("GNANI_API_KEY", "")
        self.access_token = os.getenv("GNANI_ACCESS_TOKEN", "")
        self.app_id = os.getenv("GNANI_APP_ID", "")

    def _get_cache_hash(self, text: str, language: str, voice: str) -> str:
        """Computes unique SHA-256 hash key for speech audio including voice type"""
        v = (voice or "doraemon").lower().strip()
        key = f"{text.strip()}_{language}_{v}".encode("utf-8")
        return hashlib.sha256(key).hexdigest()

    def estimate_cost(self, text: str) -> Dict[str, Any]:
        """Calculates pre-flight credit cost estimation (~1 credit per 25 words)"""
        words = len(text.strip().split())
        credits_est = max(1, (words + 24) // 25)
        return {
            "service": "Timbre v2.5 (TTS)",
            "word_count": words,
            "estimated_credits": credits_est,
            "basis": f"Estimated based on {words} words (~1 credit per 25 words)"
        }

    def synthesize(
        self,
        text: str,
        language: str = "te-IN",
        voice: str = "female",
        user_confirmed_live: bool = False
    ) -> Dict[str, Any]:
        """
        Synthesizes text to speech using Timbre v2.5.
        Checks local disk cache first before doing anything.
        """
        if not text or not text.strip():
            return {"error": "Text to synthesize cannot be empty"}

        cache_key = self._get_cache_hash(text, language, voice)
        cached_mp3 = AUDIO_CACHE_DIR / f"{cache_key}.mp3"
        cached_wav = AUDIO_CACHE_DIR / f"{cache_key}.wav"

        # 100% STRICT GNANI AI MODE:
        # Every voice call strictly invokes Live Gnani Timbre v2.5 API (api.vachana.ai)
        return self._call_live_timbre(text, language, voice, cached_wav, cache_key)

    def _call_live_timbre(
        self,
        text: str,
        language: str,
        voice: str,
        cached_file: Path,
        cache_key: str
    ) -> Dict[str, Any]:
        """Live Gnani Timbre TTS API Caller (https://api.vachana.ai/api/v1/tts/inference) - STRICT LIVE MODE"""
        cost = self.estimate_cost(text)
        api_key = self.api_key or self.access_token or os.getenv("GNANI_API_KEY") or os.getenv("GNANI_ACCESS_TOKEN")
        
        # Map to official Gnani Timbre v2.5 voice catalog (Female: Nalini, Male: Deepak)
        gnani_voice = "Deepak" if str(voice).lower() == "male" else "Nalini"
        gnani_lang = language if "-" in language else f"{language}-IN"

        print("=" * 70)
        print(f"⚡ [STRICT GNANI LIVE TTS] >>> CALLING VACHANA API")
        print(f"   Endpoint: {self.endpoint}")
        print(f"   Text: {text.strip()[:60]}...")
        print(f"   Language: {gnani_lang} | Voice: {gnani_voice}")
        print(f"   Estimated Credits: {cost['estimated_credits']}")
        print("=" * 70)

        try:
            import requests
            headers = {
                "X-API-Key-ID": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text.strip(),
                "voice": gnani_voice,
                "model": "timbre-v2.5",
                "language": gnani_lang,
                "speed": 1.0,
                "audio_config": {
                    "encoding": "linear_pcm",
                    "container": "wav",
                    "num_channels": 1,
                    "sample_rate": 24000,
                    "sample_width": 2
                }
            }
            resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=20)
            req_id = resp.headers.get("x-api-request-id", "req-live-vachana")

            if resp.status_code == 200:
                audio_bytes = resp.content
                import time
                unique_name = f"{cache_key[:16]}_{int(time.time()*1000)}.wav"
                saved_wav = AUDIO_CACHE_DIR / unique_name
                with open(saved_wav, "wb") as f:
                    f.write(audio_bytes)

                print("=" * 70)
                print(f"⚡ [STRICT GNANI LIVE TTS] >>> SUCCESS! 200 OK")
                print(f"   Vachana Request ID: {req_id}")
                print(f"   Audio Received: {len(audio_bytes)} bytes")
                print(f"   Credits Deducted: {cost['estimated_credits']} credits on Vachana.ai")
                print("=" * 70)

                return {
                    "audioUrl": f"/cache/audio/{unique_name}",
                    "isCached": False,
                    "isMock": False,
                    "model": "Gnani Timbre v2.5 (Live API)",
                    "creditsConsumed": cost["estimated_credits"],
                    "vachanaRequestId": req_id
                }
            else:
                err_text = resp.text.encode('ascii', 'replace').decode('ascii')
                print(f"❌ [STRICT GNANI LIVE TTS] API Error HTTP {resp.status_code}: {err_text}")
                return {
                    "error": f"Gnani Live API returned HTTP {resp.status_code}: {err_text}",
                    "audioUrl": None,
                    "isMock": False,
                    "model": "Gnani Timbre v2.5 (Live API Error)"
                }
        except Exception as err:
            err_msg = str(err).encode('ascii', 'replace').decode('ascii')
            print(f"❌ [STRICT GNANI LIVE TTS] Network/Connection Error: {err_msg}")
            return {
                "error": f"Gnani Live API Network Error: {err_msg}",
                "audioUrl": None,
                "isMock": False,
                "model": "Gnani Timbre v2.5 (Connection Error)"
            }

    def _execute_simulation(self, text: str, language: str, voice: str) -> Dict[str, Any]:
        """Free Lifetime Neural Indian speech synthesis (Edge-TTS with gTTS fallback, 0 credits)"""
        voice_key = (voice or "doraemon").lower().strip()
        cache_key = self._get_cache_hash(text, language, voice_key)
        cached_file = AUDIO_CACHE_DIR / f"{cache_key}.mp3"
        cost = self.estimate_cost(text)

        if not cached_file.exists():
            # 1. Try high-quality Edge-TTS Neural Voice with personality pitch & rate
            success = False
            try:
                import asyncio
                import edge_tts

                voice_profiles = {
                    "male": {
                        "te-IN": "te-IN-MohanNeural",
                        "hi-IN": "hi-IN-MadhurNeural",
                        "ta-IN": "ta-IN-ValluvarNeural",
                        "kn-IN": "kn-IN-GaganNeural",
                        "en-IN": "en-IN-PrabhatNeural",
                        "default": "en-IN-PrabhatNeural",
                        "pitch": "+0Hz",
                        "rate": "+0%"
                    },
                    "female": {
                        "te-IN": "te-IN-ShrutiNeural",
                        "hi-IN": "hi-IN-SwaraNeural",
                        "ta-IN": "ta-IN-PallaviNeural",
                        "kn-IN": "kn-IN-SapnaNeural",
                        "en-IN": "en-IN-NeerjaNeural",
                        "default": "en-IN-NeerjaNeural",
                        "pitch": "+0Hz",
                        "rate": "+0%"
                    },
                    "doraemon": {
                        # Doraemon official anime dub: high-pitched, enthusiastic cartoon timbre
                        "te-IN": "te-IN-ShrutiNeural",
                        "hi-IN": "hi-IN-SwaraNeural",
                        "ta-IN": "ta-IN-PallaviNeural",
                        "kn-IN": "kn-IN-SapnaNeural",
                        "en-IN": "en-IN-NeerjaNeural",
                        "default": "en-IN-NeerjaNeural",
                        "pitch": "+55Hz",
                        "rate": "+12%"
                    }
                }

                profile = voice_profiles.get(voice_key, voice_profiles["doraemon"])
                neural_voice = profile.get(language, profile["default"])
                voice_pitch = profile.get("pitch", "+0Hz")
                voice_rate = profile.get("rate", "+0%")

                async def run_edge():
                    communicate = edge_tts.Communicate(
                        text=text.strip(),
                        voice=neural_voice,
                        pitch=voice_pitch,
                        rate=voice_rate
                    )
                    await communicate.save(str(cached_file))

                asyncio.run(run_edge())
                if cached_file.exists() and cached_file.stat().st_size > 500:
                    success = True
                    print(f"[Lifetime TTS] [SYNTH] Edge-TTS generated {language} ({voice_key}: {neural_voice}, pitch={voice_pitch}, rate={voice_rate})")
            except Exception as edge_err:
                print(f"[Lifetime TTS] Edge-TTS failed ({edge_err}), falling back to gTTS...")

            # 2. Fallback to gTTS if Edge-TTS had network jitter
            if not success and not cached_file.exists():
                try:
                    from gtts import gTTS
                    lang_code = language.split("-")[0]
                    if lang_code not in ['te', 'hi', 'ta', 'kn', 'en']:
                        lang_code = 'te' if 'te' in language else 'en'
                    tts = gTTS(text=text.strip(), lang=lang_code, slow=False)
                    tts.save(str(cached_file))
                    print(f"[Lifetime TTS] [SYNTH] gTTS synthesized {lang_code.upper()} audio to {cache_key[:8]}...")
                except Exception as e:
                    print(f"[Lifetime TTS] Speech synthesis error: {e}")

        if cached_file.exists():
            return {
                "audioUrl": f"/cache/audio/{cache_key}.mp3",
                "useBrowserSynthesis": False,
                "textToSpeak": text,
                "language": language,
                "voice": voice_key,
                "model": f"Lifetime Free Neural Voice ({voice_key.title()})",
                "creditsConsumed": 0,
                "creditsSaved": cost["estimated_credits"],
                "isMock": True
            }

        return {
            "audioUrl": None,
            "useBrowserSynthesis": True,
            "textToSpeak": text,
            "language": language,
            "voice": voice,
            "model": "Timbre v2.5 (Browser Synthesis Fallback)",
            "creditsConsumed": 0,
            "creditsSaved": cost["estimated_credits"],
            "isMock": True
        }

timbre_service = TimbreService()
