from fastapi.responses import PlainTextResponse
from datetime import datetime
from core.config import settings
from fastapi import FastAPI

app = FastAPI(
    title="Cert Auth App",
    description="A FastAPI application for certificate Authority.",
    version="0.0.0",
)


# FRONTEND
app.frontend("/", directory=settings.NG_PATH, fallback="index.html")

#  STATIC FILES
# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")


@app.get("/info", response_class=PlainTextResponse)
def get_info():
    return f"""API SERVER RUNNING... FASTAPI {app.version}.
Server time: {datetime.now()} (isoformat: {datetime.now().isoformat() })
"""


@app.get("/health_check")
async def health_check():
    return True
