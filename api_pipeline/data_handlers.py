from abc import ABC, abstractmethod
import json

class DataHandler(ABC):
    """Abstract base class for data handlers."""

    @abstractmethod
    async def handle_data(self, data: dict):
        """Handles the data from the API."""
        pass

class GCSDataHandler(DataHandler):
    """Data handler for Google Cloud Storage."""

    def __init__(self, destination_config: dict):
        self.bucket = destination_config.get("bucket")
        self.prefix = destination_config.get("prefix", "")
        self.format = destination_config.get("format", "json")

    async def handle_data(self, data: dict):
        """Handles the data by saving it to a file.

        Note: This is a placeholder and does not yet upload to GCS.
        """
        # TODO: Upload to GCS
        import os
        os.makedirs(self.prefix, exist_ok=True)
        filename = f"{self.prefix}data.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")

class BigQueryDataHandler(DataHandler):
    """Data handler for BigQuery."""

    def __init__(self, destination_config: dict):
        self.dataset = destination_config.get("dataset")
        self.table = destination_config.get("table")
        self.write_mode = destination_config.get("write_mode", "append")

    async def handle_data(self, data: dict):
        """Handles the data.

        Note: This is a placeholder and does not yet upload to BigQuery.
        """
        # TODO: Implement BigQuery data handling
        print(f"Handling data for BigQuery table {self.dataset}.{self.table}")

class PubSubDataHandler(DataHandler):
    """Data handler for Pub/Sub."""

    def __init__(self, destination_config: dict):
        self.topic = destination_config.get("topic")

    async def handle_data(self, data: dict):
        """Handles the data.

        Note: This is a placeholder and does not yet publish to Pub/Sub.
        """
        # TODO: Implement Pub/Sub data handling
        print(f"Handling data for Pub/Sub topic {self.topic}")

def get_data_handler(destination_config: dict) -> DataHandler:
    """Returns the appropriate data handler for the given config.

    Args:
        destination_config: The destination configuration.

    Returns:
        An instance of the appropriate DataHandler.
    """
    destination_type = destination_config.get("type")
    if destination_type == "gcs":
        return GCSDataHandler(destination_config)
    elif destination_type == "bigquery":
        return BigQueryDataHandler(destination_config)
    elif destination_type == "pubsub":
        return PubSubDataHandler(destination_config)
    else:
        raise ValueError(f"Unsupported destination type: {destination_type}")
