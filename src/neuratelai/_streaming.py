from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    import httpx

log = logging.getLogger(__name__)


class PlatformEvent(BaseModel):
    """An event from the org-level SSE stream at GET /v1/stream/platform."""

    type: str
    data: dict[str, Any] | None = None

    model_config = {"extra": "allow"}


class Stream:
    """Sync SSE stream. Lifecycle is managed by EventsResource.stream() context manager.
    Do not call close() manually — the context manager handles cleanup.
    """

    def __init__(self, response: httpx.Response) -> None:
        self._response = response

    def __iter__(self) -> Iterator[PlatformEvent]:
        for line in self._response.iter_lines():
            if line.startswith("data: "):
                raw = line[6:]
                if raw == "[DONE]":
                    break
                try:
                    yield PlatformEvent.model_validate(json.loads(raw))
                except Exception as e:
                    log.debug("Failed to parse SSE event: %s — %r", e, raw)
                    continue


class AsyncStream:
    """Async SSE stream. Lifecycle is managed by AsyncEventsResource.stream() context manager.
    Do not call aclose() manually — the context manager handles cleanup.
    """

    def __init__(self, response: httpx.Response) -> None:
        self._response = response

    def __aiter__(self) -> AsyncIterator[PlatformEvent]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[PlatformEvent]:
        async for line in self._response.aiter_lines():
            if line.startswith("data: "):
                raw = line[6:]
                if raw == "[DONE]":
                    break
                try:
                    yield PlatformEvent.model_validate(json.loads(raw))
                except Exception as e:
                    log.debug("Failed to parse SSE event: %s — %r", e, raw)
                    continue
