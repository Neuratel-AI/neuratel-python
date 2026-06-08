#!/usr/bin/env python3
"""Read-only smoke test against live Neuratel API.

Exercises every SDK list/get method that hits a GET endpoint.
Never creates, updates, or deletes data.

Usage:
    NEURATEL_API_KEY=nk_live_xxx uv run python scripts/smoke_prod.py
"""

from __future__ import annotations

import os
import sys

from neuratelai import AsyncNeuratelAI

API_KEY = os.environ.get("NEURATEL_API_KEY")
if not API_KEY:
    sys.exit("NEURATEL_API_KEY env var required")

PASS: list[str] = []
FAIL: list[tuple[str, int, str]] = []


def _ok(label: str) -> None:
    PASS.append(label)
    print(f"  ✓ {label}")


def _fail(label: str, status: int, detail: str) -> None:
    FAIL.append((label, status, detail))
    print(f"  ✗ {label}  [{status}] {detail[:120]}")


async def run() -> None:
    async with AsyncNeuratelAI(api_key=API_KEY) as client:
        print("neuratel-python smoke — read-only prod endpoints\n")

        # ── Agents ──
        try:
            page = await client.agents.list(limit=1)
            agents = [a async for a in page]
            _ok("agents.list()")
            if agents:
                aid = agents[0]["id"]
                try:
                    await client.agents.get(aid)
                    _ok(f"agents.get('{aid[:12]}…')")
                except Exception as e:
                    _fail(f"agents.get('{aid[:12]}…')", getattr(e, "status_code", 0), str(e))
            else:
                _ok("agents.get() — SKIPPED (no agents)")
        except Exception as e:
            _fail("agents.list()", getattr(e, "status_code", 0), str(e))

        try:
            await client.agents.templates()
            _ok("agents.templates()")
        except Exception as e:
            _fail("agents.templates()", getattr(e, "status_code", 0), str(e))

        if agents:
            try:
                await client.agents.required_variables(agents[0]["id"])
                _ok("agents.required_variables()")
            except Exception as e:
                _fail("agents.required_variables()", getattr(e, "status_code", 0), str(e))

        # ── Voice Sessions ──
        try:
            await client.voice_sessions.list(limit=1)
            _ok("voice_sessions.list()")
        except Exception as e:
            _fail("voice_sessions.list()", getattr(e, "status_code", 0), str(e))

        try:
            await client.voice_sessions.list_active()
            _ok("voice_sessions.list_active()")
        except Exception as e:
            _fail("voice_sessions.list_active()", getattr(e, "status_code", 0), str(e))

        # ── Conversations ──
        try:
            await client.conversations.list(limit=1)
            _ok("conversations.list()")
        except Exception as e:
            _fail("conversations.list()", getattr(e, "status_code", 0), str(e))

        # ── Phone Numbers ──
        try:
            await client.phone_numbers.list()
            _ok("phone_numbers.list()")
        except Exception as e:
            _fail("phone_numbers.list()", getattr(e, "status_code", 0), str(e))

        # ── Campaigns ──
        try:
            await client.campaigns.list(limit=1)
            _ok("campaigns.list()")
        except Exception as e:
            _fail("campaigns.list()", getattr(e, "status_code", 0), str(e))

        # ── Call Lists ──
        try:
            await client.call_lists.list(limit=1)
            _ok("call_lists.list()")
        except Exception as e:
            _fail("call_lists.list()", getattr(e, "status_code", 0), str(e))

        # ── Knowledge Base ──
        try:
            page = await client.knowledge_base.list(limit=1)
            kbs = [k async for k in page]
            _ok("knowledge_base.list()")
            if kbs:
                try:
                    await client.knowledge_base.get(kbs[0]["id"])
                    _ok(f"knowledge_base.get('{kbs[0]['id'][:12]}…')")
                except Exception as e:
                    _fail("knowledge_base.get()", getattr(e, "status_code", 0), str(e))
        except Exception as e:
            _fail("knowledge_base.list()", getattr(e, "status_code", 0), str(e))

        # ── Webhooks ──
        try:
            await client.webhooks.list()
            _ok("webhooks.list()")
        except Exception as e:
            _fail("webhooks.list()", getattr(e, "status_code", 0), str(e))

        # ── Billing ──
        try:
            await client.billing.balance()
            _ok("billing.balance()")
        except Exception as e:
            _fail("billing.balance()", getattr(e, "status_code", 0), str(e))

        try:
            await client.billing.usage()
            _ok("billing.usage()")
        except Exception as e:
            _fail("billing.usage()", getattr(e, "status_code", 0), str(e))

        # ── API Keys ──
        try:
            await client.api_keys.list()
            _ok("api_keys.list()")
        except Exception as e:
            _fail("api_keys.list()", getattr(e, "status_code", 0), str(e))

        # ── Integrations (now includes auth-connections) ──
        try:
            await client.integrations.list()
            _ok("integrations.list()")
        except Exception as e:
            _fail("integrations.list()", getattr(e, "status_code", 0), str(e))

        try:
            await client.integrations.list_connections()
            _ok("integrations.list_connections()")
        except Exception as e:
            _fail("integrations.list_connections()", getattr(e, "status_code", 0), str(e))

        # ── DNC ──
        try:
            await client.dnc.list_entries(limit=1)
            _ok("dnc.list_entries()")
        except Exception as e:
            _fail("dnc.list_entries()", getattr(e, "status_code", 0), str(e))

        try:
            await client.dnc.get_settings()
            _ok("dnc.get_settings()")
        except Exception as e:
            _fail("dnc.get_settings()", getattr(e, "status_code", 0), str(e))

        try:
            await client.dnc.check("+12125551234")
            _ok("dnc.check()")
        except Exception as e:
            _fail("dnc.check()", getattr(e, "status_code", 0), str(e))

        # ── Analytics ──
        try:
            await client.analytics.dashboard()
            _ok("analytics.dashboard()")
        except Exception as e:
            _fail("analytics.dashboard()", getattr(e, "status_code", 0), str(e))

        # ── WhatsApp ──
        try:
            await client.whatsapp.list_accounts()
            _ok("whatsapp.list_accounts()")
        except Exception as e:
            _fail("whatsapp.list_accounts()", getattr(e, "status_code", 0), str(e))

        # ── Workflows ──
        try:
            await client.workflows.list(limit=1)
            _ok("workflows.list()")
        except Exception as e:
            _fail("workflows.list()", getattr(e, "status_code", 0), str(e))

    # ── Summary ──
    print(f"\n{'='*50}")
    total = len(PASS) + len(FAIL)
    print(f"  {len(PASS)}/{total} passed, {len(FAIL)} failed")
    if FAIL:
        print("\n  FAILURES:")
        for label, status, detail in FAIL:
            print(f"    [{status}] {label}: {detail[:80]}")
        sys.exit(1)
    else:
        print("  ALL GREEN ✓")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
