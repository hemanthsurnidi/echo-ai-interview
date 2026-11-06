# ECHO — System Architecture Specification
**Think in Your Language. Speak with Confidence.**

---

## 🏛️ High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          ECHO CLIENT (Vite + React)                    │
│                                                                        │
│  ┌─────────────────────────┐   ┌────────────────────────────────────┐  │
│  │    VIRTUAL INTERVIEWER  │   │     DUAL-TRACK RESPONSE STATION    │  │
│  │   • Avatar States       │   │   • Step 1: Native Audio Stream    │  │
│  │   • Waveform Visualizer │   │   • Step 2: English Audio Stream   │  │
│  │   • Audio Player (TTS)  │   │   • MediaRecorder API Capture      │  │
│  └─────────────────────────┘   └────────────────────────────────────┘  │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                  BILINGUAL ARTICULATION REPORT                   │  │
│  │   • Concept Score (Native)  vs  Fluency Score (English)          │  │
│  │   • Semantic Delta: Technical nuances lost in translation        │  │
│  │   • Golden English Bridge Sentence Frames & Audio Feedback       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ HTTPS / REST (JSON & Multipart)
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        ECHO BACKEND (Python FastAPI)                   │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     SAFETY & CREDIT GUARD LAYER                  │  │
│  │   • Ledger Tracker (5,000 Gnani Credits Safe Storage)            │  │
│  │   • Pre-flight Consumption Estimator                             │  │
│  │   • Explicit User Authorization Verification                     │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────┐ │
│  │  PRISMA v2.5 STT │  │  TIMBRE v2.5 TTS │  │ EVON REASONING ADAPTER│ │
│  │  • Indian Langs  │  │  • Indian Voice  │  │ • Bilingual Evaluator │ │
│  │  • Live / Mock   │  │  • Disk Cache    │  │ • Mock / Gemini / Evon│ │
│  └──────────────────┘  └──────────────────┘  └───────────────────────┘ │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │               DOCUMENT & PROJECT INTELLIGENCE (Optional)         │  │
│  │   • PyMuPDF / python-docx (Resume parsing)                       │  │
│  │   • Safe ZIP Analyzer & GitHub REST API Inspector                │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Signature Feature: The Bilingual Paired-Question Workflow (Mode C)

For every interview question, ECHO enforces this strict pedagogical progression:

```
[1. INTERVIEWER SPEAKS IN NATIVE LANGUAGE]
   Timbre v2.5 voices question (e.g., Telugu: "పైథాన్‌లో లిస్ట్‌లు మరియు ట్యుపుల్స్ మధ్య తేడా ఏమిటి?")
                         │
                         ▼
[2. CANDIDATE ANSWERS IN NATIVE LANGUAGE]
   Microphone records answer; Prisma v2.5 transcribes native speech (0 credit mock or live)
                         │
                         ▼
[3. INTERVIEWER SPEAKS EXACT SAME QUESTION IN ENGLISH]
   Timbre v2.5 voices English question ("Explain the difference between lists and tuples in Python.")
                         │
                         ▼
[4. CANDIDATE ANSWERS IN ENGLISH]
   Microphone records English answer; Prisma v2.5 transcribes English speech
                         │
                         ▼
[5. JOINT REASONING EVALUATION]
   Both answers evaluated TOGETHER:
   - Technical comprehension scored from native answer.
   - English fluency & hesitation scored from English answer.
   - Conceptual gaps (what candidate knew but couldn't say in English) extracted.
                         │
                         ▼
[6. ARTICULATION REPORT & GOLDEN BRIDGE]
   Displays side-by-side comparison, missing engineering terminology, and speaks the golden answer!
```

---

## 🛡️ Gnani AI Credit Guard Policy

1. **Default Mode = `mock`**: The application launches in Simulation Mode. All speech-to-text, text-to-speech, and evaluation run locally with zero credit drain.
2. **Pre-flight Estimation**: Before any real request is dispatched to Gnani AI, the backend calculates the exact credit requirement (e.g. ~1 credit per 10s audio for Prisma, ~1 credit per 25 words for Timbre).
3. **Explicit Modal Approval**: A confirmation modal appears in the UI requiring the user's manual approval before sending any live request.
4. **Permanent Audio Caching**: Any synthesized voice response is hashed (SHA-256) and saved to disk. Identical questions or sentences are never sent to Gnani twice.
