from fastapi import HTTPException, Request
from functools import wraps
from .config import config
from .server_client import validate_with_server

def apikey(endpoint_id: str = None):
    """
    Decorator for API key validation. 
    - If `endpoint_id` is provided, server validation is used.
    - If `endpoint_id` is not provided, local validation is used.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            api_key = request.headers.get("X-Api-Key")
            if not api_key:
                raise HTTPException(status_code=403, detail="API key missing")

            if endpoint_id:  # Server validation
                is_valid, message = await validate_with_server(api_key, endpoint_id)
                if not is_valid:
                    raise HTTPException(status_code=403, detail=message)
            else:  # Local validation
                if not config.local_key or api_key != config.local_key:
                    raise HTTPException(status_code=403, detail="Invalid API key")
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
