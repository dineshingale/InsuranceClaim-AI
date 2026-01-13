import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.pipeline import Pipeline
from datetime import datetime
from core.config import MODEL_PATH
from core.utils import sigmoid_scale, calculate_priority

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
    # Fallback if Policy_Type not present
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
