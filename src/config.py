import os
from pathlib import Path

# Get the root directory
ROOT_DIR = Path(__file__).parent.parent

# --- CONFIGURATION ---
# Model path - supports environment variable for production
MODEL_PATH = os.getenv("MODEL_PATH", str(ROOT_DIR / "models" / "churn_model.pkl"))
CLAIMS_DB_PATH = os.getenv("CLAIMS_DB_PATH", str(ROOT_DIR / "data" / "insurance_claims.csv"))

# Ensure directories exist
os.makedirs(ROOT_DIR / "models", exist_ok=True)
os.makedirs(ROOT_DIR / "data", exist_ok=True)
