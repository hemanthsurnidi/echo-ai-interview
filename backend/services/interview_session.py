"""
ECHO — Bilingual Interview Session State Machine (Mode C)
Enforces the strict paired sequential workflow:
Turn 1: Interviewer Native Question
Turn 2: Candidate Native Answer
Turn 3: Interviewer English Question
Turn 4: Candidate English Answer
Turn 5: Joint Evaluation
Turn 6: Feedback & Articulation Report
Turn 7: Next Question
"""

import uuid
from typing import Dict, Any, List, Optional
from services.question_engine import QuestionEngine

class InterviewSessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(
        self,
        role: str = "python_backend",
        language_mode: str = "mode_c",
        primary_language: str = "te-IN",
        candidate_profile: Optional[Dict[str, Any]] = None,
        count: int = 3
    ) -> Dict[str, Any]:
        session_id = f"echo_{uuid.uuid4().hex[:8]}"
        playlist = QuestionEngine.generate_session_questions(
            role=role,
            candidate_profile=candidate_profile,
            count=count
        )

        session = {
            "session_id": session_id,
            "role": role,
            "language_mode": language_mode,
            "primary_language": primary_language,
            "candidate_profile": candidate_profile,
            "playlist": playlist,
            "total_questions": len(playlist),
            "current_index": 0,
            "current_turn": "turn_1_native_question" if language_mode != "mode_a" else "turn_3_english_question",
            "history": []
        }
        self.sessions[session_id] = session
        return self._format_session_state(session)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        session = self.sessions.get(session_id)
        if not session:
            return None
        return self._format_session_state(session)

    def submit_answer(
        self,
        session_id: str,
        phase: str,  # 'native' or 'english'
        transcript: str
    ) -> Dict[str, Any]:
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        current_q = session["playlist"][session["current_index"]]
        
        # Find or initialize question entry in history
        if len(session["history"]) <= session["current_index"]:
            session["history"].append({
                "question_id": current_q["id"],
                "question_title": current_q["title"],
                "native_transcript": "",
                "english_transcript": "",
                "status": "in_progress"
            })

        entry = session["history"][session["current_index"]]

        if phase == "native":
            entry["native_transcript"] = transcript
            session["current_turn"] = "turn_3_english_question"
        elif phase == "english":
            entry["english_transcript"] = transcript
            # If both are completed or single mode, ready to evaluate
            session["current_turn"] = "turn_5_evaluate"

        return self._format_session_state(session)

    def advance_question(self, session_id: str) -> Dict[str, Any]:
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        if session["current_index"] + 1 < session["total_questions"]:
            session["current_index"] += 1
            session["current_turn"] = "turn_1_native_question" if session["language_mode"] != "mode_a" else "turn_3_english_question"
            return {
                "success": True,
                "has_more": True,
                "session": self._format_session_state(session)
            }
        else:
            session["current_turn"] = "completed"
            return {
                "success": True,
                "has_more": False,
                "session": self._format_session_state(session)
            }

    def _format_session_state(self, session: Dict[str, Any]) -> Dict[str, Any]:
        curr_q = session["playlist"][session["current_index"]] if session["current_index"] < session["total_questions"] else None
        curr_history = session["history"][session["current_index"]] if len(session["history"]) > session["current_index"] else {
            "native_transcript": "",
            "english_transcript": ""
        }

        return {
            "session_id": session["session_id"],
            "role": session["role"],
            "language_mode": session["language_mode"],
            "primary_language": session["primary_language"],
            "current_index": session["current_index"],
            "total_questions": session["total_questions"],
            "question_progress": f"Question {session['current_index'] + 1} of {session['total_questions']}",
            "current_question": curr_q,
            "current_turn": session["current_turn"],
            "captured_answers": curr_history,
            "can_evaluate": bool(
                curr_history.get("native_transcript") and curr_history.get("english_transcript")
            ) if session["language_mode"] == "mode_c" else bool(
                curr_history.get("native_transcript") or curr_history.get("english_transcript")
            )
        }

session_manager = InterviewSessionManager()
