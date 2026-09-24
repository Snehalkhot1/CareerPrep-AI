"""Database initialization and seeding for CareerPrep AI."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_seed_internships():
    """Returns curated seed internships for immediate use."""
    return [
        {
            "company": "Infosys InStep",
            "role": "Python Developer Intern",
            "location": "Bangalore",
            "stipend": "₹25,000 / month",
            "stipend_amount": 25000,
            "internship_type": "Hybrid",
            "skills": "Python, Django, REST APIs, SQL",
            "deadline": "2026-10-30",
            "posted_date": "2 days ago",
            "source": "Campus Drive Feed",
            "url": "https://careers.infosys.com",
            "is_demo": False,
            "description": "Work with the enterprise cloud development team developing automated backend workflows and data pipelines in Python and FastAPI.",
        },
        {
            "company": "TCS Research & Innovation",
            "role": "AI/ML Engineering Intern",
            "location": "Pune",
            "stipend": "₹20,000 / month",
            "stipend_amount": 20000,
            "internship_type": "On-site",
            "skills": "Python, Machine Learning, PyTorch, Scikit-Learn",
            "deadline": "2026-11-15",
            "posted_date": "1 day ago",
            "source": "Curated Portal",
            "url": "https://www.tcs.com/careers",
            "is_demo": False,
            "description": "Collaborate on computer vision and natural language processing models for automated document intelligence.",
        },
        {
            "company": "Razorpay",
            "role": "Web Development Intern (Full Stack)",
            "location": "Remote",
            "stipend": "₹35,000 / month",
            "stipend_amount": 35000,
            "internship_type": "Work From Home",
            "skills": "JavaScript, React, Node.js, HTML, CSS",
            "deadline": "2026-10-25",
            "posted_date": "3 days ago",
            "source": "Public Tech Board",
            "url": "https://razorpay.com/jobs",
            "is_demo": False,
            "description": "Build high-performance merchant dashboard user interfaces and integrate secure payment gateway APIs.",
        },
        {
            "company": "Wipro Digital",
            "role": "Java Backend Developer Intern",
            "location": "Hyderabad",
            "stipend": "₹18,000 / month",
            "stipend_amount": 18000,
            "internship_type": "Hybrid",
            "skills": "Java, Spring Boot, MySQL, Microservices",
            "deadline": "2026-11-01",
            "posted_date": "4 days ago",
            "source": "Campus Drive Feed",
            "url": "https://careers.wipro.com",
            "is_demo": False,
            "description": "Develop and maintain robust Java microservices for global banking and financial enterprise clients.",
        },
        {
            "company": "Zerodha Tech",
            "role": "Software Developer Intern",
            "location": "Bangalore",
            "stipend": "₹40,000 / month",
            "stipend_amount": 40000,
            "internship_type": "Work From Home",
            "skills": "Python, Go, PostgreSQL, Redis",
            "deadline": "2026-10-20",
            "posted_date": "5 days ago",
            "source": "Public Tech Board",
            "url": "https://zerodha.tech",
            "is_demo": False,
            "description": "Build low-latency trading infrastructure, real-time telemetry, and resilient financial services.",
        },
        {
            "company": "Cognizant Technology Solutions",
            "role": "Data Science Intern",
            "location": "Mumbai",
            "stipend": "₹15,000 / month",
            "stipend_amount": 15000,
            "internship_type": "Hybrid",
            "skills": "Python, Pandas, SQL, Tableau, Statistics",
            "deadline": "2026-11-10",
            "posted_date": "6 days ago",
            "source": "Curated Portal",
            "url": "https://cognizant.com/careers",
            "is_demo": False,
            "description": "Analyze large-scale healthcare data, generate predictive models, and design executive business intelligence dashboards.",
        },
        {
            "company": "Zomato",
            "role": "Frontend Engineering Intern",
            "location": "Delhi",
            "stipend": "₹30,000 / month",
            "stipend_amount": 30000,
            "internship_type": "On-site",
            "skills": "JavaScript, TypeScript, React, CSS3",
            "deadline": "2026-11-05",
            "posted_date": "Just now",
            "source": "Curated Portal",
            "url": "https://zomato.com/careers",
            "is_demo": False,
            "description": "Work on customer-facing web applications, responsive food discovery pages, and performance optimization.",
        },
        {
            "company": "NextGen AI Labs (Demo)",
            "role": "AI Research Intern",
            "location": "Remote",
            "stipend": "₹12,000 / month",
            "stipend_amount": 12000,
            "internship_type": "Work From Home",
            "skills": "Python, AI/ML, NLP, LangChain",
            "deadline": "2026-12-01",
            "posted_date": "1 week ago",
            "source": "DEMO DATA",
            "url": "#",
            "is_demo": True,
            "description": "Explore agentic AI workflows, retrieval augmented generation, and prompt engineering paradigms.",
        },
        {
            "company": "CyberShield Solutions (Demo)",
            "role": "C++ Systems Intern",
            "location": "Pune",
            "stipend": "₹14,000 / month",
            "stipend_amount": 14000,
            "internship_type": "On-site",
            "skills": "C++, Linux, Networking, Multi-threading",
            "deadline": "2026-11-20",
            "posted_date": "1 week ago",
            "source": "DEMO DATA",
            "url": "#",
            "is_demo": True,
            "description": "Develop high-throughput packet inspection engines and low-level Linux networking utilities.",
        },
    ]


def init_db(app):
    """Initializes the database and seeds default student and internships."""
    with app.app_context():
        # Import models inside context to register with SQLAlchemy metadata
        from models.student import Student
        from models.internship import Internship
        from models.application import Application
        from models.interview import Interview, InterviewQuestion, InterviewAnswer, PracticeSession

        db.create_all()

        # Seed default student if none exists
        student = Student.query.first()
        if not student:
            student = Student(
                name="Aditya Sharma",
                email="aditya.sharma@college.edu",
                college="Pune Institute of Computer Technology",
                degree="B.Tech",
                branch="Computer Science and Engineering",
                year="3rd Year",
                skills="Python, Java, JavaScript, SQL, HTML, CSS, React, Flask",
                preferred_role="Python Developer",
                preferred_location="Remote",
                preferred_type="Work From Home",
            )
            db.session.add(student)
            db.session.commit()

        # Seed initial internships if table is empty
        if Internship.query.count() == 0:
            for item in get_seed_internships():
                internship = Internship(**item)
                db.session.add(internship)
            db.session.commit()
