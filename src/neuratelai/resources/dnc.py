"""DNC (Do Not Call) resource — platform DNC directory and per-org settings.

Check phone numbers against the global directory before dialing, manage
per-org additions, and toggle organisation-wide DNC protection / STOP
auto-opt-out detection.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class DNCResource:
    """`/v1/dnc` — DNC directory lookup, entries, and organization settings."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def check(self, phone: str) -> Any:
        """Check whether a phone number appears in the DNC directory.

        Args:
            phone: E.164 phone number to look up.

        Returns:
            A dict containing at least ``listed`` (bool) and the originating
            ``source`` if listed.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/dnc/check", params={"phone": phone})

    def list_entries(self, *, source: str | None = None, limit: int = 100) -> Any:
        """List DNC entries visible to the organization.

        Args:
            source: Optional filter by entry source (e.g. ``"global"``,
                ``"org"``, ``"stop_keyword"``).
            limit: Maximum number of entries to return.

        Returns:
            A list of DNC entry records.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"limit": limit}
        if source is not None:
            params["source"] = source
        return self._client._get("/dnc/entries", params=params)

    def add_entry(
        self,
        *,
        phone: str,
        reason: str | None = None,
        notes: str | None = None,
        **extra: Any,
    ) -> Any:
        """Add a phone number to the organization's DNC list.

        Args:
            phone: E.164 phone number to add.
            reason: Optional reason (e.g. ``"customer_request"``).
            notes: Optional free-form notes.
            **extra: Additional fields forwarded to the API.

        Returns:
            The created DNC entry.

        Raises:
            APIError: If the request fails.
        """
        body: dict[str, Any] = {"phone": phone, **extra}
        if reason is not None:
            body["reason"] = reason
        if notes is not None:
            body["notes"] = notes
        return self._client._post("/dnc/entries", json=body)

    def delete_entry(self, entry_id: str) -> None:
        """Remove a DNC entry by ID.

        Args:
            entry_id: The DNC entry identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/dnc/entries/{entry_id}")

    def get_settings(self) -> Any:
        """Get the organization's DNC settings.

        Returns:
            A settings record (``protection_enabled``,
            ``auto_add_inbound_optouts``, etc.).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/dnc/settings")

    def update_settings(
        self,
        *,
        protection_enabled: bool | None = None,
        auto_add_inbound_optouts: bool | None = None,
        **extra: Any,
    ) -> Any:
        """Update the organization's DNC settings.

        Args:
            protection_enabled: If provided, toggle org-wide DNC
                protection. Calls that hit the directory are blocked
                when ``True``.
            auto_add_inbound_optouts: If provided, toggle automatic
                STOP-keyword opt-out detection.
            **extra: Additional fields forwarded to the API.

        Returns:
            The updated settings record.

        Raises:
            APIError: If the request fails.
        """
        body: dict[str, Any] = {**extra}
        if protection_enabled is not None:
            body["protection_enabled"] = protection_enabled
        if auto_add_inbound_optouts is not None:
            body["auto_add_inbound_optouts"] = auto_add_inbound_optouts
        return self._client._patch("/dnc/settings", json=body)


class AsyncDNCResource:
    """Async sibling of :class:`DNCResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def check(self, phone: str) -> Any:
        """Check whether a phone number appears in the DNC directory.

        Args:
            phone: E.164 phone number to look up.

        Returns:
            A dict with ``listed`` (bool) and originating ``source``.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/dnc/check", params={"phone": phone})

    async def list_entries(self, *, source: str | None = None, limit: int = 100) -> Any:
        """List DNC entries visible to the organization.

        Args:
            source: Optional filter by entry source.
            limit: Maximum number of entries to return.

        Returns:
            A list of DNC entry records.

        Raises:
            APIError: If the request fails.
        """
        params: dict[str, Any] = {"limit": limit}
        if source is not None:
            params["source"] = source
        return await self._client._get("/dnc/entries", params=params)

    async def add_entry(
        self,
        *,
        phone: str,
        reason: str | None = None,
        notes: str | None = None,
        **extra: Any,
    ) -> Any:
        """Add a phone number to the organization's DNC list.

        Args:
            phone: E.164 phone number to add.
            reason: Optional reason.
            notes: Optional free-form notes.
            **extra: Additional fields forwarded to the API.

        Returns:
            The created DNC entry.

        Raises:
            APIError: If the request fails.
        """
        body: dict[str, Any] = {"phone": phone, **extra}
        if reason is not None:
            body["reason"] = reason
        if notes is not None:
            body["notes"] = notes
        return await self._client._post("/dnc/entries", json=body)

    async def delete_entry(self, entry_id: str) -> None:
        """Remove a DNC entry by ID.

        Args:
            entry_id: The DNC entry identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/dnc/entries/{entry_id}")

    async def get_settings(self) -> Any:
        """Get the organization's DNC settings.

        Returns:
            A settings record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/dnc/settings")

    async def update_settings(
        self,
        *,
        protection_enabled: bool | None = None,
        auto_add_inbound_optouts: bool | None = None,
        **extra: Any,
    ) -> Any:
        """Update the organization's DNC settings.

        Args:
            protection_enabled: Toggle org-wide DNC protection.
            auto_add_inbound_optouts: Toggle STOP-keyword opt-out detection.
            **extra: Additional fields forwarded to the API.

        Returns:
            The updated settings record.

        Raises:
            APIError: If the request fails.
        """
        body: dict[str, Any] = {**extra}
        if protection_enabled is not None:
            body["protection_enabled"] = protection_enabled
        if auto_add_inbound_optouts is not None:
            body["auto_add_inbound_optouts"] = auto_add_inbound_optouts
        return await self._client._patch("/dnc/settings", json=body)
