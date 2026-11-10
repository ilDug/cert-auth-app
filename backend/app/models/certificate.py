from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommonNameBodyRequest(BaseModel):
    subject: str
    alt_names: list[str] = []
    days: int = 1825


class Certificate(BaseModel):
    status: str
    exp_date: datetime
    revoke_date: datetime | None = None
    serial: str
    filename_unknown: str
    common_name: str


class RootPackage(BaseModel):
    crt: str
    key: str
    passphrase: str
