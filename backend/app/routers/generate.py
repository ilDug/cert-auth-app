from typing import Annotated

from controllers import CertificateController, Generator
from core.config import AppConfig
from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse
from models import CommonNameBodyRequest

router = APIRouter(tags=["generate"])


@router.post("/generate/certificate")
async def generate_certificate(
    body: Annotated[CommonNameBodyRequest, Body(...)], cnf: AppConfig
):
    g = Generator(cnf)
    g.priv_key(body.subject)
    g.request(body.subject, body.alt_names)
    g.certificate(body.subject, body.alt_names, body.days)

    c = CertificateController(cnf)
    info = c.cert(body.subject, pem=False)
    return PlainTextResponse(info)
