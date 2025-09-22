from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application runtime configuration loaded from environment variables."""

    app_name: str = Field(default="Taiwan Stock Intelligence API", description="Display name for the service")
    history_window: int = Field(default=180, description="Number of days of historical data to fetch")
    news_limit: int = Field(default=8, description="Maximum number of news articles to return")
    enable_cache: bool = Field(default=True, description="Toggle in-memory caching of upstream responses")

    class Config:
        env_file = ".env"
        env_prefix = "TAIWAN_AGENT_"


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()
