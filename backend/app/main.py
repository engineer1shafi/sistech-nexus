from fastapi import FastAPI
from loguru import logger

from app.api.database import router as database_router
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logger import setup_logger
from app.api.auth import router as auth_router
from app.api.device import router as device_router
from app.api.snmp import router as snmp_router
from app.api.topology import router as topology_router
from app.api.polling_policy import router as polling_policy_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.interface import router as interface_router


setup_logger()
logger.info("SISTECH NEXUS starting...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Network Operations Platform",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(database_router)
app.include_router(auth_router)
app.include_router(device_router)
app.include_router(snmp_router)
app.include_router(interface_router)
app.include_router(topology_router)
app.include_router(polling_policy_router)



@app.get("/")
async def root() -> dict:
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }