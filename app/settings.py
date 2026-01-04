"""Application settings."""

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Settings loaded from environment variables."""

    bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str | None = None

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
