from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class WebhooksResource:
    """`/v1/webhooks` — webhook CRUD, secret rotation, event catalog, and delivery logs."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def events(self) -> Any:
        """List all available webhook event types.

        Returns:
            A list of event-type definitions (name, description,
            payload schema reference).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/webhooks/events")

    def create(self, **body: Any) -> Any:
        """Create a new webhook subscription.

        Args:
            **body: Webhook fields (e.g. ``url``, ``events``,
                ``secret``, ``description``).

        Returns:
            The created webhook record (includes the signing secret if
            one was not provided).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/webhooks", json=body)

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        """List webhooks for the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            A ``SyncPage`` yielding webhook records.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/webhooks", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/webhooks",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, webhook_id: str) -> Any:
        """Fetch a single webhook by ID.

        Args:
            webhook_id: The webhook identifier.

        Returns:
            The webhook record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/webhooks/{webhook_id}")

    def update(self, webhook_id: str, **body: Any) -> Any:
        """Patch a webhook's mutable fields.

        Args:
            webhook_id: The webhook identifier.
            **body: Fields to update (e.g. ``url``, ``events``,
                ``active``).

        Returns:
            The updated webhook record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._patch(f"/webhooks/{webhook_id}", json=body)

    def delete(self, webhook_id: str) -> None:
        """Permanently delete a webhook.

        Args:
            webhook_id: The webhook identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/webhooks/{webhook_id}")

    def test(self, webhook_id: str, **body: Any) -> Any:
        """Send a synthetic test event to a webhook endpoint.

        Args:
            webhook_id: The webhook identifier.
            **body: Optional overrides for the test payload (e.g.
                ``event_type``).

        Returns:
            The delivery result (status, response code, latency).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/webhooks/{webhook_id}/test", json=body)

    def rotate_secret(self, webhook_id: str) -> Any:
        """Rotate the signing secret for a webhook.

        Returns a new secret — store it before reconfiguring your
        endpoint to verify signatures with it.

        Args:
            webhook_id: The webhook identifier.

        Returns:
            The new signing secret.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/webhooks/{webhook_id}/secret/rotate")

    def logs(self, webhook_id: str, *, skip: int = 0, limit: int = 20, **params: Any) -> Any:
        """List recent delivery attempts for a webhook.

        Args:
            webhook_id: The webhook identifier.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API
                (e.g. ``status``).

        Returns:
            A page of delivery-log records (event, status, response
            code, attempt timestamp).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(
            f"/webhooks/{webhook_id}/logs", params={"skip": skip, "limit": limit, **params}
        )


class AsyncWebhooksResource:
    """Async sibling of :class:`WebhooksResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def events(self) -> Any:
        """List all available webhook event types.

        Returns:
            A list of event-type definitions.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/webhooks/events")

    async def create(self, **body: Any) -> Any:
        """Create a new webhook subscription.

        Args:
            **body: Webhook fields (e.g. ``url``, ``events``,
                ``secret``, ``description``).

        Returns:
            The created webhook record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/webhooks", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        """List webhooks for the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            An ``AsyncPage`` yielding webhook records.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get("/webhooks", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/webhooks",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, webhook_id: str) -> Any:
        """Fetch a single webhook by ID.

        Args:
            webhook_id: The webhook identifier.

        Returns:
            The webhook record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/webhooks/{webhook_id}")

    async def update(self, webhook_id: str, **body: Any) -> Any:
        """Patch a webhook's mutable fields.

        Args:
            webhook_id: The webhook identifier.
            **body: Fields to update.

        Returns:
            The updated webhook record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._patch(f"/webhooks/{webhook_id}", json=body)

    async def delete(self, webhook_id: str) -> None:
        """Permanently delete a webhook.

        Args:
            webhook_id: The webhook identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/webhooks/{webhook_id}")

    async def test(self, webhook_id: str, **body: Any) -> Any:
        """Send a synthetic test event to a webhook endpoint.

        Args:
            webhook_id: The webhook identifier.
            **body: Optional overrides for the test payload.

        Returns:
            The delivery result.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/webhooks/{webhook_id}/test", json=body)

    async def rotate_secret(self, webhook_id: str) -> Any:
        """Rotate the signing secret for a webhook.

        Args:
            webhook_id: The webhook identifier.

        Returns:
            The new signing secret.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/webhooks/{webhook_id}/secret/rotate")

    async def logs(self, webhook_id: str, *, skip: int = 0, limit: int = 20, **params: Any) -> Any:
        """List recent delivery attempts for a webhook.

        Args:
            webhook_id: The webhook identifier.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            A page of delivery-log records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(
            f"/webhooks/{webhook_id}/logs", params={"skip": skip, "limit": limit, **params}
        )
