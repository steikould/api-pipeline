import apache_beam as beam
from .api_client import ApiClient

class ApiSource(beam.PTransform):
    """A custom Beam source for reading data from APIs."""

    def __init__(self, api_config):
        self.api_config = api_config

    def expand(self, pcoll):
        return (
            pcoll
            | "Create ApiConfig" >> beam.Create([self.api_config])
            | "Read from API" >> beam.ParDo(self._read_from_api)
        )

    def _read_from_api(self, api_config):
        """Reads data from the API endpoints."""
        api_client = ApiClient(api_config)
        for endpoint in api_config.endpoints:
            try:
                data = api_client.make_request(endpoint)
                yield data
            except Exception as e:
                # TODO: Add proper logging
                print(f"Error reading from API: {e}")
