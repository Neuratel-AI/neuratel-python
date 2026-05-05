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
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def check(self, phone: str) -> Any:
        return self._client._get("/dnc/check", params={"phone": phone})

    def list_entries(self, *, source: str | None = None, limit: int = 100) -> Any:
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
        body: dict[str, Any] = {"phone": phone, **extra}
        if reason is not None:
            body["reason"] = reason
        if notes is not None:
            body["notes"] = notes
        return self._client._post("/dnc/entries", json=body)

    def delete_entry(self, entry_id: str) -> None:
        self._client._delete(f"/dnc/entries/{entry_id}")

    def get_settings(self) -> Any:
        return self._client._get("/dnc/settings")

    def update_settings(
        self,
        *,
        protection_enabled: bool | None = None,
        auto_add_inbound_optouts: bool | None = None,
        **extra: Any,
    ) -> Any:
        body: dict[str, Any] = {**extra}
        if protection_enabled is not None:
            body["protection_enabled"] = protection_enabled
        if auto_add_inbound_optouts is not None:
            body["auto_add_inbound_optouts"] = auto_add_inbound_optouts
        return self._client._patch("/dnc/settings", json=body)


class AsyncDNCResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def check(self, phone: str) -> Any:
        return await self._client._get("/dnc/check", params={"phone": phone})

    async def list_entries(self, *, source: str | None = None, limit: int = 100) -> Any:
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
        body: dict[str, Any] = {"phone": phone, **extra}
        if reason is not None:
            body["reason"] = reason
        if notes is not None:
            body["notes"] = notes
        return await self._client._post("/dnc/entries", json=body)

    async def delete_entry(self, entry_id: str) -> None:
        await self._client._delete(f"/dnc/entries/{entry_id}")

    async def get_settings(self) -> Any:
        return await self._client._get("/dnc/settings")

    async def update_settings(
        self,
        *,
        protection_enabled: bool | None = None,
        auto_add_inbound_optouts: bool | None = None,
        **extra: Any,
    ) -> Any:
        body: dict[str, Any] = {**extra}
        if protection_enabled is not None:
            body["protection_enabled"] = protection_enabled
        if auto_add_inbound_optouts is not None:
            body["auto_add_inbound_optouts"] = auto_add_inbound_optouts
        return await self._client._patch("/dnc/settings", json=body)
