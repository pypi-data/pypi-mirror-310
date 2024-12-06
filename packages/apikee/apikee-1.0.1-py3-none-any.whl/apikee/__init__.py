from fastapi.openapi.models import APIKey
from fastapi.openapi.models import SecurityRequirement, SecurityScheme
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Security, HTTPException, Depends
from .config import config

def get_openapi_schema(app: FastAPI):
    """
    Customize the OpenAPI schema to include the API key header.
    """
    if app.openapi_schema:
        return app.openapi_schema

    # Define the security schema for the API key
    security_scheme = SecurityScheme(
        type="apiKey",
        name="X-Api-Key",  # Header name
        in_="header",
        description="API key needed to access the endpoints"
    )
    app.openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema["components"]["securitySchemes"] = {"ApiKeyAuth": security_scheme}
    app.openapi_schema["security"] = [{"ApiKeyAuth": []}]
    return app.openapi_schema

def init_app(app: FastAPI):
    """
    Initialize the FastAPI application with ApiKee configurations.
    Automatically applies Swagger customization for API key header.
    """
    app.openapi = lambda: get_openapi_schema(app)
