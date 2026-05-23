import pandas as pd
from src.engineering import DataProcessor
from src.pipeline import InsuranceModelPipeline

def train_model_logic(csv_path="data/insurance_claims.csv"):
    """
    Core logic to clean data and train the models.
    """
    print(f"--- Loading data from {csv_path} ---")
    processor = DataProcessor()
    
    # 1. Load local CSV
    raw_df = pd.read_csv(csv_path)

    # 2. Clean & Engineer Features
    # Note: Ensure your engineering.py has the clean_data and encode_target methods
    df = processor.clean_data(raw_df)
    df = processor.encode_target(df)

    # Inside your train_model_logic in src/train.py:
    feature_cols = ['amount', 'tenure', 'witness_count', 'hour', 'is_night_incident', 'suspicious_evidence']
    X = df[feature_cols]
    y = df['target']


    # 4. Initialize and Train Pipeline
    print("--- Training XGBoost & Isolation Forest ---")
    pipeline_manager = InsuranceModelPipeline()
    
    pipeline_manager.build_supervised_pipeline()
    pipeline_manager.train_fraud_model(X, y)
    pipeline_manager.train_anomaly_model(X)

    # 5. Save the models to the models/ folder
    pipeline_manager.save_models("models/")
    print("--- Training Complete. Models saved in models/ folder ---")
