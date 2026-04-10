from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class APIKeysResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        """Create an organization API key. Returns key + secret (shown once)."""
        return self._client._post("/api-keys", json=body)

    def list(self, *, include_revoked: bool = False) -> Any:
        return self._client._get("/api-keys", params={"include_revoked": include_revoked})

    def revoke(self, key_id: str) -> Any:
        """Immediately invalidate an API key."""
        return self._client._delete(f"/api-keys/{key_id}")

    def rotate(self, key_id: str, *, grace_period_hours: int = 24) -> Any:
        """Replace a key — old key stays valid for grace_period_hours (1-168)."""
        return self._client._post(
            f"/api-keys/{key_id}/rotate",
            params={"grace_period_hours": grace_period_hours},
        )

    def scopes(self) -> Any:
        """List all available scopes and preset bundles."""
        return self._client._get("/api-keys/scopes")


class AsyncAPIKeysResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        return await self._client._post("/api-keys", json=body)

    async def list(self, *, include_revoked: bool = False) -> Any:
        return await self._client._get("/api-keys", params={"include_revoked": include_revoked})

    async def revoke(self, key_id: str) -> Any:
        return await self._client._delete(f"/api-keys/{key_id}")

    async def rotate(self, key_id: str, *, grace_period_hours: int = 24) -> Any:
        return await self._client._post(
            f"/api-keys/{key_id}/rotate",
            params={"grace_period_hours": grace_period_hours},
        )

    async def scopes(self) -> Any:
        return await self._client._get("/api-keys/scopes")
