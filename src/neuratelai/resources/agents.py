from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class AgentsResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        return self._client._post("/agents", json=body)

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        data = self._client._get("/agents", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/agents",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, agent_id: str) -> Any:
        return self._client._get(f"/agents/{agent_id}")

    def update(self, agent_id: str, **body: Any) -> Any:
        return self._client._patch(f"/agents/{agent_id}", json=body)

    def delete(self, agent_id: str) -> None:
        self._client._delete(f"/agents/{agent_id}")

    def duplicate(self, agent_id: str, *, new_name: str | None = None) -> Any:
        params = {"new_name": new_name} if new_name else None
        return self._client._post(f"/agents/{agent_id}/duplicate", params=params)

    def web_call(self, agent_id: str, **body: Any) -> Any:
        """Start a WebRTC browser call. Returns token + server_url + session_id."""
        return self._client._post(f"/agents/{agent_id}/web-call", json=body)

    def list_versions(self, agent_id: str) -> Any:
        return self._client._get(f"/agents/{agent_id}/versions")

    def get_version(self, agent_id: str, version: int) -> Any:
        return self._client._get(f"/agents/{agent_id}/versions/{version}")

    def restore_version(self, agent_id: str, version: int) -> Any:
        return self._client._post(f"/agents/{agent_id}/versions/{version}/restore")

    def templates(self) -> Any:
        """List the platform's pre-built agent templates (read-only catalog)."""
        return self._client._get("/agents/templates")

    def required_variables(self, agent_id: str) -> Any:
        """List the {{variable}} placeholders an agent requires at call time.

        Returns the system catalog plus any user-defined names the agent's
        prompt references — useful for validating dynamic_variables payloads
        before placing an outbound call.
        """
        return self._client._get(f"/agents/{agent_id}/required-variables")


class AsyncAgentsResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        return await self._client._post("/agents", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        data = await self._client._get("/agents", params={"skip": skip, "limit": limit, **params})
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/agents",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, agent_id: str) -> Any:
        return await self._client._get(f"/agents/{agent_id}")

    async def update(self, agent_id: str, **body: Any) -> Any:
        return await self._client._patch(f"/agents/{agent_id}", json=body)

    async def delete(self, agent_id: str) -> None:
        await self._client._delete(f"/agents/{agent_id}")

    async def duplicate(self, agent_id: str, *, new_name: str | None = None) -> Any:
        params = {"new_name": new_name} if new_name else None
        return await self._client._post(f"/agents/{agent_id}/duplicate", params=params)

    async def web_call(self, agent_id: str, **body: Any) -> Any:
        return await self._client._post(f"/agents/{agent_id}/web-call", json=body)

    async def list_versions(self, agent_id: str) -> Any:
        return await self._client._get(f"/agents/{agent_id}/versions")

    async def get_version(self, agent_id: str, version: int) -> Any:
        return await self._client._get(f"/agents/{agent_id}/versions/{version}")

    async def restore_version(self, agent_id: str, version: int) -> Any:
        return await self._client._post(f"/agents/{agent_id}/versions/{version}/restore")

    async def templates(self) -> Any:
        """List the platform's pre-built agent templates (read-only catalog)."""
        return await self._client._get("/agents/templates")

    async def required_variables(self, agent_id: str) -> Any:
        """List the {{variable}} placeholders an agent requires at call time."""
        return await self._client._get(f"/agents/{agent_id}/required-variables")
