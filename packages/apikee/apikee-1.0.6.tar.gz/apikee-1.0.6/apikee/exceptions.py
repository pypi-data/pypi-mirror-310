class ApiKeyMissingException(Exception):
    """
    Raised when the API key is missing from the headers.
    """
    def __init__(self):
        self.status_code = 401
        self.detail = "Missing API key. Please include 'X-Api-Key' in headers."
        super().__init__(self.detail)


class ApiKeyInvalidException(Exception):
    """
    Raised when the API key is invalid.
    """
    def __init__(self):
        self.status_code = 401
        self.detail = "Invalid API key. Access denied."
        super().__init__(self.detail)


class ServerValidationException(Exception):
    """
    Raised when the server validation fails.
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.detail = message
        super().__init__(self.detail)


class ServerConnectionException(Exception):
    """
    Raised when there is an error connecting to the validation server.
    """
    def __init__(self, message: str):
        self.status_code = 500
        self.detail = f"Error contacting the server: {message}"
        super().__init__(self.detail)
