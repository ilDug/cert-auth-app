from fastapi import APIRouter
from controllers import Eraser


router = APIRouter(tags=["erase"])


@router.delete("/erase/certificate/{subject}")
async def erase_certificate(subject: str):
    e = Eraser()
    return e.certificate(subject)
