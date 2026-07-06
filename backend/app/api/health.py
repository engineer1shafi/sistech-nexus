from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():

    return {
        "status": "healthy",
        "application": "SISTECH NEXUS",
        "database": "configured",
        "version": "0.0.3-dev",
    }