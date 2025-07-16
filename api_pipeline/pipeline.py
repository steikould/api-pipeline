import asyncio
from . import config_parser
from .api_client import ApiClient
from .schema_validator import SchemaValidator
from .data_handlers import get_data_handler

async def main():
    """The main entry point for the pipeline."""
    config = config_parser.load_config("pipeline_config.yaml")
    api_configs = config_parser.get_api_configs(config)
    destination_configs = config_parser.get_destination_configs(config)
    routing_configs = config_parser.get_routing_configs(config)

    for api_config in api_configs:
        api_client = ApiClient(api_config)
        schema_validator = SchemaValidator(api_config.get("schema", {}))

        for endpoint in api_config.get("endpoints", []):
            try:
                data = await api_client.make_request(endpoint)
                schema_validator.validate(data)
                print(f"Successfully retrieved and validated data from {api_config['name']}{endpoint['path']}")

                for route in routing_configs:
                    if route["api"] == api_config["name"]:
                        for dest_name in route["destinations"]:
                            for dest_config in destination_configs:
                                if dest_config["name"] == dest_name:
                                    handler = get_data_handler(dest_config)
                                    await handler.handle_data(data)
            except Exception as e:
                print(f"Error processing API {api_config['name']}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
