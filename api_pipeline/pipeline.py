import asyncio
from . import config
from .api_client import ApiClient
from .schema_validator import SchemaValidator
from .data_handlers import get_data_handler
from .logger import setup_logger

logger = setup_logger()

async def run_pipeline(config_path: str):
    """The main entry point for the pipeline."""
    try:
        pipeline_config = config.load_config(config_path)
        logger.info("Pipeline config loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading pipeline config: {e}")
        return

    for api_config in pipeline_config.apis:
        api_client = ApiClient(api_config)
        try:
            schema_validator = SchemaValidator(api_config.schema)
        except Exception as e:
            logger.error(f"Error loading schema for API {api_config.name}: {e}")
            continue

        for endpoint in api_config.endpoints:
            try:
                data = await api_client.make_request(endpoint)
                logger.info(f"Successfully retrieved data from {api_config.name}{endpoint.path}")
            except Exception as e:
                logger.error(f"Error retrieving data from {api_config.name}{endpoint.path}: {e}")
                continue

            try:
                schema_validator.validate(data)
                logger.info(f"Successfully validated data from {api_config.name}{endpoint.path}")
            except Exception as e:
                logger.error(f"Error validating data from {api_config.name}{endpoint.path}: {e}")
                continue

            for route in pipeline_config.routing:
                if route.api == api_config.name:
                    for dest_name in route.destinations:
                        for dest_config in pipeline_config.destinations:
                            if dest_config.name == dest_name:
                                try:
                                    handler = get_data_handler(dest_config)
                                    await handler.handle_data(data)
                                    logger.info(f"Successfully handled data for destination {dest_name}")
                                except Exception as e:
                                    logger.error(f"Error handling data for destination {dest_name}: {e}")
