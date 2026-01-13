import math

def sigmoid_scale(x):
    """Maps anomaly score to 1-9 range."""
    try:
        val = 1 / (1 + math.exp(-x * 10))
    except OverflowError:
        val = 0 if x < 0 else 1
    
    # Scale 0..1 to 1..9
    scaled = int(val * 8 + 1)
    return max(1, min(9, scaled))

def calculate_priority(urgency, amount, tenure):
    """Calculates priority 1-9 based on business rules."""
    score = 0
    
    # 1. Urgency (Max 3)
    if urgency == "High":
        score += 3
    else:
        score += 1
        
    # 2. Amount (Max 3)
    if amount > 5000:
        score += 3
    elif amount > 1000:
        score += 2
    else:
        score += 1
        
    # 3. Tenure (Max 3)
    if tenure > 10:
        score += 3
    elif tenure > 3:
        score += 2
    else:
        score += 1

    return score
