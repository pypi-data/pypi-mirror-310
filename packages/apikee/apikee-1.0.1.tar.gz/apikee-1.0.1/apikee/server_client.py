import aiohttp
from .config import config

async def validate_with_server(api_key: str, endpoint_id: str) -> (bool, str):
    if not config.server_url or not config.server_key:
        return False, "Server configuration is incomplete"

    payload = {
        "api_key": api_key,
        "endpoint_id": endpoint_id,
        "project_id": config.project_id,
        "environment": config.environment,
    }

    headers = {"Authorization": f"Bearer {config.server_key}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{config.server_url}/validate", json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("isValid", False), data.get("message", "Unknown error")
            return False, f"Server error: {response.status}"
