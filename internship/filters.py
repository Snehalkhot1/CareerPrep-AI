"""Internship search and filtering module."""
from sqlalchemy import or_


def apply_internship_filters(query, InternshipModel, filters):
    """Applies search, technology, location, stipend, type, and sort filters

    to an SQLAlchemy Internship query.
    """
    keyword = filters.get("keyword", "").strip()
    technology = filters.get("technology", "").strip()
    location = filters.get("location", "").strip()
    stipend = filters.get("stipend", "").strip()
    internship_type = filters.get("type", "").strip()
    sort_by = filters.get("sort", "latest").strip().lower()

    # Keyword Search (company, role, skills, description)
    if keyword:
        kw_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                InternshipModel.company.ilike(kw_pattern),
                InternshipModel.role.ilike(kw_pattern),
                InternshipModel.skills.ilike(kw_pattern),
                InternshipModel.description.ilike(kw_pattern),
            )
        )

    # Technology Filter
    if technology and technology.lower() != "all":
        # Handle technology aliases
        tech_map = {
            "ai/ml": ["ai", "ml", "machine learning", "deep learning", "pytorch"],
            "web development": ["web", "html", "css", "javascript", "react", "node"],
            "data science": ["data", "pandas", "analytics", "sql", "tableau"],
        }
        aliases = tech_map.get(technology.lower(), [technology.lower()])
        conditions = [InternshipModel.skills.ilike(f"%{alias}%") for alias in aliases]
        conditions.extend([InternshipModel.role.ilike(f"%{alias}%") for alias in aliases])
        query = query.filter(or_(*conditions))

    # Location Filter
    if location and location.lower() != "any":
        query = query.filter(InternshipModel.location.ilike(f"%{location}%"))

    # Stipend Filter
    if stipend and stipend.lower() != "all":
        if stipend == "Unpaid":
            query = query.filter(InternshipModel.stipend_amount == 0)
        elif stipend == "₹1-5000":
            query = query.filter(InternshipModel.stipend_amount.between(1, 5000))
        elif stipend == "₹5000-10000":
            query = query.filter(InternshipModel.stipend_amount.between(5000, 10000))
        elif stipend == "₹10000+":
            query = query.filter(InternshipModel.stipend_amount >= 10000)

    # Type Filter (Work From Home, Hybrid, On-site)
    if internship_type and internship_type.lower() != "all":
        query = query.filter(InternshipModel.internship_type.ilike(f"%{internship_type}%"))

    # Sorting
    if sort_by == "stipend":
        query = query.order_by(InternshipModel.stipend_amount.desc())
    elif sort_by == "deadline":
        query = query.order_by(InternshipModel.deadline.asc())
    else:  # 'latest'
        query = query.order_by(InternshipModel.id.desc())

    return query
