import os

# --- CONFIGURATION ---
MODEL_PATH = "models/trained_brain.pkl"
CLAIMS_DB_PATH = "data/submitted_claims.csv"

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)
