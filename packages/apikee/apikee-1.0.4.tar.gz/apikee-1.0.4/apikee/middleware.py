from functools import wraps
from .exceptions import ApiKeyMissingException, ApiKeyInvalidException
from .settings import ApiKeeConfig
import asyncio

def apikey(endpoint_id: str = None):
    """
    Asynchronous decorator for API key validation.
    :param endpoint_id: Optional endpoint ID for server-based validation.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract headers from the request object
            request = kwargs.get("request") or (args[0] if args else None)
            if not request:
                raise ValueError("The `request` object is required for API key validation.")

            headers = getattr(request, "headers", {})
            api_key = headers.get("X-Api-Key")
            if not api_key:
                raise ApiKeyMissingException()

            # Local validation
            if endpoint_id is None:
                if api_key != ApiKeeConfig.local_key:
                    raise ApiKeyInvalidException()
            else:
                # Server validation (asynchronously)
                if not await ApiKeeConfig.validate_server_key(api_key, endpoint_id):
                    raise ApiKeyInvalidException()

            return await func(*args, **kwargs)
        return wrapper
    return decorator
