# Changelog

## 0.2.0 (2026-05-05)

### New resources

- `client.conversations` — wraps `/v1/conversations/*` (the unified SMS / WhatsApp / voice inbox shipped during the comms-taxonomy unification on 2026-04-26). Methods: `list`, `get`, `list_messages`, `send_message`, `mark_read`, `timeline`, `update_dynamic_variables`, `analytics_dashboard`. Body shapes match `ConversationSendRequest` (`body` / `media_urls` / `client_temp_id`) and `ConversationDynamicVariablesUpdateRequest` (`dynamic_variables` / `replace`).
- `client.dnc` — wraps the platform DNC directory shipped 2026-04-27. Methods: `check`, `list_entries`, `add_entry`, `delete_entry`, `get_settings`, `update_settings`. Settings uses canonical backend names (`protection_enabled`, `auto_add_inbound_optouts`).
- `client.analytics` — wraps `GET /v1/analytics/dashboard` (combined voice + chat KPIs).
- `client.agents.templates()` and `client.agents.required_variables(agent_id)` — the two missing agent endpoints.

### Typed models

- New `neuratelai.types` module exposing Pydantic v2 BaseModel classes auto-generated from `openapi.json` via `datamodel-code-generator`. Mirrors the OpenAI / Anthropic SDK pattern (hand-rolled SDK + codegen for types).
- `scripts/generate_types.sh` regenerates `src/neuratelai/types/_generated.py` from the in-tree spec, with a fallback to staging.
- Curated re-exports cover the ~80 entity types most callers need (`AgentResponse`, `VoiceSessionResponse`, `ConversationResponse`, all four `*TranscriberConfig` discriminants including new `SonioxTranscriberConfig`, `BalanceResponse`, `OrganizationResponse`, `Sku` enum, etc.).
- Resource methods still return `Any` for v0.2.0 — customers cast via `Model.model_validate(raw)`. Future release will retrofit method signatures.
- Runtime dep change: `pydantic` → `pydantic[email]` (the spec uses `EmailStr` for `EmailSubscribeRequest`, which requires `email-validator`).

### Tests

- `tests/test_resources.py` — 20 HTTP-level tests via `pytest-httpx`, covering each new resource's path/method/body shape plus error mapping (401 → `AuthenticationError`, 404 → `NotFoundError`, 429 → `RateLimitError`, 500 → `APIError`).
- mypy strict cleanup: `_generated.py` excluded (auto-generated codegen artifact); `_base_client.py` and `knowledge_base.py` shadowed-`list` annotations resolved.

## 0.1.2 (2026-04-26)

- `feat`: retarget calls SDK at `/v1/voice-sessions` (commits `7bc6f54`, `b846fc5`, `7760496`)
- `refactor`: drop `client.calls` alias; the resource is now exclusively `client.voice_sessions`. The 0.1.0 `calls` resource was removed when the backend deleted `/v1/calls/*`.
- `feat`: add `client.voice_sessions.update()`.
- `docs`: README quickstart + resource table use `voice_sessions`.

## 0.1.1 (~2026-04-15)

- `chore`: read `__version__` from package metadata via `importlib.metadata`.
- `fix`: `from_text` field name (was sending `text`, backend expects `content`).
- `fix`: `from_file` `name` parameter forwarded correctly.
- `fix`: `calls.delete` was returning the response body, dropping data — now returns nothing per the OpenAPI contract.
- `feat`: read `NEURATEL_API_KEY` from environment if `api_key=` not passed.

## 0.1.0 (2026-04-11)

Initial release.

- Sync and async clients (`Neuratel`, `AsyncNeuratel`)
- 10 resource groups: `agents`, `voice_sessions`, `phone_numbers`, `campaigns`, `call_lists`, `knowledge_base`, `webhooks`, `billing`, `api_keys`, `integrations`
- Automatic retries with exponential backoff on `429`, `408`, `5xx`
- Pagination helpers (`SyncPage`, `AsyncPage`) with `auto_paging_iter()`
- Typed exception hierarchy (`AuthenticationError`, `NotFoundError`, `RateLimitError`, etc.)
- Context manager support for connection lifecycle
