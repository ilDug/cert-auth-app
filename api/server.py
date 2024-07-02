from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from core.middlewares import (
    cors_mw_config,
    pki_middleware,
    validation_exception_handler,
    http_rewrite_header_handler,
)
from core.install import install
from core.utils.version import fastapi_version
from routers import display_router, generate_router, pki_utils_router

from icecream import ic

ic.configureOutput(includeContext=True)


# MAIN FASTAPI APP
app = FastAPI(root_path="/api")


# MIDDLEWARE
app.add_middleware(CORSMiddleware, **cors_mw_config)


@app.middleware("http")
async def check_pki(request: Request, call_next):
    """controlla che sia istanziata una pki"""
    if not pki_middleware():
        # return JSONResponse("nessuna PKI instanziata", status_code=500)
        ic("PKI directory creation...")
        install()
    response = await call_next(request)
    return response


#  EXCEPTION HANDLERS
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_rewrite_header_handler)


# ROUTERS
app.include_router(display_router)
app.include_router(generate_router)
app.include_router(pki_utils_router)

#  STATIC FILES
# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


# MAIN ROUTE
@app.get("/", response_class=PlainTextResponse)
async def root():
    return f"""API SERVER RUNNING... FASTAPI {fastapi_version()}.
Server time: {datetime.now()} (isoformat: {datetime.now().isoformat() })
"""
