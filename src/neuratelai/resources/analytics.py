"""Analytics resource — combined voice + chat dashboard.

For per-channel analytics use the channel-specific endpoints exposed elsewhere
(voice_sessions for voice, conversations.analytics_dashboard for chat). This
resource is the union view.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class AnalyticsResource:
    """Sync client for the combined voice + chat analytics dashboard."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def dashboard(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        agent_id: str | None = None,
        channel: str | None = None,
        direction: str | None = None,
        interval: str | None = None,
    ) -> Any:
        """Fetch the combined analytics dashboard for an organization.

        Args:
            start_date: ISO-8601 lower bound (inclusive) for the date range.
            end_date: ISO-8601 upper bound (inclusive) for the date range.
            agent_id: Optional filter to a single agent.
            channel: Optional channel filter (e.g. ``"voice"``, ``"sms"``,
                ``"whatsapp"``).
            direction: Optional direction filter (e.g. ``"inbound"``,
                ``"outbound"``).
            interval: Optional bucket size for time-series data
                (e.g. ``"hour"``, ``"day"``, ``"week"``).

        Returns:
            The dashboard payload (totals + time-series).

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if agent_id is not None:
            params["agent_id"] = agent_id
        if channel is not None:
            params["channel"] = channel
        if direction is not None:
            params["direction"] = direction
        if interval is not None:
            params["interval"] = interval
        return self._client._get("/analytics/dashboard", params=params)


class AsyncAnalyticsResource:
    """Async sibling of :class:`AnalyticsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def dashboard(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        agent_id: str | None = None,
        channel: str | None = None,
        direction: str | None = None,
        interval: str | None = None,
    ) -> Any:
        """Fetch the combined analytics dashboard for an organization.

        Args:
            start_date: ISO-8601 lower bound (inclusive) for the date range.
            end_date: ISO-8601 upper bound (inclusive) for the date range.
            agent_id: Optional filter to a single agent.
            channel: Optional channel filter.
            direction: Optional direction filter.
            interval: Optional bucket size for time-series data.

        Returns:
            The dashboard payload (totals + time-series).

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if agent_id is not None:
            params["agent_id"] = agent_id
        if channel is not None:
            params["channel"] = channel
        if direction is not None:
            params["direction"] = direction
        if interval is not None:
            params["interval"] = interval
        return await self._client._get("/analytics/dashboard", params=params)
