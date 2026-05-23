from pydantic import BaseModel

class ClaimRequest(BaseModel):
    amount: float
    tenure: int
    description: str

class ClaimResponse(BaseModel):
    is_authentic: bool
    fraud_probability: float
    priority_score: int  # 1 to 10
