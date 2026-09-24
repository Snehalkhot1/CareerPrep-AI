"""Internship Tracker and Application Management."""
from datetime import datetime
from models.application import Application
from models.internship import Internship


def save_or_update_application(db, student_id, internship_id, status="Saved", notes=None):
    """Saves an internship or updates its application tracking status."""
    app = Application.query.filter_by(student_id=student_id, internship_id=internship_id).first()

    if not app:
        app = Application(
            student_id=student_id,
            internship_id=internship_id,
            status=status,
            notes=notes or f"Application marked as {status}",
            applied_date=datetime.now(),
        )
        db.session.add(app)
    else:
        app.status = status
        if notes:
            app.notes = notes
        app.updated_at = datetime.now()

    db.session.commit()
    return app


def get_application_status_map(student_id):
    """Returns a dictionary mapping internship_id -> Application object

    for fast status lookup on listings.
    """
    apps = Application.query.filter_by(student_id=student_id).all()
    return {app.internship_id: app for app in apps}


def get_dashboard_tracker_stats(student_id):
    """Computes aggregate internship application metrics for the dashboard."""
    total_internships = Internship.query.count()
    student_apps = Application.query.filter_by(student_id=student_id).all()

    status_counts = {
        "Saved": 0,
        "Interested": 0,
        "Applied": 0,
        "Interview Scheduled": 0,
        "Selected": 0,
        "Rejected": 0,
    }

    for app in student_apps:
        if app.status in status_counts:
            status_counts[app.status] += 1
        else:
            status_counts[app.status] = 1

    return {
        "total_internships": total_internships,
        "total_tracked": len(student_apps),
        "saved_count": status_counts.get("Saved", 0),
        "applied_count": status_counts.get("Applied", 0),
        "interviewing_count": status_counts.get("Interview Scheduled", 0),
        "selected_count": status_counts.get("Selected", 0),
        "rejected_count": status_counts.get("Rejected", 0),
        "status_breakdown": status_counts,
        "recent_applications": student_apps[-5:] if student_apps else [],
    }
