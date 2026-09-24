"""Session state helper for multi-step interviews and practice sessions."""
from flask import session


def get_current_interview_id():
    return session.get("active_interview_id")


def set_current_interview_id(interview_id):
    session["active_interview_id"] = interview_id


def clear_current_interview():
    session.pop("active_interview_id", None)
    session.pop("interview_start_time", None)


def set_practice_session(questions_data):
    """Stores practice questions in session for interactive stepper."""
    session["practice_questions"] = questions_data
    session["practice_index"] = 0
    session["practice_answers"] = {}


def get_practice_session():
    return {
        "questions": session.get("practice_questions", []),
        "current_index": session.get("practice_index", 0),
        "answers": session.get("practice_answers", {}),
    }


def update_practice_answer(index, answer_data):
    answers = session.get("practice_answers", {})
    answers[str(index)] = answer_data
    session["practice_answers"] = answers
