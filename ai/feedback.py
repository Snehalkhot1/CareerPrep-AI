"""Comprehensive AI Feedback Generator for CareerPrep AI."""
from .ai_service import ai_service


def generate_interview_feedback_report(role, technology, difficulty, answers_data):
    """Synthesizes question-by-question evaluations into a comprehensive interview report.

    answers_data is a list of dicts with:
    [{'question': str, 'score': float, 'technical_correctness': float, 'relevance': float,
      'completeness': float, 'clarity': float, 'covered_points': list, 'missing_points': list,
      'suggestion': str}]
    """
    if not answers_data:
        return {
            "overall_score": 0.0,
            "technical_score": 0.0,
            "relevance_score": 0.0,
            "completeness_score": 0.0,
            "clarity_score": 0.0,
            "strengths": ["No answers recorded."],
            "improvements": ["Complete all interview questions to generate feedback."],
            "recommended_topics": [technology, "Core Problem Solving", "System Architecture"],
            "summary": "The interview was incomplete.",
        }

    count = len(answers_data)
    avg_score = sum(a["score"] for a in answers_data) / count
    avg_tech = sum(a["technical_correctness"] for a in answers_data) / count
    avg_rel = sum(a["relevance"] for a in answers_data) / count
    avg_comp = sum(a["completeness"] for a in answers_data) / count
    avg_clar = sum(a["clarity"] for a in answers_data) / count

    # Scale to 0-100%
    overall_pct = round(avg_score * 10, 1)
    tech_pct = round(avg_tech * 10, 1)
    rel_pct = round(avg_rel * 10, 1)
    comp_pct = round(avg_comp * 10, 1)
    clar_pct = round(avg_clar * 10, 1)

    # Try generating high-level summary with Gemini if enabled
    if not ai_service.is_demo_mode:
        prompt = f"""
You are an encouraging college placement mentor reviewing a 3rd-year CS student's mock interview for the role '{role}' ({technology}).
Scores:
Overall: {overall_pct}%
Technical Knowledge: {tech_pct}%
Relevance: {rel_pct}%
Completeness: {comp_pct}%
Clarity: {clar_pct}%

Answers summary:
{answers_data}

Generate a structured feedback JSON object:
{{
  "strengths": ["Strength 1", "Strength 2"],
  "improvements": ["Improvement 1", "Improvement 2"],
  "recommended_topics": ["Topic 1", "Topic 2", "Topic 3"],
  "summary": "2-3 sentences synthesizing the student's readiness and recommended next steps."
}}
Do NOT make personality, medical, or psychological judgments. Focus solely on technical communication and conceptual depth.
"""
        res = ai_service.generate_json(prompt)
        if isinstance(res, dict) and "strengths" in res:
            return {
                "overall_score": overall_pct,
                "technical_score": tech_pct,
                "relevance_score": rel_pct,
                "completeness_score": comp_pct,
                "clarity_score": clar_pct,
                "strengths": res.get("strengths", []),
                "improvements": res.get("improvements", []),
                "recommended_topics": res.get("recommended_topics", []),
                "summary": res.get("summary", ""),
            }

    # Deterministic Rubric Feedback for Demo Mode
    strengths = []
    improvements = []
    topics = set()

    # Determine strengths
    if tech_pct >= 75:
        strengths.append(f"Strong fundamental understanding of {technology} concepts and terminology.")
    else:
        strengths.append("Willingness to tackle difficult technical questions and articulate ideas.")

    if rel_pct >= 80:
        strengths.append("High answer relevance; candidate stayed focused on the specific questions asked.")

    if clar_pct >= 75:
        strengths.append("Clear and structured communication style with logical flow.")

    if comp_pct >= 75:
        strengths.append("Thorough coverage of expected technical points and edge cases.")
    elif not strengths:
        strengths.append("Good start on core programming definitions and foundational terminology.")

    # Determine improvements
    if tech_pct < 75:
        improvements.append(f"Review core {technology} language internals, memory architecture, and best practices.")
    if comp_pct < 75:
        improvements.append("Elaborate further on practical examples, code implementation details, and trade-offs.")
    if clar_pct < 75:
        improvements.append("Structure answers systematically (e.g. Definition -> Working Mechanism -> Practical Use Case).")
    if rel_pct < 75:
        improvements.append("Ensure your answers directly address the interviewer's prompt without straying off-topic.")

    if not improvements:
        improvements.append("Practice writing quick whiteboard pseudocode to accompany theoretical explanations.")

    # Recommended topics based on technology
    tech_lower = (technology or "Python").lower()
    if "python" in tech_lower:
        topics.update(["Decorators & Generators", "OOP & Dunder Methods", "Memory Management (GIL)", "Asyncio & Concurrency"])
    elif "java" in tech_lower:
        topics.update(["JVM Internal Architecture", "Concurrent Collections", "Spring Boot Annotations", "Garbage Collection Tuning"])
    elif any(k in tech_lower for k in ["js", "javascript", "web"]):
        topics.update(["Event Loop & Microtasks", "Closures & Scope Chaining", "DOM Virtualization & React Hooks", "RESTful API Security"])
    elif "sql" in tech_lower or "data" in tech_lower:
        topics.update(["Database Indexing Strategies", "ACID Transactions", "Query Plan Optimization", "Window Functions"])
    elif "ai" in tech_lower or "ml" in tech_lower:
        topics.update(["Regularization & Overfitting", "Gradient Descent Variations", "Evaluation Metrics (ROC/AUC)", "Model Deployment"])
    else:
        topics.update([f"{technology} Fundamentals", "Data Structures & Algorithms", "System Design Basics", "REST APIs"])

    # Overall Summary sentence
    if overall_pct >= 80:
        summary = f"Impressive performance! The candidate demonstrated solid technical acumen in {technology} and is well-prepared for technical internship rounds. Fine-tuning architectural trade-offs will secure top placements."
    elif overall_pct >= 60:
        summary = f"Promising baseline with good foundational knowledge in {technology}. Focusing on the identified improvement areas and practicing detailed answers will significantly boost interview confidence."
    else:
        summary = f"Needs focused preparation on {technology} core topics and question structures. Regular practice using CareerPrep AI's Practice Mode will help build speed, precision, and depth."

    return {
        "overall_score": overall_pct,
        "technical_score": tech_pct,
        "relevance_score": rel_pct,
        "completeness_score": comp_pct,
        "clarity_score": clar_pct,
        "strengths": strengths,
        "improvements": improvements,
        "recommended_topics": list(topics)[:4],
        "summary": summary,
    }
