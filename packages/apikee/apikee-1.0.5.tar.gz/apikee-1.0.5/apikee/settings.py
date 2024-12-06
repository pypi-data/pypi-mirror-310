import aiohttp
from .exceptions import ServerConnectionException, ServerValidationException

class ApiKeeConfig:
    """
    Configuration for ApiKee package.
    """
    local_key = None
    server_url = None
    project_id = None
    env = None
    api_key = None

    @staticmethod
    async def validate_server_key(api_key: str, endpoint_id: str) -> bool:
        """
        Asynchronously validates the API key using the server.
        """
        if not ApiKeeConfig.server_url or not ApiKeeConfig.project_id or not ApiKeeConfig.api_key:
            raise ValueError("Server validation is not configured properly.")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{ApiKeeConfig.server_url}/validate",
                    headers={"Authorization": f"Bearer {ApiKeeConfig.api_key}"},
                    json={"api_key": api_key, "endpoint_id": endpoint_id},
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        # Raise exception with appropriate status code and message
                        message = await response.text()
                        raise ServerValidationException(response.status, message)
        except aiohttp.ClientError as e:
            raise ServerConnectionException(str(e))
