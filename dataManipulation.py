import os
from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# Set up BigQuery client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GCP_JSON_PATH')
client = bigquery.Client()
sender_password = os.getenv('KEYPASS')

def fetch_data_from_bigquery(query):
    query_job = client.query(query)
    return query_job.result().to_dataframe()
