import asyncio
from . import config
from .api_client import ApiClient
from .schema_validator import SchemaValidator
from .data_handlers import get_data_handler

async def run_pipeline():
    """The main entry point for the pipeline."""
    pipeline_config = config.load_config("pipeline_config.yaml")

    for api_config in pipeline_config.apis:
        api_client = ApiClient(api_config)
        schema_validator = SchemaValidator(api_config.schema)

        for endpoint in api_config.endpoints:
            try:
                data = await api_client.make_request(endpoint)
                schema_validator.validate(data)
                print(f"Successfully retrieved and validated data from {api_config.name}{endpoint.path}")

                for route in pipeline_config.routing:
                    if route.api == api_config.name:
                        for dest_name in route.destinations:
                            for dest_config in pipeline_config.destinations:
                                if dest_config.name == dest_name:
                                    handler = get_data_handler(dest_config)
                                    await handler.handle_data(data)
            except Exception as e:
                print(f"Error processing API {api_config.name}: {e}")
