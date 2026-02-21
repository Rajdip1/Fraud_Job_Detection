# Fraud Job Detection

An end-to-end **Machine Learning application** that classifies job postings as **Fraudulent** or **Legitimate** using NLP and structured features.
The project includes a trained ML pipeline, a **FastAPI prediction service**, and a **Streamlit demo UI** for real-time inference.

**Status:** End-to-end prototype (model + API + frontend)

---

# System Architecture
<img width="1024" height="1536" alt="System Architecture" src="https://github.com/user-attachments/assets/cbcd7d9c-0427-4837-a30d-e0e9e6b4b7e3" />

---

## 📌 Project Highlights

- 🧠 Trained ML pipeline (scikit-learn / XGBoost)
- 🚀 FastAPI backend serving predictions
- 🎛 Streamlit UI for easy testing
- 📦 Model artifacts versioned and reusable
- 🐳 Docker-ready backend (optional deployment)

---

## 📂 Repository Structure

- `app/app.py` — FastAPI app exposing `/` (health) and `/predict`
- `app/predict.py` — Model loading & prediction logic
- `st.py` — Streamlit demo UI (calls API)
- `model/` — Saved model artifacts  
  - `fraud_detection_pipeline.pkl`  
  - `decision_threshold.pkl`
- `data/` — CSV datasets used during development
- `model_notebooks/` — Training & evaluation notebooks
- `data_cleaning/`, `data_processing/` — Preprocessing notebooks
- `Dockerfile` — Backend container configuration
- `requirements.txt` — Python dependencies (Backend)
- `requirements2.txt` — Python dependencies (Frontend)

---

## 🚀 Getting Started (Local)

### 1️⃣ Setup environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Run the API

```powershell
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
```

Health check:

```http
GET http://localhost:8000/
```

Response:
```json
{"status":"API is running"}
```

---

## 🔮 Prediction Example

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description":"Work from home opportunity...",
    "telecommuting":1,
    "has_company_logo":0,
    "has_questions":0,
    "jd_word_count":18,
    "req_exp_enc":0,
    "employment_type_Full_time":0,
    "employment_type_Part_time":0,
    "employment_type_Temporary":0,
    "employment_type_Other":1,
    "employment_type_Unknown":0
  }'
```

Response includes:
- `fraud_probability`
- `prediction` (Fraud / Real)
- `threshold_used`

---

## 🧪 API Schema Notes

- The API expects **the same feature names used during training**
- Input combines:
  - Job description text
  - Binary metadata features
  - One-hot encoded employment types
- See `app/app.py` for the exact schema

---

## 🎛 Streamlit Demo

1. Update API URL inside `st.py`:
```python
API_URL = "http://localhost:8000/predict"
```

2. Run:
```powershell
streamlit run st.py
```

The Streamlit app includes retry logic to handle cold-start delays on free hosting platforms.

---

## 🐳 Docker (Optional)

The backend is Docker-ready and can be containerized later without code changes:

```bash
docker build -t fraud-job-detection .
docker run -p 8000:8000 fraud-job-detection
```

---

## 📈 Model Artifacts

Stored in `model/` and loaded at runtime:

- `fraud_detection_pipeline.pkl` — preprocessing + classifier
- `decision_threshold.pkl` — probability threshold

---

## 🔧 Future Improvements

- Add CI pipeline for linting & API smoke tests
- Add unit tests for prediction logic
- Docker Compose for API + Streamlit
- Model monitoring & logging

---

## 📜 License

MIT License

---

## 👤 Author
**Rajdip**

If you found this project useful, feel free to ⭐ the repository.
