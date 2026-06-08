from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class KnowledgeBaseResource:
    """`/v1/knowledge-base` — KB CRUD, ingestion (file/url/text), and agent binding."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        """List knowledge-base sources in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            A ``SyncPage`` yielding KB source records.

        Raises:
            APIError: If the request fails.
        """
        data = self._client._get("/knowledge-base", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/knowledge-base",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, kb_id: str) -> Any:
        """Fetch a single knowledge-base source by ID.

        Args:
            kb_id: The knowledge-base identifier.

        Returns:
            The KB source record (status, document count, etc.).

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/knowledge-base/{kb_id}")

    def update(self, kb_id: str, **body: Any) -> Any:
        """Replace a knowledge-base source's mutable fields.

        Args:
            kb_id: The knowledge-base identifier.
            **body: Fields to update (e.g. ``name``, ``description``).

        Returns:
            The updated KB source record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._put(f"/knowledge-base/{kb_id}", json=body)

    def delete(self, kb_id: str) -> None:
        """Permanently delete a knowledge-base source.

        Args:
            kb_id: The knowledge-base identifier.

        Raises:
            APIError: If the request fails.
        """
        self._client._delete(f"/knowledge-base/{kb_id}")

    def from_file(self, file_path: str, *, name: str | None = None) -> Any:
        """Upload a file (PDF, DOCX, TXT) as a knowledge base source.

        Args:
            file_path: Local path to the file to upload.
            name: Optional display name. Defaults to the file's basename.

        Returns:
            The created KB source record (server will then ingest the
            document asynchronously).

        Raises:
            APIError: If the request fails.
            OSError: If the local file cannot be read.
        """
        import os

        filename = name or os.path.basename(file_path)
        with open(file_path, "rb") as f:
            response = self._client._http.request(
                "POST",
                "/knowledge-base/from-file",
                data={"name": filename},
                files={"file": (filename, f)},
            )
        from .._base_client import _raise_for_status

        _raise_for_status(response)
        return response.json()

    def from_url(self, url: str, **body: Any) -> Any:
        """Ingest a knowledge-base source from a public URL.

        Args:
            url: The URL to fetch and ingest.
            **body: Additional ingestion options (e.g. ``name``,
                ``refresh_interval``).

        Returns:
            The created KB source record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/knowledge-base/from-url", json={"url": url, **body})

    def from_text(self, text: str, **body: Any) -> Any:
        """Ingest a knowledge-base source from raw text.

        Args:
            text: The text content to ingest.
            **body: Additional ingestion options (e.g. ``name``).

        Returns:
            The created KB source record.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/knowledge-base/from-text", json={"content": text, **body})

    def query(self, query: str, **body: Any) -> Any:
        """Run a semantic query against the knowledge base.

        Args:
            query: The natural-language query string.
            **body: Additional query options (e.g. ``top_k``,
                ``agent_id``, ``min_score``).

        Returns:
            A list of matching chunks with scores and source metadata.

        Raises:
            APIError: If the request fails.
        """
        return self._client._post("/knowledge-base/query", json={"query": query, **body})

    def list_for_agent(self, agent_id: str) -> Any:
        """List KB sources currently bound to an agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            A list of KB source records bound to the agent.

        Raises:
            APIError: If the request fails.
        """
        return self._client._get(f"/knowledge-base/agent/{agent_id}")

    def assign_to_agent(self, agent_id: str, *, knowledge_base_ids: Any) -> Any:
        """Replace the KB sources bound to an agent.

        Args:
            agent_id: The agent identifier.
            knowledge_base_ids: Full list of KB source IDs the agent
                should be bound to (replaces any existing bindings).

        Returns:
            The updated agent record (with ``knowledge_base_ids``).

        Raises:
            APIError: If the request fails.
        """
        # `Any` (not `list[str]`) because mypy resolves the inner `list` as the
        # class-level `def list()` method, not the builtin. Real typing lands
        # in Phase 1D's _generated.py models.
        return self._client._put(
            f"/knowledge-base/agent/{agent_id}", json={"knowledge_base_ids": knowledge_base_ids}
        )


class AsyncKnowledgeBaseResource:
    """Async sibling of :class:`KnowledgeBaseResource`."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
        """List knowledge-base sources in the organization.

        Args:
            skip: Number of items to skip for pagination.
            limit: Maximum number of items per page.
            **params: Additional query parameters forwarded to the API.

        Returns:
            An ``AsyncPage`` yielding KB source records.

        Raises:
            APIError: If the request fails.
        """
        data = await self._client._get(
            "/knowledge-base", params={"skip": skip, "limit": limit, **params}
        )
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/knowledge-base",
            params={"skip": skip, "limit": limit, **params},
        )

    async def get(self, kb_id: str) -> Any:
        """Fetch a single knowledge-base source by ID.

        Args:
            kb_id: The knowledge-base identifier.

        Returns:
            The KB source record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/knowledge-base/{kb_id}")

    async def update(self, kb_id: str, **body: Any) -> Any:
        """Replace a knowledge-base source's mutable fields.

        Args:
            kb_id: The knowledge-base identifier.
            **body: Fields to update.

        Returns:
            The updated KB source record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(f"/knowledge-base/{kb_id}", json=body)

    async def delete(self, kb_id: str) -> None:
        """Permanently delete a knowledge-base source.

        Args:
            kb_id: The knowledge-base identifier.

        Raises:
            APIError: If the request fails.
        """
        await self._client._delete(f"/knowledge-base/{kb_id}")

    async def from_file(self, file_path: str, *, name: str | None = None) -> Any:
        """Upload a file (PDF, DOCX, TXT) as a knowledge base source.

        Args:
            file_path: Local path to the file to upload.
            name: Optional display name. Defaults to the file's basename.

        Returns:
            The created KB source record.

        Raises:
            APIError: If the request fails.
            OSError: If the local file cannot be read.
        """
        import asyncio
        import os

        filename = name or os.path.basename(file_path)
        file_bytes = await asyncio.to_thread(self._read_file, file_path)
        response = await self._client._http.request(
            "POST",
            "/knowledge-base/from-file",
            data={"name": filename},
            files={"file": (filename, file_bytes)},
        )
        from .._base_client import _raise_for_status

        _raise_for_status(response)
        return response.json()

    @staticmethod
    def _read_file(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    async def from_url(self, url: str, **body: Any) -> Any:
        """Ingest a knowledge-base source from a public URL.

        Args:
            url: The URL to fetch and ingest.
            **body: Additional ingestion options.

        Returns:
            The created KB source record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post("/knowledge-base/from-url", json={"url": url, **body})

    async def from_text(self, text: str, **body: Any) -> Any:
        """Ingest a knowledge-base source from raw text.

        Args:
            text: The text content to ingest.
            **body: Additional ingestion options.

        Returns:
            The created KB source record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(
            "/knowledge-base/from-text", json={"content": text, **body}
        )

    async def query(self, query: str, **body: Any) -> Any:
        """Run a semantic query against the knowledge base.

        Args:
            query: The natural-language query string.
            **body: Additional query options (e.g. ``top_k``,
                ``agent_id``, ``min_score``).

        Returns:
            A list of matching chunks with scores and source metadata.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._post(
            "/knowledge-base/query", json={"query": query, **body}
        )

    async def list_for_agent(self, agent_id: str) -> Any:
        """List KB sources currently bound to an agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            A list of KB source records bound to the agent.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._get(f"/knowledge-base/agent/{agent_id}")

    async def assign_to_agent(self, agent_id: str, *, knowledge_base_ids: Any) -> Any:
        """Replace the KB sources bound to an agent.

        Args:
            agent_id: The agent identifier.
            knowledge_base_ids: Full list of KB source IDs (replaces any
                existing bindings).

        Returns:
            The updated agent record.

        Raises:
            APIError: If the request fails.
        """
        return await self._client._put(
            f"/knowledge-base/agent/{agent_id}", json={"knowledge_base_ids": knowledge_base_ids}
        )
