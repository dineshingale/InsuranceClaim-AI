import wandb
from sklearn.model_selection import train_test_split
from src.pipeline import InsuranceModelPipeline

def train_model_logic(X, y): # Added arguments here
    # Split data with stratification
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Class distribution: {y.value_counts().to_dict()} (0=legitimate, 1=fraud)")

    # Initialize and train pipeline
    pipeline_manager = InsuranceModelPipeline()
    pipeline_manager.build_supervised_pipeline()
    
    fraud_model = pipeline_manager.train_fraud_model(X_train, y_train)
    anomaly_model = pipeline_manager.train_anomaly_model(X_train)
    
    # Log metrics
    fraud_score = fraud_model.score(X_test, y_test)
    # Note: If anomaly_model is an IsolationForest, .score() returns negative outlier scores, 
    # not accuracy. Ensure your pipeline handles this.
    anomaly_scores = anomaly_model.score_samples(X_test) 
    avg_anomaly_score = anomaly_scores.mean()
    
    wandb.log({"fraud_test_accuracy": fraud_score, "anomaly_test_accuracy": avg_anomaly_score})

    return pipeline_manager, fraud_model, anomaly_model
