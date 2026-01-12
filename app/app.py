from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path
import pandas as pd

# =========================
# Load model artifacts
# =========================
MODEL_DIR = Path("model")

pipeline = joblib.load(MODEL_DIR / "fraud_detection_pipeline.pkl")
THRESHOLD = joblib.load(MODEL_DIR / "decision_threshold.pkl")

EXPECTED_NUMERIC_COLS = [
    "telecommuting",
    "has_company_logo",
    "has_questions",
    "jd_word_count",
    "req_exp_enc",
    "employment_type_Full-time",
    "employment_type_Part-time",
    "employment_type_Temporary",
    "employment_type_Other",
    "employment_type_Unknown",
]


# =========================
# FastAPI app
# =========================
app = FastAPI(
    title="Fraud Job Detection API",
    description="Detect fraudulent job postings using ML",
    version="1.0"
)

# =========================
# Request schema
# =========================
class JobInput(BaseModel):
    job_description: str
    telecommuting: int
    has_company_logo: int
    has_questions: int
    jd_word_count: int
    req_exp_enc: int
    employment_type_Full_time: int 
    employment_type_Part_time: int 
    employment_type_Temporary: int
    employment_type_Other: int
    employment_type_Unknown: int

# =========================
# Health check
# =========================
@app.get("/")
def health_check():
    return {"status": "API is running"}

# =========================
# Prediction endpoint
# =========================
@app.post("/predict")
def predict_fraud(job: JobInput):

    data = job.dict()

    # Rename API-friendly keys → training feature names
    data["employment_type_Full-time"] = data.pop("employment_type_Full_time")
    data["employment_type_Part-time"] = data.pop("employment_type_Part_time")

    # Ensure all expected numeric columns exist
    for col in EXPECTED_NUMERIC_COLS:
        if col not in data:
            data[col] = 0

    # Create DataFrame
    X_input = pd.DataFrame([data])

    # Predict probability
    prob = pipeline.predict_proba(X_input)[0, 1]

    # Convert NumPy → Python native types
    prob = float(prob)
    pred = int(prob >= THRESHOLD)

    return {
        "fraud_probability": round(prob, 4),
        "prediction": "Fraud" if pred else "Real",
        "threshold_used": float(THRESHOLD)
    }
