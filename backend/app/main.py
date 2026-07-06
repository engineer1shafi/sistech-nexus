from fastapi import FastAPI

from app.api.health import router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(router)


@app.get("/")
async def root():

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }