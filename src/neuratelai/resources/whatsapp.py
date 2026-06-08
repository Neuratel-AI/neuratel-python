from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class WhatsappResource:
    """`/v1/whatsapp` — WhatsApp Business account management, templates, and outbound messaging."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    # ---- Accounts ----

    def list_accounts(self, *, agent_id: str | None = None) -> Any:
        """List WhatsApp Business accounts, optionally filtered by agent.

        Args:
            agent_id: Optional agent identifier to filter accounts by.

        Returns:
            A list of WhatsApp account records.

        Raises:
            APIError: If the request fails.
        """
        params = {"agent_id": agent_id} if agent_id else None
        return self._client._get("/whatsapp/accounts", params=params)

    def import_account(self, **body: Any) -> Any:
        """Import a WhatsApp Business account via the OAuth flow.

        Args:
            **body: OAuth-flow fields (e.g. ``code``, ``redirect_uri``,
                ``state``).

        Returns:
            The imported account record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/accounts/import", json=body)

    def import_account_manual(self, **body: Any) -> Any:
        """Import a WhatsApp Business account by manually providing credentials.

        Args:
            **body: Account credentials and metadata (e.g.
                ``phone_number_id``, ``business_account_id``, ``access_token``).

        Returns:
            The imported account record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/accounts/import-manual", json=body)

    def get_account(self, phone_number_id: str) -> Any:
        """Get a single WhatsApp account by its phone number ID.

        Args:
            phone_number_id: The WhatsApp phone number identifier.

        Returns:
            The account record (phone number, display name, status,
            quality rating, etc.).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/whatsapp/accounts/{phone_number_id}")

    def update_account(self, phone_number_id: str, **body: Any) -> Any:
        """Update a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            **body: Fields to update (e.g. ``agent_id``, ``webhook_url``).

        Returns:
            The updated account record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._patch(f"/whatsapp/accounts/{phone_number_id}", json=body)

    def delete_account(self, phone_number_id: str) -> None:
        """Delete a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/whatsapp/accounts/{phone_number_id}")

    # ---- Per-account sub-resources ----

    def list_templates(self, phone_number_id: str, *, status: str | None = None) -> Any:
        """List message templates for a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            status: Optional filter (e.g. ``"APPROVED"``,
                ``"PENDING"``, ``"REJECTED"``).

        Returns:
            A list of template records.

        Raises:
            APIError: If the request fails.
        """
        params = {"status": status} if status else None
        return self._client._get(f"/whatsapp/accounts/{phone_number_id}/templates", params=params)

    def check_call_permission(self, phone_number_id: str, *, user_wa_id: str) -> Any:
        """Check whether a WhatsApp user has granted call permissions.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            user_wa_id: The recipient's WhatsApp user ID.

        Returns:
            A permission record (``allowed`` bool, expiry, etc.).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(
            f"/whatsapp/accounts/{phone_number_id}/call-permissions",
            params={"user_wa_id": user_wa_id},
        )

    def get_call_status(self, phone_number_id: str, intent_id: str) -> Any:
        """Get the status of a WhatsApp call by intent ID.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            intent_id: The call intent identifier returned by
                :meth:`send_outbound_call`.

        Returns:
            A call-status record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/whatsapp/accounts/{phone_number_id}/calls/{intent_id}")

    def verify_account(self, phone_number_id: str) -> Any:
        """Run a health/verification check on a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.

        Returns:
            A verification report.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/whatsapp/accounts/{phone_number_id}/verify")

    # ---- Outbound ----

    def send_outbound_call(self, **body: Any) -> Any:
        """Initiate a WhatsApp outbound call.

        Args:
            **body: Call fields (e.g. ``agent_id``, ``to``,
                ``dynamic_variables``).

        Returns:
            The call intent (use ``intent_id`` with
            :meth:`get_call_status` to poll).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/outbound-call", json=body)

    def send_outbound_message(self, **body: Any) -> Any:
        """Send a WhatsApp outbound message (template or freeform).

        Args:
            **body: Message fields (e.g. ``agent_id``, ``to``,
                ``template``, ``variables``, ``type``).

        Returns:
            The sent message record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/outbound-message", json=body)

    def send_outbound_text(self, **body: Any) -> Any:
        """Send a WhatsApp outbound text message.

        Args:
            **body: Text-message fields (e.g. ``agent_id``, ``to``,
                ``body``).

        Returns:
            The sent message record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/outbound-text", json=body)

    def send_outbound_voice(self, **body: Any) -> Any:
        """Send a WhatsApp outbound voice note.

        Args:
            **body: Voice-note fields (e.g. ``agent_id``, ``to``,
                ``media_url``).

        Returns:
            The sent message record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/outbound-voice", json=body)

    def batch_call(self, **body: Any) -> Any:
        """Initiate a batch of WhatsApp outbound calls.

        Args:
            **body: Batch fields (e.g. ``agent_id``, ``contacts``,
                ``scheduled_at``).

        Returns:
            The batch job record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/whatsapp/batch-call", json=body)

    # ---- Media ----

    def get_message_media(self, message_id: str) -> Any:
        """Proxy WhatsApp media for a specific message.

        Args:
            message_id: The message identifier whose media to fetch.

        Returns:
            The media binary/redirect (see API for response shape).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/whatsapp/messages/{message_id}/media")


class AsyncWhatsappResource:
    """Async sibling of :class:`WhatsappResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    # ---- Accounts ----

    async def list_accounts(self, *, agent_id: str | None = None) -> Any:
        """List WhatsApp Business accounts, optionally filtered by agent.

        Args:
            agent_id: Optional agent identifier to filter accounts by.

        Returns:
            A list of WhatsApp account records.

        Raises:
            APIError: If the request fails.
        """
        params = {"agent_id": agent_id} if agent_id else None
        return await self._client._get("/whatsapp/accounts", params=params)

    async def import_account(self, **body: Any) -> Any:
        """Import a WhatsApp Business account via the OAuth flow.

        Args:
            **body: OAuth-flow fields.

        Returns:
            The imported account record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/accounts/import", json=body)

    async def import_account_manual(self, **body: Any) -> Any:
        """Import a WhatsApp Business account by manually providing credentials.

        Args:
            **body: Account credentials and metadata.

        Returns:
            The imported account record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/accounts/import-manual", json=body)

    async def get_account(self, phone_number_id: str) -> Any:
        """Get a single WhatsApp account by its phone number ID.

        Args:
            phone_number_id: The WhatsApp phone number identifier.

        Returns:
            The account record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/whatsapp/accounts/{phone_number_id}")

    async def update_account(self, phone_number_id: str, **body: Any) -> Any:
        """Update a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            **body: Fields to update.

        Returns:
            The updated account record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._patch(f"/whatsapp/accounts/{phone_number_id}", json=body)

    async def delete_account(self, phone_number_id: str) -> None:
        """Delete a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/whatsapp/accounts/{phone_number_id}")

    # ---- Per-account sub-resources ----

    async def list_templates(self, phone_number_id: str, *, status: str | None = None) -> Any:
        """List message templates for a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            status: Optional filter (e.g. ``"APPROVED"``,
                ``"PENDING"``, ``"REJECTED"``).

        Returns:
            A list of template records.

        Raises:
            APIError: If the request fails.
        """
        params = {"status": status} if status else None
        return await self._client._get(
            f"/whatsapp/accounts/{phone_number_id}/templates", params=params
        )

    async def check_call_permission(self, phone_number_id: str, *, user_wa_id: str) -> Any:
        """Check whether a WhatsApp user has granted call permissions.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            user_wa_id: The recipient's WhatsApp user ID.

        Returns:
            A permission record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(
            f"/whatsapp/accounts/{phone_number_id}/call-permissions",
            params={"user_wa_id": user_wa_id},
        )

    async def get_call_status(self, phone_number_id: str, intent_id: str) -> Any:
        """Get the status of a WhatsApp call by intent ID.

        Args:
            phone_number_id: The WhatsApp phone number identifier.
            intent_id: The call intent identifier.

        Returns:
            A call-status record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/whatsapp/accounts/{phone_number_id}/calls/{intent_id}")

    async def verify_account(self, phone_number_id: str) -> Any:
        """Run a health/verification check on a WhatsApp account.

        Args:
            phone_number_id: The WhatsApp phone number identifier.

        Returns:
            A verification report.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/whatsapp/accounts/{phone_number_id}/verify")

    # ---- Outbound ----

    async def send_outbound_call(self, **body: Any) -> Any:
        """Initiate a WhatsApp outbound call.

        Args:
            **body: Call fields.

        Returns:
            The call intent record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/outbound-call", json=body)

    async def send_outbound_message(self, **body: Any) -> Any:
        """Send a WhatsApp outbound message (template or freeform).

        Args:
            **body: Message fields.

        Returns:
            The sent message record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/outbound-message", json=body)

    async def send_outbound_text(self, **body: Any) -> Any:
        """Send a WhatsApp outbound text message.

        Args:
            **body: Text-message fields.

        Returns:
            The sent message record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/outbound-text", json=body)

    async def send_outbound_voice(self, **body: Any) -> Any:
        """Send a WhatsApp outbound voice note.

        Args:
            **body: Voice-note fields.

        Returns:
            The sent message record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/outbound-voice", json=body)

    async def batch_call(self, **body: Any) -> Any:
        """Initiate a batch of WhatsApp outbound calls.

        Args:
            **body: Batch fields.

        Returns:
            The batch job record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/whatsapp/batch-call", json=body)

    # ---- Media ----

    async def get_message_media(self, message_id: str) -> Any:
        """Proxy WhatsApp media for a specific message.

        Args:
            message_id: The message identifier whose media to fetch.

        Returns:
            The media payload.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/whatsapp/messages/{message_id}/media")
