import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Insurance Premium Predictor", page_icon="💰")

st.title("💰 Insurance Premium Prediction")
st.write("Enter your details to predict the insurance premium category.")

# ------------------ User Inputs ------------------

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=25
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    value=70.0
)

height = st.number_input(
    "Height (meters)",
    min_value=0.5,
    max_value=2.5,
    value=1.70,
    step=0.01
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.0,
    value=8.0
)

smoker = st.selectbox(
    "Smoker",
    ["yes", "no"]
)

city = st.selectbox(
    "City",
    [
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Chennai",
        "Hyderabad",
        "Kolkata",
        "Pune",
        "Indore",
        "Bhopal",
        "Nagpur",
        "Jaipur",
        "Jabalpur",
        "Lucknow",
        "Surat",
        "Patna",
        "Other"
    ]
)

occupation = st.selectbox(
    "Occupation",
    [
        "student",
        "private_job",
        "business_owner",
        "government_job",
        "freelancer",
        "retired"
    ]
)

# ------------------ Prediction ------------------

if st.button("Predict Premium Category"):

    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            st.success(
                f"Predicted Premium Category : **{result['predicted_category']}**"
            )

        else:
            st.error(response.text)

    except Exception as e:
        st.error(f"Cannot connect to FastAPI.\n\n{e}")