from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends
from icecream import ic
from pydantic_settings import BaseSettings, SettingsConfigDict

ic.configureOutput(includeContext=True)


# Application settings configuration
class PkiPaths(BaseSettings):
    ROOT: Path = Path(__file__).resolve().parents[2]

    MODE: Literal["development", "production"]
    PKI: Path = Path(__file__).resolve().parents[2] / "PKI"  #Path("/app/PKI")

    ROOT_CA: Path = PKI / "ca/root"
    INTERMEDIATE_CA: Path = PKI / "ca/intermediate"
    CLIENTS: Path = PKI / "issued/clients"
    SERVERS: Path = PKI / "issued/servers"

    ROOT_CRT: Path = ROOT_CA / "certs/root.crt"
    ROOT_KEY: Path = ROOT_CA / "private/root.key"
    ROOT_PASS: Path = ROOT_CA / "private/passphrase"

    INTERMEDIATE_CRT: Path = INTERMEDIATE_CA / "certs/intermediate-ca.crt"
    INTERMEDIATE_KEY: Path = INTERMEDIATE_CA / "private/intermediate-ca.key"
    INTERMEDIATE_PASS: Path = INTERMEDIATE_CA / "private/passphrase"

    CONFIGS_PATH: Path = ROOT / "configs"
    CONFIG_ROOT: Path = CONFIGS_PATH / "root-ca.cnf"
    CONFIG_INTERMEDIATE: Path = CONFIGS_PATH / "intermediate-ca.cnf"
    CONFIG_LEAF: Path = CONFIGS_PATH / "leaf-certificate.cnf"
    EXT_SERVER: Path = CONFIGS_PATH / "server.ext"
    EXT_CLIENT: Path = CONFIGS_PATH / "client.ext"

    model_config = SettingsConfigDict(env_file=".env", env_file_depth=1, extra="ignore")


# instance of the settings class to be used throughout the application
paths = PkiPaths()


# function to get the cached settings instance for dependency injection
@lru_cache
def get_settings() -> PkiPaths:
    """Get the cached paths instance."""
    ic("Getting cached settings instance", paths)
    return paths
