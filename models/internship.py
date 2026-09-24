"""Internship model."""
from datetime import datetime
from database.database import db


class Internship(db.Model):
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False, default="Remote")
    stipend = db.Column(db.String(80), nullable=False, default="₹15,000 / month")
    stipend_amount = db.Column(db.Integer, nullable=False, default=15000)  # Numeric for sorting
    internship_type = db.Column(db.String(50), nullable=False, default="Work From Home")  # Work From Home, Hybrid, On-site
    skills = db.Column(db.String(255), nullable=False, default="Python, Flask")
    deadline = db.Column(db.String(50), nullable=True, default="Rolling")
    posted_date = db.Column(db.String(50), nullable=True, default="Recently")
    source = db.Column(db.String(80), nullable=False, default="Curated Feed")
    url = db.Column(db.String(500), nullable=True, default="#")
    is_demo = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    applications = db.relationship("Application", back_populates="internship", cascade="all, delete-orphan")
    interviews = db.relationship("Interview", back_populates="internship")

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "location": self.location,
            "stipend": self.stipend,
            "stipend_amount": self.stipend_amount,
            "internship_type": self.internship_type,
            "skills": self.get_skills_list(),
            "deadline": self.deadline,
            "posted_date": self.posted_date,
            "source": self.source,
            "url": self.url,
            "is_demo": self.is_demo,
            "description": self.description,
        }
