import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from src.data_generator import generate_synthetic_data

# Page Configuration
st.set_page_config(
    page_title="Smart Insurance Claims AI",
    page_icon="🛡️",
    layout="wide"
)

# --- UTILS ---
@st.cache_resource
def load_or_train_models():
    """
    Trains the Multi-Modal AI System:
    1. NLP Model for Classification
    2. Anomaly Detection Model for Fraud
    """
    # 1. Load Data
    data_path = "insurance_claims.csv"
    if not os.path.exists(data_path):
        with st.spinner("Generating Synthetic Data..."):
            df = generate_synthetic_data(1000)
            df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    # 2. Stream A: NLP For Classification (Category)
    X_text = df['Description']
    y_category = df['Policy_Type']
    
    # Text Pipeline
    nlp_pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english')),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    nlp_pipeline.fit(X_text, y_category)

    # 3. Stream B: Anomaly Detection (Fraud)
    # Features: Amount, Customer_Tenure
    X_numeric = df[['Amount', 'Customer_Tenure']]
    
    # Contamination is approx the expected fraud rate (10%)
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    iso_forest.fit(X_numeric)

    return nlp_pipeline, iso_forest, df

def analyze_urgency(text):
    """Simple keyword based urgency detection."""
    urgency_keywords = ['emergency', 'severe', 'critical', 'urgent', 'immediately', 'pain', 'crash']
    text_lower = text.lower()
    for word in urgency_keywords:
        if word in text_lower:
            return "High"
    return "Medium" # Default

# --- APP UI ---

st.title("🛡️ Intelligent Insurance Claim & Fraud Guard")
st.markdown("""
**System Architecture:** Multi-Modal AI Analysis
*   **Stream A (NLP):** Analyzes claim text for Categorization & Urgency.
*   **Stream B (Anomaly):** Analyzes numerical metadata for Fraud detection.
*   **Fusion Layer:** Combines signals for final decision.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Submit New Claim")
    with st.form("claim_form"):
        customer_id = st.text_input("Customer ID", value="CUST-8821")
        tenure = st.slider("Customer Tenure (Years)", 0, 30, 5)
        amount = st.number_input("Claim Amount ($)", min_value=0.0, value=1500.0, step=100.0)
        description = st.text_area("Claim Description", height=150, 
                                   value="I slipped in the kitchen and have severe back pain. Need physiotherapy sessions.")
        
        submitted = st.form_submit_button("Process Claim")

if submitted:
    # Load Brain
    nlp_model, fraud_model, history_df = load_or_train_models()
    
    # --- PROCESSING ---
    
    # 1. Stream A: NLP Analysis
    category_pred = nlp_model.predict([description])[0]
    urgency_pred = analyze_urgency(description)
    
    # 2. Stream B: Fraud Analysis
    # IsolationForest returns -1 for anomaly, 1 for normal
    # We convert to a Risk Score for display (Invert logic roughly for display)
    features = pd.DataFrame([[amount, tenure]], columns=['Amount', 'Customer_Tenure'])
    fraud_label = fraud_model.predict(features)[0] 
    
    # Calculate an anomaly score (decision_function returns negative for anomalies)
    anomaly_score = fraud_model.decision_function(features)[0]
    
    if fraud_label == -1:
        fraud_risk = "High"
        risk_color = "red"
    else:
        fraud_risk = "Low"
        risk_color = "green"

    # 3. Fusion Layer (The "Smart" Decision)
    decision = "Review"
    explanation = ""

    if fraud_risk == "Low" and urgency_pred == "High":
        decision = "Auto-Approve (Fast Track)"
        decision_color = "green"
        explanation = "High urgency verified and Low fraud risk detected."
    elif fraud_risk == "High":
        decision = "Flag for Investigation"
        decision_color = "red"
        explanation = "Statistical anomaly detected in Amount vs Tenure ratio."
    else:
        decision = "Manual Review"
        decision_color = "orange"
        explanation = "Standard claim processing required."

    # --- DISPLAY RESULTS ---
    with col2:
        st.header("🧠 AI Analysis Results")
        
        # Metrics Top Row
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Predicted Category", category_pred)
        with c2:
            st.metric("Urgency", urgency_pred, delta="Priority" if urgency_pred=="High" else None)
        with c3:
            st.metric("Fraud Risk", fraud_risk, delta_color="inverse", 
                      delta=f"Score: {anomaly_score:.2f}")

        st.divider()

        # Final Decision Block
        st.subheader("🎯 Final Fusion Decision")
        st.markdown(f":{decision_color}-background[**{decision}**]")
        st.caption(f"Reasoning: {explanation}")
        
        # Detailed Debug Info
        with st.expander("Show internal model signals"):
            st.write(f"**NLP Data:** '{description}'")
            st.write(f"**Structured Data:** Amount=${amount}, Tenure={tenure}yrs")
            st.write(f"**Anomaly Score:** {anomaly_score} (Lower is more anomalous)")

        # Historical Context
        st.subheader("📊 Historical Context (Similar Claims)")
        # Filter for similar category
        similar_claims = history_df[history_df['Policy_Type'] == category_pred].head(5)
        st.dataframe(similar_claims[['Description', 'Amount', 'Is_Fraud']], use_container_width=True)

else:
    with col2:
        st.info("👈 Enter claim details and click Process to see the AI in action.")
        
        # Show some stats about the 'Brain'
        nlp_model, fraud_model, df = load_or_train_models()
        st.write(f"**System Status:** Trained on {len(df)} historical records.")
        st.write(f"**Fraud Rate in Training Data:** {df['Is_Fraud'].mean()*100:.1f}%")
