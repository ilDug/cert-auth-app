from fastapi import APIRouter
from controllers import Eraser
from core.config import AppConfig

router = APIRouter(tags=["erase"])


@router.delete("/erase/certificate/{subject}")
async def erase_certificate(subject: str, cnf: AppConfig):
    e = Eraser(cnf)
    return e.certificate(subject)
