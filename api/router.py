from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.schemas import ClaimSubmission
from src.ml_service import load_model, analyze_claim

router = APIRouter()

class PredictionResponse(BaseModel):
    category: str
    urgency: str
    fraud_risk: str
    anomaly_score: float
    authenticity_score: int
    priority_score: int
    rank_score: float

@router.post("/predict", response_model=PredictionResponse)
def predict_claim(claim: ClaimSubmission):
    """
    Predict fraud status, authenticity, or manual review needed for an insurance claim.
    
    Returns:
    - category: Predicted policy category
    - urgency: High, Medium, or Low
    - fraud_risk: High or Low
    - anomaly_score: Numerical score from the anomaly detection model
    - authenticity_score: 1-9 scale (1=fraudulent, 9=authentic)
    - priority_score: 1-9 scale for handling priority
    - rank_score: Combined rank score
    """
    existing_model = load_model()
    if not existing_model:
        raise HTTPException(status_code=503, detail="Model not loaded. Model file not found.")

    cat, urg, risk, score, auth, prio, rank = analyze_claim(
        existing_model, claim.description, claim.amount, claim.tenure
    )
    
    return PredictionResponse(
        category=cat,
        urgency=urg,
        fraud_risk=risk,
        anomaly_score=score,
        authenticity_score=auth,
        priority_score=prio,
        rank_score=rank
    )

@router.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    model = load_model()
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@router.get("/model-info")
def get_model_info():
    """Get information about the loaded model."""
    model = load_model()
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "loaded": True,
        "meta": model.get('meta', {}),
        "training_count": model.get('meta', {}).get('training_count', 0)
    }
