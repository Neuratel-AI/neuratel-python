from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class BillingResource:
    """`/v1/billing` — current balance, recent usage, and balance history."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def balance(self) -> Any:
        """Get the organization's current billing balance.

        Returns:
            A balance record (credit remaining, currency, etc.).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/billing/balance")

    def usage(self, *, days: int = 30) -> Any:
        """Get recent usage for the organization.

        Args:
            days: Lookback window in days. Defaults to 30.

        Returns:
            A usage record aggregated over the requested window.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/billing/usage", params={"days": days})

    def balance_history(self, *, skip: int = 0, limit: int = 20) -> Any:
        """List historical balance-change events.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of balance-history records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/billing/balance/history", params={"skip": skip, "limit": limit})


class AsyncBillingResource:
    """Async sibling of :class:`BillingResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def balance(self) -> Any:
        """Get the organization's current billing balance.

        Returns:
            A balance record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/billing/balance")

    async def usage(self, *, days: int = 30) -> Any:
        """Get recent usage for the organization.

        Args:
            days: Lookback window in days. Defaults to 30.

        Returns:
            A usage record aggregated over the requested window.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/billing/usage", params={"days": days})

    async def balance_history(self, *, skip: int = 0, limit: int = 20) -> Any:
        """List historical balance-change events.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of balance-history records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(
            "/billing/balance/history", params={"skip": skip, "limit": limit}
        )
