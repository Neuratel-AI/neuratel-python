from __future__ import annotations

import asyncio
import email.utils
import time
from random import random
from typing import Any

import httpx

from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from ._version import __version__

DEFAULT_BASE_URL = "https://api.neuratel.ai/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2
INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8.0


def _build_headers(api_key: str, extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": f"neuratel-python/{__version__}",
    }
    if extra:
        headers.update(extra)
    return headers


def _parse_error_message(response: httpx.Response) -> str:
    try:
        body = response.json()
        detail = body.get("detail") or body.get("message")
        if isinstance(detail, list):
            # FastAPI 422: [{"loc": [...], "msg": "...", "type": "..."}]
            return "; ".join(
                f"{'.'.join(str(x) for x in e.get('loc', []))}: {e.get('msg', '')}"
                for e in detail
                if isinstance(e, dict)
            ) or str(detail)
        if isinstance(detail, str):
            return detail
    except Exception:
        pass
    return response.text or f"HTTP {response.status_code}"


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return

    message = _parse_error_message(response)
    code = response.status_code
    kwargs: dict[str, Any] = {"status_code": code, "body": message}

    if code == 401:
        raise AuthenticationError(message, **kwargs)
    elif code == 403:
        raise PermissionDeniedError(message, **kwargs)
    elif code == 404:
        raise NotFoundError(message, **kwargs)
    elif code == 409:
        raise ConflictError(message, **kwargs)
    elif code == 422:
        raise UnprocessableEntityError(message, **kwargs)
    elif code == 429:
        raise RateLimitError(message, **kwargs)
    elif code >= 500:
        raise InternalServerError(message, **kwargs)
    else:
        raise APIError(message, **kwargs)


_JITTER_FACTOR = 0.2  # 20% — matches Vapi/industry standard


def _parse_retry_after(headers: httpx.Headers) -> float | None:
    """Parse Retry-After or retry-after-ms header. Handles both numeric and date formats."""
    # retry-after-ms takes priority (milliseconds)
    retry_after_ms = headers.get("retry-after-ms")
    if retry_after_ms is not None:
        try:
            ms = int(retry_after_ms)
            return ms / 1000 if ms > 0 else 0.0
        except (ValueError, TypeError):
            pass

    retry_after = headers.get("retry-after")
    if retry_after is None:
        return None

    # Numeric seconds
    try:
        seconds = float(retry_after)
        return max(seconds, 0.0)
    except ValueError:
        pass

    # RFC 2822 date string (e.g. "Wed, 21 Oct 2015 07:28:00 GMT")
    parsed = email.utils.parsedate_tz(retry_after)
    if parsed:
        reset_time = email.utils.mktime_tz(parsed)
        seconds = reset_time - time.time()
        return max(seconds, 0.0)

    return None


def _parse_ratelimit_reset(headers: httpx.Headers) -> float | None:
    """Parse X-RateLimit-Reset header (Unix timestamp)."""
    reset = headers.get("x-ratelimit-reset")
    if reset is None:
        return None
    try:
        seconds = int(reset) - time.time()
        return max(seconds, 0.0)
    except (ValueError, TypeError):
        return None


def _retry_delay(attempt: int, response: httpx.Response | None = None) -> float:
    """Exponential backoff with 20% jitter. Priority: Retry-After > X-RateLimit-Reset > backoff."""
    if response is not None:
        # 1. Retry-After / retry-after-ms
        retry_after = _parse_retry_after(response.headers)
        if retry_after is not None:
            return retry_after * (1 + random() * _JITTER_FACTOR)

        # 2. X-RateLimit-Reset
        ratelimit_reset = _parse_ratelimit_reset(response.headers)
        if ratelimit_reset is not None:
            return min(ratelimit_reset, MAX_RETRY_DELAY) * (1 + random() * _JITTER_FACTOR)

    # 3. Exponential backoff with symmetric jitter (±10%)
    delay = min(INITIAL_RETRY_DELAY * (2**attempt), MAX_RETRY_DELAY)
    return delay * (1 + (random() - 0.5) * _JITTER_FACTOR)


class SyncAPIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        httpx_client: httpx.Client | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._http = httpx_client or httpx.Client(
            base_url=self._base_url,
            headers=_build_headers(api_key),
            timeout=httpx.Timeout(timeout),
        )

    def _get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, *, json: Any = None, params: dict[str, Any] | None = None) -> Any:
        return self._request("POST", path, json=json, params=params)

    def _patch(self, path: str, *, json: Any = None) -> Any:
        return self._request("PATCH", path, json=json)

    def _put(self, path: str, *, json: Any = None) -> Any:
        return self._request("PUT", path, json=json)

    def _delete(self, path: str, *, params: dict[str, Any] | None = None) -> None:
        self._request("DELETE", path, params=params, expect_body=False)

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        expect_body: bool = True,
        _attempt: int = 0,
    ) -> Any:
        try:
            response = self._http.request(method, path, json=json, params=params)
        except httpx.TimeoutException as e:
            raise APITimeoutError(str(e)) from e
        except httpx.RequestError as e:
            raise APIConnectionError(str(e)) from e

        try:
            _raise_for_status(response)
        except APIError:
            # Retry on 429, 408 (request timeout), 5xx
            if response.status_code in (429, 408) or response.status_code >= 500:
                if _attempt < self._max_retries:
                    time.sleep(_retry_delay(_attempt, response))
                    return self._request(
                        method,
                        path,
                        json=json,
                        params=params,
                        expect_body=expect_body,
                        _attempt=_attempt + 1,
                    )
            raise

        if not expect_body or response.status_code == 204:
            return None
        return response.json()

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> SyncAPIClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Neuratel(base_url={self._base_url!r})"


class AsyncAPIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._http = httpx_client or httpx.AsyncClient(
            base_url=self._base_url,
            headers=_build_headers(api_key),
            timeout=httpx.Timeout(timeout),
        )

    async def _get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def _post(
        self, path: str, *, json: Any = None, params: dict[str, Any] | None = None
    ) -> Any:
        return await self._request("POST", path, json=json, params=params)

    async def _patch(self, path: str, *, json: Any = None) -> Any:
        return await self._request("PATCH", path, json=json)

    async def _put(self, path: str, *, json: Any = None) -> Any:
        return await self._request("PUT", path, json=json)

    async def _delete(self, path: str, *, params: dict[str, Any] | None = None) -> None:
        await self._request("DELETE", path, params=params, expect_body=False)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        expect_body: bool = True,
        _attempt: int = 0,
    ) -> Any:
        try:
            response = await self._http.request(method, path, json=json, params=params)
        except httpx.TimeoutException as e:
            raise APITimeoutError(str(e)) from e
        except httpx.RequestError as e:
            raise APIConnectionError(str(e)) from e

        try:
            _raise_for_status(response)
        except APIError:
            if response.status_code in (429, 408) or response.status_code >= 500:
                if _attempt < self._max_retries:
                    await asyncio.sleep(_retry_delay(_attempt, response))
                    return await self._request(
                        method,
                        path,
                        json=json,
                        params=params,
                        expect_body=expect_body,
                        _attempt=_attempt + 1,
                    )
            raise

        if not expect_body or response.status_code == 204:
            return None
        return response.json()

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncAPIClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return f"AsyncNeuratel(base_url={self._base_url!r})"
