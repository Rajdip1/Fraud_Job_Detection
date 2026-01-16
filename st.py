import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_URL = "https://YOUR-FASTAPI-URL.onrender.com/predict"

st.set_page_config(page_title="Fraud Job Detection", layout="centered")

st.title("🕵️ Fraud Job Detection System")
st.markdown(
    "Predict whether a job posting is **Fraudulent** or **Legitimate** "
    "using a Machine Learning model."
)

st.divider()

# =========================
# Inputs
# =========================
job_description = st.text_area("Job Description", height=180)

telecommuting = st.selectbox("Telecommuting", [0, 1])
has_company_logo = st.selectbox("Has Company Logo", [0, 1])
has_questions = st.selectbox("Has Screening Questions", [0, 1])
jd_word_count = st.number_input("Job Description Word Count", min_value=0, value=50)
req_exp_enc = st.selectbox("Experience Required (Encoded)", [0, 1])

employment_type = st.selectbox(
    "Employment Type",
    ["Full-time", "Part-time", "Temporary", "Other", "Unknown"]
)

employment_features = {
    "employment_type_Full-time": 0,
    "employment_type_Part-time": 0,
    "employment_type_Temporary": 0,
    "employment_type_Other": 0,
    "employment_type_Unknown": 0,
}
employment_features[f"employment_type_{employment_type}"] = 1

# =========================
# Predict
# =========================
if st.button("🔍 Predict Fraud"):

    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        payload = {
            "job_description": job_description,
            "telecommuting": telecommuting,
            "has_company_logo": has_company_logo,
            "has_questions": has_questions,
            "jd_word_count": jd_word_count,
            "req_exp_enc": req_exp_enc,
            **employment_features
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            st.subheader("Prediction Result")
            st.write(f"**Fraud Probability:** `{result['fraud_probability']}`")
            st.write(f"**Threshold Used:** `{result['threshold_used']}`")

            if result["prediction"] == "Fraud":
                st.error("🚨 Fraudulent Job")
            else:
                st.success("✅ Legitimate Job")
        else:
            st.error("API error. Please try again later.")
