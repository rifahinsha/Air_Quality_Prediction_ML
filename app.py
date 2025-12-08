import streamlit as st
import numpy as np
import joblib

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Air Quality Prediction",
    layout="centered"
)

# ---------------- RISK LEVEL FUNCTION ----------------
# (Same logic you mentioned in Python code)
def get_risk_level(pred):
    if pred <= 50:
        return "🟢 Good"
    elif pred <= 100:
        return "🟡 Moderate"
    elif pred <= 150:
        return "🟠 Unhealthy"
    else:
        return "🔴 Hazardous"

# ---------------- APP UI ----------------
st.title("🌍 Air Quality Prediction Application")

st.write("✅ App loaded successfully")

# ---------------- MODEL SELECTION ----------------
model_choice = st.selectbox(
    "Select Machine Learning Model",
    ["Linear Regression", "Random Forest", "SVR", "Decision Tree"]
)

# ---------------- LOAD MODEL SAFELY ----------------
try:
    if model_choice == "Linear Regression":
        model = joblib.load("linear_model.pkl")
    elif model_choice == "Random Forest":
        model = joblib.load("random_forest_model.pkl")
    elif model_choice == "SVR":
        model = joblib.load("svr_model.pkl")
    else:
        model = joblib.load("decision_tree_model.pkl")

    st.success("✅ Model loaded successfully")

except Exception as e:
    st.error("❌ Model loading failed")
    st.exception(e)
    st.stop()

# ---------------- INPUT FIELDS ----------------
st.subheader("Enter Sensor Values")

CO = st.number_input("CO (Carbon Monoxide)", value=0.0)
PT08_S1 = st.number_input("PT08.S1 (CO Sensor)", value=0.0)
C6H6 = st.number_input("C6H6 (Benzene)", value=0.0)
PT08_S2 = st.number_input("PT08.S2 (NMHC Sensor)", value=0.0)
PT08_S3 = st.number_input("PT08.S3 (NOx Sensor)", value=0.0)
PT08_S4 = st.number_input("PT08.S4 (NO2 Sensor)", value=0.0)
PT08_S5 = st.number_input("PT08.S5 (O3 Sensor)", value=0.0)
T = st.number_input("Temperature (°C)", value=0.0)
RH = st.number_input("Relative Humidity (%)", value=0.0)
AH = st.number_input("Absolute Humidity", value=0.0)

# ---------------- PREDICTION ----------------
if st.button("🔮 Predict Air Quality"):

    input_data = np.array([[CO, PT08_S1, C6H6, PT08_S2,
                            PT08_S3, PT08_S4,
                            PT08_S5, T, RH, AH]])

    try:
        prediction = model.predict(input_data)[0]
        risk = get_risk_level(prediction)

        st.success(f"✅ Predicted Air Quality Value: **{prediction:.2f}**")

        # Risk level coloring
        if "Good" in risk:
            st.success(f"⚠️ Risk Level: {risk}")
        elif "Moderate" in risk:
            st.warning(f"⚠️ Risk Level: {risk}")
        else:
            st.error(f"⚠️ Risk Level: {risk}")

    except Exception as e:
        st.error("❌ Prediction failed")
        st.exception(e)
