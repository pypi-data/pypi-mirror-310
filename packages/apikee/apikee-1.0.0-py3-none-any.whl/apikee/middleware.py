from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from .config import config

class SwaggerProtectedMiddleware(BaseHTTPMiddleware):
    """
    Middleware to protect Swagger and Redoc documentation endpoints.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            api_key = request.headers.get("X-Api-Key")
            if not api_key or api_key != config.local_key:
                raise HTTPException(status_code=403, detail="Access to documentation is restricted")
        return await call_next(request)
