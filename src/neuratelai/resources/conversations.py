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
    """`/v1/conversations` — threads, messages, timelines, dynamic variables."""

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
        """List conversations in the organization.

        Args:
            channel: Optional channel filter (e.g. ``"sms"``,
                ``"whatsapp"``).
            status: Optional status filter (e.g. ``"open"``,
                ``"closed"``).
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of conversation summaries.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if channel is not None:
            params["channel"] = channel
        if status is not None:
            params["status"] = status
        return self._client._get("/conversations", params=params)

    def get(self, conversation_id: str) -> Any:
        """Fetch a single conversation by ID.

        Args:
            conversation_id: The conversation identifier.

        Returns:
            The conversation record (contact, channel, status, last
            message preview, etc.).

        Raises:
            APIError: If the request fails.
        """
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
        """List messages in a conversation, oldest first.

        Args:
            conversation_id: The conversation identifier.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            since: Optional ISO-8601 lower bound on message timestamp.
            before: Optional ISO-8601 upper bound on message timestamp.

        Returns:
            A page of message records.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return self._client._get(f"/conversations/{conversation_id}/messages", params=params)

    def send_message(
        self,
        conversation_id: str,
        *,
        body: str,
        media_urls: Any = None,
        client_temp_id: str | None = None,
        **extra: Any,
    ) -> Any:
        """Send a message in a conversation (as the agent / from the API).

        Args:
            conversation_id: The conversation identifier.
            body: Message body text.
            media_urls: Optional list of media URLs to attach.
            client_temp_id: Optional client-generated ID for idempotency /
                dedupe.
            **extra: Additional fields forwarded to the API.

        Returns:
            The created message record.

        Raises:
            APIError: If the request fails.
        """
        payload: dict[str, Any] = {"body": body, **extra}
        if media_urls is not None:
            payload["media_urls"] = media_urls
        if client_temp_id is not None:
            payload["client_temp_id"] = client_temp_id
        return self._client._post(f"/conversations/{conversation_id}/messages", json=payload)

    def mark_read(self, conversation_id: str) -> Any:
        """Mark all messages in a conversation as read.

        Args:
            conversation_id: The conversation identifier.

        Returns:
            The updated conversation record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/conversations/{conversation_id}/read")

    def timeline(
        self,
        conversation_id: str,
        *,
        limit: int = 50,
        since: str | None = None,
        before: str | None = None,
    ) -> Any:
        """Fetch the interleaved timeline of messages + system events.

        Args:
            conversation_id: The conversation identifier.
            limit: Maximum number of events to return.
            since: Optional ISO-8601 lower bound on event timestamp.
            before: Optional ISO-8601 upper bound on event timestamp.

        Returns:
            A list of timeline events (inbound/outbound messages, status
            changes, hand-offs, etc.).

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return self._client._get(f"/conversations/{conversation_id}/timeline", params=params)

    def update_dynamic_variables(
        self,
        conversation_id: str,
        *,
        dynamic_variables: dict[str, Any] | None = None,
        replace: bool = False,
    ) -> Any:
        """Merge (or replace) the conversation's dynamic variables mid-call.

        Args:
            conversation_id: The conversation identifier.
            dynamic_variables: Variables to write. If ``replace`` is
                ``False``, these keys are merged into the existing map.
            replace: If ``True``, the existing variables are fully
                replaced. Defaults to ``False`` (merge).

        Returns:
            The updated conversation record.

        Raises:
            APIError: If the request fails.
        """
        body: dict[str, Any] = {"replace": replace}
        if dynamic_variables is not None:
            body["dynamic_variables"] = dynamic_variables
        return self._client._patch(f"/conversations/{conversation_id}/dynamic_variables", json=body)

    def analytics_dashboard(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        channel: str | None = None,
        agent_id: str | None = None,
        interval: str | None = None,
    ) -> Any:
        """Fetch the chat-conversations analytics dashboard.

        Args:
            start_date: ISO-8601 lower bound (inclusive).
            end_date: ISO-8601 upper bound (inclusive).
            channel: Optional channel filter.
            agent_id: Optional agent filter.
            interval: Optional bucket size for time-series data.

        Returns:
            The dashboard payload.

        Raises:
            APIError: If the request fails.
        """
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
        return self._client._get("/conversations/analytics/dashboard", params=params)


class AsyncConversationsResource:
    """Async sibling of :class:`ConversationsResource`."""

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
        """List conversations in the organization.

        Args:
            channel: Optional channel filter.
            status: Optional status filter.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of conversation summaries.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if channel is not None:
            params["channel"] = channel
        if status is not None:
            params["status"] = status
        return await self._client._get("/conversations", params=params)

    async def get(self, conversation_id: str) -> Any:
        """Fetch a single conversation by ID.

        Args:
            conversation_id: The conversation identifier.

        Returns:
            The conversation record.

        Raises:
            APIError: If the request fails.
        """
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
        """List messages in a conversation, oldest first.

        Args:
            conversation_id: The conversation identifier.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            since: Optional ISO-8601 lower bound on message timestamp.
            before: Optional ISO-8601 upper bound on message timestamp.

        Returns:
            A page of message records.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return await self._client._get(f"/conversations/{conversation_id}/messages", params=params)

    async def send_message(
        self,
        conversation_id: str,
        *,
        body: str,
        media_urls: Any = None,
        client_temp_id: str | None = None,
        **extra: Any,
    ) -> Any:
        """Send a message in a conversation.

        Args:
            conversation_id: The conversation identifier.
            body: Message body text.
            media_urls: Optional list of media URLs to attach.
            client_temp_id: Optional client-generated ID for idempotency.
            **extra: Additional fields forwarded to the API.

        Returns:
            The created message record.

        Raises:
            APIError: If the request fails.
        """
        payload: dict[str, Any] = {"body": body, **extra}
        if media_urls is not None:
            payload["media_urls"] = media_urls
        if client_temp_id is not None:
            payload["client_temp_id"] = client_temp_id
        return await self._client._post(f"/conversations/{conversation_id}/messages", json=payload)

    async def mark_read(self, conversation_id: str) -> Any:
        """Mark all messages in a conversation as read.

        Args:
            conversation_id: The conversation identifier.

        Returns:
            The updated conversation record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/conversations/{conversation_id}/read")

    async def timeline(
        self,
        conversation_id: str,
        *,
        limit: int = 50,
        since: str | None = None,
        before: str | None = None,
    ) -> Any:
        """Fetch the interleaved timeline of messages + system events.

        Args:
            conversation_id: The conversation identifier.
            limit: Maximum number of events to return.
            since: Optional ISO-8601 lower bound on event timestamp.
            before: Optional ISO-8601 upper bound on event timestamp.

        Returns:
            A list of timeline events.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"limit": limit}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        return await self._client._get(f"/conversations/{conversation_id}/timeline", params=params)

    async def update_dynamic_variables(
        self,
        conversation_id: str,
        *,
        dynamic_variables: dict[str, Any] | None = None,
        replace: bool = False,
    ) -> Any:
        """Merge (or replace) the conversation's dynamic variables mid-call.

        Args:
            conversation_id: The conversation identifier.
            dynamic_variables: Variables to write.
            replace: If ``True``, replace the existing map instead of
                merging. Defaults to ``False``.

        Returns:
            The updated conversation record.

        Raises:
            APIError: If the request fails.
        """
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
        """Fetch the chat-conversations analytics dashboard.

        Args:
            start_date: ISO-8601 lower bound (inclusive).
            end_date: ISO-8601 upper bound (inclusive).
            channel: Optional channel filter.
            agent_id: Optional agent filter.
            interval: Optional bucket size for time-series data.

        Returns:
            The dashboard payload.

        Raises:
            APIError: If the request fails.
        """
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
        return await self._client._get("/conversations/analytics/dashboard", params=params)
