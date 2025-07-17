import json

def upload_to_gcs(bucket_name: str, blob_name: str, data: dict):
    """MOCKED: Uploads data to a GCS bucket."""
    print(f"MOCKED: Data uploaded to gs://{bucket_name}/{blob_name}")

def insert_into_bigquery(dataset_name: str, table_name: str, data: dict):
    """MOCKED: Inserts data into a BigQuery table."""
    print(f"MOCKED: Data inserted into BigQuery table {dataset_name}.{table_name}")

def publish_to_pubsub(topic_name: str, data: dict):
    """MOCKED: Publishes a message to a Pub/Sub topic."""
    print(f"MOCKED: Message published to Pub/Sub topic {topic_name}")
