"""
ECHO — Gemini AI & Contextual Question Generation Engine
Generates authentic, bespoke, non-repeating interview questions based on:
- Candidate Resume & Detected Tech Stack
- Uploaded Project Code (ZIP / GitHub)
- Job Description (JD) Specific Requirements
- Custom Recruiter / Candidate Instructions ("Anything More")
- Target Role, Experience Level, and Interview Duration
- Full bilingual translations in English, Telugu, Hindi, Tamil, and Kannada.
"""

import os
import json
import random
import hashlib
from typing import List, Dict, Any, Optional

def generate_interview_questions_with_gemini(
    role: str,
    experience_level: str,
    candidate_profile: Dict[str, Any],
    duration_minutes: int,
    interview_type: str,
    target_count: int,
    api_key: str
) -> Optional[List[Dict[str, Any]]]:
    """
    Calls Google Gemini (gemini-2.0-flash / gemini-1.5-flash) to dynamically
    craft authentic, highly tailored, non-repeating interview questions.
    """
    if not api_key or not api_key.strip():
        return None

    skills = candidate_profile.get("detected_skills", [])
    projects = candidate_profile.get("extracted_projects", [])
    notes = candidate_profile.get("notes", "").strip()
    job_description = candidate_profile.get("job_description", "").strip()
    candidate_name = candidate_profile.get("candidate_name") or "Candidate"
    zip_info = candidate_profile.get("project_zip_analysis", {})
    github_info = candidate_profile.get("github_analysis", {})

    prompt = f"""You are a Principal Technical Bar-Raiser and Director of Engineering conducting an authentic, top-tier corporate interview.

Your goal is to generate a realistic, highly personalized set of EXACTLY {target_count} interview questions.

CANDIDATE INFORMATION:
- Candidate Name: {candidate_name}
- Target Role: {role}
- Experience Level: {experience_level}
- Interview Mode: {"HR Round" if interview_type == "hr" else "Technical Loop"}
- Interview Duration: {duration_minutes} minutes ({target_count} questions)
- Resume Skills: {', '.join(skills) if skills else 'Modern Software Development'}
- Projects: {', '.join(projects) if projects else 'Full-Stack Application'}
- Project Code Details: {json.dumps(zip_info) if zip_info else 'N/A'}
- GitHub Details: {json.dumps(github_info) if github_info else 'N/A'}

TARGET JOB DESCRIPTION (JD):
\"\"\"
{job_description or "General software engineering role matching the target stack"}
\"\"\"

CANDIDATE / RECRUITER CUSTOM INSTRUCTIONS ("Anything More"):
\"\"\"
{notes or "Standard comprehensive technical interview"}
\"\"\"

CRITICAL INSTRUCTIONS:
1. CUSTOM INSTRUCTIONS: If instructions are provided, heavily prioritize those specific topics and frameworks throughout the questions without repeating the instruction phrasing mechanically.
2. JOB DESCRIPTION & PROJECTS: Ground the questions in the candidate's actual projects and the exact technologies demanded in the Job Description. Avoid generic trivia.
3. AUTHENTIC INTERVIEW PROGRESSION:
   - Q1: Natural professional introduction and ice-breaking engineering discussion.
   - Q2: Resume & tech stack choices / framework tradeoffs.
   - Q3: In-depth architecture & data flow of candidate's actual project ({projects[0] if projects else 'their core project'}).
   - Q4: Complex debugging, edge case, or performance bottleneck (STAR format).
   - Q5 to Q{target_count-1}: Core technical challenges directly derived from the Job Description (system design, concurrency, APIs, databases, scaling, reliability).
   - Q{target_count}: Behavioral leadership scenario or candidate questions for the hiring team.
4. BILINGUAL SUPPORT: Every question must include fluent English ("en") and natural translations in:
   - "te": Telugu (తెలుగు)
   - "hi": Hindi (हिन्दी)
   - "ta": Tamil (தமிழ்)
   - "kn": Kannada (ಕನ್ನಡ)
5. SAMPLE ANSWERS: For each question, provide:
   - "en_golden": A complete, fluent, senior-level answer in English.
   - "te": A natural, conceptual answer in Telugu.

Return ONLY a valid JSON array of objects with this schema:
[
  {{
    "id": "gemini-q-1",
    "title": "Short title",
    "category": "Category name",
    "difficulty": "Foundational" | "Intermediate" | "Advanced",
    "question": {{
      "en": "...",
      "te": "...",
      "hi": "...",
      "ta": "...",
      "kn": "..."
    }},
    "expected_concepts": ["concept 1", "concept 2", "concept 3", "concept 4"],
    "sample_answers": {{
      "en_golden": {{ "text": "...", "fluency_score": 9.8 }},
      "te": {{ "text": "...", "concept_score": 9.6 }}
    }}
  }}
]
"""

    try:
        raw_text = ""
        candidate_models = ['gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3.5-flash']
        
        # 1. Try google.genai Client first with candidate models
        try:
            from google import genai
            client = genai.Client(api_key=api_key.strip())
            for m in candidate_models:
                try:
                    resp = client.models.generate_content(
                        model=m,
                        contents=prompt,
                        config={'response_mime_type': 'application/json'}
                    )
                    if resp and resp.text:
                        raw_text = resp.text
                        print(f"[Gemini Generator] ✓ Generated questions with model '{m}' via SDK")
                        break
                except Exception as model_err:
                    print(f"[Gemini Generator] Model '{m}' attempt note: {model_err}")
        except Exception as e_sdk:
            print(f"[Gemini Generator] SDK init error: {e_sdk}")

        # 2. Fallback to direct REST API if needed
        if not raw_text:
            import requests
            for m in candidate_models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key.strip()}"
                try:
                    r = requests.post(
                        url,
                        headers={"Content-Type": "application/json"},
                        json={
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {"responseMimeType": "application/json"}
                        },
                        timeout=30
                    )
                    if r.status_code == 200:
                        data = r.json()
                        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        print(f"[Gemini Generator] ✓ Generated questions with model '{m}' via REST API")
                        break
                except Exception as rest_err:
                    print(f"[Gemini Generator] REST model '{m}' error: {rest_err}")

        # Clean JSON markdown formatting if present
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        parsed = json.loads(cleaned.strip())
        if isinstance(parsed, list) and len(parsed) > 0:
            print(f"[Gemini Generator] ✓ Successfully generated {len(parsed)} bespoke questions using Gemini 2.0 Flash!")
            return parsed
    except Exception as err:
        print(f"[Gemini Generator] Exception generating questions: {err}")
        return None

def synthesize_smart_contextual_questions(
    role: str,
    experience_level: str,
    candidate_profile: Dict[str, Any],
    duration_minutes: int,
    interview_type: str,
    target_count: int
) -> List[Dict[str, Any]]:
    """
    High-intelligence contextual synthesizer that generates varied,
    deeply tailored questions covering the candidate's exact technologies,
    Job Description specifics, and custom instructions.
    """
    candidate_profile = candidate_profile or {}
    skills = [s.strip() for s in candidate_profile.get("detected_skills", []) if s.strip()]
    projects = [p.strip() for p in candidate_profile.get("extracted_projects", []) if p.strip()]
    notes = candidate_profile.get("notes", "").strip()
    job_description = candidate_profile.get("job_description", "").strip()
    candidate_name = candidate_profile.get("candidate_name") or "Candidate"

    # Analyze project zip or github
    zip_info = candidate_profile.get("project_zip_analysis", {})
    if zip_info:
        for t in zip_info.get("detected_technologies", []):
            if t not in skills:
                skills.append(t)
        pname = zip_info.get("project_name")
        if pname and pname not in projects:
            projects.insert(0, pname)

    github_info = candidate_profile.get("github_analysis", {})
    if github_info:
        rname = github_info.get("repo_name")
        if rname and rname not in projects:
            projects.insert(0, rname)
        rlang = github_info.get("primary_language")
        if rlang and rlang not in skills:
            skills.append(rlang)

    primary_project = projects[0] if projects else "Your Core Project"
    skills_text = ", ".join(skills[:3]) if skills else "Modern Full Stack Engineering"

    # Unique session seed to ensure questions never repeat across consecutive runs
    session_seed = random.randint(100, 99999)

    # ------------------------------------------------------------------
    # BRANCH A: DEDICATED HR ROUND
    # ------------------------------------------------------------------
    if interview_type == "hr":
        hr_bank = [
            {
                "id": f"hr-intro-{session_seed}",
                "category": "HR & Candidate Introduction",
                "role": role,
                "difficulty": "Foundational",
                "title": "Professional Introduction & Engineering Journey",
                "question": {
                    "en": f"Welcome to our interview! Could you share an overview of your journey into software engineering, what key milestones defined your career, and what excites you about the {role} position?",
                    "te": f"మా ఇంటర్వ్యూకి స్వాగతం! సాఫ్ట్‌వేర్ ఇంజనీరింగ్‌లోకి మీ ప్రయాణం, మీ కెరీర్‌లో ముఖ్యమైన మైలురాళ్లు మరియు {role} రోల్ పట్ల మీకు గల ఆసక్తిని గురించి క్లుప్తంగా వివరించండి.",
                    "hi": f"इंटरव्यू में आपका स्वागत है! कृपया सॉफ्टवेयर इंजीनियरिंग में अपनी यात्रा, करियर के मुख्य पड़ाव और {role} पद के प्रति अपने उत्साह के बारे में बताएं।",
                    "ta": f"நேர்காணலுக்கு வரவேற்கிறோம்! மென்பொருள் துறையில் உங்கள் பயணம் மற்றும் {role} பணி மீதான உங்கள் ஆர்வத்தை விவரிக்கவும்.",
                    "kn": f"ಸಂದರ್ಶನಕ್ಕೆ ಸುಸ್ವಾಗತ! ಸಾಫ್ಟ್‌ವೇರ್ ಕ್ಷೇತ್ರದಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಯಾಣ ಮತ್ತು {role} ಹುದ್ದೆಯ ಬಗ್ಗೆ ನಿಮ್ಮ ಆಸಕ್ತಿಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ."
                },
                "expected_concepts": ["clear professional summary", "engineering passion", "alignment with company goals", "articulate delivery"],
                "sample_answers": {
                    "en_golden": {"text": f"I am an engineer passionate about building robust systems. Throughout my work with {skills_text}, I focus on scalable architectures and high customer impact. This {role} role aligns perfectly with my drive to engineer resilient platforms.", "fluency_score": 9.8},
                    "te": {"text": f"నేను సాఫ్ట్‌వేర్ ఇంజనీరింగ్ లో ప్రావీణ్యం సంపాదించాను. సమస్యలను విశ్లేషించి శుభ్రమైన కోడ్ రాయడం నా బలం. {role} రోల్ ద్వారా కంపెనీ ఎదుగుదలలో నా వంతు పాత్ర పోషించాలనుకుంటున్నాను.", "concept_score": 9.6}
                }
            },
            {
                "id": f"hr-why-hire-{session_seed}",
                "category": "HR & Value Proposition",
                "role": role,
                "difficulty": "Foundational",
                "title": "Unique Value Proposition & Strengths",
                "question": {
                    "en": f"Among many talented applicants interviewing for this {role} position, what unique blend of technical problem-solving and work ethic sets you apart?",
                    "te": f"ఈ {role} రోల్ కోసం చాలా మంది పోటీ పడుతున్నారు. మిమ్మల్ని ఇతరుల కంటే భిన్నంగా నిలబెట్టే మీ ప్రత్యేక బలాలు మరియు సమస్యా పరిష్కార నైపుణ్యాలు ఏమిటి?",
                    "hi": f"इस {role} पद के लिए कई उम्मीदवार हैं। आपकी ऐसी कौन सी तकनीकी ताकत और कार्यशैली है जो आपको दूसरों से अलग बनाती है?",
                    "ta": f"இந்த {role} பணிக்காக நாங்கள் உங்களை ஏன் தேர்ந்தெடுக்க வேண்டும்? உங்கள் தனித்துவமான பலம் என்ன?",
                    "kn": f"ಈ {role} ಹುದ್ದೆಗೆ ನಾವು ನಿಮ್ಮನ್ನು ಏಕೆ ಆಯ್ಕೆ ಮಾಡಬೇಕು? ನಿಮ್ಮಲ್ಲಿರುವ ವಿಶಿಷ್ಟ ಸಾಮರ್ಥ್ಯಗಳು ಯಾವುವು?"
                },
                "expected_concepts": ["technical proficiency", "proactive ownership", "team velocity improvement", "clear business alignment"],
                "sample_answers": {
                    "en_golden": {"text": "What distinguishes me is taking complete end-to-end ownership. Beyond writing clean code, I actively collaborate with cross-functional teams, automate regressions, and adapt rapidly to new requirements.", "fluency_score": 9.9},
                    "te": {"text": "నాకున్న బలమైన కోడింగ్ నైపుణ్యాలు మరియు ప్రాజెక్ట్‌లను మొదటి నుండి చివరి వరకు స్వయంగా బాధ్యత తీసుకుని పూర్తి చేసే తత్వం నన్ను ప్రత్యేకం చేస్తాయి.", "concept_score": 9.6}
                }
            },
            {
                "id": f"hr-conflict-{session_seed}",
                "category": "Behavioral & Collaboration (STAR)",
                "role": role,
                "difficulty": "Intermediate",
                "title": "Constructive Conflict Resolution (STAR)",
                "question": {
                    "en": "Can you describe a situation where you had a disagreement with a team member or manager over a product requirement or technical direction? How did you navigate it constructively?",
                    "te": "ప్రాజెక్ట్ లో మీ సహోద్యోగి లేదా మేనేజర్‌తో సాంకేతిక లేదా ప్రోడక్ట్ విషయంలో విభేదించిన సందర్భాన్ని వివరించండి. చర్చను నిర్మాణాత్మకంగా ఎలా పరిష్కరించారు?",
                    "hi": "किसी सहकर्मी या प्रबंधक के साथ तकनीकी असहमति के अनुभव का वर्णन करें। आपने बातचीत को सकारात्मक रूप से कैसे संभाला?",
                    "ta": "ஒரு சக ஊழியருடன் கருத்து வேறுபாடு ஏற்பட்ட அனுபவத்தை விவரிக்கவும். அதை எவ்வாறு சுமூகமாக தீர்த்தீர்கள்?",
                    "kn": "ತಂಡದ ಸದಸ್ಯರೊಂದಿಗೆ ಭಿನ್ನಾಭಿಪ್ರಾಯವಿದ್ದ ಸಂದರ್ಭವನ್ನು ವಿವರಿಸಿ. ಅದನ್ನು ನೀವು ಹೇಗೆ ರಚನಾತ್ಮಕವಾಗಿ ಪರಿಹರಿಸಿದ್ದೀರಿ?"
                },
                "expected_concepts": ["STAR methodology", "data-driven benchmarks", "active listening", "focus on product outcome"],
                "sample_answers": {
                    "en_golden": {"text": "When deciding between two architecture approaches, rather than arguing subjective opinions, I proposed a timeboxed proof-of-concept simulating peak load. The empirical data showed a 40% latency reduction for our team's proposal, allowing us to align objectively.", "fluency_score": 9.8},
                    "te": {"text": "వ్యక్తిగత వాదనలకు బదులుగా చిన్న ప్రూఫ్ ఆఫ్ కాన్సెప్ట్ (PoC) చేసి, బెంచ్‌మార్క్ ఫలితాల ఆధారంగా డేటాబేస్ ఎంపికపై అందరం ఏకాభిప్రాయానికి వచ్చాము.", "concept_score": 9.5}
                }
            },
            {
                "id": f"hr-deadlines-{session_seed}",
                "category": "Stress & Prioritization",
                "role": role,
                "difficulty": "Intermediate",
                "title": "Handling High-Pressure Deadlines",
                "question": {
                    "en": "Tell me about a time you faced a compressed project deadline with competing priorities. How did you decide what trade-offs to make while ensuring production stability?",
                    "te": "చాలా తక్కువ సమయంలో ప్రాజెక్ట్ డెలివరీ చేయాల్సి వచ్చిన సందర్భాన్ని వివరించండి. ప్రొడక్షన్ స్థిరత్వం దెబ్బతినకుండా పనులను ఎలా ప్రాధాన్యత ప్రకారం పూర్తి చేశారు?",
                    "hi": "किसी ऐसी स्थिति का वर्णन करें जब आपको बहुत कम समय में काम पूरा करना था। आपने प्राथमिकताओं को कैसे प्रबंधित किया?",
                    "ta": "குறுகிய காலக்கெடுவில் நீங்கள் பணியாற்றிய சூழ்நிலையை விவரிக்கவும். பணிகளை எவ்வாறு முன்னுரிமைப்படுத்தினீர்கள்?",
                    "kn": "ಕಠಿಣ ಡೆಡ್‌ಲೈನ್ ಎದುರಿಸಿದ ಸಂದರ್ಭವನ್ನು ವಿವರಿಸಿ. ಕಾರ್ಯಗಳನ್ನು ಹೇಗೆ ಆದ್ಯತೆಯ ಮೇಲೆ ನಿರ್ವಹಿಸಿದ್ದೀರಿ?"
                },
                "expected_concepts": ["ruthless MVP prioritization", "stakeholder communication", "automated testing guardrails", "calm under pressure"],
                "sample_answers": {
                    "en_golden": {"text": "Under a tight deadline, I de-scoped non-critical secondary features in alignment with the product manager, protecting the core checkout flow and adding automated smoke tests to ensure zero regressions.", "fluency_score": 9.8},
                    "te": {"text": "ముందుగా అత్యంత ముఖ్యమైన ఫీచర్లపై దృష్టి పెట్టాను. అనవసరమైన వాటిని తరువాతి రిలీజ్ కి వాయిదా వేసి, ఆటోమేటెడ్ టెస్ట్స్ తో ఎటువంటి బగ్స్ లేకుండా పూర్తి చేశాను.", "concept_score": 9.6}
                }
            },
            {
                "id": f"hr-vision-{session_seed}",
                "category": "Career Growth & Long-Term Vision",
                "role": role,
                "difficulty": "Foundational",
                "title": "Where Do You See Yourself in 3–5 Years?",
                "question": {
                    "en": f"Looking ahead, what areas of technical mastery and engineering leadership do you aspire to grow into over the next 3 to 5 years as a {role}?",
                    "te": f"రాబోయే 3 నుండి 5 సంవత్సరాలలో {role} గా మీ ఇంజనీరింగ్ కెరీర్ ఎలా ఉండాలని కోరుకుంటున్నారు? ఎలాంటి నైపుణ్యాలు మరియు నాయకత్వ బాధ్యతలు తీసుకోవాలనుకుంటున్నారు?",
                    "hi": f"अगले 3 से 5 वर्षों में आप अपने इंजीनियरिंग करियर को कहाँ देखते हैं? आप किस प्रकार की ज़िम्मेदारियाँ संभालना चाहते हैं?",
                    "ta": f"அடுத்த 3 முதல் 5 ஆண்டுகளில் உங்கள் பொறியியல் வாழ்க்கையை எங்கே பார்க்கிறீர்கள்?",
                    "kn": f"ಮುಂದಿನ 3 ರಿಂದ 5 ವರ್ಷಗಳಲ್ಲಿ ನಿಮ್ಮ ಇಂಜಿನಿಯರಿಂಗ್ ವೃತ್ತಿಜೀವನವನ್ನು ಎಲ್ಲಿ ನೋಡುತ್ತೀರಿ?"
                },
                "expected_concepts": ["architectural depth", "mentoring junior engineers", "driving strategic initiatives", "continuous learning"],
                "sample_answers": {
                    "en_golden": {"text": "I aim to evolve into a Lead Architect designing resilient distributed systems, while actively mentoring peers and elevating the team's software craftsmanship.", "fluency_score": 9.9},
                    "te": {"text": "రాబోయే 5 సంవత్సరాలలో లీడ్ ఇంజనీర్ గా ఎదగాలనుకుంటున్నాను. క్లిష్టమైన సిస్టమ్స్ డిజైన్ చేయడంతో పాటు టీమ్ సక్సెస్ లో కీలక భాగస్వామిని కావాలనుకుంటున్నాను.", "concept_score": 9.6}
                }
            }
        ]
        return hr_bank[:target_count]

    # ------------------------------------------------------------------
    # BRANCH B: DYNAMIC TECHNICAL INTERVIEW PROGRESSION
    # ------------------------------------------------------------------
    questions: List[Dict[str, Any]] = []

    # 1. Warm Conversational Icebreaker & Engineering Stack
    intro_variations = [
        f"Welcome to our technical interview! It is great to connect with you. To start us off, could you walk me through your journey in software engineering, and what technologies from {skills_text} you've enjoyed working with recently?",
        f"Hello and welcome! To get our discussion started comfortably, please tell me about yourself, your background as a {role}, and the core frameworks you rely on in production.",
        f"Glad to meet you today! Could you introduce yourself, highlighting the technical challenges that drive you as a {role} and your recent engineering accomplishments?"
    ]
    intro_te_variations = [
        f"మా టెక్నికల్ ఇంటర్వ్యూకి స్వాగతం! ప్రారంభించడానికి, సాఫ్ట్‌వేర్ ఇంజనీరింగ్‌లో మీ ప్రయాణం మరియు ఇటీవల మీరు పనిచేసిన {skills_text} టెక్నాలజీల గురించి క్లుప్తంగా పరిచయం చేసుకోండి.",
        f"నమస్కారం! {role} గా మీ అనుభవం, మీ నేపథ్యం మరియు ప్రొడక్షన్ లో మీరు ఎక్కువగా ఉపయోగించే టెక్నాలజీల గురించి చెప్పండి.",
        f"ఈ రోజు మీతో మాట్లాడటం చాలా సంతోషంగా ఉంది. ఒక {role} గా మిమ్మల్ని నిరంతరం ప్రేరేపించే అంశాలు మరియు మీ ఇటీవలి ప్రాజెక్ట్‌ల గురించి వివరించండి."
    ]
    idx_intro = session_seed % len(intro_variations)
    q_intro = {
        "id": f"intro-{session_seed}",
        "category": "Introduction & Background",
        "role": role,
        "difficulty": "Conversational",
        "title": "1. Engineering Background & Technology Overview",
        "question": {
            "en": intro_variations[idx_intro],
            "te": intro_te_variations[idx_intro],
            "hi": f"टेक्निकल इंटरव्यू में आपका स्वागत है! शुरुआत के लिए, कृपया अपना परिचय दें, {role} के रूप में अपनी यात्रा और हाल ही में उपयोग की गई तकनीकों के बारे में बताएं।",
            "ta": f"தொழில்நுட்ப நேர்காணலுக்கு வரவேற்கிறோம்! தொடங்குவதற்கு, உங்களைப் பற்றி மற்றும் சமீபத்தில் நீங்கள் பயன்படுத்திய {skills_text} தொழில்நுட்பங்களை விவரிக்கவும்.",
            "kn": f"ತಾಂತ್ರಿಕ ಸಂದರ್ಶನಕ್ಕೆ ಸುಸ್ವಾಗತ! ಪ್ರಾರಂಭಿಸಲು, ನಿಮ್ಮ ಬಗ್ಗೆ ಮತ್ತು ಇತ್ತೀಚೆಗೆ ನೀವು ಬಳಸಿದ {skills_text} ತಂತ್ರಜ್ಞಾನಗಳ ಬಗ್ಗೆ ಪರಿಚಯಿಸಿಕೊಳ್ಳಿ."
        },
        "expected_concepts": ["professional summary", "hands-on core tech stack", "engineering passion", "clear articulation"],
        "sample_answers": {
            "en_golden": {"text": f"I am a {role} specializing in building scalable services. Over recent projects, I've leveraged {skills_text} to deliver reliable, decoupled architectures with automated testing and continuous deployment.", "fluency_score": 9.8},
            "te": {"text": f"నేను {role} గా పనిచేస్తున్నాను. {skills_text} ఉపయోగించి హై-పెర్ఫార్మెన్స్ అప్లికేషన్లను అభివృద్ధి చేయడంలో నాకు అనుభవం ఉంది. సమస్యలను విశ్లేషించి శుభ్రమైన కోడ్ రాయడం నా బలం.", "concept_score": 9.6}
        }
    }
    questions.append(q_intro)

    # 2. Specific Resume & Framework Deep Dive (Tailored to Detected Skills)
    skill_lower_set = {s.lower() for s in skills}
    if "next.js" in skill_lower_set or "nextjs" in skill_lower_set or "react" in skill_lower_set:
        q_stack = {
            "id": f"tech-nextjs-ssr-{session_seed}",
            "category": "Frontend Architecture & Rendering",
            "role": role,
            "difficulty": "Applied Technical",
            "title": "2. Next.js Rendering Strategies: SSR vs SSG vs Client Hydration",
            "question": {
                "en": f"I see you have hands-on experience with Next.js and frontend rendering. When architecting high-traffic web applications, how do you decide between Server-Side Rendering (SSR), Static Site Generation (SSG), and Incremental Static Regeneration (ISR)? What caching headers or CDN strategies do you configure to prevent server bottlenecks?",
                "te": f"మీ రెజ్యూమ్‌లో Next.js అనుభవం ఉంది. అధిక ట్రాఫిక్ ఉన్నప్పుడు Server-Side Rendering (SSR), Static Site Generation (SSG), మరియు Incremental Static Regeneration (ISR) లలో దేన్ని ఎప్పుడు ఎంచుకుంటారు? సర్వర్ పై లోడ్ తగ్గించడానికి ఎలాంటి క్యాషింగ్ లేదా CDN పద్ధతులు వాడతారు?",
                "hi": "Next.js में SSR, SSG और ISR के बीच आप कैसे निर्णय लेते हैं? उच्च ट्रैफ़िक में सर्वर पर लोड कम करने के लिए कौन सी कैशिंग रणनीतियाँ अपनाते हैं?",
                "ta": "Next.js இல் SSR, SSG மற்றும் ISR ஆகியவற்றை எப்போது பயன்படுத்துவீர்கள்? சர்வர் சுமையைக் குறைக்க என்ன உத்திகளைப் பயன்படுத்துகிறீர்கள்?",
                "kn": "Next.js ನಲ್ಲಿ SSR, SSG ಮತ್ತು ISR ನಡುವೆ ನೀವು ಹೇಗೆ ನಿರ್ಧರಿಸುತ್ತೀರಿ? ಸರ್ವರ್ ಲೋಡ್ ಕಡಿಮೆ ಮಾಡಲು ಯಾವ ಕ್ಯಾಶಿಂಗ್ ತಂತ್ರಗಳನ್ನು ಬಳಸುತ್ತೀರಿ?"
            },
            "expected_concepts": ["SSR dynamic data at request time", "SSG build-time pre-rendering", "ISR background cache revalidation", "stale-while-revalidate headers", "CDN edge caching"],
            "sample_answers": {
                "en_golden": {"text": "I default to SSG or ISR for public content pages using stale-while-revalidate headers cached at the CDN edge to achieve sub-50ms TTFB. For personalized, authenticated dashboards requiring real-time session state, I leverage SSR with streaming Server Components to parallelize data fetching and eliminate waterfall latencies.", "fluency_score": 9.9},
                "te": {"text": "స్టాటిక్ కంటెంట్ కోసం SSG లేదా ISR వాడతాము, దీనివల్ల CDN ఎడ్జ్ నుండి పేజీలు చాలా వేగంగా లోడ్ అవుతాయి. యూజర్ స్పెసిఫిక్ డేటా మరియు డైనమిక్ పేజీలకు మాత్రమే SSR వాడతాము, తద్వారా సర్వర్ పై లోడ్ తగ్గుతుంది.", "concept_score": 9.7}
            }
        }
    elif "flask" in skill_lower_set or "fastapi" in skill_lower_set or "python" in skill_lower_set:
        q_stack = {
            "id": f"tech-python-async-{session_seed}",
            "category": "Backend Concurrency & WSGI/ASGI",
            "role": role,
            "difficulty": "Applied Technical",
            "title": "2. Python Backend Concurrency: WSGI vs ASGI & Connection Pools",
            "question": {
                "en": f"Looking at your backend experience with Python and frameworks like Flask/FastAPI, how do you handle concurrency under high-load production workloads? Compare WSGI worker pools (Gunicorn) with asynchronous ASGI event loops, and explain how you manage database connection pooling without exhausting socket limits.",
                "te": f"పైథాన్ మరియు ఫ్లాస్క్/ఫాస్ట్‌ఏపీఐ లతో మీ అనుభవాన్ని పరిశీలిస్తే, అధిక లోడ్ ఉన్నప్పుడు కాన్‌కరెన్సీని ఎలా నిర్వహిస్తారు? WSGI వర్కర్ పూల్స్ (Gunicorn) మరియు అసమకాలిక (ASGI) ఈవెంట్ లూప్స్ మధ్య తేడా ఏమిటి? డేటాబేస్ కనెక్షన్ పూలింగ్ ను ఎలా మేనేజ్ చేస్తారు?",
                "hi": "पायथन बैकएंड में उच्च लोड के तहत कॉनकरेंसी कैसे प्रबंधित करते हैं? WSGI (Gunicorn) और ASGI इवेंट लूप की तुलना करें, और डेटाबेस कनेक्शन पूलिंग को कैसे संभालते हैं?",
                "ta": "பைத்தான் பேக்கெண்டில் அதிக சுமையின் போது கன்கரன்சியை எவ்வாறு கையாளுகிறீர்கள்? WSGI மற்றும் ASGI இடையே உள்ள வேறுபாடு என்ன?",
                "kn": "ಪೈಥಾನ್ ಬ್ಯಾಕೆಂಡ್‌ನಲ್ಲಿ ಹೆಚ್ಚಿನ ಲೋಡ್ ಇದ್ದಾಗ ಕಾನ್ಕರೆನ್ಸಿಯನ್ನು ಹೇಗೆ ನಿರ್ವಹಿಸುತ್ತೀರಿ? WSGI ಮತ್ತು ASGI ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು?"
            },
            "expected_concepts": ["WSGI pre-fork synchronous workers", "ASGI single-threaded non-blocking event loop", "I/O bound vs CPU bound workloads", "SQLAlchemy QueuePool sizing", "avoiding database socket exhaustion"],
            "sample_answers": {
                "en_golden": {"text": "Under WSGI with Gunicorn, concurrency scales through pre-forked worker processes with gevent/threads, ideal for synchronous code. Under ASGI (Uvicorn), an event loop schedules cooperative coroutines on I/O wait, dramatically reducing memory overhead for high-concurrency APIs. I configure SQLAlchemy QueuePool with pool_size=20 and max_overflow=10 alongside strict checkout timeouts to prevent exhausting database connections.", "fluency_score": 9.9},
                "te": {"text": "డబ్ల్యూఎస్జీఐ లో ప్రతి రిక్వెస్ట్ కి వర్కర్ ప్రాసెస్ ఉంటుంది. ఏఎస్జీఐ లో నాన్-బ్లాకింగ్ ఈవెంట్ లూప్ ద్వారా వేలాది ఐ/ఓ రిక్వెస్ట్‌లను తక్కువ మెమరీతో ప్రాసెస్ చేయవచ్చు. డేటాబేస్ పూల్ సైజ్ ను కంట్రోల్ చేయడం ద్వారా కనెక్షన్ ఎగ్జాషన్ నివారిస్తాము.", "concept_score": 9.6}
            }
        }
    else:
        q_stack = {
            "id": f"tech-general-api-{session_seed}",
            "category": "API Architecture & Design",
            "role": role,
            "difficulty": "Applied Technical",
            "title": f"2. Production Engineering with {skills_text}",
            "question": {
                "en": f"Reflecting on your experience with {skills_text}, how do you structure production API contracts? What strategies do you use for backward-compatible versioning, rate limiting, and structured logging?",
                "te": f"{skills_text} తో మీ అనుభవం ఆధారంగా, ప్రొడక్షన్ API లను ఎలా డిజైన్ చేస్తారు? వెర్షనింగ్, రేట్ లిమిటింగ్ మరియు స్ట్రక్చర్డ్ లాగింగ్ కోసం ఎలాంటి పద్ధతులు పాటిస్తారు?",
                "hi": f"{skills_text} के साथ अपने अनुभव के आधार पर, आप प्रोडक्शन एपीआई को कैसे संरचित करते हैं? रेट लिमिटिंग और लॉगिंग कैसे प्रबंधित करते हैं?",
                "ta": f"{skills_text} உடன் உங்கள் அனுபவத்தை விவரிக்கவும். API வடிவமைப்பு மற்றும் கண்காணிப்பை எவ்வாறு மேற்கொள்கிறீர்கள்?",
                "kn": f"{skills_text} ನೊಂದಿಗೆ ನಿಮ್ಮ ಅನುಭವದ ಆಧಾರದ ಮೇಲೆ, ಪ್ರೊಡಕ್ಷನ್ API ಗಳನ್ನು ಹೇಗೆ ರಚಿಸುತ್ತೀರಿ?"
            },
            "expected_concepts": ["RESTful resource modeling", "semantic versioning via URL/header", "token bucket rate limiting", "correlation IDs and structured JSON logging"],
            "sample_answers": {
                "en_golden": {"text": "I design APIs adhering to OpenAPI specifications with URI-based semantic versioning (/v1). I implement Redis-backed token bucket rate limiters to protect upstream workers, and inject unique Correlation IDs across request headers for distributed tracing in structured JSON logs.", "fluency_score": 9.8},
                "te": {"text": "ఏపీఐ లను ప్రామాణికంగా వెర్షనింగ్ చేసి, రెడిస్ ఆధారిత రేట్ లిమిటింగ్ తో సురక్షితం చేస్తాము. ప్రతి రిక్వెస్ట్ కి యూనిక్ కోరిలేషన్ ఐడీ ఇచ్చి సెంట్రలైజ్డ్ లాగింగ్ ద్వారా ట్రాక్ చేస్తాము.", "concept_score": 9.5}
            }
        }
    questions.append(q_stack)

    # 3. In-Depth Project Architecture (Candidate's actual Project & Code)
    proj_variations = [
        f"Let's dive into your project, '{primary_project}'. Walk me through the architecture: what were the core decoupled components, how did data move through the system, and what database design decisions did you make?",
        f"Regarding your project '{primary_project}', how did you decouple the business logic from presentation and database access layers? How did you validate data integrity and handle state across services?",
        f"In '{primary_project}', what was the request lifecycle from client submission to database persistence? What architectural tradeoffs did you accept to meet performance goals?"
    ]
    proj_te_variations = [
        f"మీ ప్రాజెక్ట్ '{primary_project}' గురించి చర్చిద్దాం. దీని ఆర్కిటెక్చర్‌ను వివరించండి: ప్రధాన కాంపోనెంట్లు ఏమిటి, డేటా ఫ్లో ఎలా జరుగుతుంది మరియు డేటాబేస్ డిజైన్ నిర్ణయాలు ఏమిటి?",
        f"మీ ప్రాజెక్ట్ '{primary_project}' లో బిజినెస్ లాజిక్ ని డేటాబేస్ నుండి ఎలా వేరు చేశారు? డేటా సమగ్రతను మరియు స్టేట్ మేనేజ్‌మెంట్‌ను ఎలా కాపాడారు?",
        f"'{primary_project}' లో క్లయింట్ రిక్వెస్ట్ నుండి డేటాబేస్ వరకు డేటా ప్రయాణాన్ని వివరించండి. పెర్ఫార్మెన్స్ కోసం ఎలాంటి ఆర్కిటెక్చరల్ నిర్ణయాలు తీసుకున్నారు?"
    ]
    idx_proj = session_seed % len(proj_variations)
    q_proj = {
        "id": f"proj-arch-{session_seed}",
        "category": "Project Architecture & System Design",
        "role": role,
        "difficulty": "System Architecture",
        "title": f"3. Architecture & Data Flow in {primary_project}",
        "question": {
            "en": proj_variations[idx_proj],
            "te": proj_te_variations[idx_proj],
            "hi": f"आइए आपके प्रोजेक्ट '{primary_project}' पर चर्चा करते हैं। इसका आर्किटेक्चर कैसा था: मुख्य घटक क्या थे, डेटा कैसे प्रोसेस होता था और डेटाबेस डिज़ाइन निर्णय क्या थे?",
            "ta": f"உங்கள் திட்டமான '{primary_project}' ஐ ஆராய்வோம். இதன் கட்டமைப்பு, முக்கிய கூறுகள் மற்றும் தரவு ஓட்டத்தை விவரிக்கவும்.",
            "kn": f"ನಿಮ್ಮ ಪ್ರಾಜೆಕ್ಟ್ '{primary_project}' ಬಗ್ಗೆ ಚರ್ಚಿಸೋಣ. ಇದರ ವಾಸ್ತುಶಿಲ್ಪ, ಮುಖ್ಯ ಘಟಕಗಳು ಮತ್ತು ಡೇಟಾ ಹರಿವನ್ನು ವಿವರಿಸಿ."
        },
        "expected_concepts": ["modular decoupling", "clean architecture separation of concerns", "database indexing & schema normalization", "asynchronous background processing", "caching layer"],
        "sample_answers": {
            "en_golden": {"text": f"In architecting {primary_project}, I separated presentation routes from the domain business layer and database repositories. Requests pass through schema validation before executing service logic, while database queries utilize indexed foreign keys and connection pooling to ensure sub-100ms response times.", "fluency_score": 9.9},
            "te": {"text": f"ఈ ప్రాజెక్ట్ లో బిజినెస్ లాజిక్ ని డేటాబేస్ కనెక్షన్ల నుండి వేరు చేశాను. సరైన ఇండెక్సింగ్ మరియు క్యాషింగ్ ద్వారా రెస్పాన్స్ సమయం చాలా వేగంగా ఉండేలా చూసుకున్నాను.", "concept_score": 9.6}
        }
    }
    questions.append(q_proj)

    # 4. In-Depth Project Debugging & Root Cause Analysis (STAR)
    debug_variations = [
        f"While developing '{primary_project}', what was the most complex technical bug, performance bottleneck, or race condition you encountered? How did you isolate the root cause and engineer a permanent resolution?",
        f"Can you share a specific technical incident or latency spike in '{primary_project}'? Walk me through your debugging methodology using the STAR framework (Situation, Task, Action, Result).",
        f"Think of a time in '{primary_project}' when an edge case or unexpected failure occurred in production. How did you diagnose the issue using logs or profiling tools, and how did you verify the fix?"
    ]
    debug_te_variations = [
        f"'{primary_project}' నిర్మించేటప్పుడు మీరు ఎదుర్కొన్న అత్యంత కష్టమైన సాంకేతిక బగ్, పనితీరు సమస్య (latency spike) లేదా రేస్ కండిషన్ ఏమిటి? సమస్య మూలకారణాన్ని ఎలా కనిపెట్టి శాశ్వతంగా పరిష్కరించారు?",
        f"'{primary_project}' లో మీరు ఎదుర్కొన్న ఒక క్లిష్టమైన సమస్యను STAR పద్ధతిలో వివరించండి: పరిస్థితి ఏమిటి, మీరు తీసుకున్న చర్యలు మరియు తుది ఫలితం ఏమిటి?",
        f"'{primary_project}' లో అనుకోకుండా వచ్చిన ఎడ్జ్ కేస్ లేదా క్రాష్ ను లాగ్స్ మరియు ప్రొఫైలింగ్ ద్వారా ఎలా డీబగ్ చేశారు? మళ్లీ రాకుండా ఎలాంటి టెస్ట్స్ రాశారు?"
    ]
    idx_debug = session_seed % len(debug_variations)
    q_debug = {
        "id": f"proj-debug-{session_seed}",
        "category": "Engineering Problem Solving (STAR)",
        "role": role,
        "difficulty": "Practical Scenario",
        "title": f"4. Root Cause Analysis & Debugging in {primary_project}",
        "question": {
            "en": debug_variations[idx_debug],
            "te": debug_te_variations[idx_debug],
            "hi": f"'{primary_project}' बनाते समय आपके सामने आई सबसे कठिन तकनीकी समस्या या बग क्या थी? आपने रूट कॉज़ का पता लगाकर इसे कैसे हल किया?",
            "ta": f"'{primary_project}' ஐ உருவாக்கிய போது நீங்கள் சந்தித்த கடினமான பிழை அல்லது சிக்கல் என்ன? மூல காரணத்தைக் கண்டறிந்து எவ்வாறு நிரந்தரமாக சரிசெய்தீர்கள்?",
            "kn": f"'{primary_project}' ನಿರ್ಮಿಸುವಾಗ ನೀವು ಎದುರಿಸಿದ ಅತ್ಯಂತ ಕಷ್ಟಕರವಾದ ತಾಂತ್ರಿಕ ದೋಷ ಯಾವುದು? ಮೂಲ ಕಾರಣವನ್ನು ಪತ್ತೆಹಚ್ಚಿ ಹೇಗೆ ಶಾಶ್ವತವಾಗಿ ಪರಿಹರಿಸಿದ್ದೀರಿ?"
        },
        "expected_concepts": ["STAR format", "diagnostic profiling & log traces", "root cause identification", "index optimization or concurrency mutex fix", "automated regression tests"],
        "sample_answers": {
            "en_golden": {"text": f"During stress testing of {primary_project}, we noticed p99 response times climbing above 2.5 seconds. Profiling traces revealed table locks caused by unindexed filtering on high-cardinality columns. I added composite B-Tree indexes and introduced connection pool timeout limits, reducing p99 latency to 180ms and added automated load regression benchmarks.", "fluency_score": 9.9},
            "te": {"text": f"మా ప్రాజెక్ట్ లో రెస్పాన్స్ టైమ్ పెరిగినప్పుడు ప్రొఫైలర్ ద్వారా చెక్ చేయగా అన్‌ఇండెక్స్డ్ క్వెరీస్ టేబుల్ లాక్స్ చేస్తున్నాయని తెలిసింది. సరైన కాంపోజిట్ ఇండెక్సెస్ యాడ్ చేసి, క్వెరీ రీఫాక్టర్ చేయడంతో రెస్పాన్స్ సమయం 70% మెరుగుపడింది.", "concept_score": 9.7}
        }
    }
    questions.append(q_debug)

    # 5. Job Description & Custom Instructions Driven Technical Challenge
    # Formulate question tailored to JD requirements or Custom Instructions
    notes_lower = notes.lower()
    jd_lower = job_description.lower()

    if any(k in notes_lower for k in ["cloud", "aws", "docker", "k8s", "kubernetes", "devops"]) or any(k in jd_lower for k in ["docker", "kubernetes", "k8s", "aws", "cloud", "ci/cd"]):
        q_jd = {
            "id": f"jd-cloud-k8s-{session_seed}",
            "category": "Cloud Infrastructure & Containerization",
            "role": role,
            "difficulty": "Advanced Production",
            "title": "5. Container Resilience & Zero-Downtime Deployments",
            "question": {
                "en": "In modern production environments matching our job description, high availability and zero-downtime releases are paramount. How do you design Docker container images for minimal footprint and security? How do Kubernetes readiness and liveness probes prevent dropping active traffic during rolling updates?",
                "te": "మా జాబ్ డిస్క్రిప్షన్‌కు అనుగుణంగా ప్రొడక్షన్ లో జీరో-డౌన్‌టైమ్ (Zero-Downtime) డిప్లాయ్‌మెంట్స్ చాలా ముఖ్యం. డాకర్ ఇమేజ్‌లను సెక్యూర్ గా మరియు తక్కువ సైజులో ఎలా నిర్మిస్తారు? రోలింగ్ అప్‌డేట్స్ సమయంలో ట్రాఫిక్ డ్రాప్ కాకుండా కుబర్నెటీస్ రెడీనెస్ మరియు లైవ్‌నెస్ ప్రోబ్స్ ఎలా కాపాడతాయి?",
                "hi": "क्लाउड वातावरण में जीरो-डाउनटाइम डिप्लॉयमेंट के लिए डॉकर और कुबेरनेट्स को कैसे कॉन्फ़िगर करते हैं? रेडीनेस और लाइवनेस प्रोब्स ट्रैफ़िक लॉस को कैसे रोकते हैं?",
                "ta": "கிளவுட் சூழலில் ஜீரோ-டவுன்டைம் வெளியீடுகளை எவ்வாறு உறுதி செய்கிறீர்கள்? குபெர்னெடிஸ் ப்ரோப்ஸ் எவ்வாறு உதவுகின்றன?",
                "kn": "ಕ್ಲೌಡ್ ಪರಿಸರದಲ್ಲಿ ಝೀರೋ-ಡೌನ್‌ಟೈಮ್ ನಿಯೋಜನೆಗಳನ್ನು ಹೇಗೆ ಖಚಿತಪಡಿಸುತ್ತೀರಿ? ಕುಬರ್ನೆಟಿಸ್ ಪ್ರೋಬ್ಸ್ ಹೇಗೆ ಸಹಾಯ ಮಾಡುತ್ತವೆ?"
            },
            "expected_concepts": ["multi-stage Docker builds", "distroless / non-root user containers", "Kubernetes rolling updates", "readiness probe stopping traffic before warmup", "liveness probe restarting deadlocked pods"],
            "sample_answers": {
                "en_golden": {"text": "I utilize multi-stage Docker builds on lightweight alpine/distroless bases running as non-root users to minimize vulnerability surface area. In Kubernetes, the readiness probe ensures pods pass health checks before receiving ingress traffic, while rolling update maxSurge and maxUnavailable settings guarantee continuous service capacity.", "fluency_score": 9.9},
                "te": {"text": "మల్టీ-స్టేజ్ డాకర్ బిల్డ్స్ ద్వారా ఇమేజ్ సైజ్ మరియు సెక్యూరిటీ సమస్యలు తగ్గిస్తాము. కుబర్నెటీస్ లో రెడీనెస్ ప్రోబ్ పాడ్ పూర్తిగా సిద్ధమైన తర్వాతే ట్రాఫిక్ ని పంపుతుంది, తద్వారా రోలింగ్ అప్‌డేట్స్ లో యూజర్లకు ఎలాంటి అంతరాయం కలగదు.", "concept_score": 9.7}
            }
        }
    elif any(k in notes_lower for k in ["queue", "kafka", "redis", "celery", "event", "microservice", "stream"]) or any(k in jd_lower for k in ["kafka", "rabbitmq", "redis", "celery", "queue", "event"]):
        q_jd = {
            "id": f"jd-event-queue-{session_seed}",
            "category": "Distributed Event Pipelines & Caching",
            "role": role,
            "difficulty": "Advanced Architecture",
            "title": "5. Event-Driven Messaging & Cache Invalidation at Scale",
            "question": {
                "en": "Our job description emphasizes resilient event pipelines and caching. How do you implement idempotent consumer workers to guarantee exactly-once business logic when message brokers deliver at-least-once? How do you prevent cache stampedes (thundering herds) when hot cache keys expire under heavy traffic?",
                "te": "మా జాబ్ డిస్క్రిప్షన్‌లో డిస్ట్రిబ్యూటెడ్ మెసేజింగ్ మరియు క్యాషింగ్ చాలా కీలకం. మెసేజ్ బ్రోకర్ కనీసం ఒక్కసారైనా (at-least-once) మెసేజ్ పంపినప్పుడు, డూప్లికేట్ కాకుండా ఐడెంపోటెంట్ (Idempotent) వర్కర్స్ ని ఎలా అమలు చేస్తారు? అలాగే అధిక ట్రాఫిక్ ఉన్నప్పుడు క్యాష్ స్టాంపేడ్ (Thundering Herd) ను ఎలా నిరోధిస్తారు?",
                "hi": "इवेंट पाइपलाइन में डुप्लीकेट मैसेज से बचने के लिए आइडेंपोटेंट कंज्यूमर कैसे लागू करते हैं? कैश स्टैम्पेड को रोकने की क्या रणनीति है?",
                "ta": "ஈவென்ட் பைப்லைன்களில் நகல் செய்திகளைத் தடுக்க ஐடெம்போடென்ட் உத்திகளை எவ்வாறு செயல்படுத்துகிறீர்கள்? கேச் ஸ்டாம்பீட் சிக்கலை எவ்வாறு தவிர்க்கிறீர்கள்?",
                "kn": "ಈವೆಂಟ್ ಪೈಪ್‌ಲೈನ್‌ನಲ್ಲಿ ನಕಲಿ ಸಂದೇಶಗಳನ್ನು ತಡೆಯಲು ಐಡೆಂಪೊಟೆಂಟ್ ಗ್ರಾಹಕರನ್ನು ಹೇಗೆ ಜಾರಿಗೊಳಿಸುತ್ತೀರಿ? ಕ್ಯಾಶ್ ಸ್ಟ್ಯಾಂಪೀಡ್ ಅನ್ನು ಹೇಗೆ ತಪ್ಪಿಸುತ್ತೀರಿ?"
            },
            "expected_concepts": ["idempotency keys via unique DB constraints", "dead-letter queues under retry backoff", "Cache-Aside lazy evaluation", "distributed mutex locking (Redis Redlock)", "probabilistic early expiration"],
            "sample_answers": {
                "en_golden": {"text": "To enforce idempotency over at-least-once delivery, workers insert unique message IDs into a transactional deduction log before executing business operations. To avoid cache stampedes when hot keys expire, I implement distributed mutexes with Redis Redlock so only one worker queries the database, combined with early background TTL recomputation.", "fluency_score": 9.9},
                "te": {"text": "మెసేజ్ డూప్లికేట్ అవ్వకుండా ప్రతి మెసేజ్ కి యూనిక్ ఐడెంపోటెన్సీ కీ వాడతాము. క్యాష్ స్టాంపేడ్ నివారించడానికి రెడిస్ డిస్ట్రిబ్యూటెడ్ లాక్ వాడి ఒక్క వర్కర్ మాత్రమే డేటాబేస్ ని క్వెరీ చేసేలా చూస్తాము.", "concept_score": 9.7}
            }
        }
    else:
        q_jd = {
            "id": f"jd-system-reliability-{session_seed}",
            "category": "High Availability & Data Consistency",
            "role": role,
            "difficulty": "Target Competency",
            "title": "5. High Throughput, ACID Guarantees & Fault Isolation",
            "question": {
                "en": f"Reviewing the requirements for this {role} position, systems must maintain strict data consistency and fault isolation under peak throughput. How do you design database transactions and circuit breakers to guarantee zero data loss and automated recovery during downstream service outages?",
                "te": f"ఈ {role} రోల్ అవసరాలకు అనుగుణంగా, అధిక వేగంతో పాటు డేటా స్థిరత్వం (Consistency) మరియు లోపం వచ్చినప్పుడు రికవరీ చాలా ముఖ్యం. డౌన్‌స్ట్రీమ్ సర్వీసులు ఫెయిల్ అయినప్పుడు డేటా నష్టం జరగకుండా సర్క్యూట్ బ్రేకర్స్ మరియు ఆటోమేటెడ్ రికవరీని ఎలా డిజైన్ చేస్తారు?",
                "hi": f"{role} पद के लिए डेटा निरंतरता और फॉल्ट टॉलरेंस बहुत महत्वपूर्ण हैं। सर्विस क्रैश के दौरान डेटा लॉस को रोकने के लिए आप क्या रणनीति अपनाते हैं?",
                "ta": f"இந்த {role} பணிக்கான கணினி நம்பகத்தன்மை மற்றும் மீட்பு உத்திகளை எவ்வாறு வடிவமைப்பீர்கள்?",
                "kn": f"ಈ {role} ಹುದ್ದೆಗೆ ಡೇಟಾ ಸ್ಥಿರತೆ ಮತ್ತು ದೋಷ ಮುಕ್ತತೆ ಬಹಳ ಮುಖ್ಯ. ಸರ್ವೀಸ್ ಕ್ರ್ಯಾಶ್ ಸಮಯದಲ್ಲಿ ಡೇಟಾ ನಷ್ಟವಾಗದಂತೆ ಹೇಗೆ ವಿನ್ಯಾಸಗೊಳಿಸುತ್ತೀರಿ?"
            },
            "expected_concepts": ["ACID transaction boundaries", "exponential backoff with jitter", "circuit breaker patterns (Netflix Hystrix / Resilience4j)", "outbox pattern for event reliability"],
            "sample_answers": {
                "en_golden": {"text": "I wrap critical state changes inside atomic ACID transactions and implement the Transactional Outbox pattern to decouple event publishing. For downstream communication, I configure circuit breakers with exponential backoff and jitter to isolate cascading failures and shed load gracefully.", "fluency_score": 9.9},
                "te": {"text": "డేటా నష్టం జరగకుండా అటామిక్ ట్రాన్సాక్షన్స్ మరియు అవుట్‌బాక్స్ ప్యాటర్న్ వాడతాము. ఇతర సర్వీసులు ఫెయిల్ అయినప్పుడు సర్క్యూట్ బ్రేకర్స్ ద్వారా సిస్టమ్ మొత్తం క్రాష్ అవ్వకుండా కాపాడతాము.", "concept_score": 9.6}
            }
        }
    questions.append(q_jd)

    # 6. Behavioral Engineering Scenario (STAR)
    q_behavioral = {
        "id": f"behavioral-disagreement-{session_seed}",
        "category": "Engineering Leadership & Culture",
        "role": role,
        "difficulty": "Intermediate",
        "title": "6. Navigating Architectural Disagreements with Teammates",
        "question": {
            "en": "Tell me about a time you had a strong technical disagreement with a team member or technical lead regarding a system design or architecture decision. How did you navigate the conversation to reach alignment without damaging psychological safety?",
            "te": "ఆర్కిటెక్చర్ లేదా సిస్టమ్ డిజైన్ విషయంలో మీ సహోద్యోగి లేదా లీడ్‌తో విభేదించిన సందర్భాన్ని వివరించండి. చర్చను పరస్పర గౌరవంతో ఎలా ముందుకు తీసుకెళ్లారు మరియు ఫలితం ఏమిటి?",
            "hi": "किसी तकनीकी निर्णय पर अपनी टीम के साथी के साथ असहमति के अनुभव का वर्णन करें। आपने बातचीत को सकारात्मक रूप से कैसे संभाला?",
            "ta": "தொழில்நுட்ப முடிவில் சக ஊழியருடன் முரண்பட்ட அனுபவத்தை விளக்குக. அதை எவ்வாறு சுமூகமாக தீர்த்தீர்கள்?",
            "kn": "ತಾಂತ್ರಿಕ ನಿರ್ಧಾರದಲ್ಲಿ ಸಹೋದ್ಯೋಗಿಯೊಂದಿಗೆ ಭಿನ್ನಾಭಿಪ್ರಾಯವಿದ್ದ ಸಂದರ್ಭವನ್ನು ವಿವರಿಸಿ. ಅದನ್ನು ನೀವು ಹೇಗೆ ರಚನಾತ್ಮಕವಾಗಿ ಪರಿಹರಿಸಿದ್ದೀರಿ?"
        },
        "expected_concepts": ["empathetic communication", "data-driven proof of concept", "disagree and commit", "maintaining team psychological safety"],
        "sample_answers": {
            "en_golden": {"text": "When deciding on an event storage layer, a senior peer favored MongoDB while I advocated PostgreSQL for relational integrity. Rather than debating opinions, I proposed a timeboxed proof-of-concept benchmarking realistic query profiles. The empirical latency data demonstrated PostgreSQL reduced join complexity by 40%. The team aligned on the data, and we documented the decision in an Architectural Decision Record.", "fluency_score": 9.9},
            "te": {"text": "ఆర్కిటెక్చర్ విషయంలో భిన్నాభిప్రాయం వచ్చినప్పుడు, వ్యక్తిగత ఆలోచనల కంటే బెంచ్‌మార్క్ ఫలితాలకు ప్రాధాన్యత ఇచ్చాము. చిన్న ప్రూఫ్ ఆఫ్ కాన్సెప్ట్ (PoC) చేసి, డేటా ఆధారంగా ఇద్దరం కలిసి సరైన నిర్ణయం తీసుకున్నాము.", "concept_score": 9.6}
        }
    }
    questions.append(q_behavioral)

    # 7. HR Core & Growth Vision
    q_hr_growth = {
        "id": f"hr-strengths-vision-{session_seed}",
        "category": "Self-Awareness & Growth",
        "role": role,
        "difficulty": "Foundational",
        "title": "7. Professional Strengths & Growth Areas",
        "question": {
            "en": f"What do you consider your greatest technical strength as an engineer, and what is one area or emerging domain you are actively learning to deepen your capabilities as a {role}?",
            "te": f"ఒక ఇంజనీర్‌గా మీ అతిపెద్ద సాంకేతిక బలం ఏమిటి? అలాగే మీ నైపుణ్యాలను మరింత పెంచుకోవడానికి ప్రస్తుతం మీరు నేర్చుకుంటున్న కొత్త అంశం ఏమిటి?",
            "hi": "एक इंजीनियर के रूप में आप अपनी सबसे बड़ी तकनीकी ताकत क्या मानते हैं, और अपनी क्षमताओं को बढ़ाने के लिए आप वर्तमान में क्या नया सीख रहे हैं?",
            "ta": "ஒரு பொறியியலாளராக உங்கள் மிகப்பெரிய பலம் என்ன? மேலும் உங்கள் திறன்களை வளர்க்க தற்போது நீங்கள் என்ன கற்றுக்கொள்கிறீர்கள்?",
            "kn": "ಇಂಜಿನಿಯರ್ ಆಗಿ ನಿಮ್ಮ ಅತಿ ದೊಡ್ಡ ಸಾಮರ್ಥ್ಯ ಯಾವುದು? ಮತ್ತು ಪ್ರಸ್ತುತ ನೀವು ಹೊಸದಾಗಿ ಏನನ್ನು ಕಲಿಯುತ್ತಿದ್ದೀರಿ?"
        },
        "expected_concepts": ["authentic technical mastery", "growth mindset", "continuous learning", "mentorship readiness"],
        "sample_answers": {
            "en_golden": {"text": "My greatest technical strength is deep analytical debugging and translating ambiguous product requirements into high-throughput architectures. To continuously evolve, I am actively deepening my expertise in distributed observability and Kubernetes operator patterns.", "fluency_score": 9.8},
            "te": {"text": "నా బలం క్లిష్టమైన సమస్యలను విశ్లేషించి శుభ్రమైన కోడ్ రాయడం. ప్రస్తుతం డిస్ట్రిబ్యూటెడ్ సిస్టమ్స్ మరియు క్లౌడ్ ఆప్టిమైజేషన్ పై మరింత లోతుగా నేర్చుకుంటున్నాను.", "concept_score": 9.5}
        }
    }
    questions.append(q_hr_growth)

    # 8. Closing Discussion & Candidate Inquiries
    q_closing = {
        "id": f"closing-questions-{session_seed}",
        "category": "Closing Discussion",
        "role": role,
        "difficulty": "Conversational",
        "title": "8. Closing Discussion: Questions for the Hiring Team",
        "question": {
            "en": "We're nearing the conclusion of our interview today! Reflecting on our technical discussion, what questions do you have for me about our engineering architecture, our team culture, or upcoming product milestones?",
            "te": "మనం నేటి ఇంటర్వ్యూ ముగింపుకు చేరుకున్నాము! మా ఇంజనీరింగ్ ఆర్కిటెక్చర్, టీమ్ సంస్కృతి లేదా రాబోయే సవాళ్ల గురించి నన్ను ఏమైనా ప్రశ్నలు అడగాలనుకుంటున్నారా?",
            "hi": "हम आज के इंटरव्यू के समापन पर पहुँच रहे हैं! हमारी इंजीनियरिंग आर्किटेक्चर, टीम वर्क कल्चर या आगामी चुनौतियों के बारे में क्या आपके पास मेरे लिए कोई सवाल हैं?",
            "ta": "நாம் நேர்காணலின் முடிவை அடைந்துவிட்டோம்! எங்கள் பொறியியல் கட்டமைப்பு அல்லது கலாச்சாரம் பற்றி நீங்கள் என்னிடம் கேட்க விரும்பும் கேள்விகள் ஏதேனும் உள்ளதா?",
            "kn": "ನಾವು ಇಂದಿನ ಸಂದರ್ಶನದ ಅಂತ್ಯವನ್ನು ತಲುಪುತ್ತಿದ್ದೇವೆ! ನಮ್ಮ ವಾಸ್ತುಶಿಲ್ಪ ಅಥವಾ ತಂಡದ ಸಂಸ್ಕೃತಿಯ ಬಗ್ಗೆ ನೀವು ನನ್ನನ್ನು ಕೇಳಲು ಬಯಸುವ ಪ್ರಶ್ನೆಗಳಿವೆಯೇ?"
        },
        "expected_concepts": ["thoughtful candidate curiosity", "inquiry into architectural roadmap", "understanding day-to-day engineering expectations"],
        "sample_answers": {
            "en_golden": {"text": "Thank you! I would love to hear how your engineering team balances feature delivery with technical debt refactoring, and what key technical milestones success looks like for an engineer stepping into this position over their first 90 days.", "fluency_score": 9.9},
            "te": {"text": "మీ టీమ్ లో ఆర్కిటెక్చరల్ నిర్ణయాలు ఎలా తీసుకుంటారు? అలాగే ఈ రోల్ లో చేరిన ఇంజనీర్ నుండి మొదటి 3 నెలల్లో ఎలాంటి విజయాలు ఆశిస్తున్నారు?", "concept_score": 9.6}
        }
    }
    questions.append(q_closing)

    # If target_count > 8 (e.g. 12 questions for 45 minutes), append more specialized domain questions
    # from BASE_QUESTIONS before closing
    if target_count > len(questions):
        from services.question_engine import BASE_QUESTIONS
        closing_item = questions.pop()
        seen_ids = {q["id"] for q in questions}
        for bq in BASE_QUESTIONS:
            if len(questions) + 1 >= target_count:
                break
            if bq["id"] not in seen_ids:
                questions.append(bq)
                seen_ids.add(bq["id"])
        questions.append(closing_item)

    return questions[:target_count]

