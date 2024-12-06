import os
import requests

class ApiKeeConfig:
    """
    Configuration for ApiKee package.
    Manages local key and server-based validation.
    """
    local_key = None
    server_url = None
    project_id = None
    env = None
    api_key = None

    @staticmethod
    def validate_server_key(api_key: str, endpoint_id: str) -> bool:
        """
        Validates the API key using the configured server.
        :param api_key: API key from the request.
        :param endpoint_id: ID of the endpoint being validated.
        :return: True if valid, False otherwise.
        """
        if not ApiKeeConfig.server_url or not ApiKeeConfig.project_id or not ApiKeeConfig.api_key:
            raise ValueError("Server validation is not properly configured.")

        # Send a validation request to the server
        try:
            response = requests.post(
                f"{ApiKeeConfig.server_url}/validate",
                headers={"Authorization": f"Bearer {ApiKeeConfig.api_key}"},
                json={"api_key": api_key, "endpoint_id": endpoint_id},
            )
            return response.status_code == 200
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to the validation server: {e}")

def init_apikee(local_key=None, server_url=None, project_id=None, env=None, api_key=None):
    """
    Initializes the ApiKeeConfig with user-provided values.
    """
    ApiKeeConfig.local_key = local_key or os.getenv("APIKEE_LOCAL_KEY")
    ApiKeeConfig.server_url = server_url or os.getenv("APIKEE_SERVER_URL")
    ApiKeeConfig.project_id = project_id or os.getenv("APIKEE_PROJECT_ID")
    ApiKeeConfig.env = env or os.getenv("APIKEE_ENV")
    ApiKeeConfig.api_key = api_key or os.getenv("APIKEE_API_KEY")

    if not ApiKeeConfig.local_key and not ApiKeeConfig.server_url:
        raise ValueError("Either local_key or server_url must be provided.")
