from fastapi import FastAPI, Security
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader

# Define the API key header
api_key_header = APIKeyHeader(name="X-Api-Key", auto_error=False)

def get_openapi_schema(app: FastAPI):
    """
    Customize the OpenAPI schema to include the API key header.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add the security schema to OpenAPI
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "X-Api-Key",
            "in": "header",
        }
    }

    # Apply the security scheme globally
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def init_app(app: FastAPI):
    """
    Initialize the FastAPI application with ApiKee configurations.
    Automatically applies Swagger customization for API key header.
    """
    app.openapi = lambda: get_openapi_schema(app)
