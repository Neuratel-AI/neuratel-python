# Changelog

## 0.1.0 (2026-04-11)

Initial release.

- Sync and async clients (`Neuratel`, `AsyncNeuratel`)
- 10 resource groups: `agents`, `voice_sessions`, `phone_numbers`, `campaigns`, `call_lists`, `knowledge_base`, `webhooks`, `billing`, `api_keys`, `integrations`
- Automatic retries with exponential backoff on `429`, `408`, `5xx`
- Pagination helpers (`SyncPage`, `AsyncPage`) with `auto_paging_iter()`
- Typed exception hierarchy (`AuthenticationError`, `NotFoundError`, `RateLimitError`, etc.)
- Context manager support for connection lifecycle
