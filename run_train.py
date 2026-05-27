import pandas as pd
import wandb
from src.train import train_model_logic
from src.engineering import DataProcessor

def main():
    # Initialize wandb run
    run = wandb.init(project="insuranceClaim-ai", job_type="train")

    # Load and process data
    raw_df = pd.read_csv("data/insurance_claims.csv")
    processor = DataProcessor()
    
    df = processor.clean_data(raw_df)
    df = processor.encode_target(df)

    # Feature selection
    feature_cols = ['amount', 'tenure', 'witness_count', 'hour', 'is_night_incident', 'suspicious_evidence']
    X = df[feature_cols]
    y = df['target']
    
    # Call the logic from train.py
    pipeline_manager, fraud_model, anomaly_model = train_model_logic(X, y)

    # Save models
    pipeline_manager.save_models("models/")
    
    wandb.finish()
    print("Training Complete. Models saved to models/")

if __name__ == "__main__":
    main()
