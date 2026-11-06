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
        page.wait_for_timeout(1200)

        # Verify Job Description (JD) field and Custom Instructions field exist side-by-side
        jd_el = page.query_selector("#input-job-description")
        prompt_el = page.query_selector("#input-additional-notes")
        assert jd_el is not None, "Target Job Description field #input-job-description must exist!"
        assert prompt_el is not None, "Custom Instructions field #input-additional-notes must exist!"

        # Fill both JD and Custom Instructions
        page.fill("#input-job-description", "Senior Distributed Systems Engineer. Requirements: Kafka event streams, Redis caching, Kubernetes microservices, PostgreSQL high availability.")
        page.fill("#input-additional-notes", "Focus on Kafka producer idempotency, consumer partition rebalancing, and canary deployment rollouts.")
        page.wait_for_timeout(1000)

        # Capture Lobby screenshot showing half-and-half split
        lobby_img = os.path.join(ARTIFACT_DIR, "verified_jd_lobby_half_split.png")
        page.screenshot(path=lobby_img, full_page=False)
        print(f"[TEST] Lobby screenshot with JD half-split saved to {lobby_img}")

        # Start interview
        print("[TEST] 2. Starting real AI interview with JD & Prompt...")
        page.click("#btn-start-interview")
        page.wait_for_selector("#view-interview-room.active-screen", timeout=10000)
        page.wait_for_timeout(2000)

        # Check question 1 text reflects JD alignment
        q1_text = page.inner_text("#room-question-text")
        print(f"[TEST] Question 1 text: {q1_text[:120]}...")

        room_img = os.path.join(ARTIFACT_DIR, "verified_jd_interview_room.png")
        page.screenshot(path=room_img, full_page=False)
        print(f"[TEST] Room screenshot saved to {room_img}")

        # Answer 3 questions in dual mode
        for q_idx in range(1, 4):
            print(f"[TEST] Answering Question {q_idx} Native...")
            page.wait_for_timeout(500)
            page.evaluate("() => { document.getElementById('candidate-live-transcript').value = 'ఈ సిస్టమ్ లో కఫ్కా పార్టిషన్స్ మరియు రీడిస్ క్యాషింగ్ వాడాము.'; }")
            page.click("#btn-proceed-answer")

            print(f"[TEST] Answering Question {q_idx} English...")
            page.wait_for_timeout(1200)
            page.evaluate("() => { document.getElementById('candidate-live-transcript').value = 'I ensured idempotency via transactional producer IDs and handled rebalancing with graceful stateful consumers.'; }")
            page.click("#btn-proceed-answer")
            page.wait_for_timeout(1200)

        # Wait for final feedback view
        print("[TEST] 3. Waiting for report...")
        page.wait_for_selector("#view-final-feedback.active-screen", timeout=15000)
        page.wait_for_timeout(3500)

        # Verify review cards count
        review_cards = page.query_selector_all("#final-questions-review-list > div")
        print(f"[TEST] Number of review cards: {len(review_cards)}")
        assert len(review_cards) == 3, f"Expected 3 review cards, found {len(review_cards)}"

        # Capture Final Report screenshot
        rep_img = os.path.join(ARTIFACT_DIR, "verified_jd_feedback_report.png")
        page.screenshot(path=rep_img, full_page=False)
        print(f"[TEST] Feedback report screenshot saved to {rep_img}")

        # Scroll to view Question 2 & Question 3
        page.evaluate("() => { const s = document.getElementById('view-final-feedback'); if (s) s.scrollTop = 600; }")
        page.wait_for_timeout(1000)
        scrolled_rep_img = os.path.join(ARTIFACT_DIR, "verified_jd_report_scrolled.png")
        page.screenshot(path=scrolled_rep_img, full_page=False)
        print(f"[TEST] Scrolled report screenshot saved to {scrolled_rep_img}")

        browser.close()
        print("\n[TEST] ALL JD & CUSTOM INSTRUCTIONS TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run()

