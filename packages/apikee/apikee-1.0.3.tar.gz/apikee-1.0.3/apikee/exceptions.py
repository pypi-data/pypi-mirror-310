class ApiKeyMissingException(Exception):
    """Raised when the API key is missing in the request."""
    pass

class ApiKeyInvalidException(Exception):
    """Raised when the API key provided is invalid."""
    pass
