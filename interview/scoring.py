"""Interview scoring and metric calculation utilities."""


def calculate_composite_score(technical, relevance, completeness, clarity):
    """Calculates a weighted composite score on a 0-100 scale.

    Technical Knowledge: 35%
    Relevance: 25%
    Completeness: 20%
    Clarity: 20%
    """
    composite_10 = (
        (technical * 0.35) +
        (relevance * 0.25) +
        (completeness * 0.20) +
        (clarity * 0.20)
    )
    return round(composite_10 * 10, 1)


def get_grade_and_badge(overall_score):
    """Returns a letter grade and CSS badge class based on percentage."""
    if overall_score >= 85:
        return "A+", "badge-success", "Outstanding Ready"
    elif overall_score >= 75:
        return "A", "badge-primary", "Strong Candidate"
    elif overall_score >= 60:
        return "B", "badge-info", "Interview Ready with Polish"
    elif overall_score >= 45:
        return "C", "badge-warning", "Needs Targeted Practice"
    else:
        return "D", "badge-danger", "Foundational Study Required"
