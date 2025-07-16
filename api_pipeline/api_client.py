import aiohttp
from . import auth_manager

class ApiClient:
    """A client for making API requests."""

    def __init__(self, api_config: dict):
        self.base_url = api_config.get("base_url")
        self.auth_manager = auth_manager.get_auth_manager(api_config.get("auth", {}))

    async def make_request(self, endpoint: dict) -> dict:
        """Makes a request to the API.

        Args:
            endpoint: The endpoint configuration.

        Returns:
            The JSON response from the API.
        """
        async with aiohttp.ClientSession() as session:
            auth = await self.auth_manager.get_auth()
            url = f"{self.base_url}{endpoint.get('path')}"
            method = endpoint.get("method", "GET").upper()

            async with session.request(
                method, url, auth=auth
            ) as response:
                response.raise_for_status()
                return await response.json()
