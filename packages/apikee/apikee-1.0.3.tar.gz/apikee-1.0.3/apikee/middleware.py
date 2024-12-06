from functools import wraps
from .settings import ApiKeeConfig
from .exceptions import ApiKeyMissingException, ApiKeyInvalidException

def apikey(endpoint_id: str = None):
    """
    Decorator to validate API keys for any Python API framework.
    :param endpoint_id: Optional endpoint ID for server-based validation.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract API key from headers or context (generic logic)
            request = kwargs.get("request") or (args[0] if args else None)
            if not request:
                raise ValueError("Request object not provided for API key validation.")

            # Extract API key based on the request framework
            api_key = getattr(request, "headers", {}).get("X-Api-Key")
            if not api_key:
                raise ApiKeyMissingException("API key is missing in the request.")

            # Local validation
            if endpoint_id is None:
                if api_key != ApiKeeConfig.local_key:
                    raise ApiKeyInvalidException("Invalid API key provided.")
            else:
                # Server-based validation
                if not ApiKeeConfig.validate_server_key(api_key, endpoint_id):
                    raise ApiKeyInvalidException("Server-based API key validation failed.")

            # If validation passes, proceed to the actual function
            return func(*args, **kwargs)

        return wrapper
    return decorator
