/**
 * ECHO — Client Audio Recorder & Web Audio Visualizer
 * Capabilities:
 * - MediaStream / MediaRecorder for real microphone audio capture
 * - Web Audio API AnalyserNode for live visualizer and volume meters
 * - WebSpeech API integration for real-time speech preview
 * - Pure browser 16kHz Mono WAV encoder for high-accuracy Speech-to-Text
 */

class AudioRecorder {
  constructor() {
    this.audioContext = null;
    this.analyser = null;
    this.mediaStream = null;
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.isRecording = false;
    this.speechRecognition = null;
    this.currentLiveTranscript = '';
    this.latestFullTranscript = '';
    this.volumeCallback = null;
    this._animFrameId = null;

    this._initSpeechRecognition();
  }

  _initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        this.speechRecognition = new SpeechRecognition();
        this.speechRecognition.continuous = true;
        this.speechRecognition.interimResults = true;
      } catch (e) {
        console.warn('[AudioRecorder] SpeechRecognition initialization note:', e);
      }
    }
  }

  /**
   * Prompts the browser explicitly for microphone permissions.
   */
  async requestPermission() {
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        console.log('[AudioRecorder] Requesting browser microphone permissions...');
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());
        console.log('[AudioRecorder] ✓ Browser microphone permission GRANTED');
        return true;
      }
      return false;
    } catch (err) {
      console.warn('[AudioRecorder] Microphone permission denied or dismissed:', err.message);
      return false;
    }
  }

  /**
   * Start recording audio with live visualization and volume callback
   */
  async startRecording({ language = 'te-IN', onTranscriptUpdate, onVolume, visualizerEl }) {
    if (this.isRecording) return;
    this.audioChunks = [];
    this.accumulatedFinalTranscript = '';
    this.currentSessionFinalTranscript = '';
    this.latestFullTranscript = '';
    this.volumeCallback = onVolume || null;

    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({
          audio: {
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
          }
        });
        this.isRecording = true;

        // 1. Setup Web Audio API Analyser for live volume
        try {
          const AudioCtx = window.AudioContext || window.webkitAudioContext;
          this.audioContext = new AudioCtx();
          const source = this.audioContext.createMediaStreamSource(this.mediaStream);
          this.analyser = this.audioContext.createAnalyser();
          this.analyser.fftSize = 128;
          source.connect(this.analyser);

          this._startVolumeMeter();

          if (visualizerEl) {
            visualizerEl.classList.add('active');
          }
        } catch (ctxErr) {
          console.warn('[AudioRecorder] Web Audio visualizer setup note:', ctxErr);
        }

        // 2. Setup MediaRecorder
        try {
          // Prefer webm/opus or default
          const mime = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
            ? 'audio/webm;codecs=opus'
            : MediaRecorder.isTypeSupported('audio/webm')
            ? 'audio/webm'
            : '';
          const options = mime ? { mimeType: mime, audioBitsPerSecond: 128000 } : {};
          this.mediaRecorder = new MediaRecorder(this.mediaStream, options);
          this.mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
              this.audioChunks.push(event.data);
            }
          };
          // Record cleanly without sub-second fragmentation to prevent cluster decode corruption
          this.mediaRecorder.start(1000);
        } catch (recErr) {
          console.warn('[AudioRecorder] MediaRecorder setup note:', recErr);
        }
      }
    } catch (micErr) {
      console.warn('[AudioRecorder] Live mic capture note (permission or device):', micErr);
    }

    // 3. Setup WebSpeech Recognition for live preview with continuous auto-reconnect across pauses
    if (this.speechRecognition) {
      this.speechRecognition.lang = language;
      this.speechRecognition.onresult = (event) => {
        let sessionFinal = '';
        let interimTranscript = '';
        for (let i = 0; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            sessionFinal += event.results[i][0].transcript + ' ';
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }
        this.currentSessionFinalTranscript = sessionFinal;
        const full = (this.accumulatedFinalTranscript + ' ' + sessionFinal + interimTranscript).trim();
        this.latestFullTranscript = full;
        if (onTranscriptUpdate && full) {
          onTranscriptUpdate(this.cleanTechnicalTranscript(full));
        }
      };
      this.speechRecognition.onerror = (e) => {
        console.warn('[AudioRecorder] WebSpeech event note:', e.error);
        if (this.isRecording && e.error !== 'aborted') {
          setTimeout(() => {
            if (this.isRecording) {
              try { this.speechRecognition.start(); } catch (err) {}
            }
          }, 200);
        }
      };
      this.speechRecognition.onend = () => {
        // Automatically reconnect if Chrome ends session during natural speaking pauses
        if (this.isRecording) {
          this.accumulatedFinalTranscript = (this.accumulatedFinalTranscript + ' ' + this.currentSessionFinalTranscript).trim();
          this.currentSessionFinalTranscript = '';
          try {
            this.speechRecognition.start();
            console.log('[AudioRecorder] Continuous speech listener kept alive across pause.');
          } catch (e) {}
        }
      };
      try {
        this.speechRecognition.start();
      } catch (e) {
        // Already started
      }
    }

    console.log('[AudioRecorder] 🎙️ Recording started in language:', language);
  }

  _startVolumeMeter() {
    if (!this.analyser) return;
    const dataArray = new Uint8Array(this.analyser.frequencyBinCount);

    const update = () => {
      if (!this.isRecording) return;
      this.analyser.getByteFrequencyData(dataArray);
      let sum = 0;
      for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
      }
      const avg = sum / dataArray.length;
      const normalizedVolume = Math.min(1.0, avg / 80); // 0.0 to 1.0

      if (this.volumeCallback) {
        this.volumeCallback(normalizedVolume);
      }
      this._animFrameId = requestAnimationFrame(update);
    };
    this._animFrameId = requestAnimationFrame(update);
  }

  /**
   * Stop recording and return raw audioBlob, converted wavBlob, and transcript
   */
  async stopRecording(visualizerEl) {
    if (this._animFrameId) {
      cancelAnimationFrame(this._animFrameId);
      this._animFrameId = null;
    }
    this.isRecording = false;

    if (visualizerEl) {
      visualizerEl.classList.remove('active');
    }

    if (this.speechRecognition) {
      try { this.speechRecognition.stop(); } catch (e) {}
    }

    const rawBlob = await new Promise((resolve) => {
      if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') {
        resolve(this.audioChunks.length ? new Blob(this.audioChunks, { type: 'audio/webm' }) : null);
        return;
      }

      this.mediaRecorder.onstop = () => {
        const b = new Blob(this.audioChunks, { type: 'audio/webm' });
        resolve(b);
      };

      try {
        // Explicitly flush final audio slice before stopping to capture ending words
        if (this.mediaRecorder.state === 'recording') {
          this.mediaRecorder.requestData();
        }
        this.mediaRecorder.stop();
      } catch (e) {
        resolve(this.audioChunks.length ? new Blob(this.audioChunks, { type: 'audio/webm' }) : null);
      }
    });

    // Cleanup audio context & media tracks
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
      this.mediaStream = null;
    }
    if (this.audioContext && this.audioContext.state !== 'closed') {
      try { this.audioContext.close(); } catch (e) {}
    }

    // Convert rawBlob to standard 16kHz mono WAV for high-accuracy Speech Recognition
    let wavBlob = null;
    if (rawBlob && rawBlob.size > 0) {
      try {
        wavBlob = await this.convertToWav(rawBlob);
      } catch (convErr) {
        console.warn('[AudioRecorder] WAV conversion note, using raw blob:', convErr);
        wavBlob = rawBlob;
      }
    }

    const rawTranscript = (this.latestFullTranscript || (this.accumulatedFinalTranscript + ' ' + (this.currentSessionFinalTranscript || '')) || '').trim();
    const cleanedTranscript = this.cleanTechnicalTranscript(rawTranscript);

    return {
      audioBlob: rawBlob,
      wavBlob: wavBlob,
      transcript: cleanedTranscript
    };
  }

  /**
   * Normalizes Indic phonetic misrecognitions for software and cloud terminology.
   */
  cleanTechnicalTranscript(text) {
    if (!text) return '';
    const replacements = [
      [/\bఎస్\s*ఎస్\s*ఆర్\b/gi, 'SSR (Server-Side Rendering)'],
      [/\bఎస్ఎస్ఆర్\b/gi, 'SSR (Server-Side Rendering)'],
      [/\bఎస్ఎస్ ఆర్\b/gi, 'SSR (Server-Side Rendering)'],
      [/\bఅద్భుతమైన\s*ఎస్\b/gi, 'SSR'],
      [/\bనెక్స్ట్\s*(?:డాట్|dot)?\s*జేఎస్\b/gi, 'Next.js'],
      [/\bనెక్స్ట్\s*జే\s*ఎస్\b/gi, 'Next.js'],
      [/\bపైథాన్\b/gi, 'Python'],
      [/\bఫ్లాస్క్\b/gi, 'Flask'],
      [/\bఫాస్ట్\s*ఏపీఐ\b/gi, 'FastAPI'],
      [/\bజావా\s*స్క్రిప్ట్\b/gi, 'JavaScript'],
      [/\bటైప్\s*స్క్రిప్ట్\b/gi, 'TypeScript'],
      [/\bడాకర్\b/gi, 'Docker'],
      [/\bకూబర్నెటీస్\b/gi, 'Kubernetes'],
      [/\bమైక్రో\s*సర్వీసెస్\b/gi, 'Microservices'],
      [/\bడేటాబేస్\b/gi, 'Database'],
      [/\bరియాక్ట్\b/gi, 'React'],
      [/\bఏపీఐ\b/gi, 'API'],
      [/\bఏపిఐ\b/gi, 'API'],
      [/\bitem\s+potency\b/gi, 'idempotency'],
      [/\bitem\s+potent\b/gi, 'idempotent'],
      [/\bready\s+is\b/gi, 'Redis'],
      [/\bread\s+is\b/gi, 'Redis'],
      [/\bcup\s+car\b/gi, 'Kafka'],
      [/\bcough\s+car\b/gi, 'Kafka'],
      [/\bpost\s+grass\b/gi, 'PostgreSQL'],
      [/\bpost\s+grease\b/gi, 'PostgreSQL'],
      [/\bcuberneties\b/gi, 'Kubernetes'],
      [/\bcoobernetes\b/gi, 'Kubernetes'],
      [/\bdock\s+her\b/gi, 'Docker'],
      [/\bmongo\s+db\b/gi, 'MongoDB'],
      [/\brest\s+full\b/gi, 'RESTful'],
      [/\bdead\s+letter\s+(cue|line)\b/gi, 'Dead Letter Queue'],
      [/\basset\s+properties\b/gi, 'ACID properties'],
      [/\basid\s+properties\b/gi, 'ACID properties'],
      [/\bgraphic\s+ql\b/gi, 'GraphQL'],
      [/\bgraph\s+ql\b/gi, 'GraphQL'],
      [/\bweb\s+socket\b/gi, 'WebSocket']
    ];
    let res = text;
    for (const [pattern, rep] of replacements) {
      res = res.replace(pattern, rep);
    }
    return res;
  }

  /**
   * Converts any audio Blob into standard 16kHz 16-bit Mono WAV Blob
   */
  async convertToWav(audioBlob) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const tempCtx = new AudioCtx({ sampleRate: 16000 });
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioBuffer = await tempCtx.decodeAudioData(arrayBuffer);

    const sampleRate = 16000;
    const numChannels = 1;
    const samples = audioBuffer.getChannelData(0);

    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    const writeString = (v, offset, str) => {
      for (let i = 0; i < str.length; i++) {
        v.setUint8(offset + i, str.charCodeAt(i));
      }
    };

    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM
    view.setUint16(22, numChannels, true); // Mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * numChannels * 2, true);
    view.setUint16(32, numChannels * 2, true);
    view.setUint16(34, 16, true); // 16-bit
    writeString(view, 36, 'data');
    view.setUint32(40, samples.length * 2, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i++, offset += 2) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    try { await tempCtx.close(); } catch (e) {}

    return new Blob([view], { type: 'audio/wav' });
  }
}

window.AudioRecorder = AudioRecorder;
