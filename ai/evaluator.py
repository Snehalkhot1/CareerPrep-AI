"""AI Answer Evaluator for CareerPrep AI."""
import re
from .ai_service import ai_service


def evaluate_answer_with_rules(question_text, expected_points, candidate_answer):
    """Transparent rubric-based fallback evaluator when AI API is not active.

    Evaluates answer based on keyword matching, conceptual coverage, depth, and clarity.
    """
    candidate_answer = candidate_answer.strip() if candidate_answer else ""
    words = candidate_answer.split()
    word_count = len(words)

    # Empty or trivial response
    if word_count < 4:
        return {
            "score": 1.0,
            "technical_correctness": 1.0,
            "relevance": 2.0,
            "completeness": 1.0,
            "clarity": 2.0,
            "covered_points": [],
            "missing_points": expected_points if expected_points else ["No substantive answer provided"],
            "suggestion": "The answer was too brief. Try to explain the concept clearly, define key terms, and give a short practical example.",
        }

    # Normalize words for matching
    lower_answer = candidate_answer.lower()
    covered = []
    missing = []

    # Check match for each expected point
    for pt in (expected_points or []):
        # Extract meaningful keywords (length >= 4) from expected point
        pt_words = [re.sub(r"[^a-zA-Z0-9]", "", w).lower() for w in pt.split() if len(w) >= 4]
        matches = [w for w in pt_words if w in lower_answer]
        # If at least 25% of distinctive words match or at least 2 keywords match
        if matches and (len(matches) >= 2 or len(matches) / max(len(pt_words), 1) >= 0.25):
            covered.append(pt)
        else:
            missing.append(pt)

    # Conceptual coverage ratio
    total_pts = max(len(expected_points or [1]), 1)
    coverage_ratio = len(covered) / total_pts

    # Metric calculations (0 - 10 scale)
    # 1. Relevance: based on matching keywords to question and points
    q_words = [re.sub(r"[^a-zA-Z0-9]", "", w).lower() for w in question_text.split() if len(w) >= 4]
    q_matches = [w for w in q_words if w in lower_answer]
    q_ratio = min(len(q_matches) / max(len(q_words), 1), 1.0)
    relevance = min(round(5.0 + (q_ratio * 4.5) + (coverage_ratio * 1.5), 1), 10.0)

    # 2. Completeness: word count & coverage ratio
    if word_count > 60 and coverage_ratio >= 0.6:
        completeness = min(round(7.5 + (coverage_ratio * 2.5), 1), 10.0)
    elif word_count > 30:
        completeness = min(round(5.5 + (coverage_ratio * 3.5), 1), 9.0)
    else:
        completeness = min(round(3.5 + (coverage_ratio * 3.0), 1), 7.0)

    # 3. Technical correctness: aligned with coverage ratio and key concepts
    tech_correctness = min(round(4.0 + (coverage_ratio * 5.5), 1), 10.0)

    # 4. Clarity: structural flow, punctuation, sentence variety
    sentences = [s for s in re.split(r"[.!?]", candidate_answer) if s.strip()]
    clarity = 7.5 if len(sentences) >= 2 else 6.0
    if word_count > 25 and len(sentences) >= 2:
        clarity = 8.5

    # Overall weighted score out of 10
    # Weights: Technical (35%), Relevance (25%), Completeness (20%), Clarity (20%)
    overall = round(
        (tech_correctness * 0.35) + (relevance * 0.25) + (completeness * 0.20) + (clarity * 0.20),
        1
    )

    # Generate constructive suggestion
    if missing:
        suggestion = f"Good attempt! To achieve full marks, be sure to also explain: '{missing[0]}'."
    elif overall >= 8.5:
        suggestion = "Excellent, precise answer! You clearly demonstrated core theoretical and practical understanding."
    else:
        suggestion = "Solid answer. Consider adding a quick code snippet or real-world example to illustrate the mechanism."

    return {
        "score": overall,
        "technical_correctness": tech_correctness,
        "relevance": relevance,
        "completeness": completeness,
        "clarity": clarity,
        "covered_points": covered,
        "missing_points": missing,
        "suggestion": suggestion,
    }


def evaluate_interview_answer(question_text, expected_points, candidate_answer):
    """Evaluates candidate's answer using Google Gemini if available,

    or falls back to the deterministic rubric evaluator.
    """
    if not candidate_answer or not candidate_answer.strip():
        return evaluate_answer_with_rules(question_text, expected_points, "")

    if not ai_service.is_demo_mode:
        prompt = f"""
You are an objective technical interviewer evaluating a student candidate's response in an internship interview.

Question: {question_text}
Expected Key Points to cover:
{expected_points}

Candidate's Answer:
\"\"\"{candidate_answer}\"\"\"

Evaluate the answer strictly and transparently across 4 dimensions on a 0 to 10 scale:
- technical_correctness (0-10)
- relevance (0-10)
- completeness (0-10)
- clarity (0-10)
- score (composite weighted 0-10 score: 35% technical + 25% relevance + 20% completeness + 20% clarity)

Return ONLY a JSON object matching this schema:
{{
  "score": 8.0,
  "technical_correctness": 8.5,
  "relevance": 9.0,
  "completeness": 7.0,
  "clarity": 8.0,
  "covered_points": ["Concepts accurately addressed"],
  "missing_points": ["Concepts missing or inaccurate"],
  "suggestion": "1-2 sentences of constructive advice"
}}
"""
        result = ai_service.generate_json(prompt)
        if isinstance(result, dict) and "score" in result:
            return {
                "score": float(result.get("score", 7.0)),
                "technical_correctness": float(result.get("technical_correctness", 7.0)),
                "relevance": float(result.get("relevance", 7.0)),
                "completeness": float(result.get("completeness", 7.0)),
                "clarity": float(result.get("clarity", 7.0)),
                "covered_points": result.get("covered_points", []),
                "missing_points": result.get("missing_points", []),
                "suggestion": result.get("suggestion", "Good explanation. Keep practicing standard problem patterns."),
            }

    # Fallback to deterministic rubric
    return evaluate_answer_with_rules(question_text, expected_points, candidate_answer)
