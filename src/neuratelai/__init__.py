"""Neuratel Python SDK — official client for the Neuratel API."""

from ._client import AsyncNeuratel, AsyncNeuratelAI, Neuratel, NeuratelAI
from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    ConflictError,
    InternalServerError,
    NeuratelError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from ._pagination import AsyncPage, PaginationMetadata, SyncPage
from ._streaming import AsyncStream, PlatformEvent, Stream
from ._version import __version__

__all__ = [
    "NeuratelAI",
    "AsyncNeuratelAI",
    "Neuratel",  # backwards-compatible alias
    "AsyncNeuratel",  # backwards-compatible alias
    "NeuratelError",
    "APIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "APIConnectionError",
    "APITimeoutError",
    "PaginationMetadata",
    "SyncPage",
    "AsyncPage",
    "PlatformEvent",
    "Stream",
    "AsyncStream",
    "__version__",
]
