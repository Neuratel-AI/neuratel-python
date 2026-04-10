from __future__ import annotations

from typing import Any


class NeuratelError(Exception):
    """Base exception for all Neuratel SDK errors."""


class APIError(NeuratelError):
    message: str
    status_code: int | None
    body: Any

    def __init__(self, message: str, *, status_code: int | None = None, body: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code})"
        )


class AuthenticationError(APIError):
    """401 — Invalid or missing API key."""


class PermissionDeniedError(APIError):
    """403 — API key lacks required permissions."""


class NotFoundError(APIError):
    """404 — Resource not found."""


class ConflictError(APIError):
    """409 — Resource already exists or state conflict."""


class UnprocessableEntityError(APIError):
    """422 — Request validation failed."""


class RateLimitError(APIError):
    """429 — Too many requests."""


class InternalServerError(APIError):
    """5xx — Neuratel server error."""


class APIConnectionError(APIError):
    """Network-level error — could not reach the API."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=None)


class APITimeoutError(APIConnectionError):
    """Request timed out."""
