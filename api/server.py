from datetime import datetime
from fastapi import FastAPI


from fastapi.responses import PlainTextResponse
from icecream import ic

ic.configureOutput(includeContext=True)


# MAIN FASTAPI APP
app = FastAPI(root_path="/api")

# MIDDLEWARE
# app.add_middleware(CORSMiddleware, **cors_mw_config)


#  EXCEPTION HANDLERS
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(HTTPException, http_rewrite_header_handler)


# ROUTERS


#  STATIC FILES
# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


# MAIN ROUTE
@app.get("/", response_class=PlainTextResponse)
async def root():
    return f"""API SERVER RUNNING... FASTAPI {fastapi_version()}.
Server time: {datetime.now()} (isoformat: {datetime.now().isoformat() })
"""
