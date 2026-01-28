
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8")

    GEMINI_API_KEY: str | None = None
    DATABASE_URL: str | None = None
    
    ENV: str = "dev"  # dev | prod
    ENABLE_DB: bool = False

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
