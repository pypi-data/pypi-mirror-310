from .config import config
from .decorators import apikey
from .middleware import SwaggerProtectedMiddleware

def init_app(app):
    """
    Initialize the FastAPI application with ApiKee configurations.
    This automatically adds middleware to protect Swagger endpoints.
    """
    app.add_middleware(SwaggerProtectedMiddleware)
