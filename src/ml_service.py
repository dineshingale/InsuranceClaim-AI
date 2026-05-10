import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from datetime import datetime
from src.config import MODEL_PATH
from src.utils import sigmoid_scale, calculate_priority

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def save_model(nlp_pipeline, iso_forest, training_meta, label_encoder=None):
    joblib.dump({
        'nlp': nlp_pipeline,
        'fraud': iso_forest,
        'meta': training_meta,
        'label_encoder': label_encoder
    }, MODEL_PATH)

def train_system_logic(df):
    # --- DATA ENGINEERING & PANDAS ---
    # Cleaning: Fill missing numeric values using median
    df['Amount'] = df['Amount'].fillna(df['Amount'].median() if not df['Amount'].empty else 0)
    df['Customer_Tenure'] = df['Customer_Tenure'].fillna(0)

    # Fallback if Policy_Type not present
    if 'Policy_Type' not in df.columns:
        df['Policy_Type'] = df['Category'] if 'Category' in df.columns else 'Unknown'
    
    # Lambda Maps & Series: Clean description text
    df['Description'] = df['Description'].map(lambda x: str(x).lower().strip())
    
    # Grouping & Data Transformation: Mean Amount by Policy_Type
    amount_map = df.groupby('Policy_Type')['Amount'].mean().to_dict()
    df['Avg_Policy_Amount'] = df['Policy_Type'].map(amount_map)
    
    # Synthetic Features: Amount Ratio and Tenure Risk
    df['Amount_Ratio'] = df['Amount'] / df['Avg_Policy_Amount'].fillna(1)
    df['Tenure_Risk'] = df['Customer_Tenure'].apply(lambda x: 1.0 if x < 2 else (0.5 if x < 5 else 0.1))
    
    # One-Hot Encoding for Fraud Model
    df_fraud = pd.get_dummies(df, columns=['Policy_Type'], prefix='Pol')
    
    # --- ML UPGRADES: NLP (XGBoost & Tuning) ---
    X_text = df['Description']
    y_category = df['Policy_Type']
    
    # Label Encoding for XGBoost
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_category)
    
    # Pipeline for Data Leakage Prevention during tuning
    nlp_pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english')),
        ('classifier', XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss'))
    ])
    
    # Tuning & Cross-Validation
    param_grid = {
        'classifier__n_estimators': [50, 100],
        'classifier__max_depth': [3, 5]
    }
    grid_search = GridSearchCV(nlp_pipeline, param_grid, cv=min(3, len(df)//2 if len(df)>2 else 2), scoring='accuracy')
    grid_search.fit(X_text, y_encoded)
    best_nlp_pipeline = grid_search.best_estimator_

    # --- FRAUD DETECTION ---
    iso_forest = None
    fraud_features = ['Amount', 'Customer_Tenure', 'Amount_Ratio', 'Tenure_Risk']
    
    # Add one-hot encoded columns to features
    one_hot_cols = [col for col in df_fraud.columns if col.startswith('Pol_')]
    fraud_features.extend(one_hot_cols)
    
    if all(col in df_fraud.columns for col in ['Amount', 'Customer_Tenure']):
        X_numeric = df_fraud[fraud_features].fillna(0)
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        iso_forest.fit(X_numeric)
    
    meta = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'training_count': len(df),
        'amount_map': amount_map,
        'fraud_features': fraud_features
    }
    return best_nlp_pipeline, iso_forest, meta, le

def analyze_claim(model_bundle, description, amount, tenure):
    nlp = model_bundle['nlp']
    fraud = model_bundle['fraud']
    meta = model_bundle.get('meta', {})
    le = model_bundle.get('label_encoder')
    
    # NLP
    clean_desc = str(description).lower().strip()
    encoded_pred = nlp.predict([clean_desc])[0]
    category = le.inverse_transform([encoded_pred])[0] if le else encoded_pred
    
    # Urgency
    urgency_keywords = ['emergency', 'severe', 'critical', 'urgent', 'immediately', 'pain', 'crash']
    urgency = "Medium"
    if any(k in clean_desc for k in urgency_keywords):
        urgency = "High"

    # Fraud & Authenticity
    fraud_risk = "Unknown"
    anomaly_score = 0.0
    authenticity = 5 # Default neutral
    
    if fraud:
        # Synthetic features for inference
        avg_amt = meta.get('amount_map', {}).get(category, 1000)
        amount_ratio = amount / max(avg_amt, 1)
        tenure_risk = 1.0 if tenure < 2 else (0.5 if tenure < 5 else 0.1)
        
        # Build DataFrame for inference
        inference_data = {
            'Amount': [amount],
            'Customer_Tenure': [tenure],
            'Amount_Ratio': [amount_ratio],
            'Tenure_Risk': [tenure_risk]
        }
        
        # Add one-hot features (all 0 except the matched category)
        fraud_features = meta.get('fraud_features', ['Amount', 'Customer_Tenure'])
        for col in fraud_features:
            if col.startswith('Pol_'):
                inference_data[col] = [1 if col == f"Pol_{category}" else 0]
                
        features = pd.DataFrame(inference_data)[fraud_features]
        
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
