/**
 * ECHO — Gnani AI Timbre v2.5 Text-to-Speech Service
 * 
 * Capabilities:
 * - Natural speech synthesis for Indian languages (Telugu, Hindi, Tamil, etc.) and English
 * - Powers the AI Interviewer voice and Golden English pronunciation feedback
 * - Strict Audio Caching (never regenerates the same phrase, saving credits)
 * - Credit Guard & Mock/Live switchable execution
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const creditManager = require('./creditManager');

const AUDIO_CACHE_DIR = path.join(__dirname, '..', 'cache', 'audio');

class GnaniTimbreService {
  constructor() {
    this.mode = process.env.GNANI_MODE || 'mock';
    this.endpoint = process.env.GNANI_TTS_ENDPOINT || 'https://api.gnani.ai/v1/voice/tts';
    this.apiKey = process.env.GNANI_API_KEY || '';
    this.accessToken = process.env.GNANI_ACCESS_TOKEN || '';
    this.appId = process.env.GNANI_APP_ID || '';

    // Ensure audio cache directory exists
    if (!fs.existsSync(AUDIO_CACHE_DIR)) {
      fs.mkdirSync(AUDIO_CACHE_DIR, { recursive: true });
    }
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
   * Compute unique cache key for a speech request
   */
  _getCacheKey(text, language, voice = 'female') {
    return crypto.createHash('sha256').update(`${text.trim()}_${language}_${voice}`).digest('hex');
  }

  /**
   * Synthesize speech for a given text
   * @param {Object} options
   * @param {string} options.text - Text to convert to speech
   * @param {string} options.language - 'te-IN', 'hi-IN', 'ta-IN', 'en-IN'
   * @param {string} options.voice - 'female' | 'male'
   * @param {boolean} options.userConfirmedLive - Explicit user approval for live call
   */
  async synthesize({ text, language = 'te-IN', voice = 'female', userConfirmedLive = false }) {
    if (!text || text.trim().length === 0) {
      throw new Error('Text to synthesize cannot be empty');
    }

    const cacheKey = this._getCacheKey(text, language, voice);
    const cachedFilePath = path.join(AUDIO_CACHE_DIR, `${cacheKey}.mp3`);

    // 1. Check if cached audio already exists on disk
    if (fs.existsSync(cachedFilePath)) {
      console.log(`[Timbre v2.5] 💾 Serving from local audio cache: ${cacheKey.substring(0, 8)}... (0 Credits Consumed)`);
      creditManager.recordMockSavings('TIMBRE_V2_5_TTS_CACHE', 1, { language, cached: true });
      return {
        audioUrl: `/cache/audio/${cacheKey}.mp3`,
        isCached: true,
        isMock: false,
        model: 'Timbre v2.5 (Cached Local Audio)',
        creditsConsumed: 0
      };
    }

    // 2. Decide between Live Gnani API or Mock
    const isLive = this.mode === 'live' && userConfirmedLive && this.apiKey;

    if (isLive) {
      return await this._callRealTimbreApi({ text, language, voice, cachedFilePath, cacheKey });
    } else {
      return this._executeMockTimbre({ text, language, voice });
    }
  }

  /**
   * Real Gnani Timbre v2.5 API Caller
   */
  async _callRealTimbreApi({ text, language, voice, cachedFilePath, cacheKey }) {
    const costEstimate = creditManager.estimateTtsCost(text);
    console.log(`[Timbre v2.5] ⚡ Calling LIVE Gnani TTS API (${language}). Estimated cost: ${costEstimate.estimatedCredits} credits.`);

    const startTime = Date.now();
    try {
      const headers = {
        'Authorization': `Bearer ${this.accessToken || this.apiKey}`,
        'x-api-key': this.apiKey,
        'x-app-id': this.appId,
        'Content-Type': 'application/json'
      };

      const payload = {
        text: text.trim(),
        language_code: language,
        voice_gender: voice.toUpperCase(),
        audio_encoding: 'MP3',
        model: 'TIMBRE_V2_5'
      };

      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Gnani API responded with HTTP ${response.status}: ${await response.text()}`);
      }

      // Handle binary audio or base64 response
      const contentType = response.headers.get('content-type') || '';
      let audioBuffer;

      if (contentType.includes('application/json')) {
        const json = await response.json();
        const b64 = json.audio_content || json.audio || '';
        audioBuffer = Buffer.from(b64, 'base64');
      } else {
        const arrayBuffer = await response.arrayBuffer();
        audioBuffer = Buffer.from(arrayBuffer);
      }

      // Save to disk cache permanently to prevent ever paying credits for this text again
      fs.writeFileSync(cachedFilePath, audioBuffer);

      const elapsed = Date.now() - startTime;
      creditManager.recordRealUsage('TIMBRE_V2_5_TTS', costEstimate.estimatedCredits, {
        language,
        wordCount: costEstimate.wordCount
      });

      return {
        audioUrl: `/cache/audio/${cacheKey}.mp3`,
        isCached: false,
        isMock: false,
        model: 'Timbre v2.5 (Live Gnani API)',
        latencyMs: elapsed,
        creditsConsumed: costEstimate.estimatedCredits
      };
    } catch (err) {
      console.error('[Timbre v2.5] Live API call failed, falling back to mock:', err.message);
      return {
        ...this._executeMockTimbre({ text, language, voice }),
        warning: `Live Timbre request failed (${err.message}). Defaulted to simulated voice.`
      };
    }
  }

  /**
   * Mock / Simulation Engine for Timbre v2.5 (0 Credits Consumed)
   */
  _executeMockTimbre({ text, language, voice }) {
    const costEstimate = creditManager.estimateTtsCost(text);
    creditManager.recordMockSavings('TIMBRE_V2_5_TTS', costEstimate.estimatedCredits, {
      language,
      wordCount: costEstimate.wordCount
    });

    // In mock mode, the browser Web Speech API synthesizes the speech on the client
    // with exact pitch, rate, and Indian voice selection!
    return {
      audioUrl: null,
      useBrowserSynthesis: true,
      textToSpeak: text,
      language,
      voice,
      model: 'Timbre v2.5 (Simulation via Browser SpeechSynthesis - 0 Credits)',
      creditsConsumed: 0,
      creditsSaved: costEstimate.estimatedCredits,
      isMock: true
    };
  }
}

module.exports = new GnaniTimbreService();
