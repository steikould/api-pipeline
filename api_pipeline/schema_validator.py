import json
from jsonschema import validate

class SchemaValidator:
    """A class for validating data against a JSON schema."""

    def __init__(self, schema_config: dict):
        self.schema_file = schema_config.get("file")
        self.schema = self._load_schema()

    def _load_schema(self) -> dict:
        """Loads the JSON schema from the file."""
        with open(self.schema_file, "r") as f:
            return json.load(f)

    def validate(self, data: dict):
        """Validates the data against the schema.

        Args:
            data: The data to validate.
        """
        validate(instance=data, schema=self.schema)
