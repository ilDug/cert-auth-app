from fastapi.responses import PlainTextResponse
import fastapi
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.config import CORS, settings, AppConfig
from core.pki_middleware import pki_middleware
from core.install import install
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from core.exception_handlers import (
    validation_exception_handler,
    http_rewrite_header_handler,
)
from routers import display_router, generate_router, pki_utils_router, erase_router

from icecream import ic

ic.configureOutput(includeContext=True)

app = FastAPI(
    title="Cert Auth App",
    description="A FastAPI application for certificate Authority.",
    version="0.0.0",
)


# MIDDLEWARE
app.add_middleware(CORSMiddleware, **CORS)


@app.middleware("http")
async def check_pki(request: Request, call_next):
    """controlla che sia istanziata una pki"""
    if not pki_middleware(settings.PKI_PATH):
        ic("PKI directory creation...")
        install()
    response = await call_next(request)
    return response


# EXCEPTION HANDLERS
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_rewrite_header_handler)
# app.add_exception_handler(PyMongoError, mongo_error_handler)

# ROUTERS
app.include_router(display_router)
app.include_router(generate_router)
app.include_router(pki_utils_router)
app.include_router(erase_router)


# FRONTEND
app.frontend("/", directory=settings.NG_PATH, fallback="index.html")

#  STATIC FILES
# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


@app.get("/info", response_class=PlainTextResponse)
def get_info():
    return f"""API SERVER RUNNING... FASTAPI {fastapi.__version__}
App version: {app.version}.
Server time: {datetime.now()} (isoformat: {datetime.now().isoformat() })
"""


@app.get("/health_check")
async def health_check():
    return True
