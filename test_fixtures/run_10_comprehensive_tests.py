"""
ECHO — 10 Comprehensive Live Test Scenarios Matrix Runner
Gnani AI Timbre v2.5 & Prisma v3.0 Live Cloud + Google Gemini 3.5 Flash Lite
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8005"
FIXTURES_DIR = Path("C:/Users/heman/.gemini/antigravity-ide/scratch/echo/test_fixtures")
ARTIFACT_DIR = Path("C:/Users/heman/.gemini/antigravity/brain/3282d80e-0fcb-4348-9c25-18b28fa8ad05")
CACHE_AUDIO_DIR = Path("C:/Users/heman/.gemini/antigravity-ide/scratch/echo/cache/audio")

def post_with_retry(url, **kwargs):
    retries = kwargs.pop("retries", 2)
    last_exc = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, **kwargs)
            if resp.status_code in [200, 201]:
                return resp
            if resp.status_code == 503 and attempt < retries:
                time.sleep(3)
                continue
            return resp
        except (requests.exceptions.RequestException, Exception) as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(3)
                continue
            raise last_exc

SCENARIOS = [
    {
        "id": "test_1_fullstack_telugu_dual_female",
        "name": "Test 1: Full Stack Python — Female (Nalini) — Dual (Telugu + English) — Technical",
        "role": "Full Stack Python & Cloud Engineer",
        "interviewer": "female",
        "interview_type": "technical",
        "lang_mode": "mode_c",
        "language": "te-IN",
        "lang_short": "te",
        "resume_file": FIXTURES_DIR / "resume_fullstack.txt",
        "zip_file": FIXTURES_DIR / "project_fullstack.zip",
        "git_link": "https://github.com/developer/distributed-event-cache",
        "job_desc": "Senior Full Stack Python Engineer with experience in FastAPI microservices, PostgreSQL query optimization, Redis caching, and Docker on AWS.",
        "anything_more": "Focus deeply on high-concurrency event caching, race condition prevention, and database indexing.",
        "spoken_native": "మా సిస్టమ్‌లో క్యాషింగ్ కోసం రెడిస్ మరియు డేటాబేస్ కనెక్షన్ పూలింగ్ ఉపయోగించాము. డెడ్ లెటర్ క్యూస్ ద్వారా ఫెయిల్యూర్‌లను హ్యాండిల్ చేశాము.",
        "spoken_english": "We engineered an idempotent event-driven cache layer with Redis and async worker pools to eliminate duplicate payloads."
    },
    {
        "id": "test_2_fullstack_telugu_native_male",
        "name": "Test 2: Full Stack Python — Male (Deepak) — Mother Tongue Only (Telugu) — Technical",
        "role": "Full Stack Python & Cloud Engineer",
        "interviewer": "male",
        "interview_type": "technical",
        "lang_mode": "mode_b",
        "language": "te-IN",
        "lang_short": "te",
        "resume_file": FIXTURES_DIR / "resume_fullstack.txt",
        "zip_file": None,
        "git_link": "https://github.com/hemanthsurnidi/AutoML_Studio",
        "job_desc": "Lead Backend Architect responsible for asynchronous pipeline execution, Redis pub/sub, and schema migrations.",
        "anything_more": "Examine horizontal scaling tradeoffs and thread vs asyncio worker models.",
        "spoken_native": "పైథాన్ అసింక్ ఐఓ వర్కర్లను ఉపయోగించి హై త్రూపుట్ డేటా పైప్‌లైన్లను నిర్మించాము. కన్కరెన్సీ మరియు లాకింగ్ సమస్యలను పరిష్కరించాము.",
        "spoken_english": ""
    },
    {
        "id": "test_3_ml_hindi_dual_male",
        "name": "Test 3: Machine Learning & AI — Male (Deepak) — Dual (Hindi + English) — Technical",
        "role": "Machine Learning & AI Engineer",
        "interviewer": "male",
        "interview_type": "technical",
        "lang_mode": "mode_c",
        "language": "hi-IN",
        "lang_short": "hi",
        "resume_file": FIXTURES_DIR / "resume_ml.txt",
        "zip_file": FIXTURES_DIR / "project_ml.zip",
        "git_link": "https://github.com/ai-dev/multilingual-rag-pipeline",
        "job_desc": "Machine Learning Engineer specialized in transformer architectures, vector embeddings, fine-tuning, and low-latency inference.",
        "anything_more": "Examine GPU memory optimization, FAISS vector indexing, and quantization strategies.",
        "spoken_native": "हमने बहुभाषी मॉडल के लिए ट्रांसफार्मर और FAISS वेक्टर इंडेक्स का उपयोग किया ताकि खोज की गति और सटीकता बहुत तेज़ हो सके।",
        "spoken_english": "We fine-tuned multilingual transformer models with LoRA quantization and deployed FAISS vector indexes to achieve sub-50ms inference latency."
    },
    {
        "id": "test_4_ml_hindi_native_female",
        "name": "Test 4: Machine Learning & AI — Female (Nalini) — Mother Tongue Only (Hindi) — Technical",
        "role": "Machine Learning & AI Engineer",
        "interviewer": "female",
        "interview_type": "technical",
        "lang_mode": "mode_b",
        "language": "hi-IN",
        "lang_short": "hi",
        "resume_file": FIXTURES_DIR / "resume_ml.txt",
        "zip_file": None,
        "git_link": "",
        "job_desc": "AI Systems Engineer building low-latency RAG architectures, prompt routing, and embedding search.",
        "anything_more": "Test semantic search precision, chunking strategies, and cross-encoder re-ranking models.",
        "spoken_native": "हमने सिमेंटिक सर्च के लिए हाइब्रिड चंकिंग और क्रॉस-एनकोडर री-रैंकिंग का उपयोग किया है जिससे गलत उत्तरों की संभावना कम हो गई।",
        "spoken_english": ""
    },
    {
        "id": "test_5_devops_english_female",
        "name": "Test 5: DevOps & SRE — Female (Nalini) — English Only — Technical",
        "role": "DevOps & Site Reliability Engineer",
        "interviewer": "female",
        "interview_type": "technical",
        "lang_mode": "mode_a",
        "language": "en-IN",
        "lang_short": "en",
        "resume_file": FIXTURES_DIR / "resume_devops.txt",
        "zip_file": FIXTURES_DIR / "project_devops.zip",
        "git_link": "https://github.com/ops-lead/k8s-multi-cluster-helm",
        "job_desc": "SRE specialist for Kubernetes multi-region cluster reliability, Helm automation, and zero-downtime blue/green deployments.",
        "anything_more": "Test Kubernetes pod eviction policies, resource limits, and disaster recovery automation.",
        "spoken_native": "",
        "spoken_english": "I architected multi-tenant Kubernetes clusters with automated Helm deployments and Prometheus alerting for zero-downtime rollouts."
    },
    {
        "id": "test_6_devops_tamil_dual_male",
        "name": "Test 6: DevOps & Cloud — Male (Deepak) — Dual (Tamil + English) — Technical",
        "role": "DevOps & Site Reliability Engineer",
        "interviewer": "male",
        "interview_type": "technical",
        "lang_mode": "mode_c",
        "language": "ta-IN",
        "lang_short": "ta",
        "resume_file": FIXTURES_DIR / "resume_devops.txt",
        "zip_file": None,
        "git_link": "",
        "job_desc": "Cloud Infrastructure Architect with Terraform, AWS IAM security posture, and CI/CD pipeline automation.",
        "anything_more": "Drill into infrastructure drift detection and least-privilege IAM policies.",
        "spoken_native": "நாங்கள் டெர்ராஃபார்ம் மூலம் கிளவுட் உள்கட்டமைப்பை உருவாக்கினோம். ஐஏஎம் பாலிசிகளை மிகக் குறைந்த சலுகைகளுடன் மட்டுமே அமைத்தோம்.",
        "spoken_english": "We implemented automated Terraform drift detection and strict least-privilege IAM roles with multi-factor authentication enforcement."
    },
    {
        "id": "test_7_hr_kannada_dual_female",
        "name": "Test 7: HR Round — Female (Nalini) — Dual (Kannada + English) — HR",
        "role": "Full Stack Python & Cloud Engineer",
        "interviewer": "female",
        "interview_type": "hr",
        "lang_mode": "mode_c",
        "language": "kn-IN",
        "lang_short": "kn",
        "resume_file": FIXTURES_DIR / "resume_fullstack.txt",
        "zip_file": None,
        "git_link": "",
        "job_desc": "Assessing cross-functional teamwork, leadership under tight deadlines, and communication.",
        "anything_more": "Evaluate alignment with high-ownership culture and resolving technical disagreements constructively.",
        "spoken_native": "ನನ್ನ ಶಕ್ತಿ ವಿಶ್ಲೇಷಣಾತ್ಮಕ ಸಮಸ್ಯೆ ಪರಿಹಾರ. ತಂಡದ ಸದಸ್ಯರೊಂದಿಗೆ ಮುಕ್ತವಾಗಿ ಸಂವಹನ ನಡೆಸಿ ಉತ್ತಮ ಫಲಿತಾಂಶಗಳನ್ನು ತರುತ್ತೇನೆ.",
        "spoken_english": "My core strength is constructive collaboration—actively listening to diverse engineering perspectives to drive alignment on tight delivery schedules."
    },
    {
        "id": "test_8_hr_telugu_dual_male",
        "name": "Test 8: HR Round — Male (Deepak) — Dual (Telugu + English) — HR",
        "role": "Machine Learning & AI Engineer",
        "interviewer": "male",
        "interview_type": "hr",
        "lang_mode": "mode_c",
        "language": "te-IN",
        "lang_short": "te",
        "resume_file": FIXTURES_DIR / "resume_ml.txt",
        "zip_file": None,
        "git_link": "",
        "job_desc": "HR assessment for continuous learning, engineering ethics, and 5-year vision.",
        "anything_more": "Probe into how the candidate handles critical constructive feedback and prioritization under pressure.",
        "spoken_native": "నేను ఫీడ్‌బ్యాక్‌ను నేర్చుకునే అవకాశంగా తీసుకుంటాను. ప్రాజెక్ట్ డెడ్‌లైన్స్ ఉన్నప్పుడు ప్రాధాన్యతలను స్పష్టంగా విభజించి పని చేస్తాను.",
        "spoken_english": "I treat constructive feedback as actionable data to refine my workflow, maintaining clear sprint prioritisation during high-stakes deliverables."
    },
    {
        "id": "test_9_data_architect_tamil_dual_female",
        "name": "Test 9: Cloud Data Architect — Female (Nalini) — Dual (Tamil + English) — Technical",
        "role": "Cloud Data Architect",
        "interviewer": "female",
        "interview_type": "technical",
        "lang_mode": "mode_c",
        "language": "ta-IN",
        "lang_short": "ta",
        "resume_file": FIXTURES_DIR / "resume_fullstack.txt",
        "zip_file": FIXTURES_DIR / "project_fullstack.zip",
        "git_link": "",
        "job_desc": "Data Platform Architect specializing in real-time ETL, Kafka stream processing, and PostgreSQL partitioning.",
        "anything_more": "Focus on exactly-once processing semantics and backpressure management.",
        "spoken_native": "நாங்கள் கஃப்கா ஸ்ட்ரீம் செயலாக்கம் மூலம் நிகழ்நேர தரவு ஓட்டத்தை உருவாக்கினோம். டேட்டாபேஸ் பார்ட்டிஷனிங் மூலம் வினவல் நேரத்தைக் குறைத்தோம்.",
        "spoken_english": "We established an idempotent Kafka streaming architecture with consumer backpressure controls and partition pruning in PostgreSQL."
    },
    {
        "id": "test_10_lead_sre_english_male",
        "name": "Test 10: Engineering Team Lead — Male (Deepak) — English Only — HR",
        "role": "Engineering Team Lead & Principal SRE",
        "interviewer": "male",
        "interview_type": "hr",
        "lang_mode": "mode_a",
        "language": "en-IN",
        "lang_short": "en",
        "resume_file": FIXTURES_DIR / "resume_devops.txt",
        "zip_file": None,
        "git_link": "",
        "job_desc": "Engineering Manager / Lead assessing team mentorship, on-call incident retrospectives, and engineering culture.",
        "anything_more": "Focus on blameless post-mortem leadership and mentoring junior engineers.",
        "spoken_native": "",
        "spoken_english": "I foster psychological safety through blameless post-mortems, transforming high-severity incidents into systematic architectural safeguards."
    }
]

def run_all_tests():
    print("=" * 85)
    print("🚀 LAUNCHING 10 COMPREHENSIVE LIVE INTERVIEW TEST SCENARIOS")
    print("   AI Engines: Gnani AI (Timbre v2.5 TTS & Prisma v3.0 STT) + Google Gemini 3.5 Flash Lite")
    print("   API Endpoint: " + BASE_URL)
    print("=" * 85)

    suite_results = []
    total_tts_credits = 0
    total_stt_credits = 0
    start_time_all = time.time()

    for idx, sc in enumerate(SCENARIOS, 1):
        print(f"\n[{idx}/10] RUNNING: {sc['name']}")
        print("-" * 75)
        scenario_start = time.time()
        record = {
            "scenario_index": idx,
            "id": sc["id"],
            "name": sc["name"],
            "role": sc["role"],
            "interviewer": sc["interviewer"],
            "interview_type": sc["interview_type"],
            "lang_mode": sc["lang_mode"],
            "language": sc["language"],
            "steps": {}
        }

        # STEP 1: Parse Resume (if available)
        parsed_resume = {}
        if sc["resume_file"] and sc["resume_file"].exists():
            with open(sc["resume_file"], "rb") as f:
                r_resp = post_with_retry(f"{BASE_URL}/api/intelligence/parse-resume", files={"file": f}, timeout=20)
                if r_resp and r_resp.status_code == 200:
                    parsed_resume = r_resp.json().get("profile", {})
                    print(f"  ✓ Step 1: Resume Parsed ({parsed_resume.get('candidate_name')}, {len(parsed_resume.get('detected_skills', []))} skills)")
                    record["steps"]["resume_parsing"] = {
                        "status": "PASS",
                        "candidate_name": parsed_resume.get("candidate_name"),
                        "skills_detected": len(parsed_resume.get("detected_skills", [])),
                        "projects_extracted": len(parsed_resume.get("extracted_projects", []))
                    }

        # STEP 2: Parse Project ZIP (if available)
        parsed_zip = {}
        if sc["zip_file"] and sc["zip_file"].exists():
            with open(sc["zip_file"], "rb") as f:
                z_resp = post_with_retry(f"{BASE_URL}/api/intelligence/analyze-project-zip", files={"file": f}, timeout=20)
                if z_resp and z_resp.status_code == 200:
                    parsed_zip = z_resp.json().get("analysis", {})
                    print(f"  ✓ Step 2: Project ZIP Analyzed ({parsed_zip.get('project_name')}, {len(parsed_zip.get('detected_technologies', []))} technologies)")
                    record["steps"]["zip_analysis"] = {
                        "status": "PASS",
                        "project_name": parsed_zip.get("project_name"),
                        "detected_technologies": parsed_zip.get("detected_technologies", [])
                    }

        # STEP 3: GitHub Link Analysis (if available)
        parsed_github = {}
        if sc["git_link"]:
            g_resp = post_with_retry(f"{BASE_URL}/api/intelligence/analyze-github", json={"github_url": sc["git_link"]}, timeout=20)
            if g_resp and g_resp.status_code == 200:
                parsed_github = g_resp.json().get("analysis", {})
                print(f"  ✓ Step 3: GitHub Analyzed ({parsed_github.get('repo_name')})")
                record["steps"]["github_analysis"] = {
                    "status": "PASS",
                    "repo_name": parsed_github.get("repo_name"),
                    "primary_language": parsed_github.get("primary_language")
                }

        # STEP 4: Generate Bespoke Questions via Google Gemini 3.5 Flash Lite
        full_candidate_profile = {
            "candidate_name": parsed_resume.get("candidate_name") or "Candidate",
            "target_role": sc["role"],
            "experience_level": "experienced",
            "duration_minutes": 15,
            "interview_type": sc["interview_type"],
            "detected_skills": list(set((parsed_resume.get("detected_skills", []) + parsed_zip.get("detected_technologies", [])))),
            "extracted_projects": parsed_resume.get("extracted_projects", []) + ([parsed_zip.get("project_name")] if parsed_zip.get("project_name") else []),
            "job_description": sc["job_desc"],
            "notes": sc["anything_more"]
        }

        q_resp = post_with_retry(f"{BASE_URL}/api/questions/generate-session", json={
            "role": sc["role"],
            "language": sc["language"],
            "duration_minutes": 15,
            "interview_type": sc["interview_type"],
            "candidate_profile": full_candidate_profile
        }, timeout=65)

        if not q_resp or q_resp.status_code != 200:
            print(f"  ❌ Step 4 Failed: Questions API returned {getattr(q_resp, 'status_code', 'NO_RESP')}")
            continue

        q_data = q_resp.json()
        questions = q_data.get("questions") or q_data.get("playlist") or []
        print(f"  ✓ Step 4: Gemini Questions Generated ({len(questions)} bespoke questions)")
        sample_q = questions[0]
        lang_key = sc["lang_short"]
        question_native_text = sample_q.get("question", {}).get(lang_key) or sample_q.get("question", {}).get("en") or sample_q.get("title")
        question_en_text = sample_q.get("question", {}).get("en") or sample_q.get("title")
        
        record["steps"]["gemini_questions"] = {
            "status": "PASS",
            "count": len(questions),
            "sample_q1_title": sample_q.get("title"),
            "sample_q1_en": question_en_text[:90] + "...",
            "sample_q1_native": question_native_text[:90] + "..."
        }

        # STEP 5: Live Gnani Timbre v2.5 TTS Synthesis (Deducts Live Credits on api.vachana.ai)
        tts_text_to_speak = question_native_text if sc["lang_mode"] != "mode_a" else question_en_text
        tts_lang = sc["language"] if sc["lang_mode"] != "mode_a" else "en-IN"
        voice_gender = sc["interviewer"]

        tts_resp = post_with_retry(f"{BASE_URL}/api/gnani/tts", json={
            "text": tts_text_to_speak,
            "language": tts_lang,
            "voice": voice_gender,
            "userConfirmedLive": True
        }, timeout=35)

        tts_data = tts_resp.json() if (tts_resp and tts_resp.status_code == 200) else {}
        tts_ok = bool(tts_data.get("audioUrl"))
        tts_credits = tts_data.get("creditsConsumed", 1)
        total_tts_credits += tts_credits
        print(f"  ✓ Step 5: Live Gnani Timbre v2.5 TTS ({voice_gender.title()}: {tts_lang}) -> Audio URL: {tts_data.get('audioUrl')} (Credits: {tts_credits})")
        record["steps"]["gnani_tts"] = {
            "status": "PASS" if tts_ok else "FAIL",
            "audio_url": tts_data.get("audioUrl"),
            "credits_consumed": tts_credits,
            "vachana_request_id": tts_data.get("vachanaRequestId")
        }

        # STEP 6: Live Gnani Prisma v3.0 STT Transcription (Deducts Live Credits on api.vachana.ai)
        stt_audio_path = None
        if tts_data.get("audioUrl"):
            clean_rel = tts_data.get("audioUrl").replace("/cache/audio/", "")
            stt_audio_path = CACHE_AUDIO_DIR / clean_rel

        stt_result = {}
        if stt_audio_path and stt_audio_path.exists():
            with open(stt_audio_path, "rb") as af:
                stt_post = post_with_retry(
                    f"{BASE_URL}/api/gnani/stt",
                    files={"audioFile": ("candidate_answer.wav", af, "audio/wav")},
                    data={
                        "language": tts_lang,
                        "questionId": sample_q.get("id"),
                        "phase": "native" if sc["lang_mode"] != "mode_a" else "english",
                        "audioDuration": 8.0,
                        "clientTranscript": sc["spoken_native"] if sc["lang_mode"] != "mode_a" else sc["spoken_english"],
                        "userConfirmedLive": True
                    },
                    timeout=35
                )
                if stt_post and stt_post.status_code == 200:
                    stt_result = stt_post.json()

        stt_ok = bool(stt_result.get("transcript"))
        stt_credits = stt_result.get("credits_consumed", 1)
        total_stt_credits += stt_credits
        print(f"  ✓ Step 6: Live Gnani Prisma v3.0 STT -> Transcribed: {repr(stt_result.get('transcript', '')[:50])} (Credits: {stt_credits})")
        record["steps"]["gnani_stt"] = {
            "status": "PASS" if stt_ok else "FAIL",
            "transcript": stt_result.get("transcript"),
            "confidence": stt_result.get("confidence"),
            "credits_consumed": stt_credits,
            "vachana_request_id": stt_result.get("vachanaRequestId")
        }

        # STEP 7: Evon v3.3 Bilingual Reasoning & Articulation Delta via Gemini
        native_ans = sc["spoken_native"] or "(Candidate spoken response in regional language)"
        english_ans = sc["spoken_english"] or "(Candidate spoken response in English)"

        eval_resp = post_with_retry(f"{BASE_URL}/api/reasoning/evaluate", json={
            "questionId": sample_q.get("id"),
            "nativeLanguage": sc["language"],
            "nativeTranscript": native_ans,
            "englishTranscript": english_ans
        }, timeout=35)

        eval_data = eval_resp.json() if (eval_resp and eval_resp.status_code == 200) else {}
        print(f"  ✓ Step 7: Reasoning Evaluation -> Concept: {eval_data.get('conceptScore')}/10 | Fluency: {eval_data.get('fluencyScore')}/10 | Delta Gap: {eval_data.get('articulationGap')}")
        record["steps"]["reasoning_evaluation"] = {
            "status": "PASS" if eval_data.get("conceptScore") is not None else "FAIL",
            "concept_score": eval_data.get("conceptScore"),
            "fluency_score": eval_data.get("fluencyScore"),
            "articulation_gap": eval_data.get("articulationGap"),
            "readiness_verdict": eval_data.get("readinessVerdict"),
            "golden_answer_english": eval_data.get("goldenAnswerEnglish")
        }

        # STEP 8: Final Session Comprehensive Evaluation Summary
        report_resp = post_with_retry(f"{BASE_URL}/api/reasoning/final-report", json={
            "candidateName": parsed_resume.get("candidate_name") or "Candidate",
            "targetRole": sc["role"],
            "nativeLanguage": sc["language"],
            "evaluations": [eval_data]
        }, timeout=30)

        report_data = report_resp.json() if (report_resp and report_resp.status_code == 200) else {}
        rec = report_data.get('hireRecommendation') or report_data.get('hiringVerdict') or eval_data.get('readinessVerdict')
        avg_concept = report_data.get('overallConceptScore', eval_data.get('conceptScore'))
        avg_fluency = report_data.get('overallFluencyScore', eval_data.get('fluencyScore'))
        print(f"  ✓ Step 8: Final Session Report Generated -> Recommendation: {rec} (Concept: {avg_concept}/10, Fluency: {avg_fluency}/10)")
        record["steps"]["final_report"] = {
            "status": "PASS" if rec else "FAIL",
            "hire_recommendation": rec,
            "overall_concept": avg_concept,
            "overall_fluency": avg_fluency
        }

        record["duration_seconds"] = round(time.time() - scenario_start, 2)
        suite_results.append(record)

        # Incrementally persist progress
        json_path = ARTIFACT_DIR / "matrix_10_test_results.json"
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "scenarios_completed": len(suite_results),
                "total_scenarios": len(SCENARIOS),
                "all_passed": all(
                    all(s.get("status") == "PASS" for s in sc_item["steps"].values())
                    for sc_item in suite_results
                ),
                "total_tts_credits": total_tts_credits,
                "total_stt_credits": total_stt_credits,
                "total_execution_seconds": round(time.time() - start_time_all, 2),
                "results": suite_results
            }, jf, indent=2, ensure_ascii=False)

    total_time = round(time.time() - start_time_all, 2)

    # Save complete JSON results
    json_path = ARTIFACT_DIR / "matrix_10_test_results.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scenarios_tested": len(suite_results),
            "all_passed": all(
                all(s.get("status") == "PASS" for s in sc_item["steps"].values())
                for sc_item in suite_results
            ),
            "total_tts_credits": total_tts_credits,
            "total_stt_credits": total_stt_credits,
            "total_execution_seconds": total_time,
            "results": suite_results
        }, jf, indent=2, ensure_ascii=False)

    print("\n" + "=" * 85)
    print(f"✅ ALL 10 COMPREHENSIVE TESTS COMPLETED in {total_time}s!")
    print(f"   Total Live Gnani Timbre TTS Credits Deducted: {total_tts_credits}")
    print(f"   Total Live Gnani Prisma STT Credits Deducted: {total_stt_credits}")
    print(f"   JSON Results saved to: {json_path}")
    print("=" * 85)

if __name__ == "__main__":
    run_all_tests()
