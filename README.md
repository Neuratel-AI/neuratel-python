# Neuratel AI — Python SDK

[![PyPI](https://img.shields.io/pypi/v/neuratelai)](https://pypi.org/project/neuratelai/)
[![Python](https://img.shields.io/pypi/pyversions/neuratelai)](https://pypi.org/project/neuratelai/)
[![Docs](https://img.shields.io/badge/docs-docs.neuratel.ai-black)](https://docs.neuratel.ai/sdk/overview)

Official Python SDK for the [Neuratel](https://neuratel.ai) API — build and manage AI voice agents in a few lines of code.

## Installation

```bash
pip install neuratelai
# or
uv add neuratelai
```

## Quick Start

```python
from neuratelai import NeuratelAI

client = NeuratelAI()  # reads NEURATEL_API_KEY from env

# Create an agent
agent = client.agents.create(
    name="Support Bot",
    brain={"provider": "groq", "model": "meta-llama/llama-4-scout-17b-16e-instruct", "instructions": "You are a helpful support agent."},
    voice={"provider": "cartesia", "voice_id": "8d8ce8c9-44a4-46c4-b10f-9a927b99a853", "model": "sonic-3"},
    transcriber={"provider": "deepgram", "model": "nova-3"},
)
print(agent["id"])

# Place an outbound call
call = client.voice_sessions.outbound(
    agent_id=agent["id"],
    to_number="+14155551234",
    number_id="your-number-uuid",
)
print(call["status"])

# Iterate all agents (auto-paginates)
for agent in client.agents.list().auto_paging_iter():
    print(agent["id"], agent["name"])
```

## Async

```python
import asyncio
from neuratelai import AsyncNeuratelAI

async def main():
    async with AsyncNeuratelAI() as client:
        agent = await client.agents.create(
            name="Bot",
            brain={"provider": "groq", "model": "meta-llama/llama-4-scout-17b-16e-instruct", "instructions": "..."},
        )
        async for a in await client.agents.list():
            print(a["id"])

asyncio.run(main())
```

## Resources

| Resource | Methods |
|----------|---------|
| `agents` | `create`, `list`, `get`, `update`, `delete`, `duplicate`, `web_call`, `list_versions`, `get_version`, `restore_version`, `templates`, `required_variables` |
| `analytics` | `dashboard` |
| `api_keys` | `create`, `list`, `revoke`, `rotate`, `scopes` |
| `billing` | `balance`, `usage`, `balance_history` |
| `call_lists` | `create`, `list`, `get`, `update`, `delete`, `bulk_import`, `add_contact`, `list_contacts`, `update_contact`, `delete_contact` |
| `campaigns` | `create`, `list`, `get`, `update`, `delete`, `start`, `pause`, `stop`, `list_calls`, `get_call` |
| `conversations` | `list`, `get`, `list_messages`, `send_message`, `mark_read`, `timeline`, `update_dynamic_variables`, `analytics_dashboard` |
| `dnc` | `check`, `list_entries`, `add_entry`, `delete_entry`, `get_settings`, `update_settings` |
| `integrations` | `list`, `create`, `update`, `delete`, `list_tools`, `refresh_tools`, `list_connections`, `create_connection`, `update_connection`, `delete_connection` |
| `knowledge_base` | `list`, `get`, `update`, `delete`, `from_file`, `from_url`, `from_text`, `query`, `list_for_agent`, `assign_to_agent` |
| `phone_numbers` | `list`, `get`, `update`, `assign`, `unassign` |
| `voice_sessions` | `list`, `get`, `update`, `delete`, `outbound`, `list_active`, `concurrency`, `hangup`, `listen`, `whisper`, `barge` |
| `webhooks` | `events`, `create`, `list`, `get`, `update`, `delete`, `test`, `rotate_secret`, `logs` |
| `whatsapp` | `list_accounts`, `import_account`, `import_account_manual`, `get_account`, `update_account`, `delete_account`, `list_templates`, `check_call_permission`, `get_call_status`, `verify_account`, `send_outbound_call`, `send_outbound_message`, `send_outbound_text`, `send_outbound_voice`, `batch_call`, `get_message_media` |
| `workflows` | `create`, `list`, `get`, `update`, `delete`, `save_graph`, `publish` |

## Error Handling

```python
from neuratelai import AuthenticationError, NotFoundError, RateLimitError, APIError

try:
    agent = client.agents.get("ag_unknown")
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Agent not found")
except RateLimitError:
    print("Rate limited")
except APIError as e:
    print(f"HTTP {e.status_code}: {e}")
```

## Links

- [Documentation](https://docs.neuratel.ai/sdk/overview) · [API Reference](https://docs.neuratel.ai/api) · [Changelog](https://github.com/Neuratel-AI/neuratel-python/releases)
- [Contributing](https://github.com/Neuratel-AI/neuratel-python/blob/main/CONTRIBUTING.md) · [Security](https://github.com/Neuratel-AI/neuratel-python/blob/main/SECURITY.md) · [Code of Conduct](https://github.com/Neuratel-AI/neuratel-python/blob/main/CODE_OF_CONDUCT.md)

## Requirements

Python 3.10+
