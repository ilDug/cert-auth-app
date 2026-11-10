from pathlib import Path
from typing import Annotated, Literal
from fastapi import Depends
from functools import lru_cache
from icecream import ic
from pydantic_settings import BaseSettings


ic.configureOutput(includeContext=True)


# Application settings configuration
class Settings(BaseSettings):
    MODE: Literal["PRODUCTION", "DEVELOPMENT"] = "PRODUCTION"
    ROOT: Path = Path(__file__).resolve().parents[2]
    LIB: Path = ROOT / "lib"
    NG_PATH: Path = ROOT / "browser"
    PKI: Path = Path("/PKI")

    PKI_DB: Path = PKI / "index.txt"
    KEYS_PATH: Path = PKI / "private"
    REQS_PATH: Path = PKI / "reqs"
    CONFIGS_PATH: Path = PKI / "configs"
    CERTS_PATH: Path = PKI / "certs"
    PASSPRHASE_PATH: Path = PKI / "private/_passphrase"
    PUBLIC_PATH: Path = PKI / "public"

    CONFIG_FILE: Path = CONFIGS_PATH / "openssl.cnf"
    CA_CRT_PATH: Path = CERTS_PATH / "ca.crt"
    CA_KEY_PATH: Path = KEYS_PATH / "ca.key"
    CA_PUB_PATH: Path = PUBLIC_PATH / "ca.pub.pem"
    CA_DURATION: int = 365

    CNF_BASE_DEFAULT: Path = LIB / "openssl/default.cnf"
    CNF_BASE_OPENSSL: Path = LIB / "openssl/openssl.cnf"


# instance of the settings class to be used throughout the application
settings = Settings()


# function to get the cached settings instance for dependency injection
@lru_cache
def get_settings() -> Settings:
    """Get the cached settings instance."""
    ic("Getting cached settings instance")
    return settings


# type alias for the application configuration dependency injection
# this allows us to use AppConfig as a dependency in FastAPI routes
AppConfig = Annotated[Settings, Depends(get_settings)]
