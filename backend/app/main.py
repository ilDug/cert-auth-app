from core.config import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Cert Auth App",
    description="A FastAPI application for certificate Authority.",
    version="0.0.0",
)


# FRONTEND
app.frontend("/", directory=settings.NG_PATH, fallback="index.html")


#  STATIC FILES
# app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="static_media")
