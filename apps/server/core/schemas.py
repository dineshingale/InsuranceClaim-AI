from datetime import datetime
from pydantic import BaseModel

class ClaimSubmission(BaseModel):
    customer_id: str
    amount: float
    tenure: int
    description: str
    date_of_incident: str

class ClaimRecord(ClaimSubmission):
    timestamp: str
    category: str
    urgency: str
    fraud_risk: str
    anomaly_score: float
    authenticity_score: int
    priority_score: int
    rank_score: int
    status: str
