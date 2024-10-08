from typing import Annotated
from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse
from controllers import Generator, CertificateController
from core.models import CommonNameBodyRequest


router = APIRouter(tags=["generate"])


@router.post("/generate/certificate")
async def generate_certificate(body: Annotated[CommonNameBodyRequest, Body(...)]):
    g = Generator()
    g.priv_key(body.subject)
    g.request(body.subject, body.alt_names)
    g.certificate(body.subject, body.alt_names, body.days)

    c = CertificateController()
    info = c.cert(body.subject, pem=False)
    return PlainTextResponse(info)
