/**
 * ECHO — Doraemon Technical Interviewer Controller
 * Features:
 * - Big Still Doraemon Face
 * - Multi-engine audio playback (Gnani Timbre + Lifetime Free Edge-TTS)
 * - Supports Telugu, Hindi, Tamil, Kannada, English
 */

class AvatarController {
  constructor() {
    this.stageEl = document.getElementById('avatar-container');
    this.canvas = document.getElementById('avatar-canvas');
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.statusTextEl = document.getElementById('avatar-status-text');
    this.portraitImg = document.getElementById('avatar-portrait');
    this.roomPortraitImg = document.getElementById('room-avatar-portrait');
    this.liveEqualizer = document.getElementById('live-equalizer');
    this.cadenceSelect = document.getElementById('cadence-select');

    this.state = 'idle'; // 'idle' | 'speaking' | 'listening' | 'thinking'
    this.speechCadence = 1.0;
    this.currentVoice = 'female'; // 'male' | 'female'
    this.currentInterviewerKey = 'female';
    this.audioElement = new Audio();
    this.currentSpeechId = 0;

    // Professional Corporate Recruiter Interviewers (Clean Studio Headshots)
    this.interviewers = {
      female: {
        id: 'female',
        name: 'Female Interviewer',
        role: 'Engineering Hiring Manager',
        imgSrc: 'assets/female_interviewer_clean.jpg',
        fallbackSrc: 'assets/female_interviewer.jpg',
        voice: 'female'
      },
      male: {
        id: 'male',
        name: 'Male Interviewer',
        role: 'Senior Technical Recruiter',
        imgSrc: 'assets/male_interviewer_clean.jpg',
        fallbackSrc: 'assets/male_interviewer.jpg',
        voice: 'male'
      }
    };

    this._initCanvas();
    this._initEventListeners();
    this.setInterviewer('female');
  }

  _initCanvas() {
    if (!this.canvas || !this.stageEl) return;
    const rect = this.stageEl.getBoundingClientRect();
    this.canvas.width = rect.width || 600;
    this.canvas.height = rect.height || 340;
  }

  _initEventListeners() {
    if (this.cadenceSelect) {
      this.cadenceSelect.addEventListener('change', (e) => {
        this.speechCadence = parseFloat(e.target.value) || 1.0;
      });
    }

    window.addEventListener('resize', () => {
      this._initCanvas();
    });
  }

  setInterviewer(interviewerKey = 'female') {
    const key = (interviewerKey in this.interviewers) ? interviewerKey : 'female';
    const info = this.interviewers[key];
    this.currentInterviewerKey = key;
    this.currentVoice = info.voice;

    // 1. Update Lobby Portrait
    if (this.portraitImg) {
      this.portraitImg.onerror = () => {
        this.portraitImg.onerror = null;
        this.portraitImg.src = info.fallbackSrc;
      };
      this.portraitImg.src = info.imgSrc;
      this.portraitImg.alt = info.name;
    }

    // 2. Update Fullscreen Room Portrait
    if (this.roomPortraitImg) {
      this.roomPortraitImg.onerror = () => {
        this.roomPortraitImg.onerror = null;
        this.roomPortraitImg.src = info.fallbackSrc;
      };
      this.roomPortraitImg.src = info.imgSrc;
      this.roomPortraitImg.alt = info.name;
    }

    // 3. Name & Badges
    const theaterTitle = document.getElementById('theater-persona-title');
    if (theaterTitle) theaterTitle.textContent = info.name;

    const roomName = document.getElementById('room-interviewer-name');
    if (roomName) roomName.textContent = info.name;

    const labelName = document.getElementById('interviewer-display-name');
    if (labelName) labelName.textContent = info.name;

    console.log('[AvatarController] Switched interviewer to:', info.name, 'with voice:', info.voice);
  }

  setPersona(personaKey = 'female') {
    this.setInterviewer(personaKey);
  }

  setVoice(voiceKey = 'female') {
    const validVoices = ['male', 'female'];
    if (validVoices.includes(voiceKey)) {
      this.currentVoice = voiceKey;
      console.log('[AvatarController] Voice selected:', voiceKey);
    }
  }

  setState(newState, statusMessage = null) {
    this.state = newState;

    if (this.stageEl) {
      this.stageEl.classList.remove('idle', 'speaking', 'listening', 'thinking');
      this.stageEl.classList.add(newState);
    }

    if (this.liveEqualizer) {
      this.liveEqualizer.className = `live-equalizer active ${newState}`;
    }

    const roomStatus = document.getElementById('room-interviewer-status-text');
    if (roomStatus) {
      if (statusMessage) {
        roomStatus.textContent = statusMessage;
      } else {
        const defaultMessages = {
          idle: 'Ready to Ask',
          speaking: 'Speaking Question...',
          listening: 'Listening to your answer...',
          thinking: 'Evaluating answer...'
        };
        roomStatus.textContent = defaultMessages[newState] || 'Ready';
      }
    }
  }

  /**
   * Speaks the question or message.
   * Queries backend /api/gnani/tts (routes to Gnani Timbre or Free Edge-TTS depending on mode).
   */
  async speak(param1, param2 = 'te-IN') {
    this.currentSpeechId = (this.currentSpeechId || 0) + 1;
    const speechId = this.currentSpeechId;

    let text = '';
    let language = 'te-IN';
    let audioUrl = null;
    let onStart = null;
    let onEnd = null;

    if (typeof param1 === 'string') {
      text = param1;
      language = param2 || 'te-IN';
    } else if (typeof param1 === 'object' && param1 !== null) {
      text = param1.text || '';
      language = param1.language || 'te-IN';
      audioUrl = param1.audioUrl || null;
      onStart = param1.onStart || null;
      onEnd = param1.onEnd || null;
    }

    if (!text || !text.trim()) {
      console.warn('[AvatarController] No text provided to speak.');
      return;
    }

    this.setState('speaking', 'Speaking Question...');
    if (onStart) onStart();

    // 1. Fetch audio from backend (Strict Gnani Live API or Free Edge-TTS depending on mode)
    if (!audioUrl) {
      try {
        const isGnaniStrict = (window.echoEngineMode === 'gnani' || !window.echoEngineMode || window.echoEngineMode === 'live');
        const voiceToSend = (this.currentVoice === 'male') ? 'male' : 'female';
        
        console.log(`[AvatarController] Requesting TTS: voice=${voiceToSend}, lang=${language}, strictGnani=${isGnaniStrict}`);
        
        const resp = await fetch('/api/gnani/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: text,
            language: language,
            voice: voiceToSend,
            userConfirmedLive: true
          })
        });

        // If stopped while fetch was in progress, cancel immediately!
        if (this.currentSpeechId !== speechId) {
          console.log('[AvatarController] Speech cancelled during fetch.');
          if (onEnd) onEnd();
          return;
        }

        if (resp.ok) {
          const data = await resp.json();
          if (data && data.audioUrl) {
            audioUrl = data.audioUrl;
            if (data.creditsConsumed && window.showCreditToast) {
              window.showCreditToast(`⚡ Live Gnani API (Timbre v2.5): ~${data.creditsConsumed} credit deducted on Vachana.ai (Req: ${data.vachanaRequestId || 'ok'})`);
            }
          } else if (data && data.error) {
            console.error('[AvatarController] Live Gnani TTS API returned error:', data.error);
            if (window.showCreditToast) {
              window.showCreditToast(`❌ Gnani TTS Error: ${data.error}`, true);
            }
          }
        } else {
          const errBody = await resp.text();
          console.error('[AvatarController] HTTP Error calling /api/gnani/tts:', resp.status, errBody);
        }
      } catch (e) {
        console.warn('[AvatarController] Backend TTS call error:', e);
      }
    }

    // Check again before playing
    if (this.currentSpeechId !== speechId) {
      if (onEnd) onEnd();
      return;
    }

    // 2. Play the native audio through Audio element
    if (audioUrl) {
      try {
        this.audioElement.src = audioUrl;
        this.audioElement.playbackRate = this.speechCadence;
        await this.audioElement.play();

        return new Promise((resolve) => {
          this.audioElement.onended = () => {
            this.setState('listening', 'Listening to your answer...');
            if (onEnd) onEnd();
            resolve();
          };
          this.audioElement.onerror = (e) => {
            console.warn('[AvatarController] Audio element error:', e);
            this.setState('listening', 'Listening to your answer...');
            if (onEnd) onEnd();
            resolve();
          };
        });
      } catch (err) {
        console.warn('[AvatarController] Audio play failed:', err);
      }
    }

    // Check before Web Speech fallback
    if (this.currentSpeechId !== speechId) {
      if (onEnd) onEnd();
      return;
    }

    // In Strict Gnani mode: DO NOT use browser speech synthesis so tests are 100% genuine!
    if (window.echoEngineMode === 'gnani' || window.echoEngineMode === 'live') {
      console.warn('[AvatarController] Strict Gnani Mode: Browser Web Speech fallback is disabled to guarantee only authentic Gnani models are tested.');
      this.setState('listening', 'Ready');
      if (onEnd) onEnd();
      return;
    }

    // 3. Fallback: Browser Web SpeechSynthesis (Only in Free Mock Mode)
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      window.speechSynthesis.resume();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language;
      if (this.currentVoice === 'doraemon') {
        utterance.pitch = 1.45;
        utterance.rate = 1.12 * this.speechCadence;
      } else if (this.currentVoice === 'female') {
        utterance.pitch = 1.1;
        utterance.rate = 1.0 * this.speechCadence;
      } else {
        utterance.pitch = 0.95;
        utterance.rate = 1.0 * this.speechCadence;
      }

      const voices = window.speechSynthesis.getVoices();
      let match = voices.find(v => v.lang === language || v.lang.startsWith(language.split('-')[0]));
      if (!match) {
        match = voices.find(v => v.lang.includes('IN') || v.name.includes('India'));
      }
      if (match) utterance.voice = match;

      return new Promise((resolve) => {
        utterance.onend = () => {
          this.setState('listening', 'Listening to your answer...');
          if (onEnd) onEnd();
          resolve();
        };
        utterance.onerror = () => {
          this.setState('listening', 'Listening to your answer...');
          if (onEnd) onEnd();
          resolve();
        };
        window.speechSynthesis.speak(utterance);
      });
    } else {
      this.setState('listening', 'Listening to your answer...');
      if (onEnd) onEnd();
    }
  }

  stopSpeech() {
    this.currentSpeechId = (this.currentSpeechId || 0) + 1;
    if (this.audioElement) {
      this.audioElement.pause();
      this.audioElement.currentTime = 0;
      this.audioElement.removeAttribute('src');
      try { this.audioElement.load(); } catch (e) {}
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    this.setState('idle', 'Ready');
  }
}

window.AvatarController = AvatarController;
