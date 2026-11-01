"""Illustrative synthetic-data ML baseline. Not validated for hiring decisions."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

FEATURES = ["resume_score", "assessment_score", "technical_score", "hr_score"]

def train_demo_model():
    rng = np.random.default_rng(42)
    X = rng.integers(35, 100, size=(600, 4))
    weighted = X @ np.array([.20, .25, .35, .20])
    y = np.where(weighted >= 80, "Ready", np.where(weighted >= 60, "Needs Improvement", "Not Ready"))
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=120, max_depth=5, random_state=42, class_weight="balanced")
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return model, {"accuracy": round(float(accuracy_score(y_test, pred)), 3), "macro_f1": round(float(f1_score(y_test, pred, average="macro")), 3), "test_samples": int(len(y_test)), "note": "Illustrative only: labels are generated from the same weighted score dimensions; metrics do not demonstrate real-world predictive validity."}
