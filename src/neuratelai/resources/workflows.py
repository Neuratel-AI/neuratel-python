from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class WorkflowsResource:
    """`/v1/workflows` — visual workflow definitions with graph revisions and publish lifecycle."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def create(self, **body: Any) -> Any:
        """Create a new workflow.

        Args:
            **body: Workflow fields (e.g. ``name``, ``description``,
                ``trigger``).

        Returns:
            The created workflow record (in draft state — call
            :meth:`save_graph` to attach a graph).

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/workflows", json=body)

    def list(self, *, skip: int = 0, limit: int = 20) -> SyncPage:
        """List workflows in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            A ``SyncPage`` yielding workflow records.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/workflows", params={"skip": skip, "limit": limit})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/workflows",
            params={"skip": skip, "limit": limit},
        )

    def get(self, workflow_id: str) -> Any:
        """Get a workflow with its full version history.

        Args:
            workflow_id: The workflow identifier.

        Returns:
            The workflow record including all graph revisions.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/workflows/{workflow_id}")

    def update(self, workflow_id: str, **body: Any) -> Any:
        """Update a workflow's metadata (not its graph).

        Use :meth:`save_graph` to add a new graph revision.

        Args:
            workflow_id: The workflow identifier.
            **body: Metadata fields to update (e.g. ``name``,
                ``description``).

        Returns:
            The updated workflow record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._patch(f"/workflows/{workflow_id}", json=body)

    def delete(self, workflow_id: str) -> None:
        """Delete a workflow and all of its revisions.

        Args:
            workflow_id: The workflow identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/workflows/{workflow_id}")

    def save_graph(self, workflow_id: str, **body: Any) -> Any:
        """Save a new graph revision on a workflow (draft).

        Args:
            workflow_id: The workflow identifier.
            **body: Graph fields (e.g. ``nodes``, ``edges``,
                ``entry_node_id``).

        Returns:
            The newly created graph revision record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/workflows/{workflow_id}/graph", json=body)

    def publish(self, workflow_id: str, **body: Any) -> Any:
        """Publish a workflow revision.

        Args:
            workflow_id: The workflow identifier.
            **body: Optional publish fields (e.g. ``revision_id``,
                ``notes``).

        Returns:
            The published workflow record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post(f"/workflows/{workflow_id}/publish", json=body)


class AsyncWorkflowsResource:
    """Async sibling of :class:`WorkflowsResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def create(self, **body: Any) -> Any:
        """Create a new workflow.

        Args:
            **body: Workflow fields.

        Returns:
            The created workflow record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/workflows", json=body)

    async def list(self, *, skip: int = 0, limit: int = 20) -> AsyncPage:
        """List workflows in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.

        Returns:
            An ``AsyncPage`` yielding workflow records.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get(
            "/workflows", params={"skip": skip, "limit": limit}
        )
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/workflows",
            params={"skip": skip, "limit": limit},
        )

    async def get(self, workflow_id: str) -> Any:
        """Get a workflow with its full version history.

        Args:
            workflow_id: The workflow identifier.

        Returns:
            The workflow record including all graph revisions.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/workflows/{workflow_id}")

    async def update(self, workflow_id: str, **body: Any) -> Any:
        """Update a workflow's metadata (not its graph).

        Args:
            workflow_id: The workflow identifier.
            **body: Metadata fields to update.

        Returns:
            The updated workflow record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._patch(f"/workflows/{workflow_id}", json=body)

    async def delete(self, workflow_id: str) -> None:
        """Delete a workflow and all of its revisions.

        Args:
            workflow_id: The workflow identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/workflows/{workflow_id}")

    async def save_graph(self, workflow_id: str, **body: Any) -> Any:
        """Save a new graph revision on a workflow (draft).

        Args:
            workflow_id: The workflow identifier.
            **body: Graph fields.

        Returns:
            The newly created graph revision record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/workflows/{workflow_id}/graph", json=body)

    async def publish(self, workflow_id: str, **body: Any) -> Any:
        """Publish a workflow revision.

        Args:
            workflow_id: The workflow identifier.
            **body: Optional publish fields.

        Returns:
            The published workflow record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(f"/workflows/{workflow_id}/publish", json=body)
