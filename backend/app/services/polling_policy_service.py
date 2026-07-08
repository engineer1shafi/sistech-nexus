from __future__ import annotations

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.polling_policy_repository import PollingPolicyRepository


class PollingPolicyService:
    def __init__(self, db: AsyncSession):
        self.repo = PollingPolicyRepository(db)

    async def list_policies(self) -> list[Any]:
        return await self.repo.list_all()

    async def create_policy(self, payload: dict) -> Any:
        return await self.repo.create(payload)
