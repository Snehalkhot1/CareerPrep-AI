"""Internship Application model."""
from datetime import datetime
from database.database import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable=False)
    status = db.Column(
        db.String(50),
        nullable=False,
        default="Saved"
    )  # Saved, Interested, Applied, Interview Scheduled, Selected, Rejected
    applied_date = db.Column(db.DateTime, default=datetime.now)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    student = db.relationship("Student", back_populates="applications")
    internship = db.relationship("Internship", back_populates="applications")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "internship_id": self.internship_id,
            "status": self.status,
            "applied_date": self.applied_date.strftime("%Y-%m-%d %H:%M") if self.applied_date else None,
            "notes": self.notes,
            "internship": self.internship.to_dict() if self.internship else None,
        }
