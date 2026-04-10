from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class IntegrationsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self) -> Any:
        """List all MCP integrations for your organization."""
        return self._client._get("/integrations/mcp")

    def create(self, **body: Any) -> Any:
        """Create a new MCP integration."""
        return self._client._post("/integrations/mcp", json=body)

    def update(self, integration_id: str, **body: Any) -> Any:
        """Update an MCP integration."""
        return self._client._put(f"/integrations/mcp/{integration_id}", json=body)

    def delete(self, integration_id: str) -> None:
        """Delete an MCP integration."""
        self._client._delete(f"/integrations/mcp/{integration_id}")

    def list_tools(self, integration_id: str) -> Any:
        """List available tools for an MCP integration."""
        return self._client._get(f"/integrations/mcp/{integration_id}/tools")

    def refresh_tools(self, integration_id: str) -> Any:
        """Refresh the tool list for an MCP integration."""
        return self._client._post(f"/integrations/mcp/{integration_id}/tools")


class AsyncIntegrationsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self) -> Any:
        return await self._client._get("/integrations/mcp")

    async def create(self, **body: Any) -> Any:
        return await self._client._post("/integrations/mcp", json=body)

    async def update(self, integration_id: str, **body: Any) -> Any:
        return await self._client._put(f"/integrations/mcp/{integration_id}", json=body)

    async def delete(self, integration_id: str) -> None:
        await self._client._delete(f"/integrations/mcp/{integration_id}")

    async def list_tools(self, integration_id: str) -> Any:
        return await self._client._get(f"/integrations/mcp/{integration_id}/tools")

    async def refresh_tools(self, integration_id: str) -> Any:
        return await self._client._post(f"/integrations/mcp/{integration_id}/tools")
