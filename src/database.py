import os
from google.cloud import bigquery
from google.oauth2 import service_account

class BigQueryHandler:
    def __init__(self, key_path="credentials.json"):
        # initialize the BigQuery client using a service account key
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Credentials file not found at {key_path}")
        
        # load credentials and initialize client
        self.credentials = service_account.Credentials.from_service_account_file(key_path)
        self.client = bigquery.Client(
            credentials=self.credentials, 
            project=self.credentials.project_id
        )

    def execute_query(self, sql_query):
        # executes a SQL query and returns a Pandas DataFrame.
        try:
            query_job = self.client.query(sql_query)  # API request
            return query_job.to_dataframe() # result to dataframe
        except Exception as e:
            print(f"Error executing BigQuery query: {e}")
            return None

    def load_training_data(self, table_id):
        query = f"SELECT * FROM `{table_id}`"
        print(f"Loading data from: {table_id}")
        df = self.execute_query(query)
        if df is not None:
            print(f"Loaded {len(df)} rows")
        return df