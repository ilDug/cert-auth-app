from typing import Annotated
from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from controllers import CertificateController, PKIController
from core.config import CERTS_PATH, KEYS_PATH, PUBLIC_PATH

router = APIRouter(tags=["display"])


@router.get("/certificates")
async def certs_list():
    c = PKIController()
    return c.list_certificates()


@router.get("/keys")
async def certs_list():
    c = PKIController()
    return c.list_keys()


@router.get("/display/certificate/pem/{subject}")
async def display_certificate_pem(subject: Annotated[str, Path()]):
    c = CertificateController()
    pem = c.cert(subject, pem=True)
    return PlainTextResponse(pem)


@router.get("/display/certificate/info/{subject}")
async def display_certificate_info(subject: Annotated[str, Path()]):
    c = CertificateController()
    info = c.cert(subject, pem=False)
    return PlainTextResponse(info)


@router.get("/display/certificate/file/{subject}")
async def display_certificate_file(subject: Annotated[str, Path()]):
    file = CERTS_PATH / f"{subject}.crt"
    if not file.exists():
        raise HTTPException(404, "certificato inesistente")
    return FileResponse(file, media_type="plain/text", filename=f"{subject}.crt")


@router.get("/display/privatekey/info/{subject}")
async def display_privatekey_info(subject: Annotated[str, Path()]):
    c = CertificateController()
    info = c.priv_key(subject, pem=False)
    return PlainTextResponse(info)


@router.get("/display/privatekey/pem/{subject}")
async def display_privatekey_pem(subject: Annotated[str, Path()]):
    c = CertificateController()
    info = c.priv_key(subject, pem=True)
    return PlainTextResponse(info)


@router.get("/display/privatekey/file/{subject}")
async def display_privatekey_file(subject: Annotated[str, Path()]):
    file = KEYS_PATH / f"{subject}.key"
    if not file.exists():
        raise HTTPException(404, "key inesistente")
    return FileResponse(file, media_type="plain/text", filename=f"{subject}.key")


@router.get("/display/publickey/pem/{subject}")
async def display_publickey_pem(subject: Annotated[str, Path()]):
    c = CertificateController()
    info = c.pub_key(subject)
    return PlainTextResponse(info)


@router.get("/display/publickey/file/{subject}")
async def display_publickey_file(subject: Annotated[str, Path()]):
    file = PUBLIC_PATH / f"{subject}.pub.pem"
    if not file.exists():
        raise HTTPException(404, "chiave pubblica inesistente")
    return FileResponse(file, media_type="plain/text", filename=f"{subject}.pub.pem")
