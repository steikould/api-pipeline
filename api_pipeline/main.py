import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from . import config
from .api_source import ApiSource
from .transforms import ValidateData, RouteData
from .sinks import get_sink

def run():
    """The main entry point for the Beam pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        dest="config_path",
        default="pipeline_config.yaml",
        help="The path to the pipeline configuration file.",
    )
    known_args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_config = config.load_config(known_args.config_path)

    with beam.Pipeline(options=pipeline_options) as p:
        for api_config in pipeline_config.apis:
            # Read from the API
            data = p | f"Read from {api_config.name}" >> ApiSource(api_config)

            # Validate the data
            validated_data = data | f"Validate {api_config.name}" >> ValidateData(api_config.schema)

            # Route the data to the appropriate destinations
            for route in pipeline_config.routing:
                if route.api == api_config.name:
                    for dest_name in route.destinations:
                        for dest_config in pipeline_config.destinations:
                            if dest_config.name == dest_name:
                                sink = get_sink(dest_config)
                                validated_data | f"Write to {dest_name}" >> sink

if __name__ == "__main__":
    run()
