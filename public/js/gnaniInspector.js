/**
 * ECHO — Gnani AI Inspector & Credit Guard Controller
 * 
 * Manages:
 * - Real-time Credit Ledger display (5,000 credits allocated)
 * - Safe switching between Mock Mode and Live Gnani APIs
 * - Explicit user confirmation modal before any live API call
 * - Pre-flight credit consumption estimator
 */

class GnaniInspector {
  constructor() {
    this.modalEl = document.getElementById('modal-inspector');
    this.confirmModalEl = document.getElementById('modal-credit-confirm');
    this.btnOpen = document.getElementById('btn-open-inspector');
    this.btnClose = document.getElementById('btn-close-inspector');
    this.btnToggleMode = document.getElementById('btn-toggle-gnani-mode');
    this.btnCalcEstimate = document.getElementById('btn-calc-estimate');
    this.btnCancelCreditCall = document.getElementById('btn-cancel-credit-call');
    this.btnApproveCreditCall = document.getElementById('btn-approve-credit-call');

    this.pendingConfirmCallback = null;
    this.currentStatus = null;

    this._bindEvents();
    this.fetchStatus();
  }

  _bindEvents() {
    if (this.btnOpen) {
      this.btnOpen.addEventListener('click', () => this.open());
    }

    if (this.btnClose) {
      this.btnClose.addEventListener('click', () => this.close());
    }

    if (this.btnToggleMode) {
      this.btnToggleMode.addEventListener('click', () => this.toggleMode());
    }

    if (this.btnCalcEstimate) {
      this.btnCalcEstimate.addEventListener('click', () => this.calculateEstimate());
    }

    if (this.btnCancelCreditCall) {
      this.btnCancelCreditCall.addEventListener('click', () => {
        this.confirmModalEl.style.display = 'none';
        if (this.pendingConfirmCallback) this.pendingConfirmCallback(false);
      });
    }

    if (this.btnApproveCreditCall) {
      this.btnApproveCreditCall.addEventListener('click', () => {
        this.confirmModalEl.style.display = 'none';
        if (this.pendingConfirmCallback) this.pendingConfirmCallback(true);
      });
    }

    // Close on outside click
    window.addEventListener('click', (e) => {
      if (e.target === this.modalEl) this.close();
    });
  }

  open() {
    this.fetchStatus();
    if (this.modalEl) this.modalEl.style.display = 'flex';
  }

  close() {
    if (this.modalEl) this.modalEl.style.display = 'none';
  }

  /**
   * Fetch current system status and credit ledger from backend
   */
  async fetchStatus() {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      this.currentStatus = data;
      this.renderStatus(data);
      return data;
    } catch (err) {
      console.error('[GnaniInspector] Failed to fetch status:', err);
    }
  }

  renderStatus(data) {
    if (!data) return;

    // Navbar pills
    const remainingValEl = document.getElementById('credit-remaining-val');
    const modeTagEl = document.getElementById('credit-mode-tag');

    if (remainingValEl) {
      remainingValEl.textContent = data.creditLedger.creditsRemaining.toLocaleString();
    }

    if (modeTagEl) {
      if (data.gnaniMode === 'live') {
        modeTagEl.textContent = 'LIVE API ACTIVE';
        modeTagEl.className = 'credit-tag live-tag';
      } else {
        modeTagEl.textContent = 'SAFE (MOCK)';
        modeTagEl.className = 'credit-tag mock-tag';
      }
    }

    // Modal ledger numbers
    const initialEl = document.getElementById('stat-initial-credits');
    const consumedEl = document.getElementById('stat-consumed-credits');
    const modalRemainingEl = document.getElementById('stat-remaining-credits');
    const savedEl = document.getElementById('stat-saved-credits');

    if (initialEl) initialEl.textContent = data.creditLedger.initialBalance.toLocaleString();
    if (consumedEl) consumedEl.textContent = data.creditLedger.creditsConsumed.toLocaleString();
    if (modalRemainingEl) modalRemainingEl.textContent = data.creditLedger.creditsRemaining.toLocaleString();
    if (savedEl) savedEl.textContent = (data.creditLedger.mockCreditsSaved || 0).toLocaleString();

    // Mode Toggle UI
    const headingEl = document.getElementById('current-mode-heading');
    const descEl = document.getElementById('current-mode-desc');
    const btnToggle = document.getElementById('btn-toggle-gnani-mode');

    if (data.gnaniMode === 'live') {
      if (headingEl) {
        headingEl.textContent = 'Current Mode: LIVE GNANI APIS ACTIVE';
        headingEl.style.color = 'var(--accent-amber)';
      }
      if (descEl) {
        descEl.innerHTML = 'Live API mode enabled. Every request will deduct from your 5,000 Gnani credits. <em>Explicit confirmation will still be required before every live call.</em>';
      }
      if (btnToggle) {
        btnToggle.textContent = 'Switch to Safe Simulation Mode';
        btnToggle.className = 'btn btn-secondary';
      }
    } else {
      if (headingEl) {
        headingEl.textContent = 'Current Mode: SIMULATION / MOCK (SAFE)';
        headingEl.style.color = 'var(--accent-emerald)';
      }
      if (descEl) {
        descEl.innerHTML = 'High-fidelity simulation active. Uses browser speech and cached responses. <strong>Zero credits</strong> will be consumed from your 5,000 challenge allocation.';
      }
      if (btnToggle) {
        btnToggle.textContent = 'Switch to Live Gnani APIs';
        btnToggle.className = 'btn btn-toggle-mode';
      }
    }
  }

  async toggleMode() {
    const currentMode = this.currentStatus ? this.currentStatus.gnaniMode : 'mock';
    const newMode = currentMode === 'live' ? 'mock' : 'live';

    try {
      const res = await fetch('/api/gnani/mode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: newMode })
      });
      const data = await res.json();
      await this.fetchStatus();
    } catch (err) {
      alert('Failed to toggle mode: ' + err.message);
    }
  }

  /**
   * Pre-flight cost calculator
   */
  async calculateEstimate() {
    const textInput = document.getElementById('input-estimate-text');
    const resultBox = document.getElementById('estimate-result-box');
    const text = textInput ? textInput.value : '';

    if (!text.trim()) return;

    try {
      const res = await fetch('/api/gnani/estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service: 'tts', text })
      });
      const data = await res.json();

      if (resultBox) {
        resultBox.style.display = 'block';
        resultBox.innerHTML = `
          <strong>Estimated Cost for Timbre v2.5:</strong> ~${data.estimatedCredits} credits (${data.wordCount} words).<br>
          <span style="color: var(--accent-emerald);">In simulation/mock mode: 0 credits consumed.</span>
        `;
      }
    } catch (err) {
      console.error(err);
    }
  }

  /**
   * Trigger explicit user confirmation dialog before any live API call
   */
  confirmLiveCall({ serviceName, estimatedCost }) {
    return new Promise((resolve) => {
      this.pendingConfirmCallback = resolve;

      const serviceEl = document.getElementById('confirm-service-name');
      const costEl = document.getElementById('confirm-cost-val');
      const remainingEl = document.getElementById('confirm-remaining-val');

      if (serviceEl) serviceEl.textContent = serviceName;
      if (costEl) costEl.textContent = `~${estimatedCost} Credits`;
      if (remainingEl && this.currentStatus) {
        remainingEl.textContent = this.currentStatus.creditLedger.creditsRemaining.toLocaleString();
      }

      if (this.confirmModalEl) {
        this.confirmModalEl.style.display = 'flex';
      }
    });
  }
}

window.GnaniInspector = GnaniInspector;
