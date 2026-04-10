from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class WebhooksResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def events(self) -> Any:
        """List all available webhook event types."""
        return self._client._get("/webhooks/events")

    def create(self, **body: Any) -> Any:
        return self._client._post("/webhooks", json=body)

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        data = self._client._get("/webhooks", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/webhooks",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, webhook_id: str) -> Any:
        return self._client._get(f"/webhooks/{webhook_id}")

    def update(self, webhook_id: str, **body: Any) -> Any:
        return self._client._patch(f"/webhooks/{webhook_id}", json=body)

    def delete(self, webhook_id: str) -> None:
        self._client._delete(f"/webhooks/{webhook_id}")

    def test(self, webhook_id: str, **body: Any) -> Any:
        return self._client._post(f"/webhooks/{webhook_id}/test", json=body)

    def rotate_secret(self, webhook_id: str) -> Any:
        return self._client._post(f"/webhooks/{webhook_id}/secret/rotate")

    def logs(self, webhook_id: str, *, skip: int = 0, limit: int = 20, **params: Any) -> Any:
        return self._client._get(
            f"/webhooks/{webhook_id}/logs", params={"skip": skip, "limit": limit, **params}
        )


class AsyncWebhooksResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def events(self) -> Any:
        """List all available webhook event types."""
        return await self._client._get("/webhooks/events")

    async def create(self, **body: Any) -> Any:
        return await self._client._post("/webhooks", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        data = await self._client._get("/webhooks", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/webhooks",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, webhook_id: str) -> Any:
        return await self._client._get(f"/webhooks/{webhook_id}")

    async def update(self, webhook_id: str, **body: Any) -> Any:
        return await self._client._patch(f"/webhooks/{webhook_id}", json=body)

    async def delete(self, webhook_id: str) -> None:
        await self._client._delete(f"/webhooks/{webhook_id}")

    async def test(self, webhook_id: str, **body: Any) -> Any:
        return await self._client._post(f"/webhooks/{webhook_id}/test", json=body)

    async def rotate_secret(self, webhook_id: str) -> Any:
        return await self._client._post(f"/webhooks/{webhook_id}/secret/rotate")

    async def logs(self, webhook_id: str, *, skip: int = 0, limit: int = 20, **params: Any) -> Any:
        return await self._client._get(
            f"/webhooks/{webhook_id}/logs", params={"skip": skip, "limit": limit, **params}
        )
