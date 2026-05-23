from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load models
XGB_MODEL = joblib.load("models/fraud_xgb.pkl")
ISO_FOREST = joblib.load("models/anomaly_iso.pkl")

class ClaimInput(BaseModel):
    amount: float
    tenure: int
    witnesses: int
    incident_hour: int # 0 to 23

@app.post("/predict")
def predict_claim(data: ClaimInput):
    # Prepare input for model
    input_dict = {
        'amount': data.amount,
        'tenure': data.tenure,
        'witness_count': data.witnesses,
        'hour': data.incident_hour,
        'is_night_incident': 1 if data.incident_hour >= 23 or data.incident_hour <= 5 else 0,
        'suspicious_evidence': 1 if (data.amount > 10000 and data.witnesses == 0) else 0
    }
    
    input_df = pd.DataFrame([input_dict])
    
    # 1. Authenticity (XGBoost + Isolation Forest)
    # Added [0] at the end to get the actual value from the array
    fraud_prob = float(XGB_MODEL.predict_proba(input_df)[0, 1])

    is_anomaly = int(ISO_FOREST.predict(input_df)[0]) # -1 is outlier
    
    is_authentic = True if (fraud_prob < 0.4 and is_anomaly == 1) else False

    # 2. Priority Score (Logic-based 1-10)
    # High Amount + low tenure = High Priority for investigation
    base_priority = (data.amount / 10000) 
    # If it's a new customer (short tenure), prioritize check
    tenure_factor = 2 if data.tenure < 6 else 0 
    
    priority_score = min(10, max(1, int(base_priority + tenure_factor)))

    return {
        "is_authentic": is_authentic,
        "fraud_probability": f"{round(fraud_prob * 100, 2)}%",
        "priority_score": priority_score,
        "recommendation": "Proceed to Payout" if is_authentic else "Flag for Manual Audit"
    }
