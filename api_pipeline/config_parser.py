import yaml

def load_config(config_path: str) -> dict:
    """Loads the YAML configuration file.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        A dictionary containing the configuration.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_api_configs(config: dict) -> list:
    """Returns the API configurations.

    Args:
        config: The pipeline configuration.

    Returns:
        A list of API configurations.
    """
    return config.get("apis", [])

def get_destination_configs(config: dict) -> list:
    """Returns the data destination configurations.

    Args:
        config: The pipeline configuration.

    Returns:
        A list of data destination configurations.
    """
    return config.get("destinations", [])

def get_routing_configs(config: dict) -> list:
    """Returns the routing configurations.

    Args:
        config: The pipeline configuration.

    Returns:
        A list of routing configurations.
    """
    return config.get("routing", [])

def get_settings(config: dict) -> dict:
    """Returns the pipeline settings.

    Args:
        config: The pipeline configuration.

    Returns:
        A dictionary containing the pipeline settings.
    """
    return config.get("settings", {})
