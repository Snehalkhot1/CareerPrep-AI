"""Student profile model."""
from datetime import datetime
from database.database import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default="Student User")
    email = db.Column(db.String(120), nullable=False, default="student@college.edu")
    college = db.Column(db.String(150), nullable=False, default="Engineering College")
    degree = db.Column(db.String(50), nullable=False, default="B.Tech")
    branch = db.Column(db.String(80), nullable=False, default="Computer Science & Engineering")
    year = db.Column(db.String(20), nullable=False, default="3rd Year")
    skills = db.Column(db.Text, nullable=False, default="Python, Java, SQL, HTML, CSS, JavaScript")
    preferred_role = db.Column(db.String(80), nullable=False, default="Python Developer")
    preferred_location = db.Column(db.String(80), nullable=False, default="Remote")
    preferred_type = db.Column(db.String(50), nullable=False, default="Work From Home")
    resume_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")
    interviews = db.relationship("Interview", back_populates="student", cascade="all, delete-orphan")

    def get_skills_list(self):
        """Return skills as a trimmed list."""
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "college": self.college,
            "degree": self.degree,
            "branch": self.branch,
            "year": self.year,
            "skills": self.get_skills_list(),
            "preferred_role": self.preferred_role,
            "preferred_location": self.preferred_location,
            "preferred_type": self.preferred_type,
            "resume_filename": self.resume_filename,
        }
