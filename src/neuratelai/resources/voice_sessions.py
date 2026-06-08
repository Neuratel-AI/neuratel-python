from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class VoiceSessionsResource:
    """`/v1/voice-sessions` — list, get, update, delete + supervisor actions."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        """List voice sessions (calls) for the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API
                (e.g. ``agent_id``, ``status``, ``direction``,
                ``start_date``, ``end_date``).

        Returns:
            A ``SyncPage`` yielding voice-session records.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/voice-sessions", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/voice-sessions",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, call_id: str, *, include: str | None = None) -> Any:
        """Fetch a single voice session by call ID.

        Args:
            call_id: The call identifier.
            include: Optional comma-separated list of related resources
                to inline (e.g. ``"transcript,recording"``).

        Returns:
            The voice-session record.

        Raises:
            APIError: If the request fails.
        """
        params = {"include": include} if include else None
        return self._client._get(f"/voice-sessions/{call_id}", params=params)

    def update(self, call_id: str, *, call_metadata: dict[str, Any]) -> Any:
        """Merge keys into the row's `call_metadata` JSONB column.

        Only `call_metadata` is mutable on this endpoint — operators attach
        CRM IDs, ticket numbers, post-call notes after the call ends. Status,
        timing, and other fields are auto-managed by the platform.

        Args:
            call_id: The call identifier.
            call_metadata: Keys to merge into the existing metadata map.

        Returns:
            The updated voice-session record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._request(
            "PATCH",
            f"/voice-sessions/{call_id}",
            json={"call_metadata": call_metadata},
        )

    def delete(
        self,
        call_id: str,
        *,
        delete_recording: bool = False,
        delete_transcript: bool = False,
    ) -> None:
        """Permanently delete a voice session.

        Args:
            call_id: The call identifier.
            delete_recording: If ``True``, also drop the audio recording.
            delete_transcript: If ``True``, also drop the transcript.

        Raises:
            APIError: If the request fails.
        """
        self._client._request(
            "DELETE",
            f"/voice-sessions/{call_id}",
            params={
                "delete_recording": delete_recording,
                "delete_transcript": delete_transcript,
            },
            expect_body=False,
        )

    def outbound(self, **body: Any) -> Any:
        """Place a single outbound call. POST /v1/voice-sessions/outbound.

        Args:
            **body: Outbound-call fields (e.g. ``agent_id``,
                ``to_number``, ``from_number``, ``dynamic_variables``,
                ``call_metadata``).

        Returns:
            The newly created voice-session record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/voice-sessions/outbound", json=body)

    def list_active(self) -> Any:
        """List voice sessions that are currently in progress.

        Returns:
            A list of in-flight voice-session records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/voice-sessions/active")

    def concurrency(self) -> Any:
        """Get the organization's current voice-call concurrency stats.

        Returns:
            A concurrency record (active calls, peak, limits).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/voice-sessions/concurrency")

    def hangup(self, call_id: str) -> Any:
        """Forcefully terminate an in-progress call.

        Args:
            call_id: The call identifier.

        Returns:
            The updated voice-session record (status ``completed`` or
            similar).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/voice-sessions/{call_id}/hangup")

    def listen(self, call_id: str) -> Any:
        """Begin silent listen-only monitoring of a call.

        Args:
            call_id: The call identifier.

        Returns:
            Connection details (e.g. supervisor token + server URL).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/voice-sessions/{call_id}/listen")

    def whisper(self, call_id: str) -> Any:
        """Whisper to the agent (caller cannot hear the supervisor).

        Args:
            call_id: The call identifier.

        Returns:
            Connection details (e.g. supervisor token + server URL).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/voice-sessions/{call_id}/whisper")

    def barge(self, call_id: str) -> Any:
        """Barge into a call (all parties can hear the supervisor).

        Args:
            call_id: The call identifier.

        Returns:
            Connection details (e.g. supervisor token + server URL).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/voice-sessions/{call_id}/barge")


class AsyncVoiceSessionsResource:
    """Async sibling of :class:`VoiceSessionsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        """List voice sessions (calls) for the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            An ``AsyncPage`` yielding voice-session records.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get(
            "/voice-sessions", params={"skip": skip, "limit": limit, **params}
        )
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/voice-sessions",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, call_id: str, *, include: str | None = None) -> Any:
        """Fetch a single voice session by call ID.

        Args:
            call_id: The call identifier.
            include: Optional comma-separated list of related resources
                to inline (e.g. ``"transcript,recording"``).

        Returns:
            The voice-session record.

        Raises:
            APIError: If the request fails.
        """
        params = {"include": include} if include else None
        return await self._client._get(f"/voice-sessions/{call_id}", params=params)

    async def update(self, call_id: str, *, call_metadata: dict[str, Any]) -> Any:
        """Merge keys into the row's ``call_metadata`` JSONB column.

        Args:
            call_id: The call identifier.
            call_metadata: Keys to merge into the existing metadata map.

        Returns:
            The updated voice-session record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._request(
            "PATCH",
            f"/voice-sessions/{call_id}",
            json={"call_metadata": call_metadata},
        )

    async def delete(
        self,
        call_id: str,
        *,
        delete_recording: bool = False,
        delete_transcript: bool = False,
    ) -> None:
        """Permanently delete a voice session.

        Args:
            call_id: The call identifier.
            delete_recording: If ``True``, also drop the audio recording.
            delete_transcript: If ``True``, also drop the transcript.

        Raises:
            APIError: If the request fails.
        """
        await self._client._request(
            "DELETE",
            f"/voice-sessions/{call_id}",
            params={
                "delete_recording": delete_recording,
                "delete_transcript": delete_transcript,
            },
            expect_body=False,
        )

    async def outbound(self, **body: Any) -> Any:
        """Place a single outbound call.

        Args:
            **body: Outbound-call fields (e.g. ``agent_id``,
                ``to_number``, ``from_number``, ``dynamic_variables``,
                ``call_metadata``).

        Returns:
            The newly created voice-session record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/voice-sessions/outbound", json=body)

    async def list_active(self) -> Any:
        """List voice sessions that are currently in progress.

        Returns:
            A list of in-flight voice-session records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/voice-sessions/active")

    async def concurrency(self) -> Any:
        """Get the organization's current voice-call concurrency stats.

        Returns:
            A concurrency record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/voice-sessions/concurrency")

    async def hangup(self, call_id: str) -> Any:
        """Forcefully terminate an in-progress call.

        Args:
            call_id: The call identifier.

        Returns:
            The updated voice-session record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/voice-sessions/{call_id}/hangup")

    async def listen(self, call_id: str) -> Any:
        """Begin silent listen-only monitoring of a call.

        Args:
            call_id: The call identifier.

        Returns:
            Connection details.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/voice-sessions/{call_id}/listen")

    async def whisper(self, call_id: str) -> Any:
        """Whisper to the agent (caller cannot hear the supervisor).

        Args:
            call_id: The call identifier.

        Returns:
            Connection details.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/voice-sessions/{call_id}/whisper")

    async def barge(self, call_id: str) -> Any:
        """Barge into a call (all parties can hear the supervisor).

        Args:
            call_id: The call identifier.

        Returns:
            Connection details.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/voice-sessions/{call_id}/barge")
