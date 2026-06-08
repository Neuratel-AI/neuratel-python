from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class CampaignsResource:
    """`/v1/campaigns` — outbound-campaign CRUD, lifecycle, and call records."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        """Create a new campaign.

        Args:
            **body: Campaign fields (e.g. ``name``, ``call_list_id``,
                ``agent_id``, ``schedule``).

        Returns:
            The created campaign record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/campaigns", json=body)

    def list(self, *, skip: int = 0, limit: int = 20) -> SyncPage:
        """List campaigns in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A ``SyncPage`` yielding campaign records.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/campaigns", params={"skip": skip, "limit": limit})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/campaigns",
            params={"skip": skip, "limit": limit},
        )

    def get(self, campaign_id: str) -> Any:
        """Fetch a single campaign by ID.

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The campaign record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/campaigns/{campaign_id}")

    def update(self, campaign_id: str, **body: Any) -> Any:
        """Replace a campaign's mutable fields.

        Args:
            campaign_id: The campaign identifier.
            **body: Fields to update.

        Returns:
            The updated campaign record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/campaigns/{campaign_id}", json=body)

    def delete(self, campaign_id: str) -> None:
        """Permanently delete a campaign.

        Args:
            campaign_id: The campaign identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/campaigns/{campaign_id}")

    def start(self, campaign_id: str) -> Any:
        """Start a campaign (begin dialing its call list).

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The updated campaign record (status ``running``).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/campaigns/{campaign_id}/start")

    def pause(self, campaign_id: str) -> Any:
        """Pause a running campaign.

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The updated campaign record (status ``paused``).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/campaigns/{campaign_id}/pause")

    def stop(self, campaign_id: str) -> Any:
        """Stop a campaign (terminal state).

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The updated campaign record (status ``stopped``).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/campaigns/{campaign_id}/stop")

    def list_calls(self, *, campaign_id: str | None = None, **params: Any) -> Any:
        """List outbound call records. Filter by campaign_id for a specific campaign.

        Args:
            campaign_id: Optional campaign identifier to scope results to.
            **params: Additional query parameters forwarded to the API
                (e.g. ``status``, ``skip``, ``limit``).

        Returns:
            A page of campaign call records.

        Raises:
            APIError: If the request fails.
        """
        p = {**params}
        if campaign_id:
            p["campaign_id"] = campaign_id
        return self._client._get("/campaigns/calls", params=p or None)

    def get_call(self, call_id: str) -> Any:
        """Get a specific campaign outbound call record.

        Args:
            call_id: The call identifier.

        Returns:
            The call record (recording, transcript, outcome, etc.).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/campaigns/calls/{call_id}")


class AsyncCampaignsResource:
    """Async sibling of :class:`CampaignsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        """Create a new campaign.

        Args:
            **body: Campaign fields.

        Returns:
            The created campaign record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/campaigns", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20) -> AsyncPage:
        """List campaigns in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            An ``AsyncPage`` yielding campaign records.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get("/campaigns", params={"skip": skip, "limit": limit})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/campaigns",
            params={"skip": skip, "limit": limit},
        )

    async def get(self, campaign_id: str) -> Any:
        """Fetch a single campaign by ID.

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The campaign record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/campaigns/{campaign_id}")

    async def update(self, campaign_id: str, **body: Any) -> Any:
        """Replace a campaign's mutable fields.

        Args:
            campaign_id: The campaign identifier.
            **body: Fields to update.

        Returns:
            The updated campaign record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/campaigns/{campaign_id}", json=body)

    async def delete(self, campaign_id: str) -> None:
        """Permanently delete a campaign.

        Args:
            campaign_id: The campaign identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/campaigns/{campaign_id}")

    async def start(self, campaign_id: str) -> Any:
        """Start a campaign (begin dialing its call list).

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The updated campaign record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/campaigns/{campaign_id}/start")

    async def pause(self, campaign_id: str) -> Any:
        """Pause a running campaign.

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The updated campaign record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/campaigns/{campaign_id}/pause")

    async def stop(self, campaign_id: str) -> Any:
        """Stop a campaign (terminal state).

        Args:
            campaign_id: The campaign identifier.

        Returns:
            The updated campaign record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/campaigns/{campaign_id}/stop")

    async def list_calls(self, *, campaign_id: str | None = None, **params: Any) -> Any:
        """List outbound call records. Filter by campaign_id for a specific campaign.

        Args:
            campaign_id: Optional campaign identifier to scope results to.
            **params: Additional query parameters forwarded to the API.

        Returns:
            A page of campaign call records.

        Raises:
            APIError: If the request fails.
        """
        p = {**params}
        if campaign_id:
            p["campaign_id"] = campaign_id
        return await self._client._get("/campaigns/calls", params=p or None)

    async def get_call(self, call_id: str) -> Any:
        """Get a specific campaign outbound call record.

        Args:
            call_id: The call identifier.

        Returns:
            The call record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/campaigns/calls/{call_id}")
