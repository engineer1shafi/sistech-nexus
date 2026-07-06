from fastapi import FastAPI

app = FastAPI(
    title="SISTECH NEXUS",
    version="0.0.1-dev",
    description="Enterprise Network Operations Platform",
)


@app.get("/")
async def root() -> dict:
    return {
        "name": "SISTECH NEXUS",
        "version": "0.0.1-dev",
        "status": "running",
    }


@app.get("/health")
async def health() -> dict:
    return {
        "status": "healthy",
        "service": "sistech-nexus-api",
    }