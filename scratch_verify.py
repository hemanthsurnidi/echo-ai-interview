import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\heman\.gemini\antigravity\brain\3282d80e-0fcb-4348-9c25-18b28fa8ad05"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            permissions=["microphone"]
        )
        page = context.new_page()

        print("[TEST] 1. Navigating to ECHO lobby...")
        page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        page.wait_for_timeout(1500)

        # 1. Fill custom prompt instructions in the lobby
        page.fill("#input-additional-notes", "Focus on Kafka idempotency, worker dead-letter queues, and high-concurrency event stream pipelines.")
        page.wait_for_timeout(1000)
        
        # Take Lobby screenshot
        lobby_img = os.path.join(ARTIFACT_DIR, "verified_fixed_lobby.png")
        page.screenshot(path=lobby_img, full_page=False)
        print(f"[TEST] Lobby screenshot saved to {lobby_img}")

        # 2. Start the interview
        print("[TEST] 2. Clicking Start Interview...")
        page.click("#btn-start-interview")
        page.wait_for_selector("#view-interview-room.active-screen", timeout=10000)
        page.wait_for_timeout(2000)

        room_img = os.path.join(ARTIFACT_DIR, "verified_fixed_interview_room.png")
        page.screenshot(path=room_img, full_page=False)
        print(f"[TEST] Interview room screenshot saved to {room_img}")

        # 3. Simulate answering 3 questions in Mode C (Dual mode: native + english)
        for q_num in range(1, 4):
            print(f"\n[TEST] ---> Answering Question {q_num} Native Phase...")
            page.wait_for_timeout(1000)
            page.evaluate("""() => {
                const ta = document.getElementById('candidate-live-transcript');
                if (ta) ta.value = 'నేను ఈ సిస్టమ్ లో మాడ్యులర్ ఆర్కిటెక్చర్ వాడాను, డేటా కనెక్షన్ పూలింగ్ మరియు కాన్‌కరెన్సీ ని బ్యాలెన్స్ చేశాను.';
            }""")
            page.wait_for_timeout(800)
            page.click("#btn-proceed-answer")

            print(f"[TEST] ---> Answering Question {q_num} English Phase...")
            page.wait_for_timeout(1500)
            page.evaluate("""() => {
                const ta = document.getElementById('candidate-live-transcript');
                if (ta) ta.value = 'I implemented resilient asynchronous event workers with unique idempotency keys, exponential retry policies, and dead letter queue error telemetry.';
            }""")
            page.wait_for_timeout(800)
            page.click("#btn-proceed-answer")
            page.wait_for_timeout(1500)

        # 4. Wait for View Final Feedback screen
        print("[TEST] 4. Waiting for view-final-feedback screen...")
        page.wait_for_selector("#view-final-feedback.active-screen", timeout=15000)
        # Give report generation 3 seconds to finalize and render cards
        page.wait_for_timeout(3500)

        # Check total questions reviewed in the report
        review_cards = page.query_selector_all("#final-questions-review-list > div")
        print(f"[TEST] Number of review cards rendered in final report: {len(review_cards)}")
        assert len(review_cards) == 3, f"Expected 3 review cards in final feedback report, but found {len(review_cards)}!"

        # Check score feedback text
        score_text = page.inner_text("#aspect-bridge-feedback")
        print(f"[TEST] Bilingual Bridge feedback: '{score_text}'")

        # Take full page screenshot of the final feedback report
        report_img = os.path.join(ARTIFACT_DIR, "verified_fixed_3_questions_report.png")
        page.screenshot(path=report_img, full_page=False)
        print(f"[TEST] Final report top screenshot saved to {report_img}")

        # Scroll down to capture Strengths & Suggestions and review cards in high contrast
        page.evaluate("() => { const s = document.getElementById('view-final-feedback'); if (s) s.scrollTop = 550; }")
        page.wait_for_timeout(1000)
        report_scroll_img = os.path.join(ARTIFACT_DIR, "verified_fixed_strengths_diagnostic.png")
        page.screenshot(path=report_scroll_img, full_page=False)
        print(f"[TEST] Final report scrolled diagnostic screenshot saved to {report_scroll_img}")

        # Scroll further down to capture Question 3 and the 4 Strengths & Suggestions cards
        page.evaluate("() => { const s = document.getElementById('view-final-feedback'); if (s) s.scrollTop = 1200; }")
        page.wait_for_timeout(1000)
        bottom_img = os.path.join(ARTIFACT_DIR, "verified_fixed_bottom_strengths.png")
        page.screenshot(path=bottom_img, full_page=False)
        print(f"[TEST] Final report bottom screenshot saved to {bottom_img}")

        browser.close()
        print("\n[TEST] ALL END-TO-END VERIFICATIONS PASSED WITH FLYING COLORS!")

if __name__ == "__main__":
    run()
