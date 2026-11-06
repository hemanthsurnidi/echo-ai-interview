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

![ECHO Banner](https://img.shields.io/badge/AI%20Engines-Gnani%20AI%20(Timbre%20v2.5%20%2B%20Prisma%20v3.0)%20%7C%20Google%20Gemini%203.5-06B6D4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-100%25%20Live%20Verified%20(10%2F10%20Pass)-10B981?style=for-the-badge)
![Live Cloud](https://img.shields.io/badge/Gnani%20Cloud-Strict%20Live%20Mode%20Active-8B5CF6?style=for-the-badge)

---

## 🎯 Executive Summary & The Problem ECHO Solves

Across India, millions of aspiring engineers and fresh graduates possess strong technical intellect and intuitive understanding of core computer science principles. However, in high-stakes job interviews conducted exclusively in English:
- Candidates often struggle with spontaneous English vocabulary, leading to hesitation, filler words, and superficial answers.
- Their deep technical reasoning is frequently misjudged as incompetence simply because of the language barrier.
- When explaining in their native tongue (**Telugu, Hindi, Tamil, Kannada**), they demonstrate rich architectural intuition, but existing mock interview platforms only evaluate English articulation.

**ECHO addresses this systemic gap through a Dual-Track Bilingual Interview Workflow:**
1. **Concept First (Mother Tongue)**: Candidates explain their technical solution in their native regional language (transcribed by **Gnani AI Prisma v3.0 STT**).
2. **Articulation Bridge (English)**: Candidates express the same concept in English as they would to an interviewer.
3. **The Semantic Delta**: Powered by **Google Gemini 3.5 Flash Lite**, ECHO computes the exact qualitative and score gap between their conceptual depth and English delivery.
4. **The Golden English Bridge**: Google Gemini synthesizes the highest-standard professional English formulation of the candidate's exact thought, spoken aloud by **Gnani AI Timbre v2.5 TTS** to train natural Indian English cadence.

---

## 🤖 AI Model Architecture & Technical Breakdown

```
                                  ┌─────────────────────────────────────────┐
                                  │       VIRTUAL INTERVIEWER AVATAR        │
                                  │   Dr. Ananya Sharma (Nalini - Female)   │
                                  │   Prof. Vikram Rao   (Deepak - Male)    │
                                  │     (Gnani AI Timbre v2.5 TTS Cloud)    │
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
                     │              GNANI AI PRISMA v3.0 (STT Cloud)           │
                     │       Transcribes Native & English Spoken Audio         │
                     │          Code-Mixed (Tenglish / Hinglish) Ready         │
                     └───────────────────────┬───────────────────┬─────────────┘
                                             │                   │
                            Native Transcript│                   │ English Transcript
                                             ▼                   ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │          GOOGLE GEMINI 3.5 FLASH LITE ENGINE            │
                     │                                                         │
                     │  1. Personalized Question Generator (Resume + ZIP + JD) │
                     │  2. Joint Conceptual Evaluation (Native Transcript)     │
                     │  3. Articulation & Fluency Evaluation (English)         │
                     │  4. Semantic Delta: Technical nuances lost in English   │
                     │  5. The Golden English Bridge: Professional Formulation │
                     └───────────────────────────────┬─────────────────────────┘
                                                     │
                                                     ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │          BILINGUAL DIAGNOSTIC MATRIX & REPORT           │
                     │   • Concept Score (e.g. 7.5/10) vs Fluency (8.5/10)     │
                     │   • Net Articulation Gap Metric (+1.5 pts)              │
                     │   • Master Technical Vocabulary Bank                    │
                     │   • Golden English Bridge Spoken with Timbre v2.5       │
                     │   • Executive Final Diagnostic Report (PDF/JSON Export) │
                     └─────────────────────────────────────────────────────────┘
```

### 1. Gnani AI Timbre v2.5 — Text to Speech (TTS)
- **Role in ECHO**: Speaks interview questions and vocalizes the candidate's Golden Bridge response.
- **Official Voice Mapping**:
  - **Female Interviewer (Dr. Ananya Sharma)**: `Nalini` (`te-IN`, `hi-IN`, `ta-IN`, `kn-IN`, `en-IN`)
  - **Male Interviewer (Prof. Vikram Rao)**: `Deepak` (`te-IN`, `hi-IN`, `ta-IN`, `kn-IN`, `en-IN`)
- **API Endpoint**: `https://api.vachana.ai/api/v1/tts/inference` (Direct Live Cloud API, consumes live Vachana credits).
- **Service Layer**: [`backend/services/timbre_service.py`](backend/services/timbre_service.py).

### 2. Gnani AI Prisma v3.0 — Speech to Text (STT)
- **Role in ECHO**: Transcribes candidate spoken answers in regional languages and English. Handles code-mixed vocabulary (Tenglish, Hinglish) and technical terminology with high confidence (0.95+).
- **API Endpoint**: `https://api.vachana.ai/stt/v3` (Direct Live Cloud API, model `prisma-v3.0`).
- **Service Layer**: [`backend/services/prisma_service.py`](backend/services/prisma_service.py).

### 3. Google Gemini 3.5 Flash Lite — Reasoning & Generation Engine
- **Role in ECHO**: 
  1. **Dynamic Question Generation**: Generates 100% bespoke, non-repeating technical and behavioral questions tailored directly to the candidate's parsed resume, uploaded project codebase archive (`.zip`), public GitHub repository link, and target job description.
  2. **Joint Bilingual Reasoning Evaluation**: Simultaneously evaluates the candidate's native-language reasoning and English delivery. Calculates:
     - **Concept Score (1.0 to 10.0)**: Measures algorithmic and architectural depth.
     - **Fluency Score (1.0 to 10.0)**: Measures English phrasing, hesitation, and structure.
     - **Articulation Delta**: The exact mathematical gap between what the candidate knows and what they communicated in English.
     - **Golden English Bridge**: The clean, high-impact English reformulation of their thought.
- **Model Fallback Cascade**: `gemini-3.5-flash-lite` → `gemini-3.1-flash-lite` → Smart Contextual Engine.
- **Service Layer**: [`backend/services/gemini_generator.py`](backend/services/gemini_generator.py) & [`backend/services/evon_reasoning.py`](backend/services/evon_reasoning.py).

---

## 🧪 Comprehensive 10-Scenario Live Test Matrix (100% Pass)

The platform was subjected to a rigorous 10-scenario end-to-end test suite hitting live Gnani AI and Gemini APIs:

| # | Role | Interviewer Persona | Language & Mode | Track | Gemini Questions | Live Timbre TTS | Live Prisma STT | Result |
|---|------|---------------------|-----------------|-------|------------------|-----------------|-----------------|--------|
| **1** | Full Stack Python & Cloud Engineer | Female (Nalini) | **Telugu + English (Dual)** | Technical | 5 Bespoke | 2 Credits (`te-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **2** | Full Stack Python & Cloud Engineer | Male (Deepak) | **Telugu (Mother Tongue)** | Technical | 5 Bespoke | 1 Credit (`te-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **3** | Machine Learning & AI Engineer | Male (Deepak) | **Hindi + English (Dual)** | Technical | 5 Bespoke | 2 Credits (`hi-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **4** | Machine Learning & AI Engineer | Female (Nalini) | **Hindi (Mother Tongue)** | Technical | 5 Bespoke | 2 Credits (`hi-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **5** | DevOps & Site Reliability Engineer | Female (Nalini) | **English Only** | Technical | 5 Bespoke | 2 Credits (`en-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **6** | DevOps & Site Reliability Engineer | Male (Deepak) | **Tamil + English (Dual)** | Technical | 5 Bespoke | 2 Credits (`ta-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **7** | Full Stack Python & Cloud Engineer | Female (Nalini) | **Kannada + English (Dual)** | HR Round | 5 Bespoke | 1 Credit (`kn-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **8** | Machine Learning & AI Engineer | Male (Deepak) | **Telugu + English (Dual)** | HR Round | 5 Bespoke | 1 Credit (`te-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **9** | Cloud Data Architect | Female (Nalini) | **Tamil + English (Dual)** | Technical | 5 Bespoke | 2 Credits (`ta-IN`) | 1 Credit (0.95 conf) | **PASS** |
| **10** | Engineering Team Lead & Principal SRE | Male (Deepak) | **English Only** | HR Round | 5 Bespoke | 2 Credits (`en-IN`) | 1 Credit (0.95 conf) | **PASS** |

- **Live Gnani Timbre TTS Credits Deducted**: 17 credits on `api.vachana.ai`.
- **Live Gnani Prisma STT Credits Deducted**: 10 credits on `api.vachana.ai`.
- **Overall Result**: **10 / 10 PASS (100% Success)**.

---

## 🚀 Deployment Guide (Git, Render & Hugging Face Spaces)

### 1. Repository Structure
```
echo/
├── backend/
│   ├── main.py                    # FastAPI server & route registration
│   ├── requirements.txt           # Python backend dependencies
│   ├── routers/                   # speech, questions, intelligence, evaluation, session
│   └── services/                  # timbre_service, prisma_service, gemini_generator
├── public/                        # Production frontend (HTML5, CSS3, ES6 JS)
│   ├── index.html                 # Modern glassmorphism UI
│   ├── css/                       # style.css, avatar.css, report.css
│   └── js/                        # app.js, audioRecorder.js, avatarController.js
├── Dockerfile                     # Multi-platform container configuration
├── render.yaml                    # Render Blueprint specification
├── Procfile                       # PaaS process file
└── requirements.txt               # Root production dependencies
```

---

### 2. Deploy to Render (Web Service)

#### Option A: One-Click via Render Blueprint
1. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New +** → **Blueprint**.
2. Connect your GitHub repository: `https://github.com/hemanthsurnidi/echo-ai-interview`.
3. Provide the environment secrets when prompted:
   - `GNANI_API_KEY`: Your live Gnani AI API key (`vach_...`)
   - `GEMINI_API_KEY`: Your Google Gemini API Studio key (`AQ.Ab...`)
4. Click **Apply**. Render will automatically build dependencies and launch your live service.

#### Option B: Manual Web Service
1. In Render, click **New +** → **Web Service** → Select `hemanthsurnidi/echo-ai-interview`.
2. Settings:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
3. Under **Environment Variables**, add:
   - `GNANI_MODE`: `live`
   - `GNANI_API_KEY`: `<your-gnani-api-key>`
   - `GEMINI_API_KEY`: `<your-gemini-key>`
4. Click **Create Web Service**.

---

### 3. Deploy to Hugging Face Spaces (Docker Space)

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Space Name: `echo-ai-interview`, SDK: **Docker** → **Blank**.
3. Under **Settings** → **Variables and secrets**, add:
   - Secret `GNANI_API_KEY`: `<your-gnani-api-key>`
   - Secret `GEMINI_API_KEY`: `<your-gemini-key>`
   - Variable `GNANI_MODE`: `live`
4. Push your repository to the Hugging Face Space remote:
   ```bash
   git remote add hf https://huggingface.co/spaces/<your-username>/echo-ai-interview
   git push hf main
   ```
5. Hugging Face Spaces will automatically build the `Dockerfile` and launch ECHO on port 7860.

---

## 🏷️ Social Sharing & Submission Metadata

- **Organiser**: Gnani AI
- **Challenge**: Great Indian AI Internship Challenge 2026
- **Live AI Models**: Gnani AI Timbre v2.5 (TTS), Gnani AI Prisma v3.0 (STT), Google Gemini 3.5 Flash Lite (Reasoning & Questions)
- **Tags & Mentions**: `@GnaniAI` `#GnaniAI` `#GreatIndianAIInternshipChallenge` `#BilingualAI` `#IndicAI`
