from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM Provider configuration
    llm_provider: str | None = None  # openai, anthropic, google, ollama
    
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-haiku-20240307"
    google_api_key: str | None = None
    google_model: str = "gemini-1.5-flash"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    model_config = SettingsConfigDict(
        env_prefix="", 
        env_file=(".env",),
        extra="ignore",
        case_sensitive=False,
        env_file_encoding="utf-8"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
