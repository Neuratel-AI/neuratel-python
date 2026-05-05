"""Conversations resource — unified inbox for chat (SMS + WhatsApp) and voice.

A conversation groups all messages and voice sessions exchanged with a single
contact through a single channel. Use this resource for chat-style operations:
listing threads, sending replies, marking read, fetching message history, and
the per-conversation analytics dashboard. For real-time voice control use
the voice_sessions resource instead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class ConversationsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(
        self,
        *,
        channel: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Any:
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if channel is not None:
            params["channel"] = channel
        if status is not None:
            params["status"] = status
        return self._client._get("/conversations", params=params)

    def get(self, conversation_id: str) -> Any:
        return self._client._get(f"/conversations/{conversation_id}")

    def list_messages(
        self,
        conversation_id: str,
        *,
        skip: int = 0,
        limit: int = 50,
        since: str | None = None,
        before: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return self._client._get(
            f"/conversations/{conversation_id}/messages", params=params
        )

    def send_message(
        self,
        conversation_id: str,
        *,
        body: str,
        media_urls: Any = None,
        client_temp_id: str | None = None,
        **extra: Any,
    ) -> Any:
        payload: dict[str, Any] = {"body": body, **extra}
        if media_urls is not None:
            payload["media_urls"] = media_urls
        if client_temp_id is not None:
            payload["client_temp_id"] = client_temp_id
        return self._client._post(
            f"/conversations/{conversation_id}/messages", json=payload
        )

    def mark_read(self, conversation_id: str) -> Any:
        return self._client._post(f"/conversations/{conversation_id}/read")

    def timeline(
        self,
        conversation_id: str,
        *,
        limit: int = 50,
        since: str | None = None,
        before: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {"limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return self._client._get(
            f"/conversations/{conversation_id}/timeline", params=params
        )

    def update_dynamic_variables(
        self,
        conversation_id: str,
        *,
        dynamic_variables: dict[str, Any] | None = None,
        replace: bool = False,
    ) -> Any:
        body: dict[str, Any] = {"replace": replace}
        if dynamic_variables is not None:
            body["dynamic_variables"] = dynamic_variables
        return self._client._patch(
            f"/conversations/{conversation_id}/dynamic_variables", json=body
        )

    def analytics_dashboard(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        channel: str | None = None,
        agent_id: str | None = None,
        interval: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if channel is not None:
            params["channel"] = channel
        if agent_id is not None:
            params["agent_id"] = agent_id
        if interval is not None:
            params["interval"] = interval
        return self._client._get(
            "/conversations/analytics/dashboard", params=params
        )


class AsyncConversationsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        channel: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Any:
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if channel is not None:
            params["channel"] = channel
        if status is not None:
            params["status"] = status
        return await self._client._get("/conversations", params=params)

    async def get(self, conversation_id: str) -> Any:
        return await self._client._get(f"/conversations/{conversation_id}")

    async def list_messages(
        self,
        conversation_id: str,
        *,
        skip: int = 0,
        limit: int = 50,
        since: str | None = None,
        before: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return await self._client._get(
            f"/conversations/{conversation_id}/messages", params=params
        )

    async def send_message(
        self,
        conversation_id: str,
        *,
        body: str,
        media_urls: Any = None,
        client_temp_id: str | None = None,
        **extra: Any,
    ) -> Any:
        payload: dict[str, Any] = {"body": body, **extra}
        if media_urls is not None:
            payload["media_urls"] = media_urls
        if client_temp_id is not None:
            payload["client_temp_id"] = client_temp_id
        return await self._client._post(
            f"/conversations/{conversation_id}/messages", json=payload
        )

    async def mark_read(self, conversation_id: str) -> Any:
        return await self._client._post(f"/conversations/{conversation_id}/read")

    async def timeline(
        self,
        conversation_id: str,
        *,
        limit: int = 50,
        since: str | None = None,
        before: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {"limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return await self._client._get(
            f"/conversations/{conversation_id}/timeline", params=params
        )

    async def update_dynamic_variables(
        self,
        conversation_id: str,
        *,
        dynamic_variables: dict[str, Any] | None = None,
        replace: bool = False,
    ) -> Any:
        body: dict[str, Any] = {"replace": replace}
        if dynamic_variables is not None:
            body["dynamic_variables"] = dynamic_variables
        return await self._client._patch(
            f"/conversations/{conversation_id}/dynamic_variables", json=body
        )

    async def analytics_dashboard(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        channel: str | None = None,
        agent_id: str | None = None,
        interval: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if channel is not None:
            params["channel"] = channel
        if agent_id is not None:
            params["agent_id"] = agent_id
        if interval is not None:
            params["interval"] = interval
        return await self._client._get(
            "/conversations/analytics/dashboard", params=params
        )
