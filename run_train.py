import wandb
from src.train import train_model_logic
from src.engineering import DataProcessor
from src.database import BigQueryHandler

def main():
    # Initialize wandb run
    run = wandb.init(project="insuranceClaim-ai", job_type="train")

    # Load from BigQuery instead of CSV
    print("Loading data from BigQuery...")
    bq_handler = BigQueryHandler(key_path="credentials.json")
    
    # Use the Table ID you copied from Step 4.2
    table_id = "insuranceclaim-ai.insurance_data.claims"  # ← UPDATE THIS!
    
    # Load data
    raw_df = bq_handler.load_training_data(table_id)
    
    if raw_df is None:
        raise Exception("Failed to load data from BigQuery")
    
    print(f"Loaded {len(raw_df)} rows from BigQuery")
    
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