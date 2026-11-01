WEIGHTS = {"resume_score": 0.20, "assessment_score": 0.25, "technical_score": 0.35, "hr_score": 0.20}

def readiness_score(candidate: dict) -> float:
    """Transparent weighted score; missing evidence is an error, not a zero."""
    missing = [k for k in WEIGHTS if candidate.get(k) is None]
    if missing:
        raise ValueError(f"Missing evaluation evidence: {', '.join(missing)}")
    for key in WEIGHTS:
        value = float(candidate[key])
        if not 0 <= value <= 100:
            raise ValueError(f"{key} must be between 0 and 100")
    return round(sum(float(candidate[k]) * w for k, w in WEIGHTS.items()), 1)

def readiness_status(score: float) -> str:
    return "Ready" if score >= 80 else "Needs Improvement" if score >= 60 else "Not Ready"

def recommendations(skills: dict) -> list[str]:
    actions = {
        "Python": "Complete practical Python exercises and build a small data application.",
        "SQL": "Practice joins, aggregations, window functions and query optimization.",
        "PowerBI": "Build an interactive Power BI report with documented DAX measures.",
        "Statistics": "Practice descriptive statistics, hypothesis testing and interpretation.",
        "Communication": "Practice structured explanations and mock stakeholder interviews.",
        "MachineLearning": "Practice model validation, feature engineering and deployment.",
        "Algorithms": "Review data structures, complexity analysis and coding exercises.",
        "Testing": "Add unit tests, edge cases and automated quality checks."
    }
    gaps = sorted(skills.items(), key=lambda item: item[1])
    return [actions.get(k, f"Develop {k} through a focused practical exercise.") for k, v in gaps if v < 75][:3]
