from fastapi import FastAPI
from loguru import logger

from app.api.database import router as database_router
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logger import setup_logger
from app.api.auth import router as auth_router
from app.api.device import router as device_router

setup_logger()
logger.info("SISTECH NEXUS starting...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Network Operations Platform",
)

app.include_router(health_router)
app.include_router(database_router)
app.include_router(auth_router)
app.include_router(device_router)


@app.get("/")
async def root() -> dict:
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }