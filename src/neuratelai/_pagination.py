from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    from ._base_client import AsyncAPIClient, SyncAPIClient


class PaginationMetadata(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool
    count: int


class SyncPage:
    """Paginated result page — {results: [...], metadata: {...}}.

    Items are returned as plain dicts. Iterate or call auto_paging_iter() to
    walk all pages automatically.

    Example::

        for agent in client.agents.list().auto_paging_iter():
            print(agent["name"])
    """

    def __init__(
        self,
        *,
        results: list[dict[str, Any]],
        metadata: PaginationMetadata,
        client: SyncAPIClient,
        path: str,
        params: dict[str, Any],
    ) -> None:
        self.results = results
        self.metadata = metadata
        self._client = client
        self._path = path
        self._params = params

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __repr__(self) -> str:
        m = self.metadata
        return f"SyncPage(count={len(self.results)}, total={m.total}, has_more={m.has_more})"

    @property
    def has_more(self) -> bool:
        return self.metadata.has_more

    def next_page(self) -> SyncPage | None:
        if not self.has_more:
            return None
        params = {**self._params, "skip": self.metadata.skip + self.metadata.limit}
        data = self._client._get(self._path, params=params)
        return SyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path=self._path,
            params=params,
        )

    def auto_paging_iter(self) -> Iterator[dict[str, Any]]:
        """Iterate over all items across all pages."""
        page: SyncPage | None = self
        while page is not None:
            yield from page
            page = page.next_page()


class AsyncPage:
    """Async paginated result page.

    Example::

        async for agent in client.agents.list():
            print(agent["name"])
    """

    def __init__(
        self,
        *,
        results: list[dict[str, Any]],
        metadata: PaginationMetadata,
        client: AsyncAPIClient,
        path: str,
        params: dict[str, Any],
    ) -> None:
        self.results = results
        self.metadata = metadata
        self._client = client
        self._path = path
        self._params = params

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[dict[str, Any]]:
        page: AsyncPage | None = self
        while page is not None:
            for item in page.results:
                yield item
            page = await page.next_page()

    def __len__(self) -> int:
        return len(self.results)

    def __repr__(self) -> str:
        m = self.metadata
        return f"AsyncPage(count={len(self.results)}, total={m.total}, has_more={m.has_more})"

    @property
    def has_more(self) -> bool:
        return self.metadata.has_more

    async def next_page(self) -> AsyncPage | None:
        if not self.has_more:
            return None
        params = {**self._params, "skip": self.metadata.skip + self.metadata.limit}
        data = await self._client._get(self._path, params=params)
        return AsyncPage(
            results=data["results"],
            metadata=PaginationMetadata.model_validate(data["metadata"]),
            client=self._client,
            path=self._path,
            params=params,
        )
