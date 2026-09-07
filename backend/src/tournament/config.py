"""Application configuration.

Config comes from the environment (12-factor). The one rule that matters for AWS:
``AWS_ENDPOINT_URL`` is **set** locally so boto3 talks to Floci, and **unset** in real
AWS so boto3 resolves the genuine service endpoints. Same code, both targets.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["local", "ci", "staging", "production"] = "local"
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://tournament:tournament@localhost:5432/tournament"

    # None => real AWS. Set to http://localhost:4566 (or http://floci:4566) for Floci.
    aws_endpoint_url: str | None = None
    aws_default_region: str = "us-east-1"

    cors_origins: list[str] = ["http://localhost:5173"]

    @property
    def is_local(self) -> bool:
        return self.environment == "local"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton. Call ``get_settings.cache_clear()`` in tests."""
    return Settings()
