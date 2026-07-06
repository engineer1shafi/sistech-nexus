from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

router = APIRouter(tags=["Database"])


@router.get("/database")
async def database_status(db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(text("SELECT version()"))
    db_version = result.scalar()

    return {
        "status": "connected",
        "database": "PostgreSQL",
        "driver": "SQLAlchemy Async",
        "version": db_version,
    }