from fastapi import APIRouter, Body, Path, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from controllers import Generator, Certificate
from core import CommonNameBodyRequest
from config import CERTS_PATH, KEYS_PATH, PUBLIC_PATH
import subprocess

router = APIRouter(tags=["display"])


@router.get("/display/certificate/pem/{subject}")
async def display_certificate_pem(subject: str = Path):
    c = Certificate()
    pem = c.cert(subject, pem=True)
    return PlainTextResponse(pem)


@router.get("/display/certificate/info/{subject}")
async def display_certificate_info(subject: str = Path):
    c = Certificate()
    info = c.cert(subject, pem=False)
    return PlainTextResponse(info)


@router.get("/display/certificate/file/{subject}")
async def display_certificate_file(subject: str = Path):
    file = CERTS_PATH / f"{subject}.crt"
    if not file.exists():
        raise HTTPException(404, "certificato inesistente")
    return FileResponse(file, media_type="plain/text", filename=f"{subject}.crt")


@router.get("/display/privatekey/info/{subject}")
async def display_privatekey_info(subject: str = Path):
    c = Certificate()
    info = c.priv_key(subject, pem=False)
    return PlainTextResponse(info)


@router.get("/display/privatekey/pem/{subject}")
async def display_privatekey_pem(subject: str = Path):
    c = Certificate()
    info = c.priv_key(subject, pem=True)
    return PlainTextResponse(info)


@router.get("/display/privatekey/file/{subject}")
async def display_privatekey_file(subject: str = Path):
    file = KEYS_PATH / f"{subject}.key"
    if not file.exists():
        raise HTTPException(404, "key inesistente")
    return FileResponse(file, media_type="plain/text", filename=f"{subject}.key")


@router.get("/display/publickey/pem/{subject}")
async def display_publickey_pem(subject: str = Path):
    c = Certificate()
    info = c.pub_key(subject)
    return PlainTextResponse(info)


@router.get("/display/publickey/file/{subject}")
async def display_publickey_file(subject: str = Path):
    file = PUBLIC_PATH / f"{subject}.pub.pem"
    if not file.exists():
        raise HTTPException(404, "chiave pubblica inesistente")
    return FileResponse(file, media_type="plain/text", filename=f"{subject}.pub.pem")
