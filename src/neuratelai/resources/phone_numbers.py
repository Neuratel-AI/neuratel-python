from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class PhoneNumbersResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        data = self._client._get("/numbers", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/numbers",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, phone_number_id: str) -> Any:
        return self._client._get(f"/numbers/{phone_number_id}")

    def update(self, phone_number_id: str, **body: Any) -> Any:
        return self._client._put(f"/numbers/{phone_number_id}", json=body)

    def assign(self, phone_number_id: str, *, agent_id: str) -> Any:
        return self._client._post(f"/numbers/{phone_number_id}/assign", json={"agent_id": agent_id})

    def unassign(self, phone_number_id: str) -> Any:
        return self._client._post(f"/numbers/{phone_number_id}/unassign")


class AsyncPhoneNumbersResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        data = await self._client._get("/numbers", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/numbers",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, phone_number_id: str) -> Any:
        return await self._client._get(f"/numbers/{phone_number_id}")

    async def update(self, phone_number_id: str, **body: Any) -> Any:
        return await self._client._put(f"/numbers/{phone_number_id}", json=body)

    async def assign(self, phone_number_id: str, *, agent_id: str) -> Any:
        return await self._client._post(
            f"/numbers/{phone_number_id}/assign", json={"agent_id": agent_id}
        )

    async def unassign(self, phone_number_id: str) -> Any:
        return await self._client._post(f"/numbers/{phone_number_id}/unassign")
