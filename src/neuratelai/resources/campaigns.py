from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class CampaignsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        return self._client._post("/campaigns", json=body)

    def list(self, *, skip: int = 0, limit: int = 20) -> SyncPage:
        data = self._client._get("/campaigns", params={"skip": skip, "limit": limit})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/campaigns",
            params={"skip": skip, "limit": limit},
        )

    def get(self, campaign_id: str) -> Any:
        return self._client._get(f"/campaigns/{campaign_id}")

    def update(self, campaign_id: str, **body: Any) -> Any:
        return self._client._put(f"/campaigns/{campaign_id}", json=body)

    def delete(self, campaign_id: str) -> None:
        self._client._delete(f"/campaigns/{campaign_id}")

    def start(self, campaign_id: str) -> Any:
        return self._client._post(f"/campaigns/{campaign_id}/start")

    def pause(self, campaign_id: str) -> Any:
        return self._client._post(f"/campaigns/{campaign_id}/pause")

    def stop(self, campaign_id: str) -> Any:
        return self._client._post(f"/campaigns/{campaign_id}/stop")

    def list_calls(self, *, campaign_id: str | None = None, **params: Any) -> Any:
        """List outbound call records. Filter by campaign_id for a specific campaign."""
        p = {**params}
        if campaign_id:
            p["campaign_id"] = campaign_id
        return self._client._get("/campaigns/calls", params=p or None)

    def get_call(self, call_id: str) -> Any:
        """Get a specific campaign outbound call record."""
        return self._client._get(f"/campaigns/calls/{call_id}")


class AsyncCampaignsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        return await self._client._post("/campaigns", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20) -> AsyncPage:
        data = await self._client._get("/campaigns", params={"skip": skip, "limit": limit})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/campaigns",
            params={"skip": skip, "limit": limit},
        )

    async def get(self, campaign_id: str) -> Any:
        return await self._client._get(f"/campaigns/{campaign_id}")

    async def update(self, campaign_id: str, **body: Any) -> Any:
        return await self._client._put(f"/campaigns/{campaign_id}", json=body)

    async def delete(self, campaign_id: str) -> None:
        await self._client._delete(f"/campaigns/{campaign_id}")

    async def start(self, campaign_id: str) -> Any:
        return await self._client._post(f"/campaigns/{campaign_id}/start")

    async def pause(self, campaign_id: str) -> Any:
        return await self._client._post(f"/campaigns/{campaign_id}/pause")

    async def stop(self, campaign_id: str) -> Any:
        return await self._client._post(f"/campaigns/{campaign_id}/stop")

    async def list_calls(self, *, campaign_id: str | None = None, **params: Any) -> Any:
        """List outbound call records. Filter by campaign_id for a specific campaign."""
        p = {**params}
        if campaign_id:
            p["campaign_id"] = campaign_id
        return await self._client._get("/campaigns/calls", params=p or None)

    async def get_call(self, call_id: str) -> Any:
        """Get a specific campaign outbound call record."""
        return await self._client._get(f"/campaigns/calls/{call_id}")
