/**
 * ECHO — Reasoning Adapter & Articulation Bridge Engine
 * 
 * Modular Reasoning Architecture:
 * - Designed around the Evon v3.3 reasoning specification
 * - Pluggable providers: 'mock' (default), 'gemini_flash', 'groq', 'evon_adapter'
 * - Evaluates technical depth (Native) vs English fluency (Articulation)
 * - Identifies the semantic delta (what was lost in translation)
 * - Generates the "Golden Bridge" sentence frames
 */

const questionBank = require('./questionBank');

class ReasoningAdapter {
  constructor() {
    this.provider = process.env.REASONING_PROVIDER || 'mock';
    this.geminiKey = process.env.GEMINI_API_KEY || '';
    this.groqKey = process.env.GROQ_API_KEY || '';
  }

  getProvider() {
    return this.provider;
  }

  setProvider(newProvider) {
    this.provider = newProvider;
    return this.provider;
  }

  /**
   * Run the Bilingual Articulation Evaluation
   */
  async evaluateInterviewAnswer({
    questionId,
    nativeLanguage,
    nativeTranscript,
    englishTranscript
  }) {
    const question = questionBank.getQuestionById(questionId);

    // If Gemini key is available and configured, use live Gemini Flash
    if (this.provider === 'gemini_flash' && this.geminiKey) {
      try {
        return await this._evaluateWithGemini({ question, nativeLanguage, nativeTranscript, englishTranscript });
      } catch (err) {
        console.error('[ReasoningAdapter] Gemini call failed, falling back to heuristic mock:', err.message);
        return this._evaluateWithMock({ question, nativeLanguage, nativeTranscript, englishTranscript, warning: err.message });
      }
    }

    // Default: Pedagogical Heuristic Mock (Instant, robust, 0 cost)
    return this._evaluateWithMock({ question, nativeLanguage, nativeTranscript, englishTranscript });
  }

  /**
   * Heuristic / Rule-Based Pedagogical Evaluation (Instant & Comprehensive)
   */
  _evaluateWithMock({ question, nativeLanguage, nativeTranscript, englishTranscript, warning = null }) {
    const expected = question.expectedConcepts || [];
    const nativeText = (nativeTranscript || '').toLowerCase();
    const englishText = (englishTranscript || '').toLowerCase();

    // Check keyword presence across both transcripts
    const nativeCaptured = expected.filter(concept => {
      const words = concept.toLowerCase().split(/\s+/);
      return words.some(w => w.length > 3 && nativeText.includes(w));
    });

    const englishCaptured = expected.filter(concept => {
      const words = concept.toLowerCase().split(/\s+/);
      return words.some(w => w.length > 3 && englishText.includes(w));
    });

    // Score calculations
    // Native score is typically higher because the candidate explains technical intuition freely
    const baseNativeScore = Math.min(9.8, Math.max(6.5, 7.0 + (nativeCaptured.length / (expected.length || 1)) * 2.8));
    const baseEnglishScore = Math.min(9.5, Math.max(4.5, 5.0 + (englishCaptured.length / (expected.length || 1)) * 3.5));

    // Calculate articulation gap
    const articulationGap = Math.max(0.5, parseFloat((baseNativeScore - baseEnglishScore).toFixed(1)));

    // Missing technical terminology in English
    const missingInEnglish = expected.filter(c => !englishCaptured.includes(c));

    // Golden answer and recommendation
    const goldenAnswer = question.sampleAnswers?.en_golden?.text || 
      'In technical interviews, anchor your explanation with mutability, memory architecture, and precise complexity tradeoffs.';

    const sentenceFrames = [
      `"The primary distinction lies in [Core Concept], where [Option A] is [Attribute 1] while [Option B] is [Attribute 2]."`,
      `"From a systems performance standpoint, this optimizes [Resource / Memory] by avoiding [Bottleneck]."`,
      `"In a production architecture, I would opt for this approach when [Real-world condition] is prioritized."`
    ];

    const langName = nativeLanguage.startsWith('te') ? 'Telugu' :
                     nativeLanguage.startsWith('hi') ? 'Hindi' :
                     nativeLanguage.startsWith('ta') ? 'Tamil' : 'Native Language';

    return {
      modelUsed: this.provider === 'mock' 
        ? 'Evon v3.3 Pedagogical Engine (Simulation Mode)' 
        : `Evon v3.3 Adapter (${this.provider})`,
      isMock: true,
      warning,
      timestamp: new Date().toISOString(),
      questionTitle: question.title,
      nativeLanguage: langName,

      // Scores (out of 10)
      conceptScore: parseFloat(baseNativeScore.toFixed(1)),
      fluencyScore: parseFloat(baseEnglishScore.toFixed(1)),
      articulationGap,

      // Qualitative Feedback
      conceptFeedback: `In ${langName}, you demonstrated clear, instinctive technical understanding of the core mechanism. Your conceptual grounding is strong.`,
      fluencyFeedback: `In English, while your core message was communicated, you hesitated and substituted formal engineering terms with colloquial phrasing.`,

      // The Core Innovation: The Articulation Bridge
      articulationDelta: [
        `You clearly explained the underlying intuition in ${langName}, but omitted the formal terminology ("${missingInEnglish.slice(0, 2).join('", "')}") in your English answer.`,
        `Your native explanation captured why this matters for performance, whereas your English response focused primarily on basic syntax.`
      ],

      keyMissingKeywords: missingInEnglish.length > 0 ? missingInEnglish : ['deterministic state', 'memory locality', 'runtime execution'],
      
      // The Golden English Bridge
      goldenAnswerEnglish: goldenAnswer,
      sentenceFrames,
      
      readinessVerdict: baseEnglishScore >= 8.0 
        ? 'Interview Ready — Fluent & Technically Rigorous'
        : baseEnglishScore >= 6.0 
        ? 'Strong Technical Core — Bridge Phrasing Recommended'
        : 'Conceptual Depth Present — Needs English Articulation Practice'
    };
  }

  /**
   * Gemini 1.5 / 2.0 Flash Live Bilingual Evaluation
   */
  async _evaluateWithGemini({ question, nativeLanguage, nativeTranscript, englishTranscript }) {
    const prompt = `
You are the evaluation engine for ECHO, an AI bilingual interview preparation platform for Indian engineers.
Candidate has answered the technical question: "${question.question.en}"

Candidate's Answer in ${nativeLanguage}:
"""${nativeTranscript}"""

Candidate's Answer in English:
"""${englishTranscript}"""

Expected Technical Concepts:
${question.expectedConcepts.map(c => `- ${c}`).join('\n')}

Analyze both responses. Compare what the candidate understood in their native language versus what they managed to articulate in English.
Return ONLY valid JSON matching this exact structure:
{
  "conceptScore": number between 1.0 and 10.0,
  "fluencyScore": number between 1.0 and 10.0,
  "articulationGap": number (conceptScore minus fluencyScore),
  "conceptFeedback": "1-2 sentences on their technical depth in native tongue",
  "fluencyFeedback": "1-2 sentences on their English phrasing, hesitation, or structure",
  "articulationDelta": ["Specific technical detail mentioned in native answer that was lost in English", "Another difference"],
  "keyMissingKeywords": ["keyword1", "keyword2"],
  "goldenAnswerEnglish": "A concise, executive-level 2-3 sentence answer in fluent technical English expressing their ideas",
  "sentenceFrames": ["Sentence pattern 1 with brackets", "Sentence pattern 2"],
  "readinessVerdict": "Interview Ready" or "Strong Technical Core - Bridge Phrasing Recommended" or "Needs English Practice"
}
`;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${this.geminiKey}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { responseMimeType: 'application/json' }
      })
    });

    if (!response.ok) {
      throw new Error(`Gemini API error ${response.status}: ${await response.text()}`);
    }

    const data = await response.json();
    const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || '{}';
    const parsed = JSON.parse(rawText);

    return {
      modelUsed: 'Gemini 1.5 Flash (Bilingual Reasoning Engine)',
      isMock: false,
      timestamp: new Date().toISOString(),
      questionTitle: question.title,
      nativeLanguage,
      ...parsed
    };
  }
}

module.exports = new ReasoningAdapter();
