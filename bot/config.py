from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables / .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: SecretStr
    log_level: str = "INFO"

    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str | None = None
    ollama_timeout: float = 120.0

    @property
    def llm_enabled(self) -> bool:
        return bool(self.ollama_model)


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
