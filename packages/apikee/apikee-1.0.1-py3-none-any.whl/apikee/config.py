from typing import Optional

class ApiKeeConfig:
    def __init__(self, local_key: Optional[str] = None, server_key: Optional[str] = None,
                 server_url: Optional[str] = None, project_id: Optional[str] = None, environment: Optional[str] = None):
        self.local_key = local_key
        self.server_key = server_key
        self.server_url = server_url
        self.project_id = project_id
        self.environment = environment

# Global configuration instance
config = ApiKeeConfig()
