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
| `agents` | `create`, `list`, `get`, `update`, `delete`, `duplicate`, `web_call`, `list_versions`, `get_version`, `restore_version` |
| `voice_sessions` | `list`, `get`, `update`, `delete`, `outbound`, `active`, `concurrency`, `hangup`, `listen`, `whisper`, `barge` |
| `phone_numbers` | `list`, `get`, `update`, `assign`, `unassign` |
| `campaigns` | `create`, `list`, `get`, `update`, `delete`, `start`, `pause`, `stop`, `list_calls`, `get_call` |
| `call_lists` | `create`, `list`, `get`, `update`, `delete`, `bulk_import`, `add_contact`, `list_contacts`, `update_contact`, `delete_contact` |
| `knowledge_base` | `list`, `get`, `update`, `delete`, `from_file`, `from_url`, `from_text`, `query`, `list_for_agent`, `assign_to_agent` |
| `webhooks` | `events`, `create`, `list`, `get`, `update`, `delete`, `test`, `rotate_secret`, `logs` |
| `billing` | `balance`, `usage`, `balance_history` |
| `api_keys` | `create`, `list`, `revoke`, `rotate`, `scopes` |
| `integrations` | `list`, `create`, `update`, `delete`, `list_tools`, `refresh_tools` |

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

## Requirements

Python 3.10+ · [docs.neuratel.ai](https://docs.neuratel.ai/sdk/overview)
