from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class BillingResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def balance(self) -> Any:
        return self._client._get("/billing/balance")

    def usage(self, *, days: int = 30) -> Any:
        return self._client._get("/billing/usage", params={"days": days})

    def balance_history(self, *, skip: int = 0, limit: int = 20) -> Any:
        return self._client._get("/billing/balance/history", params={"skip": skip, "limit": limit})


class AsyncBillingResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def balance(self) -> Any:
        return await self._client._get("/billing/balance")

    async def usage(self, *, days: int = 30) -> Any:
        return await self._client._get("/billing/usage", params={"days": days})

    async def balance_history(self, *, skip: int = 0, limit: int = 20) -> Any:
        return await self._client._get(
            "/billing/balance/history", params={"skip": skip, "limit": limit}
        )
