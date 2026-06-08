from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class APIKeysResource:
    """`/v1/api-keys` — create, list, rotate, revoke, and inspect scopes."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        """Create an organization API key. Returns key + secret (shown once).

        Args:
            **body: Key configuration (e.g. ``name``, ``scopes``,
                ``expires_at``).

        Returns:
            The new key record. The ``secret`` is returned only in this
            response — store it immediately.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/api-keys", json=body)

    def list(self, *, include_revoked: bool = False) -> Any:
        """List API keys for the organization.

        Args:
            include_revoked: If ``True``, include keys that have been
                revoked. Defaults to ``False`` (active keys only).

        Returns:
            A list of key records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/api-keys", params={"include_revoked": include_revoked})

    def revoke(self, key_id: str) -> Any:
        """Immediately invalidate an API key.

        Args:
            key_id: The key identifier to revoke.

        Returns:
            The revocation confirmation payload.

        Raises:
            APIError: If the request fails.
        """
        return self._client._delete(f"/api-keys/{key_id}")

    def rotate(self, key_id: str, *, grace_period_hours: int = 24) -> Any:
        """Replace a key — old key stays valid for grace_period_hours (1-168).

        Args:
            key_id: The key identifier to rotate.
            grace_period_hours: Hours the old key remains valid (1–168).
                Defaults to 24.

        Returns:
            A record containing the new key + secret and the old key's
            expiration time.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(
            f"/api-keys/{key_id}/rotate",
            params={"grace_period_hours": grace_period_hours},
        )

    def scopes(self) -> Any:
        """List all available scopes and preset bundles.

        Returns:
            A list of scope definitions and named preset bundles.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/api-keys/scopes")


class AsyncAPIKeysResource:
    """Async sibling of :class:`APIKeysResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        """Create an organization API key. Returns key + secret (shown once).

        Args:
            **body: Key configuration (e.g. ``name``, ``scopes``,
                ``expires_at``).

        Returns:
            The new key record. The ``secret`` is returned only here.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/api-keys", json=body)

    async def list(self, *, include_revoked: bool = False) -> Any:
        """List API keys for the organization.

        Args:
            include_revoked: If ``True``, include revoked keys.

        Returns:
            A list of key records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/api-keys", params={"include_revoked": include_revoked})

    async def revoke(self, key_id: str) -> Any:
        """Immediately invalidate an API key.

        Args:
            key_id: The key identifier to revoke.

        Returns:
            The revocation confirmation payload.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._delete(f"/api-keys/{key_id}")

    async def rotate(self, key_id: str, *, grace_period_hours: int = 24) -> Any:
        """Replace a key — old key stays valid for grace_period_hours (1-168).

        Args:
            key_id: The key identifier to rotate.
            grace_period_hours: Hours the old key remains valid (1–168).
                Defaults to 24.

        Returns:
            A record containing the new key + secret and the old key's
            expiration time.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(
            f"/api-keys/{key_id}/rotate",
            params={"grace_period_hours": grace_period_hours},
        )

    async def scopes(self) -> Any:
        """List all available scopes and preset bundles.

        Returns:
            A list of scope definitions and named preset bundles.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/api-keys/scopes")
