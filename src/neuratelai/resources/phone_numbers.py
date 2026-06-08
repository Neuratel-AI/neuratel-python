from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class PhoneNumbersResource:
    """`/v1/numbers` — phone-number inventory and agent assignment."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        """List phone numbers owned by the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            A ``SyncPage`` yielding phone-number records.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/numbers", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/numbers",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, phone_number_id: str) -> Any:
        """Fetch a single phone number by ID.

        Args:
            phone_number_id: The phone-number identifier.

        Returns:
            The phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/numbers/{phone_number_id}")

    def update(self, phone_number_id: str, **body: Any) -> Any:
        """Replace a phone number's mutable fields (e.g. friendly name).

        Args:
            phone_number_id: The phone-number identifier.
            **body: Fields to update.

        Returns:
            The updated phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/numbers/{phone_number_id}", json=body)

    def assign(self, phone_number_id: str, *, agent_id: str) -> Any:
        """Assign a phone number to an agent (routes inbound calls to it).

        Args:
            phone_number_id: The phone-number identifier.
            agent_id: The agent that should receive the calls.

        Returns:
            The updated phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/numbers/{phone_number_id}/assign", json={"agent_id": agent_id})

    def unassign(self, phone_number_id: str) -> Any:
        """Unassign a phone number from any agent.

        Args:
            phone_number_id: The phone-number identifier.

        Returns:
            The updated phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/numbers/{phone_number_id}/unassign")


class AsyncPhoneNumbersResource:
    """Async sibling of :class:`PhoneNumbersResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        """List phone numbers owned by the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            An ``AsyncPage`` yielding phone-number records.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get("/numbers", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/numbers",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, phone_number_id: str) -> Any:
        """Fetch a single phone number by ID.

        Args:
            phone_number_id: The phone-number identifier.

        Returns:
            The phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/numbers/{phone_number_id}")

    async def update(self, phone_number_id: str, **body: Any) -> Any:
        """Replace a phone number's mutable fields.

        Args:
            phone_number_id: The phone-number identifier.
            **body: Fields to update.

        Returns:
            The updated phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/numbers/{phone_number_id}", json=body)

    async def assign(self, phone_number_id: str, *, agent_id: str) -> Any:
        """Assign a phone number to an agent.

        Args:
            phone_number_id: The phone-number identifier.
            agent_id: The agent that should receive the calls.

        Returns:
            The updated phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(
            f"/numbers/{phone_number_id}/assign", json={"agent_id": agent_id}
        )

    async def unassign(self, phone_number_id: str) -> Any:
        """Unassign a phone number from any agent.

        Args:
            phone_number_id: The phone-number identifier.

        Returns:
            The updated phone-number record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/numbers/{phone_number_id}/unassign")
