import apache_beam as beam
import json

class GCSSink(beam.PTransform):
    """A Beam sink for writing data to GCS."""

    def __init__(self, destination_config):
        self.destination_config = destination_config

    def expand(self, pcoll):
        return (
            pcoll
            | "To JSON" >> beam.Map(json.dumps)
            | "Write to GCS" >> beam.Map(print) # Mocked
        )

class BigQuerySink(beam.PTransform):
    """A Beam sink for writing data to BigQuery."""

    def __init__(self, destination_config):
        self.destination_config = destination_config

    def expand(self, pcoll):
        return (
            pcoll
            | "Write to BigQuery" >> beam.Map(print) # Mocked
        )

class PubSubSink(beam.PTransform):
    """A Beam sink for writing data to Pub/Sub."""

    def __init__(self, destination_config):
        self.destination_config = destination_config

    def expand(self, pcoll):
        return (
            pcoll
            | "To Bytes" >> beam.Map(lambda x: json.dumps(x).encode("utf-8"))
            | "Write to Pub/Sub" >> beam.Map(print) # Mocked
        )

def get_sink(destination_config):
    """Returns the appropriate sink for the given destination config."""
    if destination_config.type == "gcs":
        return GCSSink(destination_config)
    elif destination_config.type == "bigquery":
        return BigQuerySink(destination_config)
    elif destination_config.type == "pubsub":
        return PubSubSink(destination_config)
    else:
        raise ValueError(f"Unsupported destination type: {destination_config.type}")
