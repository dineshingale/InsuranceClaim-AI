import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.pipeline import Pipeline
from io import StringIO

app = FastAPI()

# --- CONFIGURATION ---
MODEL_PATH = "models/trained_brain.pkl"
CLAIMS_DB_PATH = "data/submitted_claims.csv"

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class ClaimSubmission(BaseModel):
    customer_id: str
    amount: float
    tenure: int
    description: str
    date_of_incident: str

class ClaimRecord(ClaimSubmission):
    timestamp: str
    category: str
    urgency: str
    fraud_risk: str
    anomaly_score: float
    authenticity_score: int
    priority_score: int
    rank_score: int
    status: str

# --- LOGIC ---
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def save_model(nlp_pipeline, iso_forest, training_meta):
    joblib.dump({
        'nlp': nlp_pipeline,
        'fraud': iso_forest,
        'meta': training_meta
    }, MODEL_PATH)

def train_system_logic(df):
    # NLP
    X_text = df['Description']
    # Fallback if Policy_Type not present, just for demo robustness
    y_category = df['Policy_Type'] if 'Policy_Type' in df.columns else df['Category']
    
    nlp_pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english')),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    nlp_pipeline.fit(X_text, y_category)

    # Fraud
    iso_forest = None
    if 'Amount' in df.columns and 'Customer_Tenure' in df.columns:
        X_numeric = df[['Amount', 'Customer_Tenure']].fillna(0)
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        iso_forest.fit(X_numeric)
    
    meta = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'training_count': len(df)
    }
    return nlp_pipeline, iso_forest, meta

def sigmoid_scale(x):
    """Maps anomaly score to 1-9 range. 
    Score 0 (boundary) maps to ~5. 
    Very negative (anomaly) maps to 1.
    Very positive (normal) maps to 9."""
    # Sigmoid: 1 / (1 + e^-x) -> 0..1
    # We apply a gain to make the transition sharper or smoother. 
    # Anomaly scores are often small, e.g., -0.2 to 0.2. So we multiply x by ~10.
    import math
    try:
        val = 1 / (1 + math.exp(-x * 10))
    except OverflowError:
        val = 0 if x < 0 else 1
    
    # Scale 0..1 to 1..9
    scaled = int(val * 8 + 1)
    return max(1, min(9, scaled))

def calculate_priority(urgency, amount, tenure):
    """Calculates priority 1-9 based on business rules."""
    score = 0
    
    # 1. Urgency (Max 3)
    if urgency == "High":
        score += 3
    else:
        score += 1
        
    # 2. Amount (Max 3)
    if amount > 5000:
        score += 3
    elif amount > 1000:
        score += 2
    else:
        score += 1
        
    # 3. Tenure (Max 3) - VIPs get priority
    if tenure > 10:
        score += 3
    elif tenure > 3:
        score += 2
    else:
        score += 1
        
    # Total range: 3 to 9. 
    # Mapped directly since it fits well within 1-9.
    return score

def analyze_claim(model_bundle, description, amount, tenure):
    nlp = model_bundle['nlp']
    fraud = model_bundle['fraud']
    
    # NLP
    category = nlp.predict([description])[0]
    
    # Urgency
    urgency_keywords = ['emergency', 'severe', 'critical', 'urgent', 'immediately', 'pain', 'crash']
    urgency = "Medium"
    if any(k in description.lower() for k in urgency_keywords):
        urgency = "High"

    # Fraud & Authenticity
    fraud_risk = "Unknown"
    anomaly_score = 0.0
    authenticity = 5 # Default neutral
    
    if fraud:
        features = pd.DataFrame([[amount, tenure]], columns=['Amount', 'Customer_Tenure'])
        pred = fraud.predict(features)[0]
        anomaly_score = fraud.decision_function(features)[0]
        fraud_risk = "High" if pred == -1 else "Low"
        
        # Calculate Authenticity (1-9)
        authenticity = sigmoid_scale(anomaly_score)
        
    # Calculate Priority (1-9)
    priority = calculate_priority(urgency, amount, tenure)
    
    # Calculate Rank
    rank = authenticity * priority
            
    return category, urgency, fraud_risk, anomaly_score, authenticity, priority, rank

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "Smart Claims Processor API is Running"}

@app.get("/api/claims", response_model=List[dict])
def get_claims():
    if os.path.exists(CLAIMS_DB_PATH):
        df = pd.read_csv(CLAIMS_DB_PATH)
        # Convert to list of dicts, handle NaN
        return df.fillna("").to_dict(orient="records")
    return []

@app.post("/api/claims")
def submit_claim(claim: ClaimSubmission):
    existing_model = load_model()
    if not existing_model:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the system first via Admin Dashboard.")

    cat, urg, risk, score, auth, prio, rank = analyze_claim(existing_model, claim.description, claim.amount, claim.tenure)
    
    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Customer_ID": claim.customer_id,
        "Description": claim.description,
        "Amount": claim.amount,
        "Tenure": claim.tenure,
        "Category": cat,
        "Urgency": urg,
        "Fraud_Risk": risk,
        "Anomaly_Score": score,
        "authenticity_score": auth,
        "priority_score": prio,
        "rank_score": rank,
        "Status": "Pending Review"
    }
    
    df_new = pd.DataFrame([record])
    if not os.path.exists(CLAIMS_DB_PATH):
        df_new.to_csv(CLAIMS_DB_PATH, index=False)
    else:
        df_new.to_csv(CLAIMS_DB_PATH, mode='a', header=False, index=False)
    
    return {"message": "Claim submitted successfully", "data": record}

@app.post("/api/train")
async def train_model(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    s = str(content, 'utf-8')
    data = StringIO(s)
    
    try:
        df = pd.read_csv(data)
        nlp, fraud, meta = train_system_logic(df)
        save_model(nlp, fraud, meta)
        return {"message": "Training successful", "meta": meta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/model/status")
def get_model_status():
    existing_model = load_model()
    if existing_model:
        return {"active": True, "meta": existing_model['meta']}
    return {"active": False, "meta": None}
