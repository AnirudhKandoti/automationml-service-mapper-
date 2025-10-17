
import os
from pydantic import BaseModel

class Settings(BaseModel):
    api_key: str = os.getenv("API_KEY", "dev-key")
    policy_default: str = os.getenv("DEFAULT_POLICY", "public")

settings = Settings()
