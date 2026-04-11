"""Basic smoke tests — no network calls."""

import pytest

from neuratelai import (
    AsyncNeuratel,
    AsyncNeuratelAI,
    AuthenticationError,
    Neuratel,
    NeuratelAI,
    NotFoundError,
    RateLimitError,
)
from neuratelai._exceptions import APIError


def test_client_instantiation() -> None:
    client = NeuratelAI(api_key="nk_test_key")
    assert client.agents is not None
    assert client.calls is not None
    assert client.phone_numbers is not None
    assert client.campaigns is not None
    assert client.call_lists is not None
    assert client.knowledge_base is not None
    assert client.webhooks is not None
    assert client.billing is not None
    assert client.api_keys is not None
    assert client.integrations is not None


def test_backwards_compat_alias() -> None:
    """Neuratel is a backwards-compatible alias for NeuratelAI."""
    assert Neuratel is NeuratelAI
    assert AsyncNeuratel is AsyncNeuratelAI


def test_async_client_instantiation() -> None:
    client = AsyncNeuratelAI(api_key="nk_test_key")
    assert client.agents is not None
    assert client.calls is not None
    assert client.phone_numbers is not None
    assert client.campaigns is not None
    assert client.call_lists is not None
    assert client.knowledge_base is not None
    assert client.webhooks is not None
    assert client.billing is not None
    assert client.api_keys is not None
    assert client.integrations is not None


def test_exception_hierarchy() -> None:
    assert issubclass(AuthenticationError, APIError)
    assert issubclass(NotFoundError, APIError)
    assert issubclass(RateLimitError, APIError)

    err = NotFoundError("Agent not found", status_code=404)
    assert err.status_code == 404
    assert "Agent not found" in str(err)


def test_client_context_manager() -> None:
    with NeuratelAI(api_key="nk_test_key") as client:
        assert client.agents is not None


@pytest.mark.asyncio
async def test_async_client_context_manager() -> None:
    async with AsyncNeuratelAI(api_key="nk_test_key") as client:
        assert client.agents is not None
