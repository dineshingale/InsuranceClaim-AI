# run_train.py
import os
from src.train import train_model_logic

def main():
    # Path to your local dataset
    DATA_PATH = "data/insurance_claims.csv"
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}. Please place your CSV there.")
        return

    # Trigger the training
    try:
        train_model_logic(DATA_PATH)
        print("\nSuccessfully trained models! You can now start the API.")
    except Exception as e:
        print(f"\nTraining failed with error: {e}")

if __name__ == "__main__":
    main()
