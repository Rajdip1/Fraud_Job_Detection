import streamlit as st
import requests
import time

# =========================
# CONFIG
# =========================
API_URL = "https://fraud-job-detection-backend.onrender.com/predict"

st.set_page_config(
    page_title="Fraud Job Detection",
    layout="centered"
)

# =========================
# HELPER FUNCTION
# =========================
def call_backend_api(payload, retries=2, timeout=30):
    """
    Calls backend API with retry logic to handle cold starts.
    """
    for attempt in range(retries):
        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=timeout
            )
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(5)
    return None

def count_words(text):
    return len(text.split()) if text.strip() else 0

# =========================
# UI
# =========================
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

# 🔹 AUTO WORD COUNT
jd_word_count = count_words(job_description)

st.text_input(
    "Job Description Word Count",
    value=jd_word_count,
    disabled=True
)

# 🚀 OPTIONAL UX WARNING
if jd_word_count > 0 and jd_word_count < 25:
    st.warning("Very short job descriptions are often suspicious.")

telecommuting = st.selectbox("Telecommuting", [0, 1])
has_company_logo = st.selectbox("Has Company Logo", [0, 1])
has_questions = st.selectbox("Has Screening Questions", [0, 1])
req_exp_enc = st.selectbox("Experience Required (Encoded)", [0, 1])

employment_type = st.selectbox(
    "Employment Type",
    ["Full-time", "Part-time", "Temporary", "Other", "Unknown"]
)

employment_features = {
    "employment_type_Full_time": 0,
    "employment_type_Part_time": 0,
    "employment_type_Temporary": 0,
    "employment_type_Other": 0,
    "employment_type_Unknown": 0,
}

employment_features[
    f"employment_type_{employment_type.replace('-', '_')}"
] = 1

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

        with st.spinner("Waking up backend... ⏳"):
            response = call_backend_api(payload)

        if response is None:
            st.warning(
                "Backend is waking up due to inactivity.\n\n"
                "Please wait 10–20 seconds and click **Predict** again."
            )
        else:
            result = response.json()

            st.subheader("Prediction Result")
            st.write(f"**Fraud Probability:** `{result['fraud_probability']}`")
            st.write(f"**Threshold Used:** `{result['threshold_used']}`")

            if result["prediction"] == "Fraud":
                st.error("🚨 Fraudulent Job")
            else:
                st.success("✅ Legitimate Job")
