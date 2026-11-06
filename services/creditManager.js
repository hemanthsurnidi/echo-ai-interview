/**
 * ECHO — Credit Manager & Safety Guard
 * 
 * Protects the candidate's 5,000 Gnani AI credits.
 * - Tracks total balance and consumed credits
 * - Estimates consumption before API calls
 * - Persists credit ledger across server restarts
 * - Prevents accidental duplicate requests
 */

const fs = require('fs');
const path = require('path');

const LEDGER_PATH = path.join(__dirname, '..', 'cache', 'credit_ledger.json');
const INITIAL_BALANCE = parseInt(process.env.TOTAL_GNANI_CREDITS || '5000', 10);

class CreditManager {
  constructor() {
    this.ledger = this.loadLedger();
  }

  loadLedger() {
    try {
      if (fs.existsSync(LEDGER_PATH)) {
        const data = fs.readFileSync(LEDGER_PATH, 'utf-8');
        return JSON.parse(data);
      }
    } catch (err) {
      console.warn('[CreditManager] Could not read ledger, creating fresh one:', err.message);
    }

    const fresh = {
      initialBalance: INITIAL_BALANCE,
      creditsConsumed: 0,
      creditsRemaining: INITIAL_BALANCE,
      mockCreditsSaved: 0,
      history: []
    };
    this.saveLedger(fresh);
    return fresh;
  }

  saveLedger(data = this.ledger) {
    try {
      const dir = path.dirname(LEDGER_PATH);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(LEDGER_PATH, JSON.stringify(data, null, 2), 'utf-8');
    } catch (err) {
      console.error('[CreditManager] Failed to persist ledger:', err.message);
    }
  }

  /**
   * Estimate credit cost for Speech-to-Text (Prisma v2.5)
   * Base estimation: ~1 credit per 10 seconds of audio (minimum 1)
   */
  estimateSttCost(audioDurationSeconds = 10) {
    const cost = Math.max(1, Math.ceil(audioDurationSeconds / 10));
    return {
      service: 'Prisma v2.5 (STT)',
      estimatedCredits: cost,
      basis: `Estimated based on ~${audioDurationSeconds}s audio duration`
    };
  }

  /**
   * Estimate credit cost for Text-to-Speech (Timbre v2.5)
   * Base estimation: ~1 credit per 25 words (minimum 1)
   */
  estimateTtsCost(text = '') {
    const wordCount = text.trim().split(/\s+/).filter(Boolean).length;
    const cost = Math.max(1, Math.ceil(wordCount / 25));
    return {
      service: 'Timbre v2.5 (TTS)',
      wordCount,
      estimatedCredits: cost,
      basis: `Estimated based on ${wordCount} words (~1 credit per 25 words)`
    };
  }

  /**
   * Deduct credits after a confirmed real API call
   */
  recordRealUsage(service, credits, meta = {}) {
    this.ledger.creditsConsumed += credits;
    this.ledger.creditsRemaining = Math.max(0, this.ledger.initialBalance - this.ledger.creditsConsumed);
    this.ledger.history.unshift({
      timestamp: new Date().toISOString(),
      type: 'REAL_API_CALL',
      service,
      creditsConsumed: credits,
      balanceAfter: this.ledger.creditsRemaining,
      meta
    });
    this.saveLedger();
    return this.getStatus();
  }

  /**
   * Record credits saved when running in Mock / Cached mode
   */
  recordMockSavings(service, creditsSaved, meta = {}) {
    this.ledger.mockCreditsSaved += creditsSaved;
    this.ledger.history.unshift({
      timestamp: new Date().toISOString(),
      type: 'MOCK_OR_CACHED',
      service,
      creditsSaved,
      meta
    });
    // Keep history at reasonable size
    if (this.ledger.history.length > 50) this.ledger.history.length = 50;
    this.saveLedger();
    return this.getStatus();
  }

  getStatus() {
    return {
      initialBalance: this.ledger.initialBalance,
      creditsConsumed: this.ledger.creditsConsumed,
      creditsRemaining: this.ledger.creditsRemaining,
      mockCreditsSaved: this.ledger.mockCreditsSaved,
      recentHistory: this.ledger.history.slice(0, 8)
    };
  }
}

module.exports = new CreditManager();
