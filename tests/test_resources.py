"""HTTP-level tests for resource methods.

Uses pytest-httpx to mock the backend at the transport layer. These tests
prove that each method targets the right path + method, sends the right
body shape, and parses the response correctly. Errors map to the typed
exception hierarchy.
"""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from neuratelai import (
    AsyncNeuratelAI,
    AuthenticationError,
    NeuratelAI,
    NotFoundError,
    RateLimitError,
)
from neuratelai._exceptions import APIError


@pytest.fixture
def client() -> NeuratelAI:
    return NeuratelAI(api_key="nk_test_123", base_url="https://api.test/v1")


@pytest.fixture
async def aclient() -> AsyncNeuratelAI:
    return AsyncNeuratelAI(api_key="nk_test_123", base_url="https://api.test/v1")


# ── Agents ────────────────────────────────────────────────────────────────


def test_agents_get(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/agents/ag_1",
        json={"id": "ag_1", "name": "Aisha", "status": "ready"},
    )
    agent = client.agents.get("ag_1")
    assert agent["id"] == "ag_1"
    assert agent["name"] == "Aisha"


def test_agents_create_sends_body(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/agents",
        method="POST",
        json={"id": "ag_new", "name": "Salma"},
        match_json={"name": "Salma", "brain": {"provider": "groq"}},
    )
    out = client.agents.create(name="Salma", brain={"provider": "groq"})
    assert out["id"] == "ag_new"


def test_agents_templates_hits_correct_path(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/agents/templates",
        json={"templates": [{"id": "tpl_lead_qual", "name": "Lead Qualification"}]},
    )
    out = client.agents.templates()
    assert out["templates"][0]["id"] == "tpl_lead_qual"


def test_agents_required_variables(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/agents/ag_1/required-variables",
        json={"variables": ["customer_name", "appointment_date"]},
    )
    out = client.agents.required_variables("ag_1")
    assert "customer_name" in out["variables"]


def test_agents_list_paginates(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/agents?skip=0&limit=20",
        json={
            "results": [{"id": "ag_1"}, {"id": "ag_2"}],
            "metadata": {
                "total": 2,
                "skip": 0,
                "limit": 20,
                "has_more": False,
                "count": 2,
            },
        },
    )
    page = client.agents.list()
    items = list(page)
    assert [a["id"] for a in items] == ["ag_1", "ag_2"]


# ── Voice sessions ────────────────────────────────────────────────────────


def test_voice_sessions_outbound(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/voice-sessions/outbound",
        method="POST",
        json={"call_id": "vs_1", "success": True, "to_number": "+12125551234"},
        match_json={
            "agent_id": "ag_1",
            "to_number": "+12125551234",
            "number_id": "num_1",
        },
    )
    out = client.voice_sessions.outbound(
        agent_id="ag_1", to_number="+12125551234", number_id="num_1"
    )
    assert out["call_id"] == "vs_1"


def test_voice_sessions_get_includes_analysis_fields(
    httpx_mock: HTTPXMock, client: NeuratelAI
) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/voice-sessions/vs_1",
        json={
            "id": "vs_1",
            "status": "completed",
            "analysis_status": "completed",
            "user_sentiment": "positive",
            "user_sentiment_score": 0.87,
            "call_successful": "yes",
        },
    )
    session = client.voice_sessions.get("vs_1")
    assert session["analysis_status"] == "completed"
    assert session["user_sentiment"] == "positive"
    assert session["call_successful"] == "yes"


# ── Conversations (new in 1C) ─────────────────────────────────────────────


def test_conversations_list_passes_filters(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/conversations?skip=0&limit=10&channel=whatsapp",
        json={"results": [], "metadata": {"total": 0}},
    )
    out = client.conversations.list(channel="whatsapp", limit=10)
    assert "results" in out


def test_conversations_send_message_uses_body_field(
    httpx_mock: HTTPXMock, client: NeuratelAI
) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/conversations/conv_1/messages",
        method="POST",
        json={"id": "msg_1", "body": "hello", "direction": "outbound"},
        match_json={"body": "hello"},
    )
    out = client.conversations.send_message(conversation_id="conv_1", body="hello")
    assert out["id"] == "msg_1"


def test_conversations_update_dynamic_variables_includes_replace_flag(
    httpx_mock: HTTPXMock, client: NeuratelAI
) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/conversations/conv_1/dynamic_variables",
        method="PATCH",
        json={"id": "conv_1", "dynamic_variables": {"name": "Alice"}},
        match_json={
            "replace": False,
            "dynamic_variables": {"name": "Alice"},
        },
    )
    client.conversations.update_dynamic_variables(
        "conv_1", dynamic_variables={"name": "Alice"}
    )


# ── DNC (new in 1C) ───────────────────────────────────────────────────────


def test_dnc_check(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/dnc/check?phone=%2B12125551234",
        json={"phone": "+12125551234", "blocked": True, "source": "platform"},
    )
    out = client.dnc.check("+12125551234")
    assert out["blocked"] is True


def test_dnc_add_entry(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/dnc/entries",
        method="POST",
        json={"id": "dnc_1", "phone": "+12125551234"},
        match_json={"phone": "+12125551234", "reason": "customer requested"},
    )
    out = client.dnc.add_entry(
        phone="+12125551234", reason="customer requested"
    )
    assert out["id"] == "dnc_1"


def test_dnc_update_settings_uses_canonical_field_names(
    httpx_mock: HTTPXMock, client: NeuratelAI
) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/dnc/settings",
        method="PATCH",
        json={"protection_enabled": True, "auto_add_inbound_optouts": True},
        match_json={"protection_enabled": True, "auto_add_inbound_optouts": True},
    )
    client.dnc.update_settings(
        protection_enabled=True, auto_add_inbound_optouts=True
    )


# ── Analytics (new in 1C) ─────────────────────────────────────────────────


def test_analytics_dashboard_omits_unset_filters(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/analytics/dashboard?channel=phone",
        json={"voice": {}, "chat": {}},
    )
    out = client.analytics.dashboard(channel="phone")
    assert "voice" in out


# ── Error mapping ─────────────────────────────────────────────────────────


def test_404_raises_NotFoundError(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/agents/ag_missing",
        status_code=404,
        json={"error": {"message": "Not found", "code": "AGENT_NOT_FOUND"}},
    )
    with pytest.raises(NotFoundError):
        client.agents.get("ag_missing")


def test_401_raises_AuthenticationError(httpx_mock: HTTPXMock, client: NeuratelAI) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/billing/balance",
        status_code=401,
        json={"error": {"message": "Invalid key"}},
    )
    with pytest.raises(AuthenticationError):
        client.billing.balance()


def test_429_raises_RateLimitError(httpx_mock: HTTPXMock) -> None:
    # Backoff retries 429 by default; cap retries to surface the error fast.
    fast_client = NeuratelAI(
        api_key="nk_test", base_url="https://api.test/v1", max_retries=0
    )
    httpx_mock.add_response(
        url="https://api.test/v1/agents?skip=0&limit=20",
        status_code=429,
        json={"error": {"message": "Slow down"}},
        headers={"Retry-After": "1"},
    )
    with pytest.raises(RateLimitError):
        list(fast_client.agents.list())


def test_500_raises_APIError(httpx_mock: HTTPXMock) -> None:
    fast_client = NeuratelAI(
        api_key="nk_test", base_url="https://api.test/v1", max_retries=0
    )
    httpx_mock.add_response(
        url="https://api.test/v1/billing/balance",
        status_code=500,
        json={"error": {"message": "internal"}},
    )
    with pytest.raises(APIError):
        fast_client.billing.balance()


# ── Async sanity ──────────────────────────────────────────────────────────


async def test_async_voice_sessions_get(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/voice-sessions/vs_async",
        json={"id": "vs_async", "analysis_status": "pending"},
    )
    async with AsyncNeuratelAI(
        api_key="nk_test", base_url="https://api.test/v1"
    ) as client:
        out = await client.voice_sessions.get("vs_async")
    assert out["analysis_status"] == "pending"


async def test_async_dnc_check(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://api.test/v1/dnc/check?phone=%2B12125551234",
        json={"blocked": False},
    )
    async with AsyncNeuratelAI(
        api_key="nk_test", base_url="https://api.test/v1"
    ) as client:
        out = await client.dnc.check("+12125551234")
    assert out["blocked"] is False
