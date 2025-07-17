import httpx
from . import auth_manager
from .config import ApiConfig, EndpointConfig

class ApiClient:
    """A client for making API requests."""

    def __init__(self, api_config: ApiConfig):
        self.base_url = api_config.base_url
        self.auth_manager = auth_manager.get_auth_manager(api_config.auth)

    def make_request(self, endpoint: EndpointConfig) -> dict:
        """Makes a request to the API.

        Args:
            endpoint: The endpoint configuration.

        Returns:
            The JSON response from the API.
        """
        with httpx.Client() as client:
            auth = self.auth_manager.get_auth()
            url = f"{self.base_url}{endpoint.path}"
            method = endpoint.method.upper()

            response = client.request(
                method, url, auth=auth
            )
            response.raise_for_status()
            return response.json()
