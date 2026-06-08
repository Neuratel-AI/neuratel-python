from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class IntegrationsResource:
    """`/v1/mcp-servers` and `/v1/auth-connections` — MCP + auth-connection management."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self) -> Any:
        """List all MCP servers for your organization.

        Returns:
            A list of MCP-server records.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/mcp-servers")

    def create(self, **body: Any) -> Any:
        """Create a new MCP server.

        Args:
            **body: MCP-server fields (e.g. ``name``, ``url``,
                ``transport``).

        Returns:
            The created MCP-server record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/mcp-servers", json=body)

    def update(self, integration_id: str, **body: Any) -> Any:
        """Update an MCP server.

        Args:
            integration_id: The MCP-server identifier.
            **body: Fields to update.

        Returns:
            The updated MCP-server record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/mcp-servers/{integration_id}", json=body)

    def delete(self, integration_id: str) -> None:
        """Delete an MCP server.

        Args:
            integration_id: The MCP-server identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/mcp-servers/{integration_id}")

    def list_tools(self, integration_id: str) -> Any:
        """List available tools for an MCP server.

        Args:
            integration_id: The MCP-server identifier.

        Returns:
            A list of tool definitions (name, description, input schema).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/mcp-servers/{integration_id}/tools")

    def refresh_tools(self, integration_id: str) -> Any:
        """Refresh the tool list for an MCP server.

        Forces the platform to re-query the upstream MCP server's tool
        catalog and persist the latest list.

        Args:
            integration_id: The MCP-server identifier.

        Returns:
            The refreshed tool list.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/mcp-servers/{integration_id}/tools")

    def list_connections(self) -> Any:
        """List auth connections (credential vault for MCP integrations).

        Returns:
            A list of auth-connection records (no secrets — metadata only).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get("/auth-connections")

    def create_connection(self, **body: Any) -> Any:
        """Create an auth connection for MCP integrations.

        Args:
            **body: Connection fields (e.g. ``name``, ``provider``,
                ``credentials``).

        Returns:
            The created auth-connection record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/auth-connections", json=body)

    def update_connection(self, auth_id: str, **body: Any) -> Any:
        """Update an auth connection.

        Args:
            auth_id: The auth-connection identifier.
            **body: Fields to update.

        Returns:
            The updated auth-connection record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/auth-connections/{auth_id}", json=body)

    def delete_connection(self, auth_id: str) -> None:
        """Delete an auth connection.

        Args:
            auth_id: The auth-connection identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/auth-connections/{auth_id}")


class AsyncIntegrationsResource:
    """Async sibling of :class:`IntegrationsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self) -> Any:
        """List all MCP servers for your organization.

        Returns:
            A list of MCP-server records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/mcp-servers")

    async def create(self, **body: Any) -> Any:
        """Create a new MCP server.

        Args:
            **body: MCP-server fields.

        Returns:
            The created MCP-server record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/mcp-servers", json=body)

    async def update(self, integration_id: str, **body: Any) -> Any:
        """Update an MCP server.

        Args:
            integration_id: The MCP-server identifier.
            **body: Fields to update.

        Returns:
            The updated MCP-server record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/mcp-servers/{integration_id}", json=body)

    async def delete(self, integration_id: str) -> None:
        """Delete an MCP server.

        Args:
            integration_id: The MCP-server identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/mcp-servers/{integration_id}")

    async def list_tools(self, integration_id: str) -> Any:
        """List available tools for an MCP server.

        Args:
            integration_id: The MCP-server identifier.

        Returns:
            A list of tool definitions.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/mcp-servers/{integration_id}/tools")

    async def refresh_tools(self, integration_id: str) -> Any:
        """Refresh the tool list for an MCP server.

        Args:
            integration_id: The MCP-server identifier.

        Returns:
            The refreshed tool list.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/mcp-servers/{integration_id}/tools")

    async def list_connections(self) -> Any:
        """List auth connections (credential vault for MCP integrations).

        Returns:
            A list of auth-connection records.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get("/auth-connections")

    async def create_connection(self, **body: Any) -> Any:
        """Create an auth connection for MCP integrations.

        Args:
            **body: Connection fields.

        Returns:
            The created auth-connection record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/auth-connections", json=body)

    async def update_connection(self, auth_id: str, **body: Any) -> Any:
        """Update an auth connection.

        Args:
            auth_id: The auth-connection identifier.
            **body: Fields to update.

        Returns:
            The updated auth-connection record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/auth-connections/{auth_id}", json=body)

    async def delete_connection(self, auth_id: str) -> None:
        """Delete an auth connection.

        Args:
            auth_id: The auth-connection identifier.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._delete(f"/auth-connections/{auth_id}")
