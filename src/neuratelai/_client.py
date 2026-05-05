from __future__ import annotations

import os

import httpx

from ._base_client import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    AsyncAPIClient,
    SyncAPIClient,
)
from ._exceptions import AuthenticationError
from .resources.agents import AgentsResource, AsyncAgentsResource
from .resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from .resources.api_keys import APIKeysResource, AsyncAPIKeysResource
from .resources.billing import AsyncBillingResource, BillingResource
from .resources.call_lists import AsyncCallListsResource, CallListsResource
from .resources.campaigns import AsyncCampaignsResource, CampaignsResource
from .resources.conversations import AsyncConversationsResource, ConversationsResource
from .resources.dnc import AsyncDNCResource, DNCResource
from .resources.integrations import AsyncIntegrationsResource, IntegrationsResource
from .resources.knowledge_base import AsyncKnowledgeBaseResource, KnowledgeBaseResource
from .resources.phone_numbers import AsyncPhoneNumbersResource, PhoneNumbersResource
from .resources.voice_sessions import AsyncVoiceSessionsResource, VoiceSessionsResource
from .resources.webhooks import AsyncWebhooksResource, WebhooksResource


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("NEURATEL_API_KEY")
    if not key:
        raise AuthenticationError(
            "No API key provided. Pass api_key= or set the NEURATEL_API_KEY environment variable."
        )
    return key


class NeuratelAI:
    """Synchronous Neuratel API client.

    Usage::

        client = NeuratelAI()  # reads NEURATEL_API_KEY from env
        # or
        client = NeuratelAI(api_key="nk_live_...")

        agent = client.agents.create(name="Support Bot", brain={...})
        for agent in client.agents.list():
            print(agent["name"])
    """

    agents: AgentsResource
    voice_sessions: VoiceSessionsResource
    conversations: ConversationsResource
    phone_numbers: PhoneNumbersResource
    campaigns: CampaignsResource
    call_lists: CallListsResource
    knowledge_base: KnowledgeBaseResource
    webhooks: WebhooksResource
    billing: BillingResource
    api_keys: APIKeysResource
    integrations: IntegrationsResource
    dnc: DNCResource
    analytics: AnalyticsResource

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        httpx_client: httpx.Client | None = None,
    ) -> None:
        self._base = SyncAPIClient(
            _resolve_api_key(api_key),
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            httpx_client=httpx_client,
        )
        self.agents = AgentsResource(self._base)
        self.voice_sessions = VoiceSessionsResource(self._base)
        self.conversations = ConversationsResource(self._base)
        self.phone_numbers = PhoneNumbersResource(self._base)
        self.campaigns = CampaignsResource(self._base)
        self.call_lists = CallListsResource(self._base)
        self.knowledge_base = KnowledgeBaseResource(self._base)
        self.webhooks = WebhooksResource(self._base)
        self.billing = BillingResource(self._base)
        self.api_keys = APIKeysResource(self._base)
        self.integrations = IntegrationsResource(self._base)
        self.dnc = DNCResource(self._base)
        self.analytics = AnalyticsResource(self._base)

    def close(self) -> None:
        self._base.close()

    def __enter__(self) -> NeuratelAI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"NeuratelAI(base_url={self._base._base_url!r})"


# Backwards-compatible alias
Neuratel = NeuratelAI


class AsyncNeuratelAI:
    """Asynchronous Neuratel API client.

    Usage::

        async with AsyncNeuratelAI() as client:  # reads NEURATEL_API_KEY from env
            agent = await client.agents.create(name="Support Bot", brain={...})
            async for agent in await client.agents.list():
                print(agent["name"])
    """

    agents: AsyncAgentsResource
    voice_sessions: AsyncVoiceSessionsResource
    conversations: AsyncConversationsResource
    phone_numbers: AsyncPhoneNumbersResource
    campaigns: AsyncCampaignsResource
    call_lists: AsyncCallListsResource
    knowledge_base: AsyncKnowledgeBaseResource
    webhooks: AsyncWebhooksResource
    billing: AsyncBillingResource
    api_keys: AsyncAPIKeysResource
    integrations: AsyncIntegrationsResource
    dnc: AsyncDNCResource
    analytics: AsyncAnalyticsResource

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base = AsyncAPIClient(
            _resolve_api_key(api_key),
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            httpx_client=httpx_client,
        )
        self.agents = AsyncAgentsResource(self._base)
        self.voice_sessions = AsyncVoiceSessionsResource(self._base)
        self.conversations = AsyncConversationsResource(self._base)
        self.phone_numbers = AsyncPhoneNumbersResource(self._base)
        self.campaigns = AsyncCampaignsResource(self._base)
        self.call_lists = AsyncCallListsResource(self._base)
        self.knowledge_base = AsyncKnowledgeBaseResource(self._base)
        self.webhooks = AsyncWebhooksResource(self._base)
        self.billing = AsyncBillingResource(self._base)
        self.api_keys = AsyncAPIKeysResource(self._base)
        self.integrations = AsyncIntegrationsResource(self._base)
        self.dnc = AsyncDNCResource(self._base)
        self.analytics = AsyncAnalyticsResource(self._base)

    async def aclose(self) -> None:
        await self._base.aclose()

    async def __aenter__(self) -> AsyncNeuratelAI:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return f"AsyncNeuratelAI(base_url={self._base._base_url!r})"


# Backwards-compatible alias
AsyncNeuratel = AsyncNeuratelAI
