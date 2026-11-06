/**
 * ECHO — Gnani AI Prisma v2.5 Speech-to-Text Service
 * 
 * Capabilities:
 * - Indian-language speech recognition (Telugu, Hindi, Tamil, Kannada, English)
 * - Regional accents & code-mixed speech recognition
 * - Credit Guard & Mock/Live switchable execution
 */

const creditManager = require('./creditManager');
const questionBank = require('./questionBank');

class GnaniPrismaService {
  constructor() {
    this.mode = process.env.GNANI_MODE || 'mock';
    this.endpoint = process.env.GNANI_STT_ENDPOINT || 'https://api.gnani.ai/v1/voice/stt';
    this.apiKey = process.env.GNANI_API_KEY || '';
    this.accessToken = process.env.GNANI_ACCESS_TOKEN || '';
    this.appId = process.env.GNANI_APP_ID || '';
  }

  getMode() {
    return this.mode;
  }

  setMode(newMode) {
    if (newMode === 'live' || newMode === 'mock') {
      this.mode = newMode;
    }
    return this.mode;
  }

  /**
   * Transcribe an audio input
   * @param {Object} options
   * @param {Buffer|string} options.audio - Audio buffer or base64
   * @param {string} options.language - Language code ('te-IN', 'hi-IN', 'ta-IN', 'en-IN')
   * @param {string} options.questionId - Associated question id (for contextual hints)
   * @param {string} options.phase - 'native' or 'english'
   * @param {number} options.audioDuration - Estimated duration in seconds
   * @param {boolean} options.userConfirmedLive - Explicit flag if user approved live call
   */
  async transcribe({ audio, language = 'te-IN', questionId, phase = 'native', audioDuration = 8, clientTranscript = null, userConfirmedLive = false }) {
    const isLive = this.mode === 'live' && userConfirmedLive && this.apiKey;

    if (isLive) {
      return await this._callRealPrismaApi({ audio, language, audioDuration });
    } else {
      return this._executeMockPrisma({ language, questionId, phase, audioDuration, clientTranscript });
    }
  }

  /**
   * Real Gnani Prisma v2.5 API Caller
   */
  async _callRealPrismaApi({ audio, language, audioDuration }) {
    const costEstimate = creditManager.estimateSttCost(audioDuration);
    console.log(`[Prisma v2.5] ⚡ Calling LIVE Gnani STT API (${language}). Estimated cost: ${costEstimate.estimatedCredits} credits.`);

    const startTime = Date.now();
    try {
      // Gnani AI STT endpoint request
      // Supports multipart or JSON base64 based on standard Gnani voice API
      const headers = {
        'Authorization': `Bearer ${this.accessToken || this.apiKey}`,
        'x-api-key': this.apiKey,
        'x-app-id': this.appId,
        'Content-Type': 'application/json'
      };

      const payload = {
        audio_content: typeof audio === 'string' ? audio : audio.toString('base64'),
        language_code: language,
        encoding: 'LINEAR16_OR_AUTO',
        sample_rate_hertz: 16000,
        model: 'PRISMA_V2_5'
      };

      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Gnani API responded with HTTP ${response.status}: ${await response.text()}`);
      }

      const data = await response.json();
      const elapsed = Date.now() - startTime;

      // Deduct confirmed credits
      creditManager.recordRealUsage('PRISMA_V2_5_STT', costEstimate.estimatedCredits, {
        language,
        duration: audioDuration
      });

      return {
        transcript: data.transcript || data.text || '',
        confidence: data.confidence || 0.95,
        language,
        model: 'Prisma v2.5 (Live Gnani API)',
        latencyMs: elapsed,
        creditsConsumed: costEstimate.estimatedCredits,
        isMock: false
      };
    } catch (err) {
      console.error('[Prisma v2.5] Live API call failed, falling back to mock:', err.message);
      // Fallback cleanly so user is never stranded
      return {
        ...this._executeMockPrisma({ language, audioDuration }),
        warning: `Live Prisma request failed (${err.message}). Safely displayed simulated transcript.`
      };
    }
  }

  /**
   * Mock / Simulation Engine for Prisma v2.5 (0 Credits Consumed)
   */
  _executeMockPrisma({ language, questionId, phase, audioDuration, clientTranscript }) {
    const costEstimate = creditManager.estimateSttCost(audioDuration);
    creditManager.recordMockSavings('PRISMA_V2_5_STT', costEstimate.estimatedCredits, {
      language,
      phase,
      duration: audioDuration
    });

    // 1. If client sent live WebSpeech transcript, use it (giving the user 100% real spoken voice-to-text for free!)
    if (clientTranscript && clientTranscript.trim().length > 0) {
      return {
        transcript: clientTranscript.trim(),
        confidence: 0.96,
        language,
        model: 'Prisma v2.5 (Simulation via Client WebSpeech)',
        creditsConsumed: 0,
        creditsSaved: costEstimate.estimatedCredits,
        isMock: true
      };
    }

    // 2. Otherwise provide high-quality simulated answer from Question Bank
    const q = questionBank.getQuestionById(questionId);
    let sampleTranscript = '';

    if (phase === 'english') {
      sampleTranscript = q.sampleAnswers?.en_hesitant?.text || 
        'In my understanding, this component works with memory and helps run the code efficiently.';
    } else {
      const langKey = language.startsWith('te') ? 'te' :
                      language.startsWith('hi') ? 'hi' :
                      language.startsWith('ta') ? 'ta' : 'te';
      sampleTranscript = q.sampleAnswers?.[langKey]?.text || 
        'ఇది చాలా ముఖ్యమైన కాన్సెప్ట్, మెమరీ మరియు పర్ఫార్మెన్స్ ఆప్టిమైజ్ చేస్తుంది.';
    }

    return {
      transcript: sampleTranscript,
      confidence: 0.94,
      language,
      model: 'Prisma v2.5 (Simulation Mode - 0 Credits Consumed)',
      creditsConsumed: 0,
      creditsSaved: costEstimate.estimatedCredits,
      isMock: true
    };
  }
}

module.exports = new GnaniPrismaService();
