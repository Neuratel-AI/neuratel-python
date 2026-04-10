from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class CallListsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        return self._client._post("/lists", json=body)

    def list(self, *, skip: int = 0, limit: int = 20) -> Any:
        return self._client._get("/lists", params={"skip": skip, "limit": limit})

    def get(self, call_list_id: str) -> Any:
        return self._client._get(f"/lists/{call_list_id}")

    def update(self, call_list_id: str, **body: Any) -> Any:
        return self._client._put(f"/lists/{call_list_id}", json=body)

    def delete(self, call_list_id: str) -> None:
        self._client._delete(f"/lists/{call_list_id}")

    def bulk_import(self, call_list_id: str, file_path: str) -> Any:
        """Upload a CSV file to bulk import contacts. Pass the path to a CSV file."""
        with open(file_path, "rb") as f:
            response = self._client._http.request(
                "POST",
                f"/lists/{call_list_id}/bulk-import",
                files={"file": f},
            )
        from .._base_client import _raise_for_status

        _raise_for_status(response)
        return response.json()

    def add_contact(self, call_list_id: str, **body: Any) -> Any:
        return self._client._post(f"/lists/{call_list_id}/contacts", json=body)

    def list_contacts(self, call_list_id: str, *, skip: int = 0, limit: int = 50) -> Any:
        return self._client._get(
            f"/lists/{call_list_id}/contacts", params={"skip": skip, "limit": limit}
        )

    def update_contact(self, call_list_id: str, contact_id: str, **body: Any) -> Any:
        return self._client._put(f"/lists/{call_list_id}/contacts/{contact_id}", json=body)

    def delete_contact(self, call_list_id: str, contact_id: str) -> None:
        self._client._delete(f"/lists/{call_list_id}/contacts/{contact_id}")


class AsyncCallListsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        return await self._client._post("/lists", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20) -> Any:
        return await self._client._get("/lists", params={"skip": skip, "limit": limit})

    async def get(self, call_list_id: str) -> Any:
        return await self._client._get(f"/lists/{call_list_id}")

    async def update(self, call_list_id: str, **body: Any) -> Any:
        return await self._client._put(f"/lists/{call_list_id}", json=body)

    async def delete(self, call_list_id: str) -> None:
        await self._client._delete(f"/lists/{call_list_id}")

    async def bulk_import(self, call_list_id: str, file_path: str) -> Any:
        """Upload a CSV file to bulk import contacts."""
        with open(file_path, "rb") as f:
            response = await self._client._http.request(
                "POST",
                f"/lists/{call_list_id}/bulk-import",
                files={"file": f},
            )
        from .._base_client import _raise_for_status

        _raise_for_status(response)
        return response.json()

    async def add_contact(self, call_list_id: str, **body: Any) -> Any:
        return await self._client._post(f"/lists/{call_list_id}/contacts", json=body)

    async def list_contacts(self, call_list_id: str, *, skip: int = 0, limit: int = 50) -> Any:
        return await self._client._get(
            f"/lists/{call_list_id}/contacts", params={"skip": skip, "limit": limit}
        )

    async def update_contact(self, call_list_id: str, contact_id: str, **body: Any) -> Any:
        return await self._client._put(f"/lists/{call_list_id}/contacts/{contact_id}", json=body)

    async def delete_contact(self, call_list_id: str, contact_id: str) -> None:
        await self._client._delete(f"/lists/{call_list_id}/contacts/{contact_id}")
