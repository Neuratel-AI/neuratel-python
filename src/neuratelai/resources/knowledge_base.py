from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._pagination import AsyncPage, PaginationMetadata, SyncPage

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class KnowledgeBaseResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> SyncPage:
        data = self._client._get("/knowledge-base", params={"skip": skip, "limit": limit, **params})
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path="/knowledge-base",
            params={"skip": skip, "limit": limit, **params},
        )

    def get(self, kb_id: str) -> Any:
        return self._client._get(f"/knowledge-base/{kb_id}")

    def update(self, kb_id: str, **body: Any) -> Any:
        return self._client._put(f"/knowledge-base/{kb_id}", json=body)

    def delete(self, kb_id: str) -> None:
        self._client._delete(f"/knowledge-base/{kb_id}")

    def from_file(self, file_path: str, *, name: str | None = None) -> Any:
        """Upload a file (PDF, DOCX, TXT) as a knowledge base source."""
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
        return self._client._post("/knowledge-base/from-url", json={"url": url, **body})

    def from_text(self, text: str, **body: Any) -> Any:
        return self._client._post("/knowledge-base/from-text", json={"content": text, **body})

    def query(self, query: str, **body: Any) -> Any:
        return self._client._post("/knowledge-base/query", json={"query": query, **body})

    def list_for_agent(self, agent_id: str) -> Any:
        return self._client._get(f"/knowledge-base/agent/{agent_id}")

    def assign_to_agent(self, agent_id: str, *, knowledge_base_ids: list[str]) -> Any:
        return self._client._put(
            f"/knowledge-base/agent/{agent_id}", json={"knowledge_base_ids": knowledge_base_ids}
        )


class AsyncKnowledgeBaseResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def list(self, *, skip: int = 0, limit: int = 20, **params: Any) -> AsyncPage:
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
        return await self._client._get(f"/knowledge-base/{kb_id}")

    async def update(self, kb_id: str, **body: Any) -> Any:
        return await self._client._put(f"/knowledge-base/{kb_id}", json=body)

    async def delete(self, kb_id: str) -> None:
        await self._client._delete(f"/knowledge-base/{kb_id}")

    async def from_file(self, file_path: str, *, name: str | None = None) -> Any:
        """Upload a file (PDF, DOCX, TXT) as a knowledge base source."""
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
        return await self._client._post("/knowledge-base/from-url", json={"url": url, **body})

    async def from_text(self, text: str, **body: Any) -> Any:
        return await self._client._post("/knowledge-base/from-text", json={"content": text, **body})

    async def query(self, query: str, **body: Any) -> Any:
        return await self._client._post("/knowledge-base/query", json={"query": query, **body})

    async def list_for_agent(self, agent_id: str) -> Any:
        return await self._client._get(f"/knowledge-base/agent/{agent_id}")

    async def assign_to_agent(self, agent_id: str, *, knowledge_base_ids: list[str]) -> Any:
        return await self._client._put(
            f"/knowledge-base/agent/{agent_id}", json={"knowledge_base_ids": knowledge_base_ids}
        )
