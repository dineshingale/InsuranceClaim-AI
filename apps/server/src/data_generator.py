import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

def generate_synthetic_data(num_records=500):
    data = []
    
    categories = ['Medical', 'Accident', 'Theft', 'Property']
    urgency_keywords = ['emergency', 'severe', 'critical', 'urgent', 'immediately']
    normal_keywords = ['routine', 'checkup', 'follow-up', 'maintenance', 'minor']
    
    for i in range(num_records):
        claim_id = fake.uuid4()
        policy_type = random.choice(categories)
        tenure = random.randint(1, 20) # Years
        
        # Decide if fraud
        is_fraud = random.random() < 0.10 # 10% fraud rate
        
        if is_fraud:
            # Fraud Pattern: High amount, Vague description, Low tenure
            amount = np.random.normal(5000, 2000) # Higher average
            if amount < 0: amount = 1000
            
            description = random.choice([
                "I lost my items during a trip.", 
                "Accidental damage occurred.", 
                "Unknown incident causing pain.", 
                "Items missing from home.",
                "Vehicle damage due to road conditions."
            ])
            # Make description slightly randomized
            description += " " + fake.sentence()
            
            risk_type = "High"
        else:
            # Normal Pattern: Lower amount, Specific description
            amount = np.random.normal(500, 200)
            if amount < 0: amount = 50
            
            category_context = {
                'Medical': ["slipped", "back pain", "physiotherapy", "dental", "checkup"],
                'Accident': ["fender bender", "scratch", "bumper", "collision"],
                'Theft': ["bike stolen", "phone taken", "wallet lost"],
                'Property': ["pipe leak", "window broken", "roof damage"]
            }
            
            keywords = category_context.get(policy_type, ["incident"])
            base_desc = random.choice(keywords)
            
            # Inject urgency sometimes
            is_urgent = random.random() < 0.2
            urgency_word = random.choice(urgency_keywords) if is_urgent else random.choice(normal_keywords)
            
            description = f"{urgency_word} request for {base_desc}. {fake.sentence()}"
            risk_type = "Low"

        # Ensure amount is refined
        amount = round(amount, 2)
        
        data.append({
            "Claim_ID": claim_id,
            "Description": description,
            "Amount": amount,
            "Policy_Type": policy_type,
            "Customer_Tenure": tenure,
            "Is_Fraud": 1 if is_fraud else 0
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic data...")
    df = generate_synthetic_data(1000)
    df.to_csv("insurance_claims.csv", index=False)
    print("Data generated: insurance_claims.csv")
