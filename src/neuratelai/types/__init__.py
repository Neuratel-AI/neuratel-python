"""Typed Pydantic v2 models for the Neuratel API.

Auto-generated from the canonical OpenAPI spec via
`scripts/generate_types.sh` (datamodel-code-generator). This module curates
the most commonly-needed names; for the long tail of admin / internal types,
import from `neuratelai.types._generated` directly.

Example::

    from neuratelai import NeuratelAI
    from neuratelai.types import VoiceSessionResponse, AgentResponse

    client = NeuratelAI()
    raw = client.voice_sessions.get("vs_123")
    session = VoiceSessionResponse.model_validate(raw)
    print(session.analysis_status, session.user_sentiment)

The resource methods themselves still return `Any` for forward-compat —
upcoming releases will retrofit them to return these models directly.
"""

from __future__ import annotations

from . import _generated as _g

# ── Agents ────────────────────────────────────────────────────────────────
AgentResponse = _g.AgentResponse
AgentListResponse = _g.AgentListResponse
AgentVersionEntry = _g.AgentVersionEntry
AgentVersionResponse = _g.AgentVersionResponse
AgentVersionListResponse = _g.AgentVersionListResponse
AgentRestoreResponse = _g.AgentRestoreResponse
AgentRequiredVariablesResponse = _g.AgentRequiredVariablesResponse
AgentKnowledgeBaseAssignment = _g.AgentKnowledgeBaseAssignment
AgentKnowledgeBaseListResponse = _g.AgentKnowledgeBaseListResponse
AgentMetricsSummary = _g.AgentMetricsSummary
AgentPerformance = _g.AgentPerformance
AgentType = _g.AgentType

# ── Voice / Calls ─────────────────────────────────────────────────────────
VoiceSessionResponse = _g.VoiceSessionResponse
VoiceSessionListResponse = _g.VoiceSessionListResponse
VoiceSessionUpdate = _g.VoiceSessionUpdate
AgentCallRequest = _g.AgentCallRequest
AgentCallResponse = _g.AgentCallResponse
ActiveCallParticipant = _g.ActiveCallParticipant
CallListResponse = _g.CallListResponse  # call_lists resource

# ── Conversations / Messages ──────────────────────────────────────────────
ConversationResponse = _g.ConversationResponse
ConversationListResponse = _g.ConversationListResponse
ConversationSendRequest = _g.ConversationSendRequest
ConversationDynamicVariablesUpdateRequest = _g.ConversationDynamicVariablesUpdateRequest
ConversationLastMessage = _g.ConversationLastMessage
ConversationTurnSummary = _g.ConversationTurnSummary
MessageResponse = _g.MessageResponse
MessageListResponse = _g.MessageListResponse

# ── Brain (LLM) configs ───────────────────────────────────────────────────
GroqModel = _g.GroqModel
OpenAIModel = _g.OpenAIModel

# ── Voice (TTS) configs ───────────────────────────────────────────────────
CartesiaVoiceConfig = _g.CartesiaVoiceConfig
CartesiaModel = _g.CartesiaModel
CartesiaEmotion = _g.CartesiaEmotion
CartesiaSpeed = _g.CartesiaSpeed
ElevenLabsVoiceConfig = _g.ElevenLabsVoiceConfig
ElevenLabsModel = _g.ElevenLabsModel
PhantomVoiceConfig = _g.PhantomVoiceConfig

# ── Transcriber (STT) configs ─────────────────────────────────────────────
DeepgramTranscriberConfig = _g.DeepgramTranscriberConfig
DeepgramNovaModel = _g.DeepgramNovaModel
DeepgramLanguage = _g.DeepgramLanguage
OpenAITranscriberConfig = _g.OpenAITranscriberConfig
OpenAIWhisperModel = _g.OpenAIWhisperModel
SonioxTranscriberConfig = _g.SonioxTranscriberConfig
SonioxModel = _g.SonioxModel
PhantomTranscriberConfig = _g.PhantomTranscriberConfig

# ── Tools ────────────────────────────────────────────────────────────────
ToolsConfig = _g.ToolsConfig
HangupToolConfig = _g.HangupToolConfig
VoicemailToolConfig = _g.VoicemailToolConfig
VoicemailAction = _g.VoicemailAction

# ── DNC ──────────────────────────────────────────────────────────────────
DNCCheckResponse = _g.DNCCheckResponse
DNCEntryResponse = _g.DNCEntryResponse
DNCEntryAddRequest = _g.DNCEntryAddRequest
DNCEntryListResponse = _g.DNCEntryListResponse
DNCSettingsResponse = _g.DNCSettingsResponse
DNCSettingsRequest = _g.DNCSettingsRequest

# ── Webhooks ─────────────────────────────────────────────────────────────
WebhookCreateResponse = _g.WebhookCreateResponse
WebhookListResponse = _g.WebhookListResponse
WebhookDeliveryLogResponse = _g.WebhookDeliveryLogResponse

# ── Knowledge Base ───────────────────────────────────────────────────────
KnowledgeBaseCreateFromText = _g.KnowledgeBaseCreateFromText
KnowledgeBaseCreateFromURL = _g.KnowledgeBaseCreateFromURL
KnowledgeBaseUpdate = _g.KnowledgeBaseUpdate
KnowledgeBaseListResponse = _g.KnowledgeBaseListResponse
KnowledgeBaseStatus = _g.KnowledgeBaseStatus
KnowledgeBaseType = _g.KnowledgeBaseType

# ── Phone Numbers ────────────────────────────────────────────────────────
PhoneNumberResponse = _g.PhoneNumberResponse
PhoneNumberCreate = _g.PhoneNumberCreate
PhoneNumberUpdate = _g.PhoneNumberUpdate
PhoneNumberListResponse = _g.PhoneNumberListResponse

# ── Campaigns ────────────────────────────────────────────────────────────
CampaignConfig = _g.CampaignConfig
CampaignListResponse = _g.CampaignListResponse
CampaignPerformance = _g.CampaignPerformance

# ── Call Lists ───────────────────────────────────────────────────────────
CallListsListResponse = _g.CallListsListResponse

# ── Billing ──────────────────────────────────────────────────────────────
BalanceResponse = _g.BalanceResponse
BalanceCheckResponse = _g.BalanceCheckResponse
BalanceTransactionResponse = _g.BalanceTransactionResponse
BillingSettingsResponse = _g.BillingSettingsResponse
BillingPortalRequest = _g.BillingPortalRequest
BillingPortalResponse = _g.BillingPortalResponse
AutoReloadSettingsRequest = _g.AutoReloadSettingsRequest
AutoReloadSettingsResponse = _g.AutoReloadSettingsResponse
InvoiceListResponse = _g.InvoiceListResponse
PaymentMethodListResponse = _g.PaymentMethodListResponse
SetupIntentResponse = _g.SetupIntentResponse

# ── Organizations ────────────────────────────────────────────────────────
OrganizationCreate = _g.OrganizationCreate
OrganizationUpdate = _g.OrganizationUpdate
OrganizationResponse = _g.OrganizationResponse
OrganizationCredentialsUpdate = _g.OrganizationCredentialsUpdate
Sku = _g.Sku

# ── Voices catalog ───────────────────────────────────────────────────────
VoiceResponse = _g.VoiceResponse
VoiceListResponse = _g.VoiceListResponse
VoiceFilterOptions = _g.VoiceFilterOptions
VoiceSyncResponse = _g.VoiceSyncResponse

# ── Errors ───────────────────────────────────────────────────────────────
BadRequestError = _g.BadRequestError

# ── Notifications ────────────────────────────────────────────────────────
NotificationListResponse = _g.NotificationListResponse

# ── Workflows ────────────────────────────────────────────────────────────
WorkflowListResponse = _g.WorkflowListResponse

# ── Templates / MCP servers ──────────────────────────────────────────────────
TemplateListResponse = _g.TemplateListResponse
McpServerListResponse = _g.McpServerListResponse

__all__ = [
    # Agents
    "AgentResponse",
    "AgentListResponse",
    "AgentVersionEntry",
    "AgentVersionResponse",
    "AgentVersionListResponse",
    "AgentRestoreResponse",
    "AgentRequiredVariablesResponse",
    "AgentKnowledgeBaseAssignment",
    "AgentKnowledgeBaseListResponse",
    "AgentMetricsSummary",
    "AgentPerformance",
    "AgentType",
    # Voice / Calls
    "VoiceSessionResponse",
    "VoiceSessionListResponse",
    "VoiceSessionUpdate",
    "AgentCallRequest",
    "AgentCallResponse",
    "ActiveCallParticipant",
    "CallListResponse",
    # Conversations / Messages
    "ConversationResponse",
    "ConversationListResponse",
    "ConversationSendRequest",
    "ConversationDynamicVariablesUpdateRequest",
    "ConversationLastMessage",
    "ConversationTurnSummary",
    "MessageResponse",
    "MessageListResponse",
    # Brain configs
    "GroqModel",
    "OpenAIModel",
    # Voice configs
    "CartesiaVoiceConfig",
    "CartesiaModel",
    "CartesiaEmotion",
    "CartesiaSpeed",
    "ElevenLabsVoiceConfig",
    "ElevenLabsModel",
    "PhantomVoiceConfig",
    # Transcriber configs
    "DeepgramTranscriberConfig",
    "DeepgramNovaModel",
    "DeepgramLanguage",
    "OpenAITranscriberConfig",
    "OpenAIWhisperModel",
    "SonioxTranscriberConfig",
    "SonioxModel",
    "PhantomTranscriberConfig",
    # Tools
    "ToolsConfig",
    "HangupToolConfig",
    "VoicemailToolConfig",
    "VoicemailAction",
    # DNC
    "DNCCheckResponse",
    "DNCEntryResponse",
    "DNCEntryAddRequest",
    "DNCEntryListResponse",
    "DNCSettingsResponse",
    "DNCSettingsRequest",
    # Webhooks
    "WebhookCreateResponse",
    "WebhookListResponse",
    "WebhookDeliveryLogResponse",
    # Knowledge Base
    "KnowledgeBaseCreateFromText",
    "KnowledgeBaseCreateFromURL",
    "KnowledgeBaseUpdate",
    "KnowledgeBaseListResponse",
    "KnowledgeBaseStatus",
    "KnowledgeBaseType",
    # Phone Numbers
    "PhoneNumberResponse",
    "PhoneNumberCreate",
    "PhoneNumberUpdate",
    "PhoneNumberListResponse",
    # Campaigns
    "CampaignConfig",
    "CampaignListResponse",
    "CampaignPerformance",
    # Call Lists
    "CallListsListResponse",
    # Billing
    "BalanceResponse",
    "BalanceCheckResponse",
    "BalanceTransactionResponse",
    "BillingSettingsResponse",
    "BillingPortalRequest",
    "BillingPortalResponse",
    "AutoReloadSettingsRequest",
    "AutoReloadSettingsResponse",
    "InvoiceListResponse",
    "PaymentMethodListResponse",
    "SetupIntentResponse",
    # Organizations
    "OrganizationCreate",
    "OrganizationUpdate",
    "OrganizationResponse",
    "OrganizationCredentialsUpdate",
    "Sku",
    # Voices catalog
    "VoiceResponse",
    "VoiceListResponse",
    "VoiceFilterOptions",
    "VoiceSyncResponse",
    # Errors
    "BadRequestError",
    # Notifications
    "NotificationListResponse",
    # Workflows
    "WorkflowListResponse",
    # Templates / MCP
    "TemplateListResponse",
    "McpServerListResponse",
]
