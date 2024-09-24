from fastapi import Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError

from icecream import ic

ic.configureOutput(prefix="DAG - ")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """cattura tutti gli errori di validazione di pydantic"""
    ic("catch DAG PYDANTIC ERROR...")
    errors = [f"{e['msg']} - {e['type']}: {' '.join(e['loc'])}" for e in exc.errors()]

    return JSONResponse(
        content=jsonable_encoder({"error": errors[0]}),
        status_code=400,
        headers={"X-Error": errors[0]},
    )


async def http_rewrite_header_handler(req: Request, exc: HTTPException):
    """Cattura tutti gli errori per poi poterli restituire come status code nella Response del server"""
    ic("catch DAG HTTP ERROR...")

    return JSONResponse(
        content=jsonable_encoder({"error": exc.detail}),
        status_code=exc.status_code,
        headers={"X-Error": str(exc.detail)},
    )
