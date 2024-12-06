class ApiKeyMissingException(Exception):
    """
    Raised when the API key is missing from the headers.
    """
    def __init__(self):
        super().__init__("Missing API key. Please include 'X-Api-Key' in headers.")

class ApiKeyInvalidException(Exception):
    """
    Raised when the API key is invalid.
    """
    def __init__(self):
        super().__init__("Invalid API key. Access denied.")
