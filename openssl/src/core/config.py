from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends
from icecream import ic
from pydantic_settings import BaseSettings, SettingsConfigDict

ic.configureOutput(includeContext=True)


# Application settings configuration
class Settings(BaseSettings):
    MODE: Literal["development", "production"]
    ROOT: Path = Path(__file__).resolve().parents[2]
    FRONTEND_PATH: Path = ROOT / "browser"
    SECURITY_TOKEN: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_depth=1, extra="ignore")


# instance of the settings class to be used throughout the application
settings = Settings()


# function to get the cached settings instance for dependency injection
@lru_cache
def get_settings() -> Settings:
    """Get the cached settings instance."""
    ic("Getting cached settings instance", settings)
    return settings


# type alias for the application configuration dependency injection
# this allows us to use AppConfig as a dependency in FastAPI routes
AppConfig = Annotated[Settings, Depends(get_settings)]


# CORS
###############################
CORS = {
    "allow_credentials": True,
    "allow_origins": [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://ca.ek.lan",
    ],
    "allow_methods": ["OPTIONS", "POST", "PUT", "GET", "DELETE"],
    "expose_headers": [
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "X-Auth-Token",
        "Authorization",
        "X-Dag-Head",
        # "Access-Control-Expose-Headers"
    ],
    "allow_headers": [
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "Accept",
        "Authorization",
        # "Access-Control-Expose-Headers"
    ],
}
