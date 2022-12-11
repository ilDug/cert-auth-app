from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from core.middlewares import (
    req_validation_error_handler,
    dag_http_error_handler,
    pki_middleware,
)
from core.install import install
import logging

from routers import generate_router

app = FastAPI(root_path="/api")
# app = FastAPI(root_path="/")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://app3.eurokemical.lan",
    ],
    allow_methods=["OPTIONS", "POST", "PUT", "GET", "DELETE"],
    expose_headers=[
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "X-Auth-Token",
        "Authorization",
    ],
    allow_headers=[
        "Origin",
        "Content-Type",
        "Set-Cookie",
        "X-Error",
        "Accept",
        "Authorization",
    ],
    # allow_headers=["*"],)
)


@app.middleware("http")
async def check_pki(request: Request, call_next):
    """controlla che sia istanziata una pki"""
    if not pki_middleware():
        # return JSONResponse("nessuna PKI instanziata", status_code=500)
        print("PKI directory creation...")
        install()
    response = await call_next(request)
    return response


app.add_exception_handler(RequestValidationError, req_validation_error_handler)
app.add_exception_handler(HTTPException, dag_http_error_handler)
# app.add_exception_handler(PyMongoError, mongo_error_handler)

app.include_router(generate_router)

# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


@app.get("/", response_class=PlainTextResponse)
async def root():
    now = datetime.now()
    # now = datetime.isoformat(datetime.now())
    return f"API SERVER RUNNING... FAST. Server time: {now} (isoformat: {datetime.isoformat(now)})"
