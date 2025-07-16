from pydantic import BaseModel, Field
from typing import List, Optional

class AuthConfig(BaseModel):
    type: str
    username_secret: Optional[str] = None
    password_secret: Optional[str] = None
    cert_secret: Optional[str] = None
    key_secret: Optional[str] = None

class EndpointConfig(BaseModel):
    path: str
    method: str
    rate_limit: Optional[int] = None
    pagination: Optional[dict] = None

class SchemaConfig(BaseModel):
    type: str
    file: str

class ApiConfig(BaseModel):
    name: str
    base_url: str
    auth: AuthConfig
    endpoints: List[EndpointConfig]
    schema: SchemaConfig

class DestinationConfig(BaseModel):
    name: str
    type: str
    bucket: Optional[str] = None
    prefix: Optional[str] = None
    format: Optional[str] = None
    dataset: Optional[str] = None
    table: Optional[str] = None
    write_mode: Optional[str] = None
    topic: Optional[str] = None

class RoutingConfig(BaseModel):
    api: str
    destinations: List[str]

class SettingsConfig(BaseModel):
    project_id: str
    max_concurrent_requests: int
    retry_attempts: int
    timeout_seconds: int

class PipelineConfig(BaseModel):
    pipeline: dict
    apis: List[ApiConfig]
    destinations: List[DestinationConfig]
    routing: List[RoutingConfig]
    settings: SettingsConfig

def load_config(config_path: str) -> PipelineConfig:
    """Loads the YAML configuration file and validates it with Pydantic.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        A Pydantic model containing the configuration.
    """
    import yaml
    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)
    return PipelineConfig(**config_dict)
