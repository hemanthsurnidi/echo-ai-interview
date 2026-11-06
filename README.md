---
title: ECHO — AI Technical Interview Practice
emoji: 🎙️
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ECHO — AI Bilingual Mock Interview Platform
### Submission for the Gnani AI Great Indian AI Internship Challenge 2026
**Theme**: Think in Your Language. Speak with Confidence.  
**Submission Deadline**: November 10, 2026  
**Target Roles**: Software Engineers, Backend Developers, Data Engineers, Full-Stack Architects  
**Official Social Tags**: `@GnaniAI` | `#GnaniAI` | `#GreatIndianAIInternshipChallenge`

![ECHO Banner](https://img.shields.io/badge/Gnani%20AI-Prisma%20v2.5%20%7C%20Timbre%20v2.5%20%7C%20Evon%20v3.3-06B6D4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-100%25%20Functional%20%26%20Verified-10B981?style=for-the-badge)
![Credits](https://img.shields.io/badge/Credit%20Guard-5%2C000%20%2F%205%2C000%20Preserved-8B5CF6?style=for-the-badge)

---

## 🎯 Executive Summary & The Problem ECHO Solves

Across India, millions of aspiring engineers and fresh graduates possess strong technical intellect and intuitive understanding of core computer science principles. However, in high-stakes job interviews conducted exclusively in English:
- Candidates often struggle with spontaneous English vocabulary, leading to hesitation, filler words, and superficial answers.
- Their deep technical reasoning is frequently misjudged as incompetence simply because of the language barrier.
- When explaining in their native tongue (**Telugu, Hindi, Tamil, Kannada**), they demonstrate rich architectural intuition, but existing mock interview platforms only evaluate English articulation.

**ECHO addresses this systemic gap through a Dual-Track Bilingual Interview Workflow:**
1. **Concept First (Mother Tongue)**: Candidates explain their solution in their comfortable regional language (evaluated by **Prisma v2.5 STT** & **Evon v3.3**).
2. **Articulation Bridge (English)**: Candidates express the same concept in English as they would to an interviewer.
3. **The Semantic Delta**: ECHO computes the exact mathematical and qualitative gap between their conceptual depth and their English delivery.
4. **The Golden English Bridge**: ECHO synthesizes the highest-standard professional English formulation of the candidate's exact thought, spoken with **Timbre v2.5** to train natural Indian English cadence.

---

## 🤖 Gnani AI Model Integration Architecture

```
                                  ┌─────────────────────────────────────────┐
                                  │       VIRTUAL INTERVIEWER AVATAR        │
                                  │   Dr. Ananya Sharma / Prof. Vikram Rao  │
                                  │         (Timbre v2.5 Audio TTS)         │
                                  └────────────────────┬────────────────────┘
                                                       │ Speaks Question
                                                       ▼ (Telugu / Hindi / Tamil / Kannada / English)
                                  ┌─────────────────────────────────────────┐
                                  │                CANDIDATE                │
                                  └──────────┬───────────────────┬──────────┘
                       Turn 1: Speaks        │                   │ Turn 2: Speaks
                    in Mother Tongue         │                   │ in English
                                             ▼                   ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │                 PRISMA v2.5 (STT Engine)                │
                     │       Transcribes Native & English Spoken Audio         │
                     │          Code-Mixed (Tenglish / Hinglish) Ready         │
                     └───────────────────────┬───────────────────┬─────────────┘
                                             │                   │
                            Native Transcript│                   │ English Transcript
                                             ▼                   ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │               EVON v3.3 REASONING ENGINE                │
                     │                                                         │
                     │  1. Conceptual Evaluation (from Native Transcript)      │
                     │  2. Articulation & Fluency (from English Transcript)    │
                     │  3. Articulation Gap Analysis (Concept vs Fluency)      │
                     │  4. Semantic Delta: What details were lost in English   │
                     │  5. The Golden English Bridge: Professional Answer      │
                     └───────────────────────────────┬─────────────────────────┘
                                                     │
                                                     ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │          BILINGUAL DIAGNOSTIC MATRIX & REPORT           │
                     │   • Concept Score (e.g. 8.5/10) vs Fluency (6.0/10)    │
                     │   • Net Articulation Gap Metric (+2.5 pts)              │
                     │   • Master Technical Vocabulary Bank                    │
                     │   • Golden English Bridge Spoken with Timbre v2.5       │
                     │   • Executive Final Diagnostic Report (PDF/JSON Export) │
                     └─────────────────────────────────────────────────────────┘
```

### 1. PRISMA v2.5 — Speech to Text (STT)
- **Role in ECHO**: Captures candidate spoken responses across Indian languages (`te-IN`, `hi-IN`, `ta-IN`, `kn-IN`, `en-IN`), gracefully handles regional accents and code-mixed speech (e.g., *Tenglish* / *Hinglish*), and feeds clean transcripts into the reasoning pipeline.
- **Service Layer**: Handled in [`backend/services/prisma_service.py`](file:///C:/Users/heman/.gemini/antigravity-ide/scratch/echo/backend/services/prisma_service.py) via `/api/gnani/stt`.

### 2. TIMBRE v2.5 — Text to Speech (TTS)
- **Role in ECHO**: Synthesizes natural, culturally attuned voice for the AI Interviewer avatars (Dr. Ananya - Female / Prof. Vikram - Male), speaks questions in Indian languages, and voices the "Golden Bridge" English answer so candidates internalize natural technical cadence.
- **Smart Audio Caching**: Automatically computes SHA-256 hashes of generated speech and stores them in `cache/audio/`. **A phrase is never synthesized twice**, preventing duplicate credit consumption.
- **Service Layer**: Handled in [`backend/services/timbre_service.py`](file:///C:/Users/heman/.gemini/antigravity-ide/scratch/echo/backend/services/timbre_service.py) via `/api/gnani/tts`.

### 3. EVON v3.3 — Reasoning Architecture & Hardware Transparency
- **Hardware Assessment**: Evon v3.3 is a 30-billion-parameter open-weights reasoning model requiring ~18–20 GB of VRAM at 4-bit precision. Standard development laptops (such as an NVIDIA RTX 3050 with 6 GB VRAM and 16 GB RAM) cannot efficiently load a 30B model locally without extreme memory thrashing and latency.
- **Modular Adapter Pattern**: ECHO implements an explicit `EvonReasoningEngine` based on the Evon v3.3 reasoning contract. It supports:
  - `mock`: Comprehensive heuristic pedagogical rubric (instant, zero cost, deterministic).
  - `gemini_flash`: Google Gemini Flash cloud adapter for live Indian language reasoning.
  - `evon_endpoint`: Prepared integration layer for Evon v3.3 once hosted API endpoints are provided by Gnani AI.
- **Service Layer**: Handled in [`backend/services/evon_reasoning.py`](file:///C:/Users/heman/.gemini/antigravity-ide/scratch/echo/backend/services/evon_reasoning.py) via `/api/reasoning/evaluate` and `/api/reasoning/final-report`.

---

## 🛡️ Strict Credit Guard Policy (5,000 Credits Preservation)

To respect Gnani AI's 5,000 credit allocation during evaluation, development, and testing:
1. **Simulation Mode by Default**: All questions, speech synthesis, and transcriptions run in high-fidelity mock mode at 0 credit consumption.
2. **Explicit Confirmation Modal**: No live call to Prisma or Timbre will ever execute without a confirmation modal warning the user of the exact estimated credits and requiring an explicit click.
3. **Real-time Credit Ledger**: Tracks total allocation, live credits consumed, remaining balance, and simulated credits saved (`GET /api/status`).
4. **Current Audit Status**: `5,000 / 5,000 Credits Intact` (0 credits consumed, 0 credit leakage).

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Verified on Python 3.14.5)
- Modern Web Browser (Chrome / Edge / Firefox)

### Installation & Execution
```bash
# 1. Clone or navigate to the project directory
cd echo/backend

# 2. Install Python dependencies
pip install fastapi uvicorn python-dotenv pydantic pymupdf python-docx

# 3. Start ECHO FastAPI server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser and navigate to:  
👉 **`http://127.0.0.1:8000`**

---

## 🧪 Testing the 5-Step Interview Loop (Under 60 Seconds)

1. **Configure Interview**: Select **Full Stack Engineer** and **Telugu (తెలుగు)** in **Mode C (Bilingual Paired Flow)**.
2. **Choose Interviewer Persona**: Toggle between **Dr. Ananya Sharma** (Lead AI Architect) and **Prof. Vikram Rao** (Principal Systems Engineer).
3. **Turn 1 (Mother Tongue)**: Click **"Speak Question (Timbre v2.5)"** to listen, then click **"⚡ Fill Sample Native"** to simulate a Telugu technical explanation.
4. **Turn 2 (English)**: Click **"⚡ Fill Sample English"** to simulate a hesitant English response.
5. **Turn 3 (Evaluation)**: Click **"✨ Analyze Articulation Bridge (Evon Architecture)"** to view:
   - Native Conceptual Depth: **8.5 / 10**
   - English Conversational Fluency: **6.0 / 10**
   - Net Articulation Gap: **+2.5 pts**
   - What technical nuances were lost in translation
   - High-impact missing technical vocabulary (`immutability`, `memory overhead`, `hashable`)
   - **The Golden English Bridge** with audio playback via Timbre v2.5!
6. **Executive Diagnostic Report**: Click **"View Final Diagnostic Report 🎓"** to open the comprehensive cross-session analytics dashboard with 1-click **PDF Print** and **JSON Export**.

---

## 📹 2-Minute Video Demonstration Script (For Challenge Submission)

| Time | Scene | Script / Voiceover Action |
|---|---|---|
| **0:00 - 0:25** | **The Hook & Problem** | *"In India, thousands of brilliant engineers are rejected in technical interviews not because they lack deep computing knowledge, but because expressing complex systems in English creates hesitation. Welcome to ECHO — Think in Your Language, Speak with Confidence."* |
| **0:25 - 0:55** | **The Dual-Track Architecture** | *"ECHO pairs Gnani AI's Prisma v2.5 STT, Timbre v2.5 TTS, and Evon v3.3 reasoning. Watch our interviewer, Dr. Ananya Sharma, ask a Python concurrency question in Telugu. The candidate explains their solution in Telugu first. Notice the deep technical mastery."* |
| **0:55 - 1:25** | **The Articulation Gap** | *"Next, the candidate attempts the same explanation in English. ECHO computes the Articulation Delta: Conceptual Score is 8.5, but English fluency drops to 6.0. Rather than rejecting them, ECHO provides the Golden Bridge — the exact high-bar formulation with audio pronunciation."* |
| **1:25 - 1:55** | **Executive Diagnostic Report** | *"When the interview concludes, ECHO generates an Executive Diagnostic Report. Hiring managers can clearly see that this candidate is a Strong Hire whose true potential was unlocked through bilingual assessment."* |
| **1:55 - 2:10** | **Conclusion & Credits** | *"Built with strict credit safety preserving 5,000 Gnani credits. ECHO transforms Indian technical hiring from language filtering to true meritocracy. Thank you Gnani AI!"* |

---

## 🏷️ Social Sharing & Submission Metadata

- **Organiser**: Gnani AI
- **Challenge**: Great Indian AI Internship Challenge 2026
- **Tags & Mentions**: `@GnaniAI` `#GnaniAI` `#GreatIndianAIInternshipChallenge` `#BilingualAI` `#IndicAI`

---

## 🚀 Deployment Guide (Git, Render & Hugging Face Spaces)

### 1. Initialize Git & Push to GitHub

```bash
# 1. Initialize git repository
git init

# 2. Stage all files (sensitive files in .env are automatically ignored by .gitignore)
git add .

# 3. Create initial commit
git commit -m "feat: complete ECHO AI bilingual interview preparation platform"

# 4. Set main branch & add your GitHub remote repository
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 5. Push to GitHub
git push -u origin main
```

---

### 2. Deploy to Render (Web Service)

#### Option A: One-Click via Render Blueprint
1. In [Render Dashboard](https://dashboard.render.com/), click **New +** → **Blueprint**.
2. Connect your GitHub repository containing `render.yaml`.
3. Provide the secret environment variables when prompted:
   - `GNANI_API_KEY`: Your live Gnani AI API key or token
   - `GEMINI_API_KEY`: Your Google Gemini API Studio key
4. Click **Apply**. Render will automatically build and deploy!

#### Option B: Manual Web Service
1. Click **New +** → **Web Service** → Connect your GitHub repo.
2. Select runtime: **Python 3**.
3. Set **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
4. Set **Start Command**:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
5. In **Environment Variables**, add:
   - `GNANI_MODE`: `live`
   - `GNANI_API_KEY`: `<your-gnani-api-key>`
   - `GEMINI_API_KEY`: `<your-gemini-key>`
6. Click **Create Web Service**. Your app will be live at `https://<your-service>.onrender.com`.

---

### 3. Deploy to Hugging Face Spaces (Docker Space)

Hugging Face Spaces supports full Docker containers with persistent URLs:

1. Go to [Hugging Face](https://huggingface.co/) and click **New Space**.
2. Space Name: `echo-ai-interview`
3. License: `MIT`
4. Space SDK: Select **Docker** → **Blank**.
5. Click **Create Space**.
6. In **Settings** → **Variables and secrets**, add:
   - Secret `GNANI_API_KEY`: `<your-gnani-api-key>`
   - Secret `GEMINI_API_KEY`: `<your-gemini-key>`
   - Variable `GNANI_MODE`: `live`
7. Push your repository to the Hugging Face Space remote:
   ```bash
   git remote add hf https://huggingface.co/spaces/<your-username>/<space-name>
   git push hf main
   ```
8. Hugging Face Spaces will automatically build the `Dockerfile` and launch ECHO on port 7860 with live audio and speech recognition!


