from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class AgentsResource:
    """`/v1/agents` — agent CRUD, version history, and live-call helpers."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        """Create a new agent.

        Args:
            **body: Agent fields forwarded as the JSON request body (e.g.
                ``name``, ``brain``, ``voice``).

        Returns:
            The created agent as returned by the API.

        Raises:
            APIError: If the request fails (validation, auth, server error).
        """
        return self._client._post("/agents", json=body)

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        """List agents in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            A ``SyncPage`` yielding agent dicts with pagination metadata.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/agents", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/agents",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, agent_id: str) -> Any:
        """Fetch a single agent by ID.

        Args:
            agent_id: The agent identifier.

        Returns:
            The agent record.

        Raises:
            APIError: If the request fails (e.g. 404 NotFoundError).
        """
        return self._client._get(f"/agents/{agent_id}")

    def update(self, agent_id: str, **body: Any) -> Any:
        """Patch an agent's mutable fields.

        Args:
            agent_id: The agent identifier.
            **body: Fields to update.

        Returns:
            The updated agent record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._patch(f"/agents/{agent_id}", json=body)

    def delete(self, agent_id: str) -> None:
        """Permanently delete an agent.

        Args:
            agent_id: The agent identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/agents/{agent_id}")

    def duplicate(self, agent_id: str, *, new_name: str | None = None) -> Any:
        """Clone an agent and return the new agent's record.

        Args:
            agent_id: The source agent to duplicate.
            new_name: Optional name for the cloned agent. If omitted, the
                server picks a default.

        Returns:
            The newly created agent record.

        Raises:
            APIError: If the request fails.
        """
        params = {"new_name": new_name} if new_name else None
        return self._client._post(f"/agents/{agent_id}/duplicate", params=params)

    def web_call(self, agent_id: str, **body: Any) -> Any:
        """Start a WebRTC browser call. Returns token + server_url + session_id.

        Args:
            agent_id: The agent to connect the browser to.
            **body: Web call configuration (e.g. ``dynamic_variables``).

        Returns:
            A dict containing ``token``, ``server_url``, and ``session_id``.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/agents/{agent_id}/web-call", json=body)

    def list_versions(self, agent_id: str) -> Any:
        """List all saved versions of an agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            A list of version records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/agents/{agent_id}/versions")

    def get_version(self, agent_id: str, version: int) -> Any:
        """Get a specific version snapshot of an agent.

        Args:
            agent_id: The agent identifier.
            version: The version number to fetch.

        Returns:
            The version record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/agents/{agent_id}/versions/{version}")

    def restore_version(self, agent_id: str, version: int) -> Any:
        """Restore an agent to a previously saved version.

        Args:
            agent_id: The agent identifier.
            version: The version number to restore.

        Returns:
            The restored agent record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/agents/{agent_id}/versions/{version}/restore")

    def templates(self) -> Any:
        """List the platform's pre-built agent templates (read-only catalog).

        Returns:
            A list of template records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/agents/templates")

    def required_variables(self, agent_id: str) -> Any:
        """List the ``{{variable}}`` placeholders an agent requires at call time.

        Returns the system catalog plus any user-defined names the agent's
        prompt references — useful for validating dynamic_variables payloads
        before placing an outbound call.

        Args:
            agent_id: The agent identifier.

        Returns:
            A list of required variable names and metadata.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/agents/{agent_id}/required-variables")


class AsyncAgentsResource:
    """Async sibling of :class:`AgentsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        """Create a new agent.

        Args:
            **body: Agent fields forwarded as the JSON request body.

        Returns:
            The created agent as returned by the API.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/agents", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        """List agents in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            An ``AsyncPage`` yielding agent dicts with pagination metadata.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get("/agents", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/agents",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, agent_id: str) -> Any:
        """Fetch a single agent by ID.

        Args:
            agent_id: The agent identifier.

        Returns:
            The agent record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/agents/{agent_id}")

    async def update(self, agent_id: str, **body: Any) -> Any:
        """Patch an agent's mutable fields.

        Args:
            agent_id: The agent identifier.
            **body: Fields to update.

        Returns:
            The updated agent record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._patch(f"/agents/{agent_id}", json=body)

    async def delete(self, agent_id: str) -> None:
        """Permanently delete an agent.

        Args:
            agent_id: The agent identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/agents/{agent_id}")

    async def duplicate(self, agent_id: str, *, new_name: str | None = None) -> Any:
        """Clone an agent and return the new agent's record.

        Args:
            agent_id: The source agent to duplicate.
            new_name: Optional name for the cloned agent.

        Returns:
            The newly created agent record.

        Raises:
            APIError: If the request fails.
        """
        params = {"new_name": new_name} if new_name else None
        return await self._client._post(f"/agents/{agent_id}/duplicate", params=params)

    async def web_call(self, agent_id: str, **body: Any) -> Any:
        """Start a WebRTC browser call. Returns token + server_url + session_id.

        Args:
            agent_id: The agent to connect the browser to.
            **body: Web call configuration (e.g. ``dynamic_variables``).

        Returns:
            A dict containing ``token``, ``server_url``, and ``session_id``.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/agents/{agent_id}/web-call", json=body)

    async def list_versions(self, agent_id: str) -> Any:
        """List all saved versions of an agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            A list of version records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/agents/{agent_id}/versions")

    async def get_version(self, agent_id: str, version: int) -> Any:
        """Get a specific version snapshot of an agent.

        Args:
            agent_id: The agent identifier.
            version: The version number to fetch.

        Returns:
            The version record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/agents/{agent_id}/versions/{version}")

    async def restore_version(self, agent_id: str, version: int) -> Any:
        """Restore an agent to a previously saved version.

        Args:
            agent_id: The agent identifier.
            version: The version number to restore.

        Returns:
            The restored agent record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/agents/{agent_id}/versions/{version}/restore")

    async def templates(self) -> Any:
        """List the platform's pre-built agent templates (read-only catalog).

        Returns:
            A list of template records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/agents/templates")

    async def required_variables(self, agent_id: str) -> Any:
        """List the ``{{variable}}`` placeholders an agent requires at call time.

        Args:
            agent_id: The agent identifier.

        Returns:
            A list of required variable names and metadata.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/agents/{agent_id}/required-variables")
