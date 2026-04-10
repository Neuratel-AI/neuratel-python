from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class CallsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        data = self._client._get("/calls", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/calls",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, call_id: str, *, include: str | None = None) -> Any:
        params = {"include": include} if include else None
        return self._client._get(f"/calls/{call_id}", params=params)

    def delete(
        self, call_id: str, *, delete_recording: bool = False, delete_transcript: bool = False
    ) -> None:
        params: dict[str, bool] = {}
        if delete_recording:
            params["delete_recording"] = True
        if delete_transcript:
            params["delete_transcript"] = True
        self._client._request(
            "DELETE", f"/calls/{call_id}", params=params or None, expect_body=False
        )

    def outbound(self, **body: Any) -> Any:
        """Place a single outbound call. POST /v1/calls/outbound"""
        return self._client._post("/calls/outbound", json=body)

    def active(self) -> Any:
        return self._client._get("/calls/active")

    def concurrency(self) -> Any:
        return self._client._get("/calls/concurrency")

    def hangup(self, call_id: str) -> Any:
        return self._client._post(f"/calls/{call_id}/hangup")

    def listen(self, call_id: str) -> Any:
        return self._client._post(f"/calls/{call_id}/listen")

    def whisper(self, call_id: str) -> Any:
        return self._client._post(f"/calls/{call_id}/whisper")

    def barge(self, call_id: str) -> Any:
        return self._client._post(f"/calls/{call_id}/barge")


class AsyncCallsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        data = await self._client._get("/calls", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/calls",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, call_id: str, *, include: str | None = None) -> Any:
        params = {"include": include} if include else None
        return await self._client._get(f"/calls/{call_id}", params=params)

    async def delete(
        self, call_id: str, *, delete_recording: bool = False, delete_transcript: bool = False
    ) -> None:
        params: dict[str, bool] = {}
        if delete_recording:
            params["delete_recording"] = True
        if delete_transcript:
            params["delete_transcript"] = True
        await self._client._request(
            "DELETE", f"/calls/{call_id}", params=params or None, expect_body=False
        )

    async def outbound(self, **body: Any) -> Any:
        return await self._client._post("/calls/outbound", json=body)

    async def active(self) -> Any:
        return await self._client._get("/calls/active")

    async def concurrency(self) -> Any:
        return await self._client._get("/calls/concurrency")

    async def hangup(self, call_id: str) -> Any:
        return await self._client._post(f"/calls/{call_id}/hangup")

    async def listen(self, call_id: str) -> Any:
        return await self._client._post(f"/calls/{call_id}/listen")

    async def whisper(self, call_id: str) -> Any:
        return await self._client._post(f"/calls/{call_id}/whisper")

    async def barge(self, call_id: str) -> Any:
        return await self._client._post(f"/calls/{call_id}/barge")
