from enum import Enum
from typing import Dict, List, Set
from pydantic import BaseModel, Field, validator

class AuthenticationType(str, Enum):
    BEARER_TOKEN = "bearer_token"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    CUSTOM = "custom"

class PaginationType(str, Enum):
    CURSOR = "cursor"
    OFFSET = "offset"
    PAGE = "page"
    NONE = "none"

class DataFormat(str, Enum):
    JSON = "json"
    PARQUET = "parquet"
    CSV = "csv"
    AVRO = "avro"

class CloudProvider(str, Enum):
    AWS_S3 = "aws_s3"
    AZURE_BLOB = "azure_blob"
    GCP_STORAGE = "gcp_storage"

class NotificationType(str, Enum):
    SLACK = "slack"
    EMAIL = "email"
    TEAMS = "teams"
    WEBHOOK = "webhook"

class TransformationType(str, Enum):
    RENAME_FIELDS = "rename_fields"
    ADD_METADATA = "add_metadata"
    FILTER = "filter"
    FLATTEN_JSON = "flatten_json"
    CUSTOM_FUNCTION = "custom_function"
    CONVERT_TYPES = "convert_types"
    AGGREGATE = "aggregate"

class BackoffStrategy(str, Enum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"

class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Application-specific constants
class EnablonConstants:
    BASE_URL = "https://your-company.enablon.com"
    
    # Common endpoints
    ENDPOINTS = {
        "incidents": "/api/v1/incidents",
        "compliance_assessments": "/api/v1/compliance/assessments",
        "risk_assessments": "/api/v1/risk/assessments",
        "audits": "/api/v1/audits",
        "corrective_actions": "/api/v1/corrective-actions",
        "training_records": "/api/v1/training/records"
    }
    
    # Valid incident statuses
    INCIDENT_STATUSES = ["open", "in_progress", "closed", "cancelled"]
    
    # Valid severity levels
    SEVERITY_LEVELS = ["low", "medium", "high", "critical"]
    
    # Valid risk levels
    RISK_LEVELS = ["low", "medium", "high", "extreme"]
    
    # Default rate limits
    DEFAULT_RATE_LIMIT = 60  # requests per minute
    DEFAULT_BURST_LIMIT = 5
    
    # Standard field mappings
    FIELD_MAPPINGS = {
        "incident_id": "external_incident_id",
        "created_date": "created_at",
        "modified_date": "updated_at",
        "severity_level": "severity",
        "risk_level": "risk_rating",
        "status": "current_status"
    }

class PlanfulConstants:
    BASE_URL = "https://api.planful.com"
    
    # Common endpoints
    ENDPOINTS = {
        "budgets": "/v1/budgets",
        "forecasts": "/v1/forecasts",
        "actuals": "/v1/actuals",
        "scenarios": "/v1/scenarios",
        "dimensions": "/v1/dimensions",
        "accounts": "/v1/accounts"
    }
    
    # Valid fiscal years (can be dynamic)
    FISCAL_YEARS = ["2023", "2024", "2025", "2026"]
    
    # Valid forecast types
    FORECAST_TYPES = ["rolling", "annual", "quarterly", "monthly"]
    
    # Valid budget statuses
    BUDGET_STATUSES = ["draft", "approved", "locked", "archived"]
    
    # Valid granularity levels
    GRANULARITY_LEVELS = ["daily", "weekly", "monthly", "quarterly", "yearly"]
    
    # Default rate limits
    DEFAULT_RATE_LIMIT = 120  # requests per minute
    DEFAULT_BURST_LIMIT = 15
    
    # Standard field mappings
    FIELD_MAPPINGS = {
        "budget_id": "external_budget_id",
        "created_timestamp": "created_at",
        "last_modified": "updated_at",
        "fiscal_period": "period",
        "amount_usd": "amount",
        "currency_code": "currency"
    }

# Global pipeline constants
class PipelineConstants:
    # Default retry configuration
    DEFAULT_RETRY_CONFIG = {
        "max_attempts": 3,
        "delay": 1.0,
        "backoff_multiplier": 2.0,
        "retry_on_status": [429, 500, 502, 503, 504]
    }
    
    # Common HTTP headers
    STANDARD_HEADERS = {
        "User-Agent": "Corporate-Data-Pipeline/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Timeout settings
    DEFAULT_TIMEOUT = 30.0
    LONG_TIMEOUT = 120.0
    
    # Common cron schedules
    SCHEDULES = {
        "hourly": "0 * * * *",
        "daily": "0 6 * * *",
        "weekly": "0 6 * * 1",
        "monthly": "0 6 1 * *",
        "every_4_hours": "0 */4 * * *",
        "every_8_hours": "0 */8 * * *",
        "every_12_hours": "0 */12 * * *"
    }
    
    # Common transformation patterns
    METADATA_FIELDS = {
        "extracted_at": "{{ now() }}",
        "pipeline_version": "1.0",
        "data_quality_score": "{{ quality_score() }}"
    }
    
    # File naming patterns
    PATH_PATTERNS = {
        "date_partitioned": "{source}/{table}/{year}/{month}/{day}",
        "timestamp_partitioned": "{source}/{table}/{timestamp}",
        "simple": "{source}/{table}/{date}"
    }

# Validation constants
class ValidationConstants:
    # Max/min values for various settings
    MAX_RETRY_ATTEMPTS = 10
    MIN_RETRY_DELAY = 0.1
    MAX_RETRY_DELAY = 60.0
    
    MAX_RATE_LIMIT = 1000  # requests per minute
    MIN_RATE_LIMIT = 1
    
    MAX_BURST_LIMIT = 100
    MIN_BURST_LIMIT = 1
    
    # Required fields for different config sections
    REQUIRED_PIPELINE_FIELDS = ["name", "description", "source", "destination"]
    REQUIRED_SOURCE_FIELDS = ["type", "base_url", "authentication", "endpoints"]
    REQUIRED_ENDPOINT_FIELDS = ["name", "path", "method"]
    
    # Valid status codes
    SUCCESS_STATUS_CODES = [200, 201, 202, 204]
    RETRIABLE_STATUS_CODES = [429, 500, 502, 503, 504]

# Application registry
APPLICATION_REGISTRY = {
    "enablon": {
        "constants": EnablonConstants,
        "default_auth": AuthenticationType.BASIC,
        "default_format": DataFormat.PARQUET,
        "default_rate_limit": 60,
        "typical_endpoints": EnablonConstants.ENDPOINTS,
        "field_mappings": EnablonConstants.FIELD_MAPPINGS
    },
    "planful": {
        "constants": PlanfulConstants,
        "default_auth": AuthenticationType.BEARER_TOKEN,
        "default_format": DataFormat.PARQUET,
        "default_rate_limit": 120,
        "typical_endpoints": PlanfulConstants.ENDPOINTS,
        "field_mappings": PlanfulConstants.FIELD_MAPPINGS
    }
}

# Enhanced config validation with constants
class EnhancedAuthConfig(BaseModel):
    type: AuthenticationType
    token_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    scope: Optional[str] = None

class EnhancedEndpointConfig(BaseModel):
    name: str
    path: str
    method: HTTPMethod = HTTPMethod.GET
    params: Optional[Dict[str, Any]] = {}
    headers: Optional[Dict[str, str]] = {}
    depends_on: Optional[List[str]] = []
    pagination: Optional[Dict[str, Any]] = {}
    
    @validator('path')
    def validate_path(cls, v):
        if not v.startswith('/'):
            raise ValueError('Path must start with /')
        return v

class EnhancedRateLimitConfig(BaseModel):
    requests_per_minute: int = Field(default=60, ge=ValidationConstants.MIN_RATE_LIMIT, le=ValidationConstants.MAX_RATE_LIMIT)
    burst_limit: int = Field(default=10, ge=ValidationConstants.MIN_BURST_LIMIT, le=ValidationConstants.MAX_BURST_LIMIT)
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL

class EnhancedRetryConfig(BaseModel):
    max_attempts: int = Field(default=3, ge=1, le=ValidationConstants.MAX_RETRY_ATTEMPTS)
    delay: float = Field(default=1.0, ge=ValidationConstants.MIN_RETRY_DELAY, le=ValidationConstants.MAX_RETRY_DELAY)
    backoff_multiplier: float = Field(default=2.0, ge=1.0, le=10.0)
    retry_on_status: List[int] = Field(default=ValidationConstants.RETRIABLE_STATUS_CODES)

class EnhancedTransformationConfig(BaseModel):
    type: TransformationType
    mapping: Optional[Dict[str, str]] = None
    fields: Optional[Dict[str, Any]] = None
    condition: Optional[str] = None
    function: Optional[str] = None
    module: Optional[str] = None

class EnhancedDestinationConfig(BaseModel):
    type: str
    provider: Optional[CloudProvider] = None
    bucket: Optional[str] = None
    container: Optional[str] = None
    path: str
    format: DataFormat = DataFormat.JSON
    partition_by: Optional[List[str]] = None
    connection_string: Optional[str] = None
    table: Optional[str] = None

class EnhancedNotificationConfig(BaseModel):
    type: NotificationType
    webhook_url: Optional[str] = None
    channel: Optional[str] = None
    recipients: Optional[List[str]] = None
    subject: Optional[str] = None

# Utility functions for working with constants
def get_application_defaults(app_name: str) -> Dict:
    """Get default configuration values for a specific application"""
    return APPLICATION_REGISTRY.get(app_name, {})

def validate_field_mapping(app_name: str, field_name: str) -> str:
    """Get the standard field mapping for an application"""
    app_config = APPLICATION_REGISTRY.get(app_name, {})
    field_mappings = app_config.get("field_mappings", {})
    return field_mappings.get(field_name, field_name)

def get_common_endpoints(app_name: str) -> Dict[str, str]:
    """Get common endpoints for an application"""
    app_config = APPLICATION_REGISTRY.get(app_name, {})
    return app_config.get("typical_endpoints", {})

def validate_enum_value(enum_class, value: str, field_name: str) -> str:
    """Validate that a value is in the allowed enum values"""
    try:
        enum_class(value)
        return value
    except ValueError:
        valid_values = [e.value for e in enum_class]
        raise ValueError(f"Invalid {field_name}: {value}. Must be one of: {valid_values}")

# Example usage in config loading
def load_enhanced_config(config_file: str, app_name: str = None):
    """Load config with enhanced validation and defaults"""
    with open(config_file, 'r') as f:
        config_data = yaml.safe_load(f)
    
    # Apply application-specific defaults
    if app_name:
        defaults = get_application_defaults(app_name)
        # Merge defaults with config_data
        # ... implementation here
    
    # Validate enums
    if "authentication" in config_data.get("source", {}):
        auth_type = config_data["source"]["authentication"]["type"]
        validate_enum_value(AuthenticationType, auth_type, "authentication.type")
    
    return config_data