from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class CallsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        data = self._client._get("/voice-sessions", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/voice-sessions",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, call_id: str, *, include: str | None = None) -> Any:
        params = {"include": include} if include else None
        return self._client._get(f"/voice-sessions/{call_id}", params=params)

    def delete(
        self, call_id: str, *, delete_recording: bool = False, delete_transcript: bool = False
    ) -> None:
        self._client._request(
            "DELETE",
            f"/voice-sessions/{call_id}",
            params={"delete_recording": delete_recording, "delete_transcript": delete_transcript},
            expect_body=False,
        )

    def outbound(self, **body: Any) -> Any:
        """Place a single outbound call. POST /v1/voice-sessions/outbound"""
        return self._client._post("/voice-sessions/outbound", json=body)

    def active(self) -> Any:
        return self._client._get("/voice-sessions/active")

    def concurrency(self) -> Any:
        return self._client._get("/voice-sessions/concurrency")

    def hangup(self, call_id: str) -> Any:
        return self._client._post(f"/voice-sessions/{call_id}/hangup")

    def listen(self, call_id: str) -> Any:
        return self._client._post(f"/voice-sessions/{call_id}/listen")

    def whisper(self, call_id: str) -> Any:
        return self._client._post(f"/voice-sessions/{call_id}/whisper")

    def barge(self, call_id: str) -> Any:
        return self._client._post(f"/voice-sessions/{call_id}/barge")


class AsyncCallsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        data = await self._client._get("/voice-sessions", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/voice-sessions",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, call_id: str, *, include: str | None = None) -> Any:
        params = {"include": include} if include else None
        return await self._client._get(f"/voice-sessions/{call_id}", params=params)

    async def delete(
        self, call_id: str, *, delete_recording: bool = False, delete_transcript: bool = False
    ) -> None:
        await self._client._request(
            "DELETE",
            f"/voice-sessions/{call_id}",
            params={"delete_recording": delete_recording, "delete_transcript": delete_transcript},
            expect_body=False,
        )

    async def outbound(self, **body: Any) -> Any:
        return await self._client._post("/voice-sessions/outbound", json=body)

    async def active(self) -> Any:
        return await self._client._get("/voice-sessions/active")

    async def concurrency(self) -> Any:
        return await self._client._get("/voice-sessions/concurrency")

    async def hangup(self, call_id: str) -> Any:
        return await self._client._post(f"/voice-sessions/{call_id}/hangup")

    async def listen(self, call_id: str) -> Any:
        return await self._client._post(f"/voice-sessions/{call_id}/listen")

    async def whisper(self, call_id: str) -> Any:
        return await self._client._post(f"/voice-sessions/{call_id}/whisper")

    async def barge(self, call_id: str) -> Any:
        return await self._client._post(f"/voice-sessions/{call_id}/barge")
