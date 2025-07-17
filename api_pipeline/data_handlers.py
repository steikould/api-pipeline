from abc import ABC, abstractmethod
from . import gcp_util
from .config import DestinationConfig

class DataHandler(ABC):
    """Abstract base class for data handlers."""

    @abstractmethod
    async def handle_data(self, data: dict):
        """Handles the data from the API."""
        pass

class GCSDataHandler(DataHandler):
    """Data handler for Google Cloud Storage."""

    def __init__(self, destination_config: DestinationConfig):
        self.bucket = destination_config.bucket
        self.prefix = destination_config.prefix
        self.format = destination_config.format

    async def handle_data(self, data: dict):
        """Handles the data by uploading it to GCS."""
        blob_name = f"{self.prefix}data.json"  # TODO: Generate a unique name
        gcp_util.upload_to_gcs(self.bucket, blob_name, data)

class BigQueryDataHandler(DataHandler):
    """Data handler for BigQuery."""

    def __init__(self, destination_config: DestinationConfig):
        self.dataset = destination_config.dataset
        self.table = destination_config.table

    async def handle_data(self, data: dict):
        """Handles the data by inserting it into BigQuery."""
        gcp_util.insert_into_bigquery(self.dataset, self.table, data)

class PubSubDataHandler(DataHandler):
    """Data handler for Pub/Sub."""

    def __init__(self, destination_config: DestinationConfig):
        self.topic = destination_config.topic

    async def handle_data(self, data: dict):
        """Handles the data by publishing it to Pub/Sub."""
        gcp_util.publish_to_pubsub(self.topic, data)

def get_data_handler(destination_config: DestinationConfig) -> DataHandler:
    """Returns the appropriate data handler for the given config.

    Args:
        destination_config: The destination configuration.

    Returns:
        An instance of the appropriate DataHandler.
    """
    destination_type = destination_config.type
    if destination_type == "gcs":
        return GCSDataHandler(destination_config)
    elif destination_type == "bigquery":
        return BigQueryDataHandler(destination_config)
    elif destination_type == "pubsub":
        return PubSubDataHandler(destination_config)
    else:
        raise ValueError(f"Unsupported destination type: {destination_type}")
