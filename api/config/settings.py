"""
Settings for the API
"""

from typing import Optional
from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Main application settings using Pydantic for validation and type safety.
    Values are automatically loaded from .env file
    """
    environment: str

    database_url: str
    # Individual DB components (for Docker compose)
    database_host: Optional[str]
    database_port: Optional[int]
    database_name: Optional[str]
    database_user: Optional[str]
    database_password: Optional[str]

    # Redis settings
    redis_url: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of settings.
    """
    return Settings()

settings = get_settings()

    