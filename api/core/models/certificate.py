from pydantic import BaseModel


class CommonNameBodyRequest(BaseModel):
    subject: str
    alt_names: list[str] = []
