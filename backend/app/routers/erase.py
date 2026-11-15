from controllers import Eraser
from core.config import AppConfig
from fastapi import APIRouter

router = APIRouter(tags=["erase"])


@router.delete("/erase/certificate/{subject}")
async def erase_certificate(subject: str, cnf: AppConfig):
    e = Eraser(cnf)
    return e.certificate(subject)
