from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    app_name: str = Field(default="FastAPI Template", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Single module-level instance — import this everywhere
settings = Settings()
