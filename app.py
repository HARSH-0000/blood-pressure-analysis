import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
import random

st.markdown(
    """
    <style>
    /* Fix dropdown text visibility */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
    }
    div[data-baseweb="select"] span {
        color: black !important;
    }

    /* Prevent DataFrame index (extra 0 before 66 age) */
    .stDataFrame tbody th {
        display: none !important;
    }

    /* Keep words in one line inside table */
    .stDataFrame td, .stDataFrame th {
        white-space: nowrap !important;
        text-align: center !important;
    }

    /* Download Report button style */
    .stDownloadButton>button {
        background-color: #0066cc !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stDownloadButton>button:hover {
        background-color: #004080 !important;
        color: white !important;
    }
    .stDownloadButton>button:active {
        background-color: #003366 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Style the summary table */
    .stDataFrame {
        border: 2px solid #0066cc !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    .stDataFrame table {
        border-collapse: collapse !important;
        width: 100% !important;
        font-size: 15px !important;
        font-family: "Arial", sans-serif !important;
    }
    .stDataFrame thead tr {
        background-color: #0066cc !important;
        color: white !important;
        text-align: center !important;
        font-weight: bold !important;
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #f2f8ff !important;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #ffffff !important;
    }
    .stDataFrame td, .stDataFrame th {
        padding: 10px !important;
        text-align: center !important;
        white-space: nowrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)









st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966488.png", width=100)  # Replace with your hospital/clinic logo
st.sidebar.title("🏥 HealthCare Assistant")

st.sidebar.markdown("""
Welcome to the **Blood Pressure Stage Predictor**.  
This tool helps you check your BP stage & generate a health report.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("💡 Health Tip of the Day")

health_tips = [
    "✔️ Reduce salt intake to manage high BP.",
    "✔️ Exercise 30 mins a day for a healthy heart.",
    "✔️ Drink enough water & stay hydrated.",
    "✔️ Avoid smoking and alcohol for better BP control.",
    "✔️ Eat more fruits and vegetables.",
    "✔️ Sleep at least 7–8 hours daily.",
    "✔️ Manage stress with yoga or meditation.",
    "✔️ Check your BP regularly and track trends."
]

# Pick one random tip
tip_of_the_day = random.choice(health_tips)
st.sidebar.success(tip_of_the_day)

st.sidebar.markdown("---")
st.sidebar.info("⚠️ This is for awareness only. Always consult your doctor.")


# Load your trained model (update path)
model = pickle.load(open("model.pkl", "rb"))

st.title("🩺 Blood Pressure Stage Predictor")

st.markdown("""
This tool predicts **blood pressure stage** based on your inputs.  

⚠️ *Disclaimer: This is for awareness only, not a medical diagnosis.  
Always consult a doctor for confirmation and treatment.*
""")

# Collect user inputs
age = st.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
systolic = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, step=1)
diastolic = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150, step=1)
diagnosed_age = st.number_input("Age when diagnosed (if any)", min_value=0, max_value=120, step=1)

# Extra health-related features
visual_change = st.selectbox("Visual changes (blurred vision, eye strain)", ["No", "Yes"])
prev_history = st.selectbox("Previous history of hypertension", ["No", "Yes"])
already_patient = st.selectbox("Already diagnosed as a patient", ["No", "Yes"])
take_medicine = st.selectbox("Currently taking BP medicine", ["No", "Yes"])
controlled_diet = st.selectbox("Following a controlled diet", ["No", "Yes"])
nose_bleeding = st.selectbox("Frequent nose bleeding", ["No", "Yes"])
severity = st.selectbox("Severity of symptoms", ["Mild", "Moderate", "Severe"])
breath_shortness = st.selectbox("Breath shortness", ["No", "Yes"])

# Encode categorical inputs
gender_encoded = 0 if gender == "Male" else (1 if gender == "Female" else 2)
visual_change_encoded = 1 if visual_change == "Yes" else 0
prev_history_encoded = 1 if prev_history == "Yes" else 0
already_patient_encoded = 1 if already_patient == "Yes" else 0
take_medicine_encoded = 1 if take_medicine == "Yes" else 0
controlled_diet_encoded = 1 if controlled_diet == "Yes" else 0
nose_bleeding_encoded = 1 if nose_bleeding == "Yes" else 0
breath_shortness_encoded = 1 if breath_shortness == "Yes" else 0

# Encode severity (Mild=0, Severe=1, Moderate=2)
if severity == "Mild":
    severity_encoded = 0
elif severity == "Severe":
    severity_encoded = 1
else:
    severity_encoded = 2

# Prediction button
if st.button("Predict"):
    features = np.array([[
        age, systolic, diastolic, diagnosed_age, gender_encoded,
        visual_change_encoded, prev_history_encoded, already_patient_encoded,
        take_medicine_encoded, controlled_diet_encoded, nose_bleeding_encoded,
        severity_encoded, breath_shortness_encoded
    ]])

    prediction = model.predict(features)[0]

    if prediction == 0:
        stage = "Normal"
        color = "green"
        advice = "✅ Your BP is normal. Maintain a healthy lifestyle to keep it stable."
    elif prediction == 1:
        stage = "Hypertension Stage-1"
        color = "orange"
        advice = "⚠️ Slightly high Stage 1. Reduce salt intake, exercise regularly, and monitor your BP more often."
    elif prediction == 2:
        stage = "Hypertension Stage-2"
        color = "red"
        advice = "⚠️ Stage 2 hypertension. Adopt lifestyle changes (diet, activity, weight control). Medication Required."
    else:
        stage = "Hypertensive Crisis"
        color = "darkred"
        advice = "🚨 Seek medical attention immediately. Medication may be required."

    # Show prediction result
    st.markdown(f"### 🧾 Result: <span style='color:{color}'>{stage}</span>", unsafe_allow_html=True)
    st.info(advice)

    # Show input summary
    summary_data = {
        "Age": [age],
        "Gender": [gender],
        "Systolic BP": [systolic],
        "Diastolic BP": [diastolic],
        "Diagnosed Age": [diagnosed_age],
        "Visual Change": [visual_change],
        "Previous History": [prev_history],
        "Already Patient": [already_patient],
        "Taking Medicine": [take_medicine],
        "Controlled Diet": [controlled_diet],
        "Nose Bleeding": [nose_bleeding],
        "Severity": [severity],
        "Breath Shortness": [breath_shortness]
    }
    st.markdown("### 📋 Your Input Summary")
    st.table(pd.DataFrame(summary_data))

    # --- Create BP Range Chart ---
    fig, ax = plt.subplots(figsize=(6, 4))
    categories = ["Normal",  "Stage 1", "Stage 2","Crisis"]
    systolic_ranges = [120, 129, 139, 180]
    diastolic_ranges = [80, 80, 89, 120]

    ax.bar(categories, systolic_ranges, color=["green", "orange", "red", "darkred"], alpha=0.7, label="Systolic (Upper limit)")
    ax.bar(categories, diastolic_ranges, color="blue", alpha=0.4, label="Diastolic (Upper limit)")

    ax.axhline(y=systolic, color="black", linestyle="--", label=f"Your Systolic: {systolic}")
    ax.axhline(y=diastolic, color="purple", linestyle="--", label=f"Your Diastolic: {diastolic}")

    ax.set_ylabel("BP (mmHg)")
    ax.set_title("Blood Pressure Categories")
    ax.legend()

    st.pyplot(fig)

    # Save chart as image for PDF
    chart_buffer = io.BytesIO()
    fig.savefig(chart_buffer, format="PNG")
    chart_buffer.seek(0)

    # --- Generate PDF report ---
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("🩺 Blood Pressure Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Result:</b> {stage}", styles["Heading2"]))
    elements.append(Paragraph(advice, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table of inputs
    table_data = [["Feature", "Value"]]
    for key, value in summary_data.items():
        table_data.append([key, str(value[0])])
    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add chart image to PDF
    elements.append(Paragraph("Blood Pressure Category Chart", styles["Heading2"]))
    elements.append(Image(chart_buffer, width=400, height=250))

    doc.build(elements)
    buffer.seek(0)

    # Download button
    st.download_button(
        label="📥 Download Report (PDF)",
        data=buffer,
        file_name="bp_report.pdf",
        mime="application/pdf"
    )
