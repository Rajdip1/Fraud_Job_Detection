import joblib
from pathlib import Path
import pandas as pd

# =========================
# Load saved artifacts
# =========================
MODEL_DIR = Path("model")

pipeline = joblib.load(MODEL_DIR / "fraud_detection_pipeline.pkl")
THRESHOLD = joblib.load(MODEL_DIR / "decision_threshold.pkl")

# =========================
# Prediction function
# =========================
def predict_job_fraud(job_data: dict):
    """
    job_data example:
    {
        "job_description": "Work from home opportunity...",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "jd_word_count": 42,
        "req_exp_enc": 1,
        "employment_type_Full-time": 0,
        "employment_type_Part-time": 0,
        "employment_type_Temporary": 0,
        "employment_type_Other": 0,
        "employment_type_Unknown": 1
    }
    """

    # Convert input to DataFrame
    X_input = pd.DataFrame([job_data])

    # Predict probability
    prob = pipeline.predict_proba(X_input)[0, 1]

    # Apply threshold
    pred = int(prob >= THRESHOLD)

    return pred, prob

# =========================
# Test run
# =========================
if __name__ == "__main__":

    sample_job = {
        "job_description": (
            "Work from home opportunity! No experience required. "
            "Earn money fast. Limited positions available."
        ),
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "jd_word_count": 18,
        "req_exp_enc": 0,
        "employment_type_Full-time": 0,
        "employment_type_Part-time": 0,
        "employment_type_Temporary": 0,
        "employment_type_Other": 1,
        "employment_type_Unknown": 0
    }

    pred, prob = predict_job_fraud(sample_job)

    print(f"Fraud Probability: {prob:.4f}")
    print("Prediction:", "Fraud ❌" if pred else "Real ✅")
