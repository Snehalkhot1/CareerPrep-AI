"""Interview lifecycle orchestration."""
import json
from datetime import datetime
from models.interview import Interview, InterviewQuestion, InterviewAnswer
from ai import generate_interview_questions, evaluate_interview_answer, generate_interview_feedback_report


def create_interview_with_questions(db, student_id, role, technology, difficulty, interview_type, count=5, internship_id=None):
    """Initializes a new mock interview, generates questions, and persists them."""
    # 1. Generate questions using AI / local bank
    raw_questions = generate_interview_questions(
        role=role,
        technology=technology,
        difficulty=difficulty,
        question_type=interview_type,
        count=count,
    )

    # 2. Create Interview record
    interview = Interview(
        student_id=student_id,
        internship_id=internship_id,
        role=role,
        technology=technology,
        difficulty=difficulty,
        interview_type=interview_type,
        total_questions=len(raw_questions),
        status="in_progress",
        date=datetime.now(),
    )
    db.session.add(interview)
    db.session.flush()  # get interview.id

    # 3. Create InterviewQuestion records
    for i, q in enumerate(raw_questions, start=1):
        question_obj = InterviewQuestion(
            interview_id=interview.id,
            question_order=i,
            question_text=q["question"],
            question_type=q.get("type", "Technical"),
            difficulty=q.get("difficulty", difficulty),
            topic=q.get("topic", technology),
            expected_points=json.dumps(q.get("expected_answer_points", [])),
        )
        db.session.add(question_obj)

    db.session.commit()
    return interview


def submit_interview_answer(db, interview_id, question_id, answer_text, audio_filename=None):
    """Evaluates and records an individual answer for an interview question."""
    question = InterviewQuestion.query.filter_by(id=question_id, interview_id=interview_id).first_or_404()

    # AI Answer Evaluation
    eval_result = evaluate_interview_answer(
        question_text=question.question_text,
        expected_points=question.get_expected_points(),
        candidate_answer=answer_text,
    )

    # Check if answer already exists
    answer = InterviewAnswer.query.filter_by(question_id=question_id, interview_id=interview_id).first()
    if not answer:
        answer = InterviewAnswer(
            interview_id=interview_id,
            question_id=question_id,
            answer_text=answer_text,
            audio_filename=audio_filename,
            score=eval_result["score"],
            technical_correctness=eval_result["technical_correctness"],
            relevance=eval_result["relevance"],
            completeness=eval_result["completeness"],
            clarity=eval_result["clarity"],
            covered_points_json=json.dumps(eval_result.get("covered_points", [])),
            missing_points_json=json.dumps(eval_result.get("missing_points", [])),
            suggestion=eval_result.get("suggestion", ""),
        )
        db.session.add(answer)
    else:
        answer.answer_text = answer_text
        if audio_filename:
            answer.audio_filename = audio_filename
        answer.score = eval_result["score"]
        answer.technical_correctness = eval_result["technical_correctness"]
        answer.relevance = eval_result["relevance"]
        answer.completeness = eval_result["completeness"]
        answer.clarity = eval_result["clarity"]
        answer.covered_points_json = json.dumps(eval_result.get("covered_points", []))
        answer.missing_points_json = json.dumps(eval_result.get("missing_points", []))
        answer.suggestion = eval_result.get("suggestion", "")

    db.session.commit()
    return eval_result


def finalize_interview(db, interview_id, duration_seconds=0):
    """Calculates overall metrics, generates AI feedback report, and finalizes interview."""
    interview = Interview.query.get_or_404(interview_id)
    questions = InterviewQuestion.query.filter_by(interview_id=interview_id).order_by(InterviewQuestion.question_order).all()

    answers_data = []
    for q in questions:
        if q.answer:
            answers_data.append({
                "question": q.question_text,
                "score": q.answer.score,
                "technical_correctness": q.answer.technical_correctness,
                "relevance": q.answer.relevance,
                "completeness": q.answer.completeness,
                "clarity": q.answer.clarity,
                "covered_points": q.answer.get_covered_points(),
                "missing_points": q.answer.get_missing_points(),
                "suggestion": q.answer.suggestion,
            })
        else:
            # Unanswered question gets zero score
            answers_data.append({
                "question": q.question_text,
                "score": 0.0,
                "technical_correctness": 0.0,
                "relevance": 0.0,
                "completeness": 0.0,
                "clarity": 0.0,
                "covered_points": [],
                "missing_points": q.get_expected_points(),
                "suggestion": "Question skipped or left unanswered.",
            })

    # Synthesize feedback
    report = generate_interview_feedback_report(
        role=interview.role,
        technology=interview.technology,
        difficulty=interview.difficulty,
        answers_data=answers_data,
    )

    # Save to interview model
    interview.overall_score = report["overall_score"]
    interview.technical_score = report["technical_score"]
    interview.relevance_score = report["relevance_score"]
    interview.completeness_score = report["completeness_score"]
    interview.clarity_score = report["clarity_score"]
    interview.strengths_json = json.dumps(report["strengths"])
    interview.improvements_json = json.dumps(report["improvements"])
    interview.recommended_topics_json = json.dumps(report["recommended_topics"])
    interview.feedback_summary = report["summary"]
    interview.status = "completed"
    interview.duration_seconds = duration_seconds

    db.session.commit()
    return report
