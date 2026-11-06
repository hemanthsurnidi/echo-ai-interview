/**
 * ECHO — Express Backend Server
 * 
 * Orchestrates:
 * - Gnani AI Prisma v2.5 (STT) & Timbre v2.5 (TTS)
 * - Reasoning Engine (Evon v3.3 specification / Gemini Flash / Mock)
 * - Credit Guard & Ledger
 * - Static frontend hosting
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const multer = require('multer');

const creditManager = require('./services/creditManager');
const questionBank = require('./services/questionBank');
const prismaService = require('./services/gnaniPrismaService');
const timbreService = require('./services/gnaniTimbreService');
const reasoningAdapter = require('./services/reasoningAdapter');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '20mb' }));
app.use(express.urlencoded({ extended: true, limit: '20mb' }));

// File upload configuration for microphone audio blobs
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 15 * 1024 * 1024 } // 15MB max
});

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'public')));
app.use('/cache/audio', express.static(path.join(__dirname, 'cache', 'audio')));

// ==============================================================
// SYSTEM & CREDIT ENDPOINTS
// ==============================================================

/**
 * Get comprehensive system status
 */
app.get('/api/status', (req, res) => {
  res.json({
    appName: 'ECHO — Bilingual AI Mock Interview Platform',
    gnaniMode: prismaService.getMode(),
    reasoningProvider: reasoningAdapter.getProvider(),
    hasGnaniKey: Boolean(process.env.GNANI_API_KEY),
    hasGeminiKey: Boolean(process.env.GEMINI_API_KEY),
    creditLedger: creditManager.getStatus(),
    supportedLanguages: [
      { code: 'te-IN', name: 'Telugu (తెలుగు)', flag: '🇮🇳' },
      { code: 'hi-IN', name: 'Hindi (हिन्दी)', flag: '🇮🇳' },
      { code: 'ta-IN', name: 'Tamil (தமிழ்)', flag: '🇮🇳' },
      { code: 'kn-IN', name: 'Kannada (ಕನ್ನಡ)', flag: '🇮🇳' },
      { code: 'en-IN', name: 'Indian English', flag: '🇮🇳' }
    ]
  });
});

/**
 * Switch Gnani execution mode between 'mock' and 'live'
 */
app.post('/api/gnani/mode', (req, res) => {
  const { mode } = req.body;
  if (mode !== 'mock' && mode !== 'live') {
    return res.status(400).json({ error: "Invalid mode. Choose 'mock' or 'live'." });
  }

  prismaService.setMode(mode);
  timbreService.setMode(mode);

  res.json({
    success: true,
    mode,
    message: mode === 'mock' 
      ? 'Switched to Simulation Mode (0 Gnani credits will be used).'
      : 'Switched to Live Gnani API Mode. Explicit confirmation will still be required before every live call.'
  });
});

/**
 * Pre-flight credit cost estimator (Credit Safety Guard)
 */
app.post('/api/gnani/estimate', (req, res) => {
  const { service, durationSeconds, text } = req.body;

  if (service === 'stt') {
    return res.json(creditManager.estimateSttCost(durationSeconds || 10));
  } else if (service === 'tts') {
    return res.json(creditManager.estimateTtsCost(text || ''));
  }

  res.status(400).json({ error: 'Specify service as "stt" or "tts"' });
});

// ==============================================================
// QUESTION BANK ENDPOINTS
// ==============================================================

app.get('/api/questions', (req, res) => {
  res.json(questionBank.getQuestions());
});

app.get('/api/questions/:id', (req, res) => {
  const q = questionBank.getQuestionById(req.params.id);
  res.json(q);
});

// ==============================================================
// GNANI PRISMA v2.5 (SPEECH-TO-TEXT)
// ==============================================================

app.post('/api/gnani/stt', upload.single('audioFile'), async (req, res) => {
  try {
    const {
      language = 'te-IN',
      questionId,
      phase = 'native',
      audioDuration = 8,
      clientTranscript = null,
      userConfirmedLive = false
    } = req.body;

    const audioBuffer = req.file ? req.file.buffer : req.body.audio;

    const result = await prismaService.transcribe({
      audio: audioBuffer,
      language,
      questionId,
      phase,
      audioDuration: parseFloat(audioDuration) || 8,
      clientTranscript,
      userConfirmedLive: userConfirmedLive === true || userConfirmedLive === 'true'
    });

    res.json(result);
  } catch (err) {
    console.error('Error in /api/gnani/stt:', err);
    res.status(500).json({ error: err.message });
  }
});

// ==============================================================
// GNANI TIMBRE v2.5 (TEXT-TO-SPEECH)
// ==============================================================

app.post('/api/gnani/tts', async (req, res) => {
  try {
    const {
      text,
      language = 'te-IN',
      voice = 'female',
      userConfirmedLive = false
    } = req.body;

    if (!text) {
      return res.status(400).json({ error: 'Text is required for TTS synthesis.' });
    }

    const result = await timbreService.synthesize({
      text,
      language,
      voice,
      userConfirmedLive: Boolean(userConfirmedLive)
    });

    res.json(result);
  } catch (err) {
    console.error('Error in /api/gnani/tts:', err);
    res.status(500).json({ error: err.message });
  }
});

// ==============================================================
// REASONING & ARTICULATION BRIDGE EVALUATION
// ==============================================================

app.post('/api/reasoning/evaluate', async (req, res) => {
  try {
    const {
      questionId,
      nativeLanguage = 'te-IN',
      nativeTranscript,
      englishTranscript
    } = req.body;

    if (!questionId) {
      return res.status(400).json({ error: 'questionId is required.' });
    }

    const report = await reasoningAdapter.evaluateInterviewAnswer({
      questionId,
      nativeLanguage,
      nativeTranscript,
      englishTranscript
    });

    res.json(report);
  } catch (err) {
    console.error('Error in /api/reasoning/evaluate:', err);
    res.status(500).json({ error: err.message });
  }
});

// Start Server
app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🚀 ECHO Interview Platform running on http://localhost:${PORT}`);
  console.log(`🛡️  Gnani AI Safety Guard: Mode is set to '${prismaService.getMode()}'`);
  console.log(`🧠 Reasoning Provider: '${reasoningAdapter.getProvider()}'`);
  console.log(`=======================================================`);
});
