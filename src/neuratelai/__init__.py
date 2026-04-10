"""Neuratel Python SDK — official client for the Neuratel API."""

from ._client import AsyncNeuratel, Neuratel
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
    "Neuratel",
    "AsyncNeuratel",
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
