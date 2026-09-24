"""Automated Unit Tests for CareerPrep AI."""
import pytest
from app import app, db
from models.student import Student
from models.internship import Internship
from models.application import Application
from models.interview import Interview, InterviewQuestion
from internship import apply_internship_filters, save_or_update_application
from internship.sources import parse_google_jobs_page
from ai import generate_interview_questions, evaluate_interview_answer, generate_interview_feedback_report


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed test student
            s = Student(
                name="Aditya Sharma",
                email="aditya@college.edu",
                skills="Python, SQL, JavaScript",
                preferred_role="Python Developer",
            )
            db.session.add(s)

            # Seed test internships
            i1 = Internship(
                company="TechCorp",
                role="Python Developer Intern",
                location="Remote",
                stipend="₹20,000 / month",
                stipend_amount=20000,
                internship_type="Work From Home",
                skills="Python, Django, SQL",
            )
            i2 = Internship(
                company="DataSystems",
                role="Java Developer Intern",
                location="Pune",
                stipend="₹15,000 / month",
                stipend_amount=15000,
                internship_type="On-site",
                skills="Java, Spring Boot",
            )
            db.session.add_all([i1, i2])
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()


def test_database_and_student_creation(client):
    """Test student profile exists and has correct attributes."""
    with app.app_context():
        student = Student.query.first()
        assert student is not None
        assert student.name == "Aditya Sharma"
        assert "Python" in student.get_skills_list()


def test_profile_isolation_between_users(client):
    """Each logged-in user should only see and edit their own profile."""
    with app.app_context():
        alice = Student(name="Alice", email="alice@college.edu", skills="Python, SQL", preferred_role="Python Developer")
        bob = Student(name="Bob", email="bob@college.edu", skills="Java, Spring", preferred_role="Java Developer")
        db.session.add_all([alice, bob])
        db.session.commit()

    # Login as Alice and update her profile
    response = client.post("/login", data={"email": "alice@college.edu", "password": "careerprep123"}, follow_redirects=False)
    assert response.status_code == 302
    client.post(
        "/profile",
        data={
            "name": "Alice Updated",
            "email": "alice@college.edu",
            "college": "Engineering College",
            "degree": "B.Tech",
            "branch": "Computer Science & Engineering",
            "year": "3rd Year",
            "skills": "Python, SQL, Flask",
            "preferred_role": "Backend Developer",
            "preferred_location": "Remote",
            "preferred_type": "Work From Home",
        },
        follow_redirects=False,
    )

    # Log in as Bob and ensure Bob does not see Alice's updated profile
    with client.session_transaction() as session:
        session.clear()
    response = client.post("/login", data={"email": "bob@college.edu", "password": "careerprep123"}, follow_redirects=False)
    assert response.status_code == 302

    profile_response = client.get("/profile")
    assert b"Alice Updated" not in profile_response.data
    assert b"Bob" in profile_response.data


def test_internship_filtering(client):
    """Test multi-criteria filtering on technology, location, and stipend."""
    with app.app_context():
        # Filter by Python
        py_query = apply_internship_filters(Internship.query, Internship, {"technology": "Python"})
        assert py_query.count() == 1
        assert py_query.first().role == "Python Developer Intern"

        # Filter by Java
        java_query = apply_internship_filters(Internship.query, Internship, {"technology": "Java"})
        assert java_query.count() == 1

        # Filter by Stipend
        high_stipend = apply_internship_filters(Internship.query, Internship, {"stipend": "₹10000+"})
        assert high_stipend.count() == 2


def test_application_saving_and_tracking(client):
    """Test saving and tracking application statuses."""
    with app.app_context():
        student = Student.query.first()
        internship = Internship.query.first()

        # Save application
        app_record = save_or_update_application(db, student.id, internship.id, status="Applied")
        assert app_record.status == "Applied"

        # Update status
        updated = save_or_update_application(db, student.id, internship.id, status="Interview Scheduled")
        assert updated.status == "Interview Scheduled"
        assert Application.query.count() == 1


def test_ai_question_generation():
    """Test question generator returns structured questions."""
    questions = generate_interview_questions(
        role="Python Developer",
        technology="Python",
        difficulty="Medium",
        question_type="Technical",
        count=3,
    )
    assert len(questions) == 3
    for q in questions:
        assert "question" in q
        assert "expected_answer_points" in q
        assert len(q["expected_answer_points"]) > 0


def test_ai_answer_evaluation():
    """Test rubric evaluation dimensions and scoring boundaries."""
    question = "Explain the difference between mutable and immutable types in Python."
    expected = [
        "Mutable objects can be modified in place",
        "Immutable objects cannot be modified after creation",
    ]
    good_answer = "Mutable types such as lists and dictionaries can be modified in place, whereas immutable types like tuples and strings cannot be changed after creation."

    eval_result = evaluate_interview_answer(question, expected, good_answer)
    assert "score" in eval_result
    assert "technical_correctness" in eval_result
    assert "relevance" in eval_result
    assert "completeness" in eval_result
    assert "clarity" in eval_result
    assert eval_result["score"] >= 4.0
    assert len(eval_result["covered_points"]) > 0


def test_flask_routes(client):
    """Test core GET route response statuses."""
    routes = ["/", "/dashboard", "/profile", "/internships", "/interview", "/history"]
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, f"Route {route} failed with status {response.status_code}"


def test_prepare_for_interview_connection(client):
    """Test that visiting /interview with internship query parameters loads correctly."""
    with app.app_context():
        internship = Internship.query.first()
        response = client.get(f"/interview?role={internship.role}&tech=Python&internship_id={internship.id}")
        assert response.status_code == 200
        assert internship.company.encode() in response.data


def test_google_internship_parser_extracts_real_entries():
    """Google careers search results should produce real internship entries when parsed."""
    sample_html = '''
    <html><body>
    <h2>Software Engineering Intern, BS, Summer 2027</h2>
    <a href="https://www.google.com/about/careers/applications/jobs/results/123-software-engineering-intern-bs-summer-2027?q=internship">Learn more</a>
    <div>Google | Mountain View, CA, USA; +29 more</div>
    <h2>Product Design Engineering Intern, BS/MS, Summer 2027</h2>
    <a href="https://www.google.com/about/careers/applications/jobs/results/456-product-design-engineering-intern-bsms-summer-2027?q=internship">Learn more</a>
    <div>Google | London, UK</div>
    </body></html>
    '''
    items = parse_google_jobs_page(sample_html)
    assert len(items) >= 2
    assert items[0]["company"] == "Google"
    assert "Software Engineering Intern" in items[0]["role"]
    assert "Mountain View" in items[0]["location"]
