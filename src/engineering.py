import pandas as pd
import numpy as np

class DataProcessor:
    def clean_data(self, df):
        # feature eature mapping ( mapping Kaggle names to clean API names)
        df['amount'] = df['total_claim_amount']
        df['tenure'] = df['months_as_customer']
        df['witness_count'] = df['witnesses']
        df['hour'] = df['incident_hour_of_the_day']
        
        # synthetic feature: night-time risk
        # claims between 11 PM and 5 AM are statistically higher risk
        df['is_night_incident'] = df['hour'].apply(lambda x: 1 if x >= 23 or x <= 5 else 0)

        # synthetic feature: low evidence flag
        # high amount + 0 witnesses = suspicious
        df['suspicious_evidence'] = np.where((df['amount'] > 10000) & (df['witness_count'] == 0), 1, 0)

        return df

    def encode_target(self, df):
        # Kaggle dataset uses 'Y'/'N'
        if 'fraud_reported' in df.columns:
            df['target'] = df['fraud_reported'].apply(lambda x: 1 if x == 'Y' else 0)
        return df
