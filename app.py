"""CareerPrep AI - Main Flask Application Entrypoint."""
import os
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
)
from werkzeug.utils import secure_filename

from config import Config
from database.database import db, init_db
from models.student import Student
from models.internship import Internship
from models.application import Application
from models.interview import Interview, InterviewQuestion, InterviewAnswer

from internship import (
    normalize_and_save_internships,
    apply_internship_filters,
    save_or_update_application,
    get_application_status_map,
    get_dashboard_tracker_stats,
)
from ai import (
    ai_service,
    generate_interview_questions,
    evaluate_interview_answer,
    generate_interview_feedback_report,
)
from interview import (
    create_interview_with_questions,
    submit_interview_answer,
    finalize_interview,
    get_grade_and_badge,
    set_practice_session,
    get_practice_session,
    update_practice_answer,
)
from speech import is_allowed_audio_file, save_audio_file, stt_service

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)
init_db(app)


def get_current_student():
    """Return the student for the currently logged-in session only."""
    student_id = session.get("student_id")
    if not student_id:
        return None
    return db.session.get(Student, student_id)


# Context Processors for global template variables
@app.context_processor
def inject_global_variables():
    student = get_current_student()
    return {
        "student": student,
        "ai_status": ai_service.get_status(),
        "current_year": datetime.now().year,
        "logged_in": bool(student),
    }


@app.route("/login", methods=["GET", "POST"])
def login():
    """Simple login screen using the student email and password."""
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        if not email or not password:
            flash("Please enter both your email and password.", "error")
            return render_template("login.html")

        student = Student.query.filter_by(email=email).first()

        if not student:
            flash("No student record was found. Please create your profile first.", "error")
            return render_template("login.html")

        demo_password = "careerprep123"
        if password != demo_password:
            flash("Incorrect password. Use the demo password shown below.", "error")
            return render_template("login.html")

        session["student_id"] = student.id
        session["student_name"] = student.name
        flash(f"Welcome back, {student.name}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Minimal signup page to support the Create one flow."""
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        if not name or not email or not password:
            flash("Please complete all signup fields.", "error")
            return render_template("signup.html")

        existing = Student.query.filter_by(email=email).first()
        if existing:
            flash("An account with this email already exists. Please log in instead.", "error")
            return render_template("signup.html")

        student = Student(
            name=name,
            email=email,
            college="Engineering College",
            degree="B.Tech",
            branch="Computer Science & Engineering",
            year="1st Year",
            skills="Python, SQL, JavaScript",
            preferred_role="Python Developer",
            preferred_location="Remote",
            preferred_type="Work From Home",
        )
        db.session.add(student)
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    """Clear the active session and return to the login page."""
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


# ============================================================================
# 1. LANDING PAGE & DASHBOARD
# ============================================================================

@app.route("/")
def index():
    """Professional landing page showcasing the 4 core pillars."""
    if not session.get("student_id"):
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Student progress dashboard with metrics, pipeline stats, and charts."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))
    stats = get_dashboard_tracker_stats(student.id)

    # Calculate interview metrics
    interviews = Interview.query.filter_by(student_id=student.id, status="completed").order_by(Interview.id.desc()).all()
    completed_count = len(interviews)
    
    if completed_count > 0:
        avg_score = round(sum(iv.overall_score for iv in interviews) / completed_count, 1)
        avg_tech = round(sum(iv.technical_score for iv in interviews) / completed_count, 1)
        avg_rel = round(sum(iv.relevance_score for iv in interviews) / completed_count, 1)
        avg_comp = round(sum(iv.completeness_score for iv in interviews) / completed_count, 1)
        avg_clar = round(sum(iv.clarity_score for iv in interviews) / completed_count, 1)
        latest_score = round(interviews[0].overall_score, 1)
    else:
        avg_score = avg_tech = avg_rel = avg_comp = avg_clar = latest_score = 0.0

    interview_stats = {
        "completed_count": completed_count,
        "avg_score": avg_score,
        "latest_score": latest_score,
        "avg_technical": avg_tech,
        "avg_relevance": avg_rel,
        "avg_completeness": avg_comp,
        "avg_clarity": avg_clar,
    }

    return render_template(
        "dashboard.html",
        student=student,
        stats=stats,
        interview_stats=interview_stats,
        recent_interviews=interviews[:5],
    )


# ============================================================================
# 2. STUDENT PROFILE
# ============================================================================

@app.route("/profile", methods=["GET", "POST"])
def profile():
    """View and update student profile and uploaded resume."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))

    if request.method == "POST":
        student.name = request.form.get("name", student.name).strip()
        student.email = request.form.get("email", student.email).strip()
        student.college = request.form.get("college", student.college).strip()
        student.degree = request.form.get("degree", student.degree).strip()
        student.branch = request.form.get("branch", student.branch).strip()
        student.year = request.form.get("year", student.year).strip()
        student.skills = request.form.get("skills", student.skills).strip()
        student.preferred_role = request.form.get("preferred_role", student.preferred_role).strip()
        student.preferred_location = request.form.get("preferred_location", student.preferred_location).strip()
        student.preferred_type = request.form.get("preferred_type", student.preferred_type).strip()

        # Handle resume file upload
        resume_file = request.files.get("resume")
        if resume_file and resume_file.filename:
            ext = resume_file.filename.rsplit(".", 1)[1].lower() if "." in resume_file.filename else ""
            if ext in Config.ALLOWED_RESUME_EXTENSIONS:
                safe_name = f"resume_{student.id}_{secure_filename(resume_file.filename)}"
                save_path = os.path.join(Config.UPLOAD_FOLDER, safe_name)
                resume_file.save(save_path)
                student.resume_filename = safe_name

        db.session.commit()
        flash("Profile information updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", student=student)


# ============================================================================
# 3. INTERNSHIP TRACKER & SEARCH
# ============================================================================

@app.route("/internships")
def internships():
    """List internship opportunities with multi-criteria filtering."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))
    filters = {
        "keyword": request.args.get("keyword", ""),
        "technology": request.args.get("technology", "All"),
        "location": request.args.get("location", "Any"),
        "stipend": request.args.get("stipend", "All"),
        "type": request.args.get("type", "All"),
        "sort": request.args.get("sort", "latest"),
    }

    query = apply_internship_filters(Internship.query, Internship, filters)
    internship_list = query.all()
    status_map = get_application_status_map(student.id)

    return render_template(
        "internships.html",
        internships=internship_list,
        status_map=status_map,
        filters=filters,
    )


@app.route("/internships/refresh", methods=["POST"])
def refresh_internships():
    """Fetches latest opportunities from external and curated feeds."""
    added = normalize_and_save_internships(db, Internship)
    if added > 0:
        flash(f"Successfully refreshed internships! {added} new listing(s) imported.", "success")
    else:
        flash("All internship feeds are up-to-date. No duplicates found.", "info")
    return redirect(url_for("internships"))


@app.route("/internships/save", methods=["POST"])
def save_internship():
    """Saves or updates tracking status for an internship."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))
    internship_id = request.form.get("internship_id", type=int)
    status = request.form.get("status", "Saved")

    if internship_id:
        save_or_update_application(db, student.id, internship_id, status=status)
        flash(f"Internship status updated to '{status}'.", "success")

    return redirect(request.referrer or url_for("internships"))


# ============================================================================
# 4. INTERVIEW SETUP & AI QUESTION GENERATOR
# ============================================================================

@app.route("/interview")
def interview_setup():
    """Interview setup page. Pre-fills role & tech if linked from an internship."""
    target_role = request.args.get("role", "Python Developer")
    target_tech = request.args.get("tech", "Python")
    internship_id = request.args.get("internship_id", type=int)
    associated_internship = db.session.get(Internship, internship_id) if internship_id else None

    return render_template(
        "interview_setup.html",
        target_role=target_role,
        target_tech=target_tech,
        associated_internship=associated_internship,
    )


@app.route("/generate-questions", methods=["POST"])
def generate_questions_route():
    """Generates structured questions and stores them in session for exploration."""
    role = request.form.get("role", "Python Developer")
    technology = request.form.get("technology", "Python")
    difficulty = request.form.get("difficulty", "Medium")
    question_type = request.form.get("question_type", "Mixed")
    count = int(request.form.get("count", 5))

    questions = generate_interview_questions(
        role=role,
        technology=technology,
        difficulty=difficulty,
        question_type=question_type,
        count=count,
    )

    session["last_generated_questions"] = questions
    session["last_gen_role"] = role
    session["last_gen_tech"] = technology
    session["last_gen_difficulty"] = difficulty

    return redirect(url_for("view_questions"))


@app.route("/questions")
def view_questions():
    """Displays generated question bank."""
    questions = session.get("last_generated_questions", [])
    if not questions:
        flash("Please configure and generate interview questions first.", "info")
        return redirect(url_for("interview_setup"))

    return render_template(
        "questions.html",
        questions=questions,
        role=session.get("last_gen_role", "Developer"),
        technology=session.get("last_gen_tech", "Python"),
        difficulty=session.get("last_gen_difficulty", "Medium"),
    )


# ============================================================================
# 5. PRACTICE MODE
# ============================================================================

@app.route("/practice/start", methods=["POST"])
def start_practice():
    """Transfers generated questions into practice mode session."""
    questions = session.get("last_generated_questions", [])
    if not questions:
        # Generate default practice questions
        questions = generate_interview_questions("Python Developer", "Python", "Medium", "Technical", 5)

    set_practice_session(questions)
    return redirect(url_for("practice", index=0))


@app.route("/practice")
def practice():
    """Interactive question-by-question practice mode."""
    p_data = get_practice_session()
    questions = p_data["questions"]
    index = request.args.get("index", 0, type=int)

    if not questions or index >= len(questions):
        flash("Practice session ended or not started.", "info")
        return redirect(url_for("interview_setup"))

    current_q = questions[index]
    answer_record = p_data["answers"].get(str(index))

    return render_template(
        "practice.html",
        current_question=current_q,
        current_index=index,
        total_count=len(questions),
        answer_data=answer_record,
    )


@app.route("/practice/answer", methods=["POST"])
def practice_answer():
    """Evaluates answer in practice mode with immediate coaching breakdown."""
    index = request.form.get("question_index", type=int)
    answer_text = request.form.get("answer_text", "").strip()

    p_data = get_practice_session()
    questions = p_data["questions"]

    if index is not None and 0 <= index < len(questions):
        q = questions[index]
        evaluation = evaluate_interview_answer(
            question_text=q["question"],
            expected_points=q.get("expected_answer_points", []),
            candidate_answer=answer_text,
        )

        update_practice_answer(index, {
            "answer_text": answer_text,
            "evaluation": evaluation,
        })

    return redirect(url_for("practice", index=index))


# ============================================================================
# 6. AI MOCK INTERVIEW
# ============================================================================

@app.route("/mock-interview/start", methods=["POST"])
def start_mock_interview():
    """Initializes a new mock interview simulation session."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))
    role = request.form.get("role", "Python Developer")
    technology = request.form.get("technology", "Python")
    difficulty = request.form.get("difficulty", "Medium")
    interview_type = request.form.get("interview_type", "Technical")
    count = int(request.form.get("question_count", 5))
    internship_id = request.form.get("internship_id", type=int)

    interview = create_interview_with_questions(
        db=db,
        student_id=student.id,
        role=role,
        technology=technology,
        difficulty=difficulty,
        interview_type=interview_type,
        count=count,
        internship_id=internship_id,
    )

    session["current_interview_id"] = interview.id
    session["current_question_index"] = 0

    return redirect(url_for("mock_interview", q=0))


@app.route("/mock-interview")
def mock_interview():
    """Interactive mock interview screen with voice recorder & timer."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))
    interview_id = session.get("current_interview_id")

    if not interview_id:
        flash("Please start an interview first.", "info")
        return redirect(url_for("interview_setup"))

    interview = db.get_or_404(Interview, interview_id)
    questions = InterviewQuestion.query.filter_by(interview_id=interview.id).order_by(InterviewQuestion.question_order).all()

    q_index = request.args.get("q", 0, type=int)
    if q_index >= len(questions):
        # All questions answered; finalize and redirect to feedback
        finalize_interview(db, interview.id)
        session.pop("current_interview_id", None)
        return redirect(url_for("feedback_report", interview_id=interview.id))

    current_q = questions[q_index]
    existing_answer = current_q.answer

    return render_template(
        "mock_interview.html",
        student=student,
        interview=interview,
        current_question=current_q,
        current_index=q_index,
        existing_answer=existing_answer,
    )


@app.route("/mock-interview/answer", methods=["POST"])
def submit_mock_answer():
    """Saves answer, optionally processes audio, evaluates answer, and advances."""
    interview_id = request.form.get("interview_id", type=int)
    question_id = request.form.get("question_id", type=int)
    current_index = request.form.get("current_index", 0, type=int)
    answer_text = request.form.get("answer_text", "").strip()
    duration_seconds = request.form.get("duration_seconds", 0, type=int)

    # Save audio if present
    audio_filename = None
    if "audio_file" in request.files:
        audio_file = request.files["audio_file"]
        if audio_file and is_allowed_audio_file(audio_file.filename):
            audio_filename = save_audio_file(audio_file)

    # Evaluate & record answer
    submit_interview_answer(
        db=db,
        interview_id=interview_id,
        question_id=question_id,
        answer_text=answer_text,
        audio_filename=audio_filename,
    )

    interview = db.get_or_404(Interview, interview_id)
    next_index = current_index + 1

    # Check if this was the last question
    if next_index >= interview.total_questions:
        finalize_interview(db, interview_id, duration_seconds=duration_seconds)
        session.pop("current_interview_id", None)
        target_url = url_for("feedback_report", interview_id=interview_id)
    else:
        target_url = url_for("mock_interview", q=next_index)

    # If AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"success": True, "redirect": target_url})

    return redirect(target_url)


# ============================================================================
# 7. AI FEEDBACK REPORT & INTERVIEW HISTORY
# ============================================================================

@app.route("/feedback/<int:interview_id>")
def feedback_report(interview_id):
    """Displays detailed AI evaluation report with scores, strengths, and study plan."""
    interview = db.get_or_404(Interview, interview_id)
    grade, badge_class, grade_text = get_grade_and_badge(interview.overall_score)

    return render_template(
        "feedback.html",
        interview=interview,
        grade=grade,
        badge_class=badge_class,
        grade_text=grade_text,
    )


@app.route("/history")
def history():
    """Displays chronological log of past mock interviews with scorecards."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))
    past_interviews = Interview.query.filter_by(student_id=student.id, status="completed").order_by(Interview.id.desc()).all()

    return render_template("history.html", interviews=past_interviews)


# ============================================================================
# 8. SPEECH-TO-TEXT API ENDPOINT
# ============================================================================

@app.route("/api/speech-to-text", methods=["POST"])
def api_speech_to_text():
    """Receives recorded audio or client transcript and returns normalized text."""
    client_transcript = request.form.get("transcript", "")
    audio_path = None

    if "audio" in request.files:
        audio_file = request.files["audio"]
        if audio_file and is_allowed_audio_file(audio_file.filename):
            saved_name = save_audio_file(audio_file)
            audio_path = os.path.join(Config.AUDIO_FOLDER, saved_name)

    result = stt_service.transcribe(audio_file_path=audio_path, client_transcript=client_transcript)
    return jsonify(result)


# ============================================================================
# 9. ERROR HANDLING
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "base.html",
        content="""
        <div class="card" style="text-align: center; padding: 4rem 1rem;">
          <h1 style="font-size: 3rem; color: var(--accent);">404</h1>
          <h2>Page Not Found</h2>
          <p style="color: var(--text-muted); margin: 1rem 0 2rem;">The requested page could not be located.</p>
          <a href="/" class="btn btn-primary">Return to Homepage</a>
        </div>
        """
    ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template(
        "base.html",
        content="""
        <div class="card" style="text-align: center; padding: 4rem 1rem;">
          <h1 style="font-size: 3rem; color: var(--danger);">500</h1>
          <h2>Internal Processing Error</h2>
          <p style="color: var(--text-muted); margin: 1rem 0 2rem;">An unexpected system error occurred. The application is in safe mode.</p>
          <a href="/" class="btn btn-primary">Return to Homepage</a>
        </div>
        """
    ), 500


if __name__ == "__main__":
    print("=" * 65)
    print(" ⚡ CAREERPREP AI &mdash; INTERNSHIP TRACKING & MOCK INTERVIEW SYSTEM")
    print("=" * 65)
    print(f" * Operating Mode: {ai_service.get_status()['label']}")
    print(" * Server running on: http://127.0.0.1:5000")
    print(" * Press Ctrl+C in terminal to stop.")
    print("=" * 65)
    app.run(debug=True, host="127.0.0.1", port=5000)
