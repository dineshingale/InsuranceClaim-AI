import pandas as pd
import numpy as np

class DataProcessor:
    def clean_data(self, df):
        # Feature mapping for BigQuery schema
        # Rename BigQuery columns to standard names for model
        df['amount'] = df['total_claim_amount'] if 'total_claim_amount' in df.columns else df.get('claim_amount', 0)
        df['tenure'] = df['months_as_customer']
        df['witness_count'] = df['num_witnesses'] if 'num_witnesses' in df.columns else df.get('witnesses', 0)
        df['hour'] = df['incident_hour_of_the_day'] if 'incident_hour_of_the_day' in df.columns else df.get('incident_hour', 0)
        
        # synthetic feature: night-time risk
        # claims between 11 PM and 5 AM are statistically higher risk
        df['is_night_incident'] = df['hour'].apply(lambda x: 1 if x >= 23 or x <= 5 else 0)

        # synthetic feature: low evidence flag
        # high amount + 0 witnesses = suspicious
        df['suspicious_evidence'] = np.where((df['amount'] > 10000) & (df['witness_count'] == 0), 1, 0)

        return df

    def encode_target(self, df):
        # Handle multiple formats of fraud_reported
        # Supports: 'Y'/'N', 'true'/'false', True/False, 1/0
        if 'fraud_reported' in df.columns:
            def convert_to_binary(val):
                if pd.isna(val):
                    return 0
                
                # Convert to string and uppercase for comparison
                val_str = str(val).strip().upper()
                
                # Handle fraud cases (1)
                if val_str in ['Y', 'YES', 'TRUE', '1', 'T']:
                    return 1
                # Handle legitimate cases (0)
                elif val_str in ['N', 'NO', 'FALSE', '0', 'F']:
                    return 0
                # Fallback
                else:
                    return 0
            
            df['target'] = df['fraud_reported'].apply(convert_to_binary)
        
        return df
