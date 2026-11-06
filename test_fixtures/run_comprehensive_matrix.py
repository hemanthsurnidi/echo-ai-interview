import os
import time
import json
from playwright.sync_api import sync_playwright

FIXTURES_DIR = 'C:/Users/heman/.gemini/antigravity-ide/scratch/echo/test_fixtures'
ARTIFACT_DIR = 'C:/Users/heman/.gemini/antigravity/brain/3282d80e-0fcb-4348-9c25-18b28fa8ad05'

SCENARIOS = [
    {
        "id": "scenario_1_fullstack_telugu_dual_gnani_female",
        "name": "Scenario 1: Full Stack - Female - Dual Mode (Telugu + English) - Gnani AI - Technical",
        "role": "Full Stack Python & Cloud Engineer",
        "interviewer": "female",
        "engine": "live", # Gnani AI
        "interview_type": "technical",
        "lang_mode": "mode_c", # Dual
        "language": "te-IN", # Telugu
        "resume_file": os.path.join(FIXTURES_DIR, "resume_fullstack.txt"),
        "zip_file": os.path.join(FIXTURES_DIR, "project_fullstack.zip"),
        "git_link": "https://github.com/developer/distributed-event-cache",
        "job_desc": "Senior Full Stack Python Engineer with experience in FastAPI microservices, PostgreSQL query optimization, Redis caching, and Docker on AWS.",
        "anything_more": "Focus deeply on high-concurrency event caching, race condition prevention, and database indexing.",
        "spoken_native": "మా సిస్టమ్‌లో క్యాషింగ్ కోసం రెడిస్ మరియు డేటాబేస్ కనెక్షన్ పూలింగ్ ఉపయోగించాము. డెడ్ లెటర్ క్యూస్ ద్వారా ఫెయిల్యూర్‌లను హ్యాండిల్ చేశాము.",
        "spoken_english": "We engineered an idempotent event-driven cache layer with Redis and async worker pools to eliminate duplicate payloads."
    },
    {
        "id": "scenario_2_ml_hindi_native_free_male",
        "name": "Scenario 2: Machine Learning - Male - Mother Tongue Only (Hindi) - Free Neural - Technical",
        "role": "Machine Learning & AI Engineer",
        "interviewer": "male",
        "engine": "mock", # Free Neural
        "interview_type": "technical",
        "lang_mode": "mode_b", # Mother Tongue Only
        "language": "hi-IN", # Hindi
        "resume_file": os.path.join(FIXTURES_DIR, "resume_ml.txt"),
        "zip_file": os.path.join(FIXTURES_DIR, "project_ml.zip"),
        "git_link": "https://github.com/ai-dev/multilingual-rag-pipeline",
        "job_desc": "Machine Learning Engineer specialized in transformer architectures, vector embeddings, fine-tuning, and low-latency inference.",
        "anything_more": "Examine GPU memory optimization, FAISS vector indexing, and quantization strategies.",
        "spoken_native": "हमने बहुभाषी मॉडल के लिए ट्रांसफार्मर और FAISS वेक्टर इंडेक्स का उपयोग किया ताकि खोज की गति बहुत तेज़ हो सके।",
        "spoken_english": ""
    },
    {
        "id": "scenario_3_devops_english_free_female",
        "name": "Scenario 3: DevOps & SRE - Female - English Only - Free Neural - Technical",
        "role": "DevOps & Site Reliability Engineer",
        "interviewer": "female",
        "engine": "mock", # Free Neural
        "interview_type": "technical",
        "lang_mode": "mode_a", # English Only
        "language": "en-IN", # English
        "resume_file": os.path.join(FIXTURES_DIR, "resume_devops.txt"),
        "zip_file": os.path.join(FIXTURES_DIR, "project_devops.zip"),
        "git_link": "https://github.com/ops-lead/k8s-multi-cluster-helm",
        "job_desc": "SRE specialist for Kubernetes multi-region cluster reliability, Helm automation, and zero-downtime blue/green deployments.",
        "anything_more": "Test Kubernetes pod eviction policies, resource limits, and disaster recovery automation.",
        "spoken_native": "",
        "spoken_english": "I architected multi-tenant Kubernetes clusters with automated Helm deployments and Prometheus alerting for zero-downtime rollouts."
    },
    {
        "id": "scenario_4_hr_tamil_dual_gnani_male",
        "name": "Scenario 4: HR Round - Male - Dual Mode (Tamil + English) - Gnani AI",
        "role": "Full Stack Python & Cloud Engineer",
        "interviewer": "male",
        "engine": "live", # Gnani AI
        "interview_type": "hr",
        "lang_mode": "mode_c", # Dual
        "language": "ta-IN", # Tamil
        "resume_file": os.path.join(FIXTURES_DIR, "resume_fullstack.txt"),
        "zip_file": "",
        "git_link": "",
        "job_desc": "Assessing cross-functional teamwork, leadership under tight deadlines, and communication.",
        "anything_more": "Evaluate alignment with high-ownership culture and resolving technical disagreements constructively.",
        "spoken_native": "நான் ஒரு முழு-அடுக்கு பொறியாளர். சிக்கலான தொழில்நுட்ப சவால்களை எளிமைப்படுத்துவதும் குழுவுடன் இணைந்து பணியாற்றுவதும் எனது பலம்.",
        "spoken_english": "My strongest value proposition is proactive ownership—taking ambiguous requirements and turning them into reliable product milestones."
    },
    {
        "id": "scenario_5_hr_kannada_dual_free_female",
        "name": "Scenario 5: HR Round - Female - Dual Mode (Kannada + English) - Free Neural",
        "role": "Machine Learning & AI Engineer",
        "interviewer": "female",
        "engine": "mock", # Free Neural
        "interview_type": "hr",
        "lang_mode": "mode_c", # Dual
        "language": "kn-IN", # Kannada
        "resume_file": os.path.join(FIXTURES_DIR, "resume_ml.txt"),
        "zip_file": "",
        "git_link": "",
        "job_desc": "HR assessment for continuous learning, engineering ethics, and 5-year vision.",
        "anything_more": "Probe into how the candidate handles critical constructive feedback.",
        "spoken_native": "ನನ್ನ ಶಕ್ತಿ ವಿಶ್ಲೇಷಣಾತ್ಮಕ ಸಮಸ್ಯೆ ಪರಿಹಾರ. ತಂಡದ ಸದಸ್ಯರೊಂದಿಗೆ ಮುಕ್ತವಾಗಿ ಸಂವಹನ ನಡೆಸಿ ಉತ್ತಮ ಫಲಿತಾಂಶಗಳನ್ನು ತರುತ್ತೇನೆ.",
        "spoken_english": "I embrace feedback as a data-driven iteration tool to refine both my engineering craft and team collaboration."
    }
]

def run_test_suite():
    results = []
    print("=" * 80)
    print("STARTING COMPREHENSIVE AUTOMATED TEST MATRIX")
    print("=" * 80)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        for idx, sc in enumerate(SCENARIOS, 1):
            print(f"\n[{idx}/5] RUNNING: {sc['name']}")
            page.goto('http://127.0.0.1:8000')
            page.wait_for_selector('#card-interviewer-showcase')
            page.wait_for_timeout(300)

            # 1. Select Interviewer (Female vs Male)
            if sc['interviewer'] == 'male':
                page.click('#interviewer-btn-male')
            else:
                page.click('#interviewer-btn-female')
            page.wait_for_timeout(150)

            # 2. Select AI Model Engine in Column 3
            if sc['engine'] == 'mock':
                page.click('#btn-choice-free')
            else:
                page.click('#btn-choice-gnani')
            page.wait_for_timeout(150)

            # 3. Set Target Role
            page.fill('#input-job-role', sc['role'])

            # 4. Set Interview Type (Technical vs HR)
            if sc['interview_type'] == 'hr':
                page.click('#btn-type-hr')
            else:
                page.click('#btn-type-tech')
            page.wait_for_timeout(150)

            # 5. Set Language Mode
            if sc['lang_mode'] == 'mode_a':
                page.click('#label-mode-a')
            elif sc['lang_mode'] == 'mode_b':
                page.click('#label-mode-b')
            else:
                page.click('#label-mode-c')
            page.wait_for_timeout(150)

            # 6. Set Your Language (if visible)
            if sc['lang_mode'] != 'mode_a':
                page.select_option('#select-native-lang', sc['language'])
                page.wait_for_timeout(100)

            # 7. Upload Resume File
            if sc['resume_file'] and os.path.exists(sc['resume_file']):
                file_input = page.locator('#input-resume-file')
                file_input.set_input_files(sc['resume_file'])
                page.wait_for_timeout(400)

            # 8. Upload Project ZIP File
            if sc['zip_file'] and os.path.exists(sc['zip_file']):
                zip_input = page.locator('#input-project-zip')
                zip_input.set_input_files(sc['zip_file'])
                page.wait_for_timeout(400)

            # 9. Enter GitHub Link
            if sc['git_link']:
                page.fill('#input-git-link', sc['git_link'])

            # 10. Enter Job Description
            if sc['job_desc']:
                page.fill('#input-job-description', sc['job_desc'])

            # 11. Enter Anything More
            if sc['anything_more']:
                page.fill('#input-additional-notes', sc['anything_more'])

            # Capture Setup Screenshot
            setup_shot = os.path.join(ARTIFACT_DIR, f"{sc['id']}_setup.png")
            page.screenshot(path=setup_shot)

            # 12. Start Interview
            page.click('#btn-start-interview')
            page.wait_for_selector('#view-interview-room', state='visible')
            page.wait_for_timeout(1200)

            scenario_log = {
                "scenario": sc['name'],
                "role": sc['role'],
                "interviewer": sc['interviewer'],
                "engine": sc['engine'],
                "interview_type": sc['interview_type'],
                "lang_mode": sc['lang_mode'],
                "language": sc['language'],
                "questions_covered": []
            }

            # Conduct Interview loop: Answer each question
            max_steps = 15
            step_count = 0
            while step_count < max_steps:
                step_count += 1
                page.wait_for_timeout(400)
                is_report = page.is_visible('#view-final-feedback')
                if is_report:
                    break

                is_room = page.is_visible('#view-interview-room')
                if not is_room:
                    page.wait_for_timeout(400)
                    if page.is_visible('#view-final-feedback'):
                        break
                    continue

                q_title = page.evaluate("() => document.getElementById('theater-turn-badge')?.textContent || ''")
                q_text = page.evaluate("() => document.getElementById('room-question-text')?.textContent || ''")
                proceed_label = page.evaluate("() => document.getElementById('text-proceed-btn')?.textContent || ''")

                # Provide candidate response
                if 'English' in proceed_label:
                    spoken = sc['spoken_native'] or "Candidate explained technical concept."
                else:
                    spoken = sc['spoken_english'] or sc['spoken_native'] or "Candidate provided response."

                # Set candidate response transcript on the hidden textarea and speech preview
                page.evaluate("""(val) => {
                    const el = document.getElementById('candidate-live-transcript');
                    if (el) {
                        el.value = val;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    const prevRow = document.getElementById('live-speech-preview-row');
                    const prevText = document.getElementById('live-speech-preview-text');
                    if (prevRow && prevText) {
                        prevRow.style.display = 'block';
                        prevText.textContent = val;
                    }
                }""", spoken)

                scenario_log["questions_covered"].append({
                    "step": step_count,
                    "badge": q_title.strip(),
                    "question_text": q_text.strip(),
                    "candidate_spoken": spoken
                })

                # Test Repeat Question button
                btn_replay = page.locator('#btn-replay-question-audio')
                if btn_replay.is_visible():
                    btn_replay.click()
                    page.wait_for_timeout(100)

                # Click Proceed Answer
                btn_proceed = page.locator('#btn-proceed-answer')
                if btn_proceed.is_visible():
                    btn_proceed.click()
                    page.wait_for_timeout(800)

            # Wait for Final Diagnostic Report
            page.wait_for_selector('#view-final-feedback', state='visible', timeout=15000)
            page.wait_for_timeout(1500)

            # Inspect Report Details
            report_data = page.evaluate("""() => {
                const concept = document.getElementById('final-score-concept')?.textContent;
                const fluency = document.getElementById('final-score-fluency')?.textContent;
                const gap = document.getElementById('final-score-gap')?.textContent;
                const commStatus = document.getElementById('aspect-comm-status')?.textContent;
                const commFeedback = document.getElementById('aspect-comm-feedback')?.textContent;
                const knowStatus = document.getElementById('aspect-know-status')?.textContent;
                const knowFeedback = document.getElementById('aspect-know-feedback')?.textContent;
                const bridgeStatus = document.getElementById('aspect-bridge-status')?.textContent;
                const bridgeFeedback = document.getElementById('aspect-bridge-feedback')?.textContent;

                const qCards = [];
                document.querySelectorAll('#final-questions-review-list > div').forEach((card, i) => {
                    const qTitle = card.querySelector('strong')?.textContent;
                    const pTags = Array.from(card.querySelectorAll('p')).map(p => p.textContent.trim());
                    qCards.push({ index: i + 1, title: qTitle, details: pTags });
                });

                return {
                    scores: { concept, fluency, gap },
                    aspects: {
                        communication: { status: commStatus, feedback: commFeedback },
                        knowledge: { status: knowStatus, feedback: knowFeedback },
                        bilingual_bridge: { status: bridgeStatus, feedback: bridgeFeedback }
                    },
                    total_reviews: qCards.length,
                    question_reviews: qCards
                };
            }""")

            scenario_log["report_evaluation"] = report_data
            print(f"   -> Completed {len(scenario_log['questions_covered'])} interaction turns.")
            print(f"   -> Diagnostic Scores: Concept: {report_data['scores']['concept']}, Fluency: {report_data['scores']['fluency']}, Gap: {report_data['scores']['gap']}")
            print(f"   -> Question Reviews Generated: {report_data['total_reviews']}")

            # Test preferred answer audio playback button
            first_audio_btn = page.locator('.btn-speak-refined').first
            if first_audio_btn.is_visible():
                first_audio_btn.click()
                page.wait_for_timeout(300)
                first_audio_btn.click() # toggle stop

            # Capture Final Report Screenshot
            report_shot = os.path.join(ARTIFACT_DIR, f"{sc['id']}_report.png")
            page.screenshot(path=report_shot)
            scenario_log["screenshot_setup"] = setup_shot
            scenario_log["screenshot_report"] = report_shot

            results.append(scenario_log)

        browser.close()

    # Save full matrix results to JSON file
    out_json = os.path.join(ARTIFACT_DIR, "matrix_test_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"ALL 5 SCENARIOS FINISHED! Detailed log saved to: {out_json}")
    print("=" * 80)

if __name__ == "__main__":
    run_test_suite()
