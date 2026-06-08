from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class CallListsResource:
    """`/v1/lists` — outbound call-list CRUD and contact management."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        """Create a new call list.

        Args:
            **body: Call-list fields (e.g. ``name``, ``description``).

        Returns:
            The created call-list record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/lists", json=body)

    def list(self, *, skip: int = 0, limit: int = 20) -> Any:
        """List call lists in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of call-list records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/lists", params={"skip": skip, "limit": limit})

    def get(self, call_list_id: str) -> Any:
        """Fetch a single call list by ID.

        Args:
            call_list_id: The call-list identifier.

        Returns:
            The call-list record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/lists/{call_list_id}")

    def update(self, call_list_id: str, **body: Any) -> Any:
        """Replace a call list's mutable fields.

        Args:
            call_list_id: The call-list identifier.
            **body: Fields to update.

        Returns:
            The updated call-list record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/lists/{call_list_id}", json=body)

    def delete(self, call_list_id: str) -> None:
        """Permanently delete a call list (and its contacts).

        Args:
            call_list_id: The call-list identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/lists/{call_list_id}")

    def bulk_import(self, call_list_id: str, file_path: str) -> Any:
        """Upload a CSV file to bulk import contacts. Pass the path to a CSV file.

        Args:
            call_list_id: The call-list identifier.
            file_path: Local path to a CSV file containing contact rows.

        Returns:
            An import summary (counts, validation errors, etc.).

        Raises:
            APIError: If the request fails.
            OSError: If the local file cannot be read.
        """
        with open(file_path, "rb") as f:
            response = self._client._http.request(
                "POST",
                f"/lists/{call_list_id}/bulk-import",
                files={"file": f},
            )
        from .._base_client import _raise_for_status

        _raise_for_status(response)
        return response.json()

    def add_contact(self, call_list_id: str, **body: Any) -> Any:
        """Append a single contact to a call list.

        Args:
            call_list_id: The call-list identifier.
            **body: Contact fields (e.g. ``phone``, ``first_name``,
                ``custom_variables``).

        Returns:
            The created contact record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/lists/{call_list_id}/contacts", json=body)

    def list_contacts(self, call_list_id: str, *, skip: int = 0, limit: int = 50) -> Any:
        """List contacts belonging to a call list.

        Args:
            call_list_id: The call-list identifier.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of contact records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(
            f"/lists/{call_list_id}/contacts", params={"skip": skip, "limit": limit}
        )

    def update_contact(self, call_list_id: str, contact_id: str, **body: Any) -> Any:
        """Replace a contact's mutable fields.

        Args:
            call_list_id: The call-list identifier.
            contact_id: The contact identifier.
            **body: Fields to update.

        Returns:
            The updated contact record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/lists/{call_list_id}/contacts/{contact_id}", json=body)

    def delete_contact(self, call_list_id: str, contact_id: str) -> None:
        """Remove a contact from a call list.

        Args:
            call_list_id: The call-list identifier.
            contact_id: The contact identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/lists/{call_list_id}/contacts/{contact_id}")


class AsyncCallListsResource:
    """Async sibling of :class:`CallListsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        """Create a new call list.

        Args:
            **body: Call-list fields (e.g. ``name``, ``description``).

        Returns:
            The created call-list record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/lists", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20) -> Any:
        """List call lists in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of call-list records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/lists", params={"skip": skip, "limit": limit})

    async def get(self, call_list_id: str) -> Any:
        """Fetch a single call list by ID.

        Args:
            call_list_id: The call-list identifier.

        Returns:
            The call-list record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/lists/{call_list_id}")

    async def update(self, call_list_id: str, **body: Any) -> Any:
        """Replace a call list's mutable fields.

        Args:
            call_list_id: The call-list identifier.
            **body: Fields to update.

        Returns:
            The updated call-list record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/lists/{call_list_id}", json=body)

    async def delete(self, call_list_id: str) -> None:
        """Permanently delete a call list (and its contacts).

        Args:
            call_list_id: The call-list identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/lists/{call_list_id}")

    async def bulk_import(self, call_list_id: str, file_path: str) -> Any:
        """Upload a CSV file to bulk import contacts.

        Args:
            call_list_id: The call-list identifier.
            file_path: Local path to a CSV file containing contact rows.

        Returns:
            An import summary (counts, validation errors, etc.).

        Raises:
            APIError: If the request fails.
            OSError: If the local file cannot be read.
        """
        import asyncio

        file_bytes = await asyncio.to_thread(self._read_file, file_path)
        response = await self._client._http.request(
            "POST",
            f"/lists/{call_list_id}/bulk-import",
            files={"file": ("contacts.csv", file_bytes)},
        )
        from .._base_client import _raise_for_status

        _raise_for_status(response)
        return response.json()

    @staticmethod
    def _read_file(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    async def add_contact(self, call_list_id: str, **body: Any) -> Any:
        """Append a single contact to a call list.

        Args:
            call_list_id: The call-list identifier.
            **body: Contact fields (e.g. ``phone``, ``first_name``,
                ``custom_variables``).

        Returns:
            The created contact record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/lists/{call_list_id}/contacts", json=body)

    async def list_contacts(self, call_list_id: str, *, skip: int = 0, limit: int = 50) -> Any:
        """List contacts belonging to a call list.

        Args:
            call_list_id: The call-list identifier.
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A page of contact records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(
            f"/lists/{call_list_id}/contacts", params={"skip": skip, "limit": limit}
        )

    async def update_contact(self, call_list_id: str, contact_id: str, **body: Any) -> Any:
        """Replace a contact's mutable fields.

        Args:
            call_list_id: The call-list identifier.
            contact_id: The contact identifier.
            **body: Fields to update.

        Returns:
            The updated contact record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/lists/{call_list_id}/contacts/{contact_id}", json=body)

    async def delete_contact(self, call_list_id: str, contact_id: str) -> None:
        """Remove a contact from a call list.

        Args:
            call_list_id: The call-list identifier.
            contact_id: The contact identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/lists/{call_list_id}/contacts/{contact_id}")
