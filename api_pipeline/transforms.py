import apache_beam as beam
from .schema_validator import SchemaValidator

class ValidateData(beam.PTransform):
    """A Beam transform for validating data against a JSON schema."""

    def __init__(self, schema_config):
        self.schema_config = schema_config

    def expand(self, pcoll):
        return pcoll | "Validate" >> beam.ParDo(self._validate, self.schema_config)

    def _validate(self, element, schema_config):
        try:
            validator = SchemaValidator(schema_config)
            validator.validate(element)
            yield element
        except Exception as e:
            # TODO: Add proper logging and dead-letter queue
            print(f"Validation failed: {e}")

class RouteData(beam.PTransform):
    """A Beam transform for routing data to different destinations."""

    def __init__(self, routing_configs, destination_configs):
        self.routing_configs = routing_configs
        self.destination_configs = destination_configs

    def expand(self, pcoll):
        # This is a simplified routing implementation.
        # A more robust implementation would use side inputs or a different approach.
        for route in self.routing_configs:
            for dest_name in route.destinations:
                for dest_config in self.destination_configs:
                    if dest_config.name == dest_name:
                        # In a real pipeline, you would tag the output and have separate
                        # sinks for each destination.
                        yield (dest_config, pcoll)
