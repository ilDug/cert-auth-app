from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from icecream import ic
from pymongo.errors import PyMongoError

ic.configureOutput(includeContext=True)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Cattura e restituisce gli errori di validazione di Pydantic."""
    ic("catch DAG PYDANTIC ERROR...", str(exc), str(request.url.path))
    errors = [
        f"{e['msg']} - {e['type']}: {' '.join(map(str, e['loc']))}"
        for e in exc.errors()
    ]
    message = errors[0] if errors else str(exc)

    return JSONResponse(
        content=jsonable_encoder({"error": message}),
        status_code=400,
        headers={"X-Error": message},
    )


async def http_rewrite_header_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Cattura tutti gli HTTPException e le restituisce come risposta JSON."""
    ic(
        "catch DAG HTTP ERROR...",
        exc.status_code,
        exc.detail,
        str(exc),
        str(request.url.path),
    )

    return JSONResponse(
        content=jsonable_encoder({"error": exc.detail}),
        status_code=exc.status_code,
        headers={"X-Error": str(exc.detail)},
    )


async def mongo_error_handler(request: Request, exc: PyMongoError) -> PlainTextResponse:
    """Gestisce errori generici di PyMongo restituendo un 500 testuale."""
    ic("catch MONGO ERROR (by DAG):", str(exc), str(request.url.path))

    return PlainTextResponse(
        content=str(exc), status_code=500, headers={"X-Error": str(exc)}
    )
