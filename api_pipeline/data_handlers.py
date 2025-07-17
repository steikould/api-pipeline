from abc import ABC, abstractmethod
import json
from .config import DestinationConfig

class DataHandler(ABC):
    """Abstract base class for data handlers."""

    @abstractmethod
    def handle_data(self, data: dict):
        """Handles the data from the API."""
        pass

class GCSDataHandler(DataHandler):
    """Data handler for Google Cloud Storage."""

    def __init__(self, destination_config: DestinationConfig):
        self.bucket = destination_config.bucket
        self.prefix = destination_config.prefix
        self.format = destination_config.format

    def handle_data(self, data: dict):
        """Handles the data by printing it."""
        print(f"GCS Handler: Saving data to gs://{self.bucket}/{self.prefix}data.json")
        print(json.dumps(data, indent=2))


class BigQueryDataHandler(DataHandler):
    """Data handler for BigQuery."""

    def __init__(self, destination_config: DestinationConfig):
        self.dataset = destination_config.dataset
        self.table = destination_config.table

    def handle_data(self, data: dict):
        """Handles the data by printing it."""
        print(f"BigQuery Handler: Inserting data into {self.dataset}.{self.table}")
        print(json.dumps(data, indent=2))


class PubSubDataHandler(DataHandler):
    """Data handler for Pub/Sub."""

    def __init__(self, destination_config: DestinationConfig):
        self.topic = destination_config.topic

    def handle_data(self, data: dict):
        """Handles the data by printing it."""
        print(f"Pub/Sub Handler: Publishing data to {self.topic}")
        print(json.dumps(data, indent=2))

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
