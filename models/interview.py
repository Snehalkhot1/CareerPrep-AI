"""Interview, Question, Answer, and Practice models."""
from datetime import datetime
import json
from database.database import db


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable=True)
    role = db.Column(db.String(100), nullable=False, default="Software Developer")
    technology = db.Column(db.String(100), nullable=False, default="Python")
    difficulty = db.Column(db.String(50), nullable=False, default="Medium")  # Easy, Medium, Hard
    interview_type = db.Column(db.String(50), nullable=False, default="Technical")  # Technical, HR, Mixed
    date = db.Column(db.DateTime, default=datetime.now)
    total_questions = db.Column(db.Integer, nullable=False, default=5)
    
    # Scores (0 - 100)
    overall_score = db.Column(db.Float, default=0.0)
    technical_score = db.Column(db.Float, default=0.0)
    relevance_score = db.Column(db.Float, default=0.0)
    completeness_score = db.Column(db.Float, default=0.0)
    clarity_score = db.Column(db.Float, default=0.0)
    
    # Feedback components stored as JSON strings
    strengths_json = db.Column(db.Text, nullable=True, default="[]")
    improvements_json = db.Column(db.Text, nullable=True, default="[]")
    recommended_topics_json = db.Column(db.Text, nullable=True, default="[]")
    feedback_summary = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="in_progress")  # in_progress, completed
    duration_seconds = db.Column(db.Integer, default=0)

    # Relationships
    student = db.relationship("Student", back_populates="interviews")
    internship = db.relationship("Internship", back_populates="interviews")
    questions = db.relationship("InterviewQuestion", back_populates="interview", cascade="all, delete-orphan", order_by="InterviewQuestion.question_order")
    answers = db.relationship("InterviewAnswer", back_populates="interview", cascade="all, delete-orphan")

    def get_strengths(self):
        try:
            return json.loads(self.strengths_json or "[]")
        except Exception:
            return []

    def get_improvements(self):
        try:
            return json.loads(self.improvements_json or "[]")
        except Exception:
            return []

    def get_recommended_topics(self):
        try:
            return json.loads(self.recommended_topics_json or "[]")
        except Exception:
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "internship_id": self.internship_id,
            "role": self.role,
            "technology": self.technology,
            "difficulty": self.difficulty,
            "interview_type": self.interview_type,
            "date": self.date.strftime("%Y-%m-%d %H:%M"),
            "total_questions": self.total_questions,
            "overall_score": round(self.overall_score, 1),
            "technical_score": round(self.technical_score, 1),
            "relevance_score": round(self.relevance_score, 1),
            "completeness_score": round(self.completeness_score, 1),
            "clarity_score": round(self.clarity_score, 1),
            "strengths": self.get_strengths(),
            "improvements": self.get_improvements(),
            "recommended_topics": self.get_recommended_topics(),
            "feedback_summary": self.feedback_summary,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
        }


class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    question_order = db.Column(db.Integer, nullable=False, default=1)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default="Technical")  # Technical, Theory, Coding, Behavioral
    difficulty = db.Column(db.String(50), default="Medium")
    topic = db.Column(db.String(100), default="General")
    expected_points = db.Column(db.Text, nullable=True)  # JSON or text points

    # Relationships
    interview = db.relationship("Interview", back_populates="questions")
    answer = db.relationship("InterviewAnswer", back_populates="question", uselist=False, cascade="all, delete-orphan")

    def get_expected_points(self):
        try:
            return json.loads(self.expected_points or "[]")
        except Exception:
            return [self.expected_points] if self.expected_points else []

    def to_dict(self):
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "question_order": self.question_order,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "difficulty": self.difficulty,
            "topic": self.topic,
            "expected_points": self.get_expected_points(),
            "answer": self.answer.to_dict() if self.answer else None,
        }


class InterviewAnswer(db.Model):
    __tablename__ = "interview_answers"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("interview_questions.id"), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    audio_filename = db.Column(db.String(255), nullable=True)
    
    # Component scores out of 10
    score = db.Column(db.Float, default=0.0)
    technical_correctness = db.Column(db.Float, default=0.0)
    relevance = db.Column(db.Float, default=0.0)
    completeness = db.Column(db.Float, default=0.0)
    clarity = db.Column(db.Float, default=0.0)
    
    missing_points_json = db.Column(db.Text, default="[]")
    covered_points_json = db.Column(db.Text, default="[]")
    suggestion = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    interview = db.relationship("Interview", back_populates="answers")
    question = db.relationship("InterviewQuestion", back_populates="answer")

    def get_missing_points(self):
        try:
            return json.loads(self.missing_points_json or "[]")
        except Exception:
            return []

    def get_covered_points(self):
        try:
            return json.loads(self.covered_points_json or "[]")
        except Exception:
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "answer_text": self.answer_text,
            "audio_filename": self.audio_filename,
            "score": round(self.score, 1),
            "technical_correctness": round(self.technical_correctness, 1),
            "relevance": round(self.relevance, 1),
            "completeness": round(self.completeness, 1),
            "clarity": round(self.clarity, 1),
            "covered_points": self.get_covered_points(),
            "missing_points": self.get_missing_points(),
            "suggestion": self.suggestion,
        }


class PracticeSession(db.Model):
    __tablename__ = "practice_sessions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    technology = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), default="Medium")
    questions_data = db.Column(db.Text, nullable=False)  # JSON string of generated questions & answers
    total_questions = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.now)
