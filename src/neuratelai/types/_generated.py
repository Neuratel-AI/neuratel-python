# Auto-generated from openapi.json by scripts/generate_types.sh. DO NOT EDIT.

from __future__ import annotations

from enum import Enum, IntEnum
from typing import Any, Literal
from uuid import UUID

from pydantic import (
    AnyUrl,
    AwareDatetime,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    RootModel,
)


class APIKeyListMetadata(BaseModel):
    """
    Metadata for API key list responses.
    """

    total: int = Field(..., title="Total")
    count: int = Field(..., title="Count")
    include_revoked: bool = Field(..., title="Include Revoked")


class AccountResponse(BaseModel):
    """
    Mirrors ElevenLabs GetWhatsAppAccountResponse schema.
    """

    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    phone_number_id: str = Field(..., title="Phone Number Id")
    display_phone_number: str = Field(..., title="Display Phone Number")
    business_account_id: str = Field(..., title="Business Account Id")
    business_account_name: str = Field(..., title="Business Account Name")
    phone_number_name: str = Field(..., title="Phone Number Name")
    agent_id: UUID | None = Field(default=None, title="Agent Id")
    agent_name: str | None = Field(default=None, title="Agent Name")
    enable_messaging: bool | None = Field(default=True, title="Enable Messaging")
    enable_audio_message_response: bool | None = Field(
        default=True, title="Enable Audio Message Response"
    )
    enable_calling: bool | None = Field(default=False, title="Enable Calling")
    timeout_message: str | None = Field(default=None, title="Timeout Message")
    agent_tool_overrides: dict[str, Any] | None = Field(
        default=None, title="Agent Tool Overrides"
    )
    default_call_template_name: str | None = Field(
        default=None, title="Default Call Template Name"
    )
    default_call_template_language: str | None = Field(
        default=None, title="Default Call Template Language"
    )
    is_active: bool | None = Field(default=True, title="Is Active")
    webhook_verified: bool | None = Field(default=False, title="Webhook Verified")
    inbound_webhook_url: str | None = Field(default=None, title="Inbound Webhook Url")
    inbound_webhook_secret_set: bool | None = Field(
        default=False, title="Inbound Webhook Secret Set"
    )
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class ActiveCallParticipant(BaseModel):
    identity: str = Field(..., title="Identity")
    name: str | None = Field(default=None, title="Name")
    state: str | None = Field(default=None, title="State")
    kind: str | None = Field(default=None, title="Kind")
    joined_at: str | None = Field(default=None, title="Joined At")


class AddToDncConfig(BaseModel):
    """
    Configuration for the in-call ``add_to_dnc`` agent tool.

    When enabled, the LLM gets an ``add_to_dnc`` callable it can invoke
    when the user explicitly asks to never be called again. The tool
    POSTs to Platform's ``/v1/webhooks/agent/dnc-add`` and the backend
    looks up the consumer's E.164 from the voice_session row, so the
    LLM never handles the raw phone number directly.

    Whether or not this in-call tool is enabled, every finished call's
    transcript is also scanned post-hoc by ``infer_dnc_from_session_report``
    (gpt-5.4-nano classifier) — the in-call tool is a UX win (faster
    block) but defense-in-depth lives in the post-call inference job.
    """

    enabled: bool | None = Field(
        default=False, description="Enable in-call DNC opt-out tool", title="Enabled"
    )


class Action(Enum):
    add = "add"
    remove = "remove"


class AdminAdjustCreditsRequest(BaseModel):
    """
    Request to adjust organization credits (admin only).
    """

    organization_id: UUID = Field(..., title="Organization Id")
    amount: float = Field(..., title="Amount")
    action: Action = Field(..., title="Action")
    reason: str | None = Field(default=None, title="Reason")


class AdminAdjustCreditsResponse(BaseModel):
    """
    Response for admin credit adjustment.
    """

    status: str = Field(..., title="Status")
    organization_id: UUID = Field(..., title="Organization Id")
    action: str = Field(..., title="Action")
    amount_cents: int = Field(..., title="Amount Cents")
    currency: str = Field(..., title="Currency")
    transaction_id: str = Field(..., title="Transaction Id")
    new_balance_cents: int = Field(..., title="New Balance Cents")
    new_balance_dollars: float = Field(..., title="New Balance Dollars")


class AdminBillingOverridesRequest(BaseModel):
    """
    Set per-org billing overrides — DLT compliance flag and/or
    custom rate-card overrides JSONB.

    `custom_rate_overrides` is a flat dict of override keys to USD rates.
    Override keys follow `<rate_type>.<channel>.<region_tier>` (omit
    NULL parts), e.g. `voice_per_min.webrtc.GLOBAL` or `wa_text.launch`.
    Checked BEFORE the rate_cards table at billing time.

    Pass only the fields you want to change. Omitted fields are untouched.
    """

    india_dlt_registered: bool | None = Field(
        default=None, title="India Dlt Registered"
    )
    custom_rate_overrides: dict[str, float] | None = Field(
        default=None, title="Custom Rate Overrides"
    )
    concurrency_override: int | None = Field(default=None, title="Concurrency Override")
    scale_cap_override: bool | None = Field(default=None, title="Scale Cap Override")


class AdminBillingOverridesResponse(BaseModel):
    organization_id: UUID = Field(..., title="Organization Id")
    india_dlt_registered: bool = Field(..., title="India Dlt Registered")
    custom_rate_overrides: dict[str, float] = Field(..., title="Custom Rate Overrides")
    max_concurrent_calls_effective: int = Field(
        ..., title="Max Concurrent Calls Effective"
    )
    scale_cap_override: bool = Field(..., title="Scale Cap Override")


class Reason(RootModel[str]):
    root: str = Field(..., max_length=1000, title="Reason")


class AdminDNCAddRequest(BaseModel):
    phone: str = Field(..., max_length=20, min_length=5, title="Phone")
    source: str | None = Field(default="platform_seed", title="Source")
    reason: Reason | None = Field(default=None, title="Reason")


class AdminPilotActionResponse(BaseModel):
    organization_id: UUID = Field(..., title="Organization Id")
    pilot_status: str | None = Field(..., title="Pilot Status")
    message: str = Field(..., title="Message")


class TargetSku(Enum):
    launch = "launch"
    scale = "scale"


class AdminPilotConvertRequest(BaseModel):
    """
    Convert a Pilot org to Launch or Scale + apply $2K credit.
    """

    target_sku: TargetSku = Field(..., title="Target Sku")
    india_compliance: bool | None = Field(default=False, title="India Compliance")
    china_onboarding: bool | None = Field(default=False, title="China Onboarding")


class AdminPilotConvertResponse(BaseModel):
    organization_id: UUID = Field(..., title="Organization Id")
    new_sku: str = Field(..., title="New Sku")
    new_setup_fee_invoice_id: UUID = Field(..., title="New Setup Fee Invoice Id")
    pilot_credit_applied_usd: float = Field(..., title="Pilot Credit Applied Usd")


class AgentAssignRequest(BaseModel):
    """
    Request model for assigning an agent to a phone number
    """

    agent_id: UUID = Field(..., title="Agent Id")


class AgentCallRequest(BaseModel):
    """
    Request to start a browser (WebRTC) call with an agent.
    """

    session_name: str | None = Field(
        default=None, description="Optional session name override", title="Session Name"
    )
    participant_name: str | None = Field(
        default=None,
        description="Display name for the caller",
        title="Participant Name",
    )
    dynamic_variables: dict[str, Any] | None = Field(
        default=None,
        description="Dynamic {{variables}} to inject for this call",
        title="Dynamic Variables",
    )


class AgentCallResponse(BaseModel):
    """
    Response containing connection details for a browser (WebRTC) call.
    """

    success: bool = Field(
        ..., description="Whether the session was successfully created", title="Success"
    )
    session_id: str = Field(
        ..., description="Unique identifier for this call session", title="Session Id"
    )
    participant_token: str = Field(
        ...,
        description="JWT access token for the participant",
        title="Participant Token",
    )
    token: str = Field(
        ...,
        description="JWT access token (alias of participant_token for backward compat)",
        title="Token",
    )
    server_url: str = Field(
        ...,
        description="WebSocket URL of the realtime media server",
        title="Server Url",
    )
    participant_identity: str = Field(
        ...,
        description="Your participant identity in this session",
        title="Participant Identity",
    )
    expires_in: int | None = Field(
        default=3600, description="Token expiry in seconds from now", title="Expires In"
    )


class AgentType(Enum):
    """
    Agent type: advanced (form-based) or workflow (graph-based)
    """

    advanced = "advanced"
    workflow = "workflow"


class Description(RootModel[str]):
    root: str = Field(
        ..., description="Agent description", max_length=1000, title="Description"
    )


class AgentKnowledgeBaseAssignment(BaseModel):
    """
    Assign knowledge bases to an agent.
    """

    knowledge_base_ids: list[UUID] | None = Field(
        default=None, description="KB IDs to assign", title="Knowledge Base Ids"
    )


class AgentMetricsSummary(BaseModel):
    """
    Per-call analytics surface read by the call-detail modal.

    Removed (no backend writer ever populated them):
      engagement_score, call_ended_reason, call_ended_reason_details,
      voicemail_probability, interruptions_count, long_pauses_count,
      rapid_exchanges_count, backchannel_count, transfer_attempted,
      transfer_successful, unique_speakers_count, speaker_distribution,
      tool_calls_history, call_metadata.

    Renamed:
      stt_turnaround_ms -> eou_delay_ms (was mislabeled — value is
      end-of-utterance delay from the worker's eou_delay_avg_s, not STT
      processing time).
    """

    latency_ttft_ms: int | None = Field(default=None, title="Latency Ttft Ms")
    latency_ttfb_ms: int | None = Field(default=None, title="Latency Ttfb Ms")
    eou_delay_ms: int | None = Field(default=None, title="Eou Delay Ms")
    conversation_quality_score: float | None = Field(
        default=None, title="Conversation Quality Score"
    )
    sentiment_score: float | None = Field(default=None, title="Sentiment Score")
    session_duration_seconds: int | None = Field(
        default=None, title="Session Duration Seconds"
    )
    extracted_data: dict[str, Any] | None = Field(default=None, title="Extracted Data")
    llm_tokens_prompt: int | None = Field(default=None, title="Llm Tokens Prompt")
    llm_tokens_completion: int | None = Field(
        default=None, title="Llm Tokens Completion"
    )
    llm_tokens_total: int | None = Field(default=None, title="Llm Tokens Total")
    stt_provider: str | None = Field(default=None, title="Stt Provider")
    stt_model: str | None = Field(default=None, title="Stt Model")
    stt_audio_duration_seconds: float | None = Field(
        default=None, title="Stt Audio Duration Seconds"
    )
    llm_provider: str | None = Field(default=None, title="Llm Provider")
    llm_model: str | None = Field(default=None, title="Llm Model")
    tts_provider: str | None = Field(default=None, title="Tts Provider")
    tts_model: str | None = Field(default=None, title="Tts Model")
    tts_characters: int | None = Field(default=None, title="Tts Characters")
    estimated_cost_usd: float | None = Field(default=None, title="Estimated Cost Usd")


class EstimatedCostUsd(RootModel[float]):
    root: float = Field(
        ..., description="Estimated cost", ge=0.0, title="Estimated Cost Usd"
    )


class AvgLatencyMs(RootModel[float]):
    root: float = Field(
        ..., description="Average response latency", ge=0.0, title="Avg Latency Ms"
    )


class AgentPerformance(BaseModel):
    """
    Performance metrics for a single agent.
    """

    agent_id: str = Field(..., description="Agent ID", title="Agent Id")
    agent_name: str = Field(..., description="Agent display name", title="Agent Name")
    total_calls: int | None = Field(
        default=0, description="Total calls handled", ge=0, title="Total Calls"
    )
    completed_calls: int | None = Field(
        default=0, description="Successfully completed", ge=0, title="Completed Calls"
    )
    failed_calls: int | None = Field(
        default=0, description="Failed calls", ge=0, title="Failed Calls"
    )
    total_duration_sec: int | None = Field(
        default=0,
        description="Total duration in seconds",
        ge=0,
        title="Total Duration Sec",
    )
    avg_duration_sec: float | None = Field(
        default=0.0,
        description="Average call duration",
        ge=0.0,
        title="Avg Duration Sec",
    )
    success_rate: float | None = Field(
        default=0.0,
        description="Success rate (0-1)",
        ge=0.0,
        le=1.0,
        title="Success Rate",
    )
    answer_rate: float | None = Field(
        default=0.0,
        description="Answer rate (0-1)",
        ge=0.0,
        le=1.0,
        title="Answer Rate",
    )
    estimated_cost_usd: EstimatedCostUsd | None = Field(
        default=None, description="Estimated cost", title="Estimated Cost Usd"
    )
    avg_latency_ms: AvgLatencyMs | None = Field(
        default=None, description="Average response latency", title="Avg Latency Ms"
    )


class AgentRequiredVariablesResponse(BaseModel):
    """
    Variables an agent's config references.

    Field meanings (matches the frontend `AgentRequiredVariables` interface
    consumed by the outbound-campaigns Form):
    - `required_variables`: every `{{name}}` extracted from the agent config.
    - `contact_variables`: subset that must come from the call-list contact
      row (i.e. NOT auto-injected `system__*` variables).
    - `system_variables`: subset auto-injected by the worker at call time.
    - `total_required`: convenience count of `required_variables`.
    - `sources`: where each variable was found (currently grouped by
      "system" vs "contact" — extensible for future per-config-section
      breakdown without a new endpoint).
    """

    required_variables: list[str] | None = Field(
        default=None, title="Required Variables"
    )
    contact_variables: list[str] | None = Field(default=None, title="Contact Variables")
    system_variables: list[str] | None = Field(default=None, title="System Variables")
    total_required: int | None = Field(default=0, title="Total Required")
    sources: dict[str, list[str]] | None = Field(default=None, title="Sources")


class AgentResponse(BaseModel):
    """
    Flat API response for single agent.

    Returns agent data directly without wrapper.
    """

    id: str = Field(..., description="Unique agent identifier", title="Id")
    name: str = Field(..., description="Agent display name", title="Name")
    organization_id: str = Field(
        ..., description="Owning organization ID", title="Organization Id"
    )
    status: str | None = Field(
        default="ready", description="Agent status", title="Status"
    )
    is_active: bool | None = Field(
        default=True, description="Whether agent is active", title="Is Active"
    )
    brain: dict[str, Any] | None = Field(
        default=None, description="LLM/Brain configuration", title="Brain"
    )
    voice: dict[str, Any] | None = Field(
        default=None, description="TTS configuration", title="Voice"
    )
    transcriber: dict[str, Any] | None = Field(
        default=None, description="STT configuration", title="Transcriber"
    )
    turn_detection: dict[str, Any] | None = Field(default=None, title="Turn Detection")
    first_message: dict[str, Any] | None = Field(default=None, title="First Message")
    interruption: dict[str, Any] | None = Field(default=None, title="Interruption")
    timeout: dict[str, Any] | None = Field(default=None, title="Timeout")
    call_duration: dict[str, Any] | None = Field(default=None, title="Call Duration")
    background_audio: dict[str, Any] | None = Field(
        default=None, title="Background Audio"
    )
    tts_text_transforms: list[Any] | None = Field(
        default=None, title="Tts Text Transforms"
    )
    preemptive_generation: bool | None = Field(
        default=False, title="Preemptive Generation"
    )
    min_consecutive_speech_delay: float | None = Field(
        default=0.0, title="Min Consecutive Speech Delay"
    )
    tools: dict[str, Any] | None = Field(
        default=None, description="Tools configuration", title="Tools"
    )
    transfer: dict[str, Any] | None = Field(
        default=None, description="Transfer settings", title="Transfer"
    )
    analytics: dict[str, Any] | None = Field(
        default=None, description="Analytics settings", title="Analytics"
    )
    tags: list[str] | None = Field(default=None, description="Tags", title="Tags")
    description: str | None = Field(
        default=None, description="Description", title="Description"
    )
    agent_type: str | None = Field(
        default="advanced", description="Agent type", title="Agent Type"
    )
    linked_workflow: dict[str, Any] | None = Field(
        default=None,
        description="Linked workflow summary for workflow agents: {id, name, is_active, current_version}",
        title="Linked Workflow",
    )
    version: int | None = Field(
        default=1, description="Config version number", ge=1, title="Version"
    )
    call_count: int | None = Field(
        default=0,
        description="Total number of calls for this agent",
        ge=0,
        title="Call Count",
    )
    created_at: AwareDatetime | None = Field(
        default=None, description="Creation timestamp", title="Created At"
    )
    updated_at: AwareDatetime | None = Field(
        default=None, description="Last update timestamp", title="Updated At"
    )
    inbound_webhook_url: str | None = Field(
        default=None,
        description="Configured per-call inbound webhook URL",
        title="Inbound Webhook Url",
    )
    inbound_webhook_secret_set: bool | None = Field(
        default=False,
        description="True when an HMAC secret is configured. The secret value itself is never returned — operator re-enters it to change.",
        title="Inbound Webhook Secret Set",
    )


class AgentRestoreResponse(BaseModel):
    """
    Response after restoring an agent to a historical version.
    """

    success: bool = Field(..., title="Success")
    message: str = Field(..., title="Message")
    current_version: int | None = Field(default=None, title="Current Version")


class Name(RootModel[str]):
    root: str = Field(
        ...,
        description="Agent display name",
        max_length=255,
        min_length=1,
        title="Name",
    )


class Tags(RootModel[list[str]]):
    root: list[str] = Field(
        ..., description="Tags for organization", max_length=20, title="Tags"
    )


class InboundWebhookUrl(RootModel[str]):
    root: str = Field(
        ...,
        description="HTTPS URL invoked at call/message connect to fetch per-call dynamic_variables and (optional) prompt overrides. Empty/null disables the fetch. Phone-number-level URLs (when configured) take precedence for inbound voice — agent URL is the fallback.",
        max_length=2048,
        title="Inbound Webhook Url",
    )


class InboundWebhookSecret(RootModel[str]):
    root: str = Field(
        ...,
        description="Shared secret used to sign every webhook request with HMAC-SHA256 in the X-Neuratel-Signature header. Optional — null means no signature is sent (acceptable for internal/dev endpoints only).",
        max_length=255,
        title="Inbound Webhook Secret",
    )


class AgentVersionEntry(BaseModel):
    """
    A single entry in an agent's version history.
    """

    version: int = Field(..., title="Version")
    change_description: str | None = Field(default=None, title="Change Description")
    created_at: str | None = Field(default=None, title="Created At")
    config: dict[str, Any] | None = Field(default=None, title="Config")


class AgentVersionListResponse(BaseModel):
    """
    Response for listing all versions of an agent.
    """

    agent_id: str = Field(..., title="Agent Id")
    total: int = Field(..., title="Total")
    versions: list[AgentVersionEntry] = Field(..., title="Versions")


class AgentVersionResponse(BaseModel):
    """
    Response for a single agent version.
    """

    version: int = Field(..., title="Version")
    change_description: str | None = Field(default=None, title="Change Description")
    created_at: str | None = Field(default=None, title="Created At")
    config: dict[str, Any] | None = Field(default=None, title="Config")


class AnnouncementRequest(BaseModel):
    """
    Request body for status announcements
    """

    subject: str = Field(..., title="Subject")
    message: str = Field(..., title="Message")
    component_ids: list[UUID] | None = Field(default=None, title="Component Ids")


class Kind(Enum):
    bearer = "bearer"
    headers = "headers"


class Token(RootModel[str]):
    root: str = Field(..., min_length=1, title="Token")


class AuthConnectionCreate(BaseModel):
    """
    Create a new credential vault entry.

    For ``kind="bearer"``: pass the raw token in ``token``.
    For ``kind="headers"``: pass a dict in ``headers``.
    Exactly one of the two must be supplied; ``_kind_secret_match`` raises a
    422 with field-level info before the request reaches the service.
    """

    name: str = Field(..., max_length=255, min_length=1, title="Name")
    kind: Kind = Field(..., title="Kind")
    token: Token | None = Field(default=None, title="Token")
    headers: dict[str, str] | None = Field(default=None, title="Headers")


class AuthConnectionResponse(BaseModel):
    """
    Response shape — secret value never leaves the server.

    For ``kind="bearer"`` the response sets ``has_token=True`` once a
    token is stored; for ``kind="headers"`` ``header_keys`` lists the
    keys (never values).
    """

    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    name: str = Field(..., title="Name")
    kind: Kind = Field(..., title="Kind")
    has_token: bool | None = Field(default=False, title="Has Token")
    header_keys: list[str] | None = Field(default=None, title="Header Keys")
    created_at: str | None = Field(default=None, title="Created At")
    updated_at: str | None = Field(default=None, title="Updated At")


class Name1(RootModel[str]):
    root: str = Field(..., max_length=255, min_length=1, title="Name")


class AuthConnectionUpdate(BaseModel):
    name: Name1 | None = Field(default=None, title="Name")
    token: Token | None = Field(default=None, title="Token")
    headers: dict[str, str] | None = Field(default=None, title="Headers")


class AutoReloadSettingsRequest(BaseModel):
    """
    Request to update auto-reload settings.
    """

    enabled: bool = Field(..., title="Enabled")
    threshold_cents: int | None = Field(default=None, title="Threshold Cents")
    amount_cents: int | None = Field(default=None, title="Amount Cents")


class AutoReloadSettingsResponse(BaseModel):
    """
    Current auto-reload settings.
    """

    enabled: bool = Field(..., title="Enabled")
    threshold_cents: int | None = Field(default=None, title="Threshold Cents")
    amount_cents: int | None = Field(default=None, title="Amount Cents")
    threshold_dollars: float | None = Field(default=None, title="Threshold Dollars")
    amount_dollars: float | None = Field(default=None, title="Amount Dollars")


class BadRequestError(BaseModel):
    """
    400 Bad Request error response
    """

    detail: str = Field(..., title="Detail")


class BalanceCheckResponse(BaseModel):
    """
    Response for balance check before call.
    """

    can_make_call: bool = Field(..., title="Can Make Call")
    balance_cents: int = Field(..., title="Balance Cents")
    balance_dollars: float = Field(..., title="Balance Dollars")
    minimum_required_cents: int | None = Field(
        default=100, title="Minimum Required Cents"
    )
    message: str = Field(..., title="Message")


class BalanceResponse(BaseModel):
    """
    Current account balance.
    """

    balance_cents: int = Field(..., title="Balance Cents")
    balance_dollars: float = Field(..., title="Balance Dollars")
    has_credits: bool = Field(..., title="Has Credits")
    currency: str | None = Field(default="USD", title="Currency")


class BalanceTransactionResponse(BaseModel):
    """
    Balance transaction details.
    """

    id: str = Field(..., title="Id")
    amount_cents: int = Field(..., title="Amount Cents")
    amount_dollars: float = Field(..., title="Amount Dollars")
    ending_balance_cents: int = Field(..., title="Ending Balance Cents")
    description: str = Field(..., title="Description")
    created: int = Field(..., title="Created")


class TemplateBody(RootModel[str]):
    root: str = Field(
        ...,
        description="Raw template body for placeholder auto-resolution.",
        max_length=4096,
        title="Template Body",
    )


class BatchCallResponse(BaseModel):
    total: int = Field(..., title="Total")
    sent: int = Field(..., title="Sent")
    failed: int = Field(..., title="Failed")
    errors: list[dict[str, str]] = Field(..., title="Errors")


class BillingListMetadata(BaseModel):
    """
    Metadata for billing list responses.
    """

    count: int = Field(..., title="Count")
    limit: int | None = Field(default=None, title="Limit")


class FlowTypeEnum(Enum):
    payment_method_update = "payment_method_update"


class FlowType(RootModel[FlowTypeEnum | None]):
    root: FlowTypeEnum | None = Field(None, title="Flow Type")


class BillingPortalRequest(BaseModel):
    """
    Request to create a billing portal session.
    """

    return_url: str = Field(..., title="Return Url")
    flow_type: FlowType | None = Field(default=None, title="Flow Type")


class BillingPortalResponse(BaseModel):
    """
    Billing portal session response.
    """

    url: str = Field(..., title="Url")
    id: str = Field(..., title="Id")


class BillingSettingsResponse(BaseModel):
    """
    Current billing settings for organization.

    sku is the canonical pricing tier RateCardService.lookup() reads;
    payment_method gates Stripe Card vs Manual Invoice flow in
    SettingsBilling.tsx; effective_rate_per_minute_usd is the representative
    voice rate (webrtc + GLOBAL region) computed from RateCardService for
    UI display — actual billing rates vary by channel + region per call.

    Pilot pool counters (``pilot_*``) and MTD usage caches let the org-side
    Settings → Billing card render Pilot's Day-N-of-30 + pool consumption
    AND the Launch/Scale dashboard widget render volume-discount tier
    progress without an extra Organization fetch (audit fix #4 of v5
    alignment plan).
    """

    sku: str = Field(..., title="Sku")
    contract_term: str = Field(..., title="Contract Term")
    payment_method: str = Field(..., title="Payment Method")
    effective_rate_per_minute_usd: float | None = Field(
        default=None, title="Effective Rate Per Minute Usd"
    )
    stripe_customer_id: str | None = Field(default=None, title="Stripe Customer Id")
    stripe_subscription_id: str | None = Field(
        default=None, title="Stripe Subscription Id"
    )
    pilot_status: str | None = Field(default=None, title="Pilot Status")
    pilot_started_at: AwareDatetime | None = Field(
        default=None, title="Pilot Started At"
    )
    pilot_go_live_at: AwareDatetime | None = Field(
        default=None, title="Pilot Go Live At"
    )
    pilot_included_minutes_used: float | None = Field(
        default=0.0, title="Pilot Included Minutes Used"
    )
    pilot_included_minutes_total: float | None = Field(
        default=800.0, title="Pilot Included Minutes Total"
    )
    pilot_included_messages_used: int | None = Field(
        default=0, title="Pilot Included Messages Used"
    )
    pilot_included_messages_total: int | None = Field(
        default=10000, title="Pilot Included Messages Total"
    )
    month_to_date_billable_minutes: float | None = Field(
        default=0.0, title="Month To Date Billable Minutes"
    )
    month_to_date_whatsapp_call_minutes: float | None = Field(
        default=0.0, title="Month To Date Whatsapp Call Minutes"
    )
    concurrency_cap: int | None = Field(default=5, title="Concurrency Cap")


class BuiltinAudioClip(Enum):
    """
    Built-in audio clips for background and thinking sounds.

    For custom sounds, use a URL or file path string instead.
    """

    city_ambience = "city_ambience"
    forest_ambience = "forest_ambience"
    office_ambience = "office_ambience"
    crowded_room = "crowded_room"
    keyboard_typing = "keyboard_typing"
    keyboard_typing_2 = "keyboard_typing_2"
    hold_music = "hold_music"


class BulkPasteContactRow(BaseModel):
    """
    One pasted-phone row in the manual bulk-paste flow.
    """

    phone_number: str = Field(..., max_length=40, min_length=3, title="Phone Number")
    contact_data: dict[str, Any] | None = Field(
        default=None,
        description='Optional variables for this contact (e.g. {"name": "Bilal"}). Reserved keys ``phone_number`` and ``status`` are rejected.',
        title="Contact Data",
    )


class BulkPasteContactsRequest(BaseModel):
    """
    POST /call-lists/{id}/contacts/bulk — manual bulk-paste from FE.
    """

    phones: list[BulkPasteContactRow] = Field(
        ..., max_length=500, min_length=1, title="Phones"
    )


class CallDurationConfig(BaseModel):
    """
    Configuration for maximum call duration.
    """

    enabled: bool | None = Field(
        default=True, description="Enable call duration limit", title="Enabled"
    )
    max_seconds: int | None = Field(
        default=1800,
        description="Maximum call duration in seconds",
        ge=60,
        le=7200,
        title="Max Seconds",
    )
    warning_message: str | None = Field(
        default="We're approaching the end of our allotted time.",
        description="Warning message before limit",
        title="Warning Message",
    )
    warning_seconds_before: int | None = Field(
        default=60,
        description="Seconds before limit to show warning",
        ge=10,
        le=300,
        title="Warning Seconds Before",
    )
    exceeded_message: str | None = Field(
        default="We've reached the maximum call duration. Thank you for calling!",
        description="Message when limit reached",
        title="Exceeded Message",
    )


class CallListContactCreate(BaseModel):
    """
    Schema for creating call list contacts
    """

    phone_number: str = Field(
        ...,
        description="Contact phone number",
        max_length=20,
        min_length=3,
        title="Phone Number",
    )
    contact_data: dict[str, Any] | None = Field(
        default=None,
        description="Arbitrary key/value map. Every key becomes a ``{{key}}`` variable available to the agent prompt at call time. Reserved keys ``phone_number`` and ``status`` are rejected (they would override the contact's real columns).",
        title="Contact Data",
    )


class CallListContactResponse(BaseModel):
    """
    Schema for call list contact responses.

    Phase 1 dropped the `call_count`, `last_called`, `call_result` fields —
    per-attempt outcomes now live on campaign_attempts and are exposed via
    GET /v1/campaigns/{id}/attempts.
    """

    phone_number: str = Field(
        ...,
        description="Contact phone number",
        max_length=20,
        min_length=3,
        title="Phone Number",
    )
    contact_data: dict[str, Any] | None = Field(
        default=None,
        description="Arbitrary key/value map. Every key becomes a ``{{key}}`` variable available to the agent prompt at call time. Reserved keys ``phone_number`` and ``status`` are rejected (they would override the contact's real columns).",
        title="Contact Data",
    )
    id: UUID = Field(..., title="Id")
    call_list_id: UUID = Field(..., title="Call List Id")
    status: str | None = Field(default="active", title="Status")
    is_active: bool | None = Field(default=True, title="Is Active")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime | None = Field(default=None, title="Updated At")


class PhoneNumber(RootModel[str]):
    root: str = Field(
        ...,
        description="Contact phone number",
        max_length=20,
        min_length=3,
        title="Phone Number",
    )


class Status(RootModel[str]):
    root: str = Field(
        ...,
        description="Contact status: active, dnc, invalid, opted_out, or called (legacy)",
        pattern="^(active|dnc|invalid|opted_out|called)$",
        title="Status",
    )


class CallListContactUpdate(BaseModel):
    """
    Schema for updating call list contacts.
    """

    phone_number: PhoneNumber | None = Field(
        default=None, description="Contact phone number", title="Phone Number"
    )
    contact_data: dict[str, Any] | None = Field(
        default=None,
        description="Replace the contact's variable map. Pass {} to clear; omit to leave unchanged. Reserved keys ``phone_number`` and ``status`` are rejected.",
        title="Contact Data",
    )
    status: Status | None = Field(
        default=None,
        description="Contact status: active, dnc, invalid, opted_out, or called (legacy)",
        title="Status",
    )
    is_active: bool | None = Field(
        default=None, description="Contact active status", title="Is Active"
    )


class CallListCreate(BaseModel):
    """
    Schema for creating call lists
    """

    name: str = Field(
        ..., description="Call list name", max_length=255, min_length=1, title="Name"
    )
    description: str | None = Field(
        default=None, description="Call list description", title="Description"
    )


class CallListResponse(BaseModel):
    """
    Schema for call list responses
    """

    name: str = Field(
        ..., description="Call list name", max_length=255, min_length=1, title="Name"
    )
    description: str | None = Field(
        default=None, description="Call list description", title="Description"
    )
    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    total_contacts: int | None = Field(default=0, title="Total Contacts")
    active_contacts: int | None = Field(default=0, title="Active Contacts")
    is_active: bool | None = Field(default=True, title="Is Active")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class Name2(RootModel[str]):
    root: str = Field(
        ..., description="Call list name", max_length=255, min_length=1, title="Name"
    )


class CallListUpdate(BaseModel):
    """
    Schema for updating call lists
    """

    name: Name2 | None = Field(default=None, description="Call list name", title="Name")
    description: str | None = Field(
        default=None, description="Call list description", title="Description"
    )
    list_data: dict[str, Any] | None = Field(
        default=None, description="Additional list metadata", title="List Data"
    )
    is_active: bool | None = Field(
        default=None, description="List active status", title="Is Active"
    )


class CallOutcomeBreakdown(BaseModel):
    """
    Breakdown of calls by outcome for pie charts.
    """

    completed: int | None = Field(
        default=0, description="Successfully completed calls", ge=0, title="Completed"
    )
    failed: int | None = Field(
        default=0, description="Failed calls", ge=0, title="Failed"
    )
    no_answer: int | None = Field(
        default=0, description="Unanswered calls", ge=0, title="No Answer"
    )
    voicemail: int | None = Field(
        default=0, description="Voicemail calls", ge=0, title="Voicemail"
    )
    busy: int | None = Field(default=0, description="Busy signal", ge=0, title="Busy")
    canceled: int | None = Field(
        default=0, description="Canceled calls", ge=0, title="Canceled"
    )
    other: int | None = Field(
        default=0, description="Other outcomes", ge=0, title="Other"
    )


class CallPermissionStatusResponse(BaseModel):
    has_permission: bool = Field(..., title="Has Permission")
    status: str | None = Field(default=None, title="Status")
    expiration_time: int | None = Field(default=None, title="Expiration Time")
    can_call: bool | None = Field(default=False, title="Can Call")


class CallResponse(BaseModel):
    status: str = Field(..., title="Status")
    message: str = Field(..., title="Message")
    intent_id: UUID | None = Field(default=None, title="Intent Id")


class CallSchedule(BaseModel):
    """
    Campaign call scheduling window.
    """

    start_time: str | None = Field(default=None, title="Start Time")
    end_time: str | None = Field(default=None, title="End Time")
    timezone: str | None = Field(default=None, title="Timezone")
    start_hour: int | None = Field(default=None, title="Start Hour")
    end_hour: int | None = Field(default=None, title="End Hour")
    days_of_week: list[int] | None = Field(default=None, title="Days Of Week")


class CallStatusResponse(BaseModel):
    intent_id: UUID = Field(..., title="Intent Id")
    status: str = Field(..., title="Status")
    session_id: str | None = Field(default=None, title="Session Id")
    failure_reason: str | None = Field(default=None, title="Failure Reason")
    requested_at: AwareDatetime = Field(..., title="Requested At")
    granted_at: AwareDatetime | None = Field(default=None, title="Granted At")
    placed_at: AwareDatetime | None = Field(default=None, title="Placed At")
    expires_at: AwareDatetime = Field(..., title="Expires At")


class Hour(RootModel[int]):
    root: int = Field(
        ..., description="Hour (0-23) for hourly interval", ge=0, le=23, title="Hour"
    )


class AnswerRate(RootModel[float]):
    root: float = Field(
        ..., description="Answer rate (0-1)", ge=0.0, le=1.0, title="Answer Rate"
    )


class ErrorRate(RootModel[float]):
    root: float = Field(
        ..., description="Error rate (0-1)", ge=0.0, le=1.0, title="Error Rate"
    )


class BookingRate(RootModel[float]):
    root: float = Field(
        ..., description="Booking rate (0-1)", ge=0.0, le=1.0, title="Booking Rate"
    )


class CallVolumeDataPoint(BaseModel):
    """
    Single data point for call volume time series charts.
    """

    date: str = Field(..., description="Date in YYYY-MM-DD format", title="Date")
    hour: Hour | None = Field(
        default=None, description="Hour (0-23) for hourly interval", title="Hour"
    )
    calls: int | None = Field(default=0, description="Total calls", ge=0, title="Calls")
    answered: int | None = Field(
        default=0, description="Answered/completed calls", ge=0, title="Answered"
    )
    errors: int | None = Field(
        default=0, description="Failed/error calls", ge=0, title="Errors"
    )
    inbound: int | None = Field(
        default=0, description="Inbound calls", ge=0, title="Inbound"
    )
    outbound: int | None = Field(
        default=0, description="Outbound calls", ge=0, title="Outbound"
    )
    duration_minutes: float | None = Field(
        default=0.0,
        description="Total duration in minutes",
        ge=0.0,
        title="Duration Minutes",
    )
    avg_handle_time_sec: float | None = Field(
        default=0.0,
        description="Average call duration in seconds",
        ge=0.0,
        title="Avg Handle Time Sec",
    )
    answer_rate: AnswerRate | None = Field(
        default=None, description="Answer rate (0-1)", title="Answer Rate"
    )
    error_rate: ErrorRate | None = Field(
        default=None, description="Error rate (0-1)", title="Error Rate"
    )
    booking_rate: BookingRate | None = Field(
        default=None, description="Booking rate (0-1)", title="Booking Rate"
    )
    avg_latency_ttft_ms: float | None = Field(
        default=0.0,
        description="Average TTFT in ms",
        ge=0.0,
        title="Avg Latency Ttft Ms",
    )
    avg_latency_ttfb_ms: float | None = Field(
        default=0.0,
        description="Average TTFB in ms",
        ge=0.0,
        title="Avg Latency Ttfb Ms",
    )
    avg_eou_delay_ms: float | None = Field(
        default=0.0,
        description="Average end-of-utterance VAD delay in ms",
        ge=0.0,
        title="Avg Eou Delay Ms",
    )
    asr_latency_ms_p50: float | None = Field(
        default=0.0,
        description="Median ASR latency in ms",
        ge=0.0,
        title="Asr Latency Ms P50",
    )


class CampaignAttemptResponse(BaseModel):
    """
    One attempt to dial a single contact.

    Phase 1 introduces this as the per-attempt progress primitive.
    """

    id: UUID = Field(..., title="Id")
    campaign_id: UUID = Field(..., title="Campaign Id")
    contact_id: UUID = Field(..., title="Contact Id")
    attempt_number: int = Field(..., title="Attempt Number")
    outcome: str = Field(..., title="Outcome")
    error_message: str | None = Field(default=None, title="Error Message")
    scheduled_for: AwareDatetime | None = Field(default=None, title="Scheduled For")
    dispatched_at: AwareDatetime | None = Field(default=None, title="Dispatched At")
    completed_at: AwareDatetime | None = Field(default=None, title="Completed At")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class CampaignConfig(BaseModel):
    """
    Campaign dialer configuration.

    Concurrency is governed by the org-level cap (Organization.sku →
    effective_max_concurrent_calls). Per-campaign concurrency / per-minute
    knobs were removed in the May-2026 dispatcher refactor — they
    duplicated the org cap and silently throttled high-Scale orgs to a
    legacy default of 5 (or whatever the wizard slider was set to).
    """

    call_timeout_seconds: int | None = Field(default=None, title="Call Timeout Seconds")
    retry_attempts: int | None = Field(default=None, title="Retry Attempts")
    retry_delay_seconds: int | None = Field(default=None, title="Retry Delay Seconds")
    retry_outcomes: list[str] | None = Field(default=None, title="Retry Outcomes")


class CampaignPerformance(BaseModel):
    """
    Performance metrics for a single campaign.
    """

    campaign_id: str = Field(..., description="Campaign ID", title="Campaign Id")
    campaign_name: str = Field(
        ..., description="Campaign display name", title="Campaign Name"
    )
    total_calls: int | None = Field(
        default=0, description="Total calls made", ge=0, title="Total Calls"
    )
    answered: int | None = Field(
        default=0, description="Answered calls", ge=0, title="Answered"
    )
    completed: int | None = Field(
        default=0, description="Completed conversations", ge=0, title="Completed"
    )
    failed: int | None = Field(
        default=0, description="Failed calls", ge=0, title="Failed"
    )
    no_answer: int | None = Field(
        default=0, description="No answer", ge=0, title="No Answer"
    )
    voicemail: int | None = Field(
        default=0, description="Voicemail", ge=0, title="Voicemail"
    )
    answer_rate: float | None = Field(
        default=0.0,
        description="Answer rate (0-1)",
        ge=0.0,
        le=1.0,
        title="Answer Rate",
    )
    completion_rate: float | None = Field(
        default=0.0,
        description="Completion rate (0-1)",
        ge=0.0,
        le=1.0,
        title="Completion Rate",
    )
    conversion_rate: float | None = Field(
        default=0.0,
        description="Conversion/success rate (0-1)",
        ge=0.0,
        le=1.0,
        title="Conversion Rate",
    )
    total_duration_min: float | None = Field(
        default=0.0,
        description="Total duration in minutes",
        ge=0.0,
        title="Total Duration Min",
    )
    avg_duration_sec: float | None = Field(
        default=0.0,
        description="Average call duration",
        ge=0.0,
        title="Avg Duration Sec",
    )


class CampaignRetryRequest(BaseModel):
    """
    Body for POST /campaigns/{id}/retry — re-dial failed attempts.

    Both filters are optional:
    - contact_ids: restrict the retry to these contacts only.
    - outcomes:    only retry attempts whose latest outcome is in this set.
                   Default: failed, no_answer, voicemail, busy.

    Creates one new CampaignAttempt per matched contact with
    attempt_number = max(prior attempts) + 1, then enqueues dispatch.
    """

    contact_ids: list[UUID] | None = Field(
        default=None,
        description="Restrict retry to these contacts (default: all matched)",
        title="Contact Ids",
    )
    outcomes: list[str] | None = Field(
        default=None,
        description="Only retry attempts in these outcomes. Default: failed, no_answer, voicemail, busy.",
        title="Outcomes",
    )


class CampaignRetryResponse(BaseModel):
    """
    Result of POST /campaigns/{id}/retry.
    """

    requeued: int = Field(
        ..., description="Number of new attempts created", title="Requeued"
    )
    contacts: list[UUID] | None = Field(
        default=None, description="Contact IDs that were retried", title="Contacts"
    )


class CampaignTestWebhookResponse(BaseModel):
    """
    Result of POST /campaigns/{id}/test-webhook.

    The endpoint fires a synthetic ``campaign.test`` payload against the
    campaign's configured ``status_webhook`` URL so the operator can
    verify their receiver before going live. Receivers should ignore
    this event type — it's distinct from real lifecycle events
    (``campaign.completed``, ``campaign.stopped``, ``campaign.failed``).
    """

    success: bool = Field(
        ..., description="True if the receiver responded 2xx.", title="Success"
    )
    status_code: int | None = Field(
        default=None,
        description="HTTP status code from the receiver.",
        title="Status Code",
    )
    response_body: str | None = Field(
        default=None,
        description="Truncated response body (first 500 chars).",
        title="Response Body",
    )
    latency_ms: int = Field(
        ..., description="Round-trip time in milliseconds.", title="Latency Ms"
    )
    error: str | None = Field(
        default=None,
        description="Set when the request failed before getting a response.",
        title="Error",
    )


class CartesiaEmotion(Enum):
    """
    Cartesia voice emotion presets.
    """

    Happy = "Happy"
    Excited = "Excited"
    Enthusiastic = "Enthusiastic"
    Elated = "Elated"
    Euphoric = "Euphoric"
    Triumphant = "Triumphant"
    Amazed = "Amazed"
    Surprised = "Surprised"
    Flirtatious = "Flirtatious"
    Joking_Comedic = "Joking/Comedic"
    Curious = "Curious"
    Content = "Content"
    Peaceful = "Peaceful"
    Serene = "Serene"
    Calm = "Calm"
    Grateful = "Grateful"
    Affectionate = "Affectionate"
    Trust = "Trust"
    Sympathetic = "Sympathetic"
    Anticipation = "Anticipation"
    Mysterious = "Mysterious"
    Angry = "Angry"
    Mad = "Mad"
    Outraged = "Outraged"
    Frustrated = "Frustrated"
    Agitated = "Agitated"
    Threatened = "Threatened"
    Disgusted = "Disgusted"
    Contempt = "Contempt"
    Envious = "Envious"
    Sarcastic = "Sarcastic"
    Ironic = "Ironic"
    Sad = "Sad"
    Dejected = "Dejected"
    Melancholic = "Melancholic"
    Disappointed = "Disappointed"
    Hurt = "Hurt"
    Guilty = "Guilty"
    Bored = "Bored"
    Tired = "Tired"
    Rejected = "Rejected"
    Nostalgic = "Nostalgic"
    Wistful = "Wistful"
    Apologetic = "Apologetic"
    Hesitant = "Hesitant"
    Insecure = "Insecure"
    Confused = "Confused"
    Resigned = "Resigned"
    Anxious = "Anxious"
    Panicked = "Panicked"
    Alarmed = "Alarmed"
    Scared = "Scared"
    Neutral = "Neutral"
    Proud = "Proud"
    Confident = "Confident"
    Distant = "Distant"
    Skeptical = "Skeptical"
    Contemplative = "Contemplative"
    Determined = "Determined"


class CartesiaModel(Enum):
    """
    Cartesia TTS models - Updated Apr 2026.
    """

    sonic_3_5 = "sonic-3.5"
    sonic_3 = "sonic-3"


class CartesiaSpeed(Enum):
    """
    Cartesia speed presets.
    """

    fastest = "fastest"
    fast = "fast"
    normal = "normal"
    slow = "slow"
    slowest = "slowest"


class CartesiaVoiceConfig(BaseModel):
    """
    Cartesia voice configuration.

    SDK Defaults:
    - model: "sonic-3"
    - language: "en"
    - sample_rate: 24000
    """

    provider: Literal["cartesia"] = Field(default="cartesia", title="Provider")
    voice_id: str | None = Field(
        default="8d8ce8c9-44a4-46c4-b10f-9a927b99a853",
        description="Cartesia voice ID",
        title="Voice Id",
    )
    model: CartesiaModel | None = Field(
        default="sonic-3", description="Cartesia model to use"
    )
    speed: CartesiaSpeed | float | None = Field(
        default=None, description="Speaking speed. Preset name or float", title="Speed"
    )
    emotion: list[CartesiaEmotion] | None = Field(
        default=None, description="Emotion tags to apply", title="Emotion"
    )
    volume: float | None = Field(
        default=None, description="Volume adjustment", title="Volume"
    )
    language: str | None = Field(
        default="en", description="Language code", title="Language"
    )


class ChatChannelMetrics(BaseModel):
    """
    Per-channel chat slice (sms or whatsapp_chat).
    """

    channel: str = Field(..., title="Channel")
    conversations: int | None = Field(default=0, ge=0, title="Conversations")
    messages_total: int | None = Field(default=0, ge=0, title="Messages Total")
    messages_inbound: int | None = Field(default=0, ge=0, title="Messages Inbound")
    messages_outbound: int | None = Field(default=0, ge=0, title="Messages Outbound")
    delivered: int | None = Field(default=0, ge=0, title="Delivered")
    read: int | None = Field(default=0, ge=0, title="Read")
    failed: int | None = Field(default=0, ge=0, title="Failed")


class ChatDeliveryBreakdown(BaseModel):
    """
    Funnel counts per channel for the delivery rate panel.
    """

    channel: str = Field(..., title="Channel")
    sent: int | None = Field(default=0, ge=0, title="Sent")
    delivered: int | None = Field(default=0, ge=0, title="Delivered")
    read: int | None = Field(default=0, ge=0, title="Read")
    failed: int | None = Field(default=0, ge=0, title="Failed")


class AvgFirstResponseSeconds(RootModel[float]):
    root: float = Field(
        ...,
        description="Median seconds between first inbound and first outbound reply.",
        ge=0.0,
        title="Avg First Response Seconds",
    )


class ChatKPIs(BaseModel):
    """
    Top-line chat dashboard KPIs.
    """

    active_conversations: int | None = Field(
        default=0, ge=0, title="Active Conversations"
    )
    total_messages: int | None = Field(
        default=0,
        description="Inbound + outbound in window",
        ge=0,
        title="Total Messages",
    )
    inbound_messages: int | None = Field(default=0, ge=0, title="Inbound Messages")
    outbound_messages: int | None = Field(default=0, ge=0, title="Outbound Messages")
    avg_messages_per_conversation: float | None = Field(
        default=0.0, ge=0.0, title="Avg Messages Per Conversation"
    )
    avg_first_response_seconds: AvgFirstResponseSeconds | None = Field(
        default=None,
        description="Median seconds between first inbound and first outbound reply.",
        title="Avg First Response Seconds",
    )


class ChatVolumePoint(BaseModel):
    """
    One bucket of the stacked message-volume chart.
    """

    date: str = Field(..., description="ISO date or hour bucket key", title="Date")
    sms: int | None = Field(default=0, ge=0, title="Sms")
    whatsapp_chat: int | None = Field(default=0, ge=0, title="Whatsapp Chat")
    total: int | None = Field(default=0, ge=0, title="Total")


class CollectDtmfConfig(BaseModel):
    """
    Configuration for collecting DTMF (keypad) input.
    """

    enabled: bool | None = Field(
        default=False, description="Enable DTMF collection", title="Enabled"
    )
    max_digits: int | None = Field(
        default=10,
        description="Maximum digits to collect",
        ge=1,
        le=50,
        title="Max Digits",
    )
    timeout_seconds: float | None = Field(
        default=10.0,
        description="Timeout for digit entry",
        ge=1.0,
        le=60.0,
        title="Timeout Seconds",
    )
    stop_character: str | None = Field(
        default="#", description="Character to end input", title="Stop Character"
    )
    allow_spoken: bool | None = Field(
        default=True, description="Also accept spoken digits", title="Allow Spoken"
    )
    inter_digit_timeout: float | None = Field(
        default=3.0,
        description="Timeout between digits",
        ge=0.5,
        le=10.0,
        title="Inter Digit Timeout",
    )


class CombinedCost(BaseModel):
    """
    Cross-channel cost roll-up for the combined dashboard.
    """

    voice_usd: float | None = Field(default=0.0, ge=0.0, title="Voice Usd")
    chat_usd: float | None = Field(default=0.0, ge=0.0, title="Chat Usd")
    total_usd: float | None = Field(default=0.0, ge=0.0, title="Total Usd")


class ComponentAdminOut(BaseModel):
    """
    Admin view of component - no history needed
    """

    id: UUID = Field(..., title="Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(..., title="Description")
    group_name: str = Field(..., title="Group Name")
    status: str = Field(..., title="Status")
    last_response_time_ms: float | None = Field(..., title="Last Response Time Ms")
    uptime_percentage: float = Field(..., title="Uptime Percentage")
    status_url: str | None = Field(default=None, title="Status Url")
    health_check_url: str | None = Field(default=None, title="Health Check Url")
    health_check_type: str | None = Field(default=None, title="Health Check Type")
    health_check_interval: int | None = Field(
        default=None, title="Health Check Interval"
    )
    display_order: int | None = Field(default=0, title="Display Order")
    is_visible: bool | None = Field(default=True, title="Is Visible")
    created_at: AwareDatetime | None = Field(default=None, title="Created At")
    updated_at: AwareDatetime | None = Field(default=None, title="Updated At")


class ComponentCreate(BaseModel):
    name: str = Field(..., title="Name")
    description: str | None = Field(default=None, title="Description")
    group_name: str | None = Field(default="Core Services", title="Group Name")
    display_order: int | None = Field(default=0, title="Display Order")
    status_url: str | None = Field(default=None, title="Status Url")
    health_check_url: str | None = Field(default=None, title="Health Check Url")
    health_check_type: str | None = Field(default="http", title="Health Check Type")
    health_check_interval: int | None = Field(default=60, title="Health Check Interval")


class ComponentOut(BaseModel):
    id: UUID = Field(..., title="Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(..., title="Description")
    group_name: str = Field(..., title="Group Name")
    status: str = Field(..., title="Status")
    last_response_time_ms: float | None = Field(..., title="Last Response Time Ms")
    uptime_percentage: float = Field(..., title="Uptime Percentage")
    status_url: str | None = Field(default=None, title="Status Url")
    history: list[dict[str, Any]] = Field(..., title="History")


class ComponentStatusUpdate(BaseModel):
    """
    Request body for updating component status only
    """

    status: str = Field(..., title="Status")


class ComponentUpdate(BaseModel):
    name: str | None = Field(default=None, title="Name")
    description: str | None = Field(default=None, title="Description")
    group_name: str | None = Field(default=None, title="Group Name")
    status: str | None = Field(default=None, title="Status")
    display_order: int | None = Field(default=None, title="Display Order")
    status_url: str | None = Field(default=None, title="Status Url")
    health_check_url: str | None = Field(default=None, title="Health Check Url")
    health_check_type: str | None = Field(default=None, title="Health Check Type")
    health_check_interval: int | None = Field(
        default=None, title="Health Check Interval"
    )
    is_visible: bool | None = Field(default=None, title="Is Visible")


class ConcurrencyResponse(BaseModel):
    current_concurrent: int = Field(..., title="Current Concurrent")
    limit: int = Field(..., title="Limit")
    available: int = Field(..., title="Available")
    unlimited: bool = Field(..., title="Unlimited")


class ContactImportCommitRequest(BaseModel):
    """
    Body for POST /call-lists/{id}/contacts/import.

    ``mapping`` overrides ``suggested_mapping`` from the preview step.
    Headers omitted from ``mapping`` are imported into ``contact_data``
    so dynamic-variable agents can still address them.
    """

    preview_token: str = Field(..., title="Preview Token")
    mapping: dict[str, str] | None = Field(default=None, title="Mapping")
    run_async: bool | None = Field(
        default=False,
        description="Force the background path. Auto-on for files >1000 rows; the FE may also opt in to background mode for smaller files to keep the UI responsive.",
        title="Run Async",
    )


class ContactImportCommitResponse(BaseModel):
    """
    One of two shapes depending on ``run_async``:

    - sync: returns the final result inline.
    - async: returns ``{job_id, status: "queued"}`` and the FE polls
      GET /call-lists/import-jobs/{job_id} for progress.
    """

    job_id: str | None = Field(
        default=None,
        description="Set when run_async is true; poll for progress.",
        title="Job Id",
    )
    status: str = Field(..., description="queued | completed | failed", title="Status")
    imported_count: int | None = Field(default=0, title="Imported Count")
    skipped_count: int | None = Field(default=0, title="Skipped Count")
    dnc_blocked_count: int | None = Field(default=0, title="Dnc Blocked Count")
    errors: list[dict[str, Any]] | None = Field(default=None, title="Errors")


class ContactImportInvalidRow(BaseModel):
    """
    One bad row surfaced in the preview screen so the user can fix
    their CSV before committing the import.
    """

    row_number: int = Field(
        ..., description="1-indexed row number, header = row 1", title="Row Number"
    )
    reason: str = Field(
        ..., description="Why the row failed validation", title="Reason"
    )
    raw: dict[str, str] | None = Field(
        default=None, description="Raw cell values for this row", title="Raw"
    )


class ContactImportPreviewResponse(BaseModel):
    """
    What POST /call-lists/{id}/contacts/preview returns.

    The FE renders a column-mapping screen using ``detected_headers`` +
    ``suggested_mapping``. The user can override any mapping, then POSTs
    back to /import with the ``preview_token``.
    """

    preview_token: str = Field(
        ...,
        description="Opaque token to pass to /import. TTL ~10 minutes.",
        title="Preview Token",
    )
    detected_headers: list[str] = Field(..., title="Detected Headers")
    suggested_mapping: dict[str, str] | None = Field(
        default=None,
        description="raw_header → canonical_field mapping derived from header aliases.",
        title="Suggested Mapping",
    )
    sample_rows: list[dict[str, str]] | None = Field(
        default=None,
        description="First 10 rows with raw cell values.",
        title="Sample Rows",
    )
    invalid_rows_preview: list[ContactImportInvalidRow] | None = Field(
        default=None,
        description="First 10 invalid rows with reasons.",
        title="Invalid Rows Preview",
    )
    total_rows: int = Field(..., title="Total Rows")
    encoding: str = Field(..., title="Encoding")
    delimiter: str = Field(..., title="Delimiter")


class ContactImportProgressError(BaseModel):
    row_number: int = Field(..., title="Row Number")
    phone: str | None = Field(default="", title="Phone")
    reason: str = Field(..., title="Reason")


class ContactImportProgressResponse(BaseModel):
    """
    Progress snapshot for the GET /call-lists/import-jobs/{job_id} poll.
    """

    status: str = Field(
        ..., description="queued | running | completed | failed", title="Status"
    )
    total: int | None = Field(default=0, title="Total")
    processed: int | None = Field(default=0, title="Processed")
    imported: int | None = Field(default=0, title="Imported")
    skipped: int | None = Field(default=0, title="Skipped")
    dnc_blocked: int | None = Field(default=0, title="Dnc Blocked")
    errors: list[ContactImportProgressError] | None = Field(
        default=None, title="Errors"
    )
    completed_at: AwareDatetime | None = Field(default=None, title="Completed At")
    error_summary: str | None = Field(default=None, title="Error Summary")


class ContributionDataPoint(BaseModel):
    """
    Single data point for contribution heatmap (GitHub-style activity).
    """

    date: str = Field(..., description="Date in YYYY-MM-DD format", title="Date")
    count: int | None = Field(
        default=0, description="Activity count for this day", ge=0, title="Count"
    )
    level: int | None = Field(
        default=0,
        description="Intensity level 0-4 for coloring",
        ge=0,
        le=4,
        title="Level",
    )


class ConversationDynamicVariablesUpdateRequest(BaseModel):
    """
    Operator update to a conversation's per-conversation runtime variable
    bucket. Replaces the dual-purpose ``dynamic_variables`` field that used
    to live on every send request — Stage 7c (option A) split context-setting
    out of message-send so the freeform composer doesn't carry vars dead-weight.

    Default merge semantics: caller-supplied keys are merged into the
    existing bucket (last-write-wins per key). Pass ``replace=True`` to
    fully overwrite — useful for "operator typed a fresh attribute set"
    flows where stale keys should be cleared.
    """

    dynamic_variables: dict[str, str] | None = Field(
        default=None,
        description="Map of variable name to value. Keys with reserved prefix ``system__`` are stripped server-side (platform-controlled).",
        title="Dynamic Variables",
    )
    replace: bool | None = Field(
        default=False,
        description="True = full replace (existing keys not in the payload are cleared). False (default) = merge into existing bucket.",
        title="Replace",
    )


class ConversationLastMessage(BaseModel):
    """
    Denormalised preview of the most-recent message for inbox rendering.
    """

    id: str | None = Field(default=None, title="Id")
    external_message_id: str | None = Field(default=None, title="External Message Id")
    type: str = Field(..., title="Type")
    body: str | None = Field(default=None, title="Body")
    direction: str = Field(..., title="Direction")
    status: str = Field(..., title="Status")
    sent_at: AwareDatetime = Field(..., title="Sent At")


class ConversationResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    agent_id: UUID | None = Field(default=None, title="Agent Id")
    channel: str = Field(..., title="Channel")
    whatsapp_account_id: UUID | None = Field(default=None, title="Whatsapp Account Id")
    phone_number_id: UUID | None = Field(default=None, title="Phone Number Id")
    contact_address: str = Field(..., title="Contact Address")
    business_address: str = Field(..., title="Business Address")
    contact_name: str | None = Field(default=None, title="Contact Name")
    dynamic_variables: dict[str, Any] | None = Field(
        default=None, title="Dynamic Variables"
    )
    status: str = Field(..., title="Status")
    started_at: AwareDatetime = Field(..., title="Started At")
    ended_at: AwareDatetime | None = Field(default=None, title="Ended At")
    end_reason: str | None = Field(default=None, title="End Reason")
    message_count: int = Field(..., title="Message Count")
    last_message_at: AwareDatetime | None = Field(default=None, title="Last Message At")
    last_message: ConversationLastMessage | None = None
    last_read_at: AwareDatetime | None = Field(default=None, title="Last Read At")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class MediaUrls(RootModel[list[str]]):
    root: list[str] = Field(
        ...,
        description="MMS attachments (SMS only — WhatsApp text endpoint rejects).",
        max_length=10,
        title="Media Urls",
    )


class ClientTempId(RootModel[str]):
    root: str = Field(
        ...,
        description="Client-supplied id echoed back for optimistic UI reconciliation.",
        max_length=64,
        title="Client Temp Id",
    )


class ConversationSendRequest(BaseModel):
    """
    Send a message inside an existing conversation.
    """

    body: str = Field(..., max_length=4096, min_length=1, title="Body")
    media_urls: MediaUrls | None = Field(
        default=None,
        description="MMS attachments (SMS only — WhatsApp text endpoint rejects).",
        title="Media Urls",
    )
    client_temp_id: ClientTempId | None = Field(
        default=None,
        description="Client-supplied id echoed back for optimistic UI reconciliation.",
        title="Client Temp Id",
    )


class ConversationTurnSummary(BaseModel):
    speaker: str = Field(..., title="Speaker")
    text: str = Field(..., title="Text")
    timestamp: AwareDatetime = Field(..., title="Timestamp")
    sentiment_score: float | None = Field(default=None, title="Sentiment Score")
    sentiment_label: str | None = Field(default=None, title="Sentiment Label")
    speaker_id: str | None = Field(default=None, title="Speaker Id")
    speaker_confidence: float | None = Field(default=None, title="Speaker Confidence")


class CreateWorkflowRequest(BaseModel):
    name: str = Field(..., max_length=255, min_length=1, title="Name")
    description: str | None = Field(default=None, title="Description")
    agent_id: UUID | None = Field(default=None, title="Agent Id")


class DNCCheckResponse(BaseModel):
    phone: str = Field(..., title="Phone")
    canonical_phone: str | None = Field(default=None, title="Canonical Phone")
    result: str = Field(..., title="Result")
    matched_source: str | None = Field(default=None, title="Matched Source")


class DNCEntryAddRequest(BaseModel):
    phone: str = Field(..., max_length=20, min_length=5, title="Phone")
    reason: Reason | None = Field(default=None, title="Reason")


class DNCEntryResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    phone_e164: str = Field(..., title="Phone E164")
    country_iso2: str = Field(..., title="Country Iso2")
    source: str = Field(..., title="Source")
    source_org_id: UUID | None = Field(..., title="Source Org Id")
    reason: str | None = Field(..., title="Reason")
    added_at: AwareDatetime = Field(..., title="Added At")
    expires_at: AwareDatetime | None = Field(..., title="Expires At")


class DNCSettingsRequest(BaseModel):
    protection_enabled: bool | None = Field(default=None, title="Protection Enabled")
    auto_add_inbound_optouts: bool | None = Field(
        default=None, title="Auto Add Inbound Optouts"
    )


class DNCSettingsResponse(BaseModel):
    organization_id: UUID = Field(..., title="Organization Id")
    protection_enabled: bool = Field(..., title="Protection Enabled")
    auto_add_inbound_optouts: bool = Field(..., title="Auto Add Inbound Optouts")


class DayOfWeekDistribution(BaseModel):
    """
    Call distribution by day of week.
    """

    day: int = Field(
        ..., description="Day of week (0=Monday, 6=Sunday)", ge=0, le=6, title="Day"
    )
    day_name: str = Field(
        ..., description="Day name (Monday, Tuesday, etc.)", title="Day Name"
    )
    calls: int | None = Field(default=0, description="Call count", ge=0, title="Calls")
    avg_duration_sec: float | None = Field(
        default=0.0, description="Average duration", ge=0.0, title="Avg Duration Sec"
    )


class DeepgramLanguage(Enum):
    """
    Deepgram supported languages (BCP-47 format).
    """

    en = "en"
    en_US = "en-US"
    en_GB = "en-GB"
    en_AU = "en-AU"
    ar = "ar"
    ar_AE = "ar-AE"
    ar_SA = "ar-SA"
    ar_EG = "ar-EG"
    ar_QA = "ar-QA"
    ar_KW = "ar-KW"
    ar_JO = "ar-JO"
    ar_LB = "ar-LB"
    ar_SY = "ar-SY"
    ar_IQ = "ar-IQ"
    ar_MA = "ar-MA"
    ar_DZ = "ar-DZ"
    ar_TN = "ar-TN"
    ar_PS = "ar-PS"
    ar_SD = "ar-SD"
    ar_TD = "ar-TD"
    ar_IR = "ar-IR"
    es = "es"
    es_419 = "es-419"
    fr = "fr"
    de = "de"
    it = "it"
    pt = "pt"
    pt_BR = "pt-BR"
    nl = "nl"
    hi = "hi"
    ru = "ru"
    ja = "ja"
    zh = "zh"
    ko = "ko"
    tr = "tr"
    uk = "uk"
    pl = "pl"
    vi = "vi"
    multi = "multi"


class DeepgramNovaModel(Enum):
    """
    Deepgram Nova-3 transcription models - uses STT class (/v1/listen API).

    SDK Default: model="nova-3", language="en-US"
    No Nova-4 exists as of 2026-04. Deepgram Flux is a separate model line (removed).
    """

    nova_3 = "nova-3"
    nova_3_medical = "nova-3-medical"
    flux = "flux"
    flux_multilingual = "flux-multilingual"


class DeepgramTranscriberConfig(BaseModel):
    """
    Deepgram Nova-3 transcriber configuration - uses STT class (/v1/listen API).

    Best-in-class accuracy for general transcription.
    Full feature set: punctuation, smart formatting, diarization, language detection.
    """

    provider: Literal["deepgram"] = Field(default="deepgram", title="Provider")
    model: DeepgramNovaModel | None = Field(
        default="nova-3", description="Deepgram Nova-3 model to use for transcription"
    )
    language: DeepgramLanguage | None = Field(
        default="en-US",
        description="Transcription language (BCP-47 format). Use 'multi' for multilingual streaming.",
    )
    smart_format: bool | None = Field(
        default=False,
        description="Apply smart formatting (numbers, dates, addresses)",
        title="Smart Format",
    )
    punctuate: bool | None = Field(
        default=True, description="Add punctuation to transcription", title="Punctuate"
    )
    numerals: bool | None = Field(
        default=False, description="Convert spoken numbers to digits", title="Numerals"
    )
    enable_diarization: bool | None = Field(
        default=False,
        description="Enable speaker diarization (identify different speakers)",
        title="Enable Diarization",
    )
    keyterms: list[str] | None = Field(
        default=None,
        description="Key terms to improve recognition accuracy (Nova-3 only)",
        title="Keyterms",
    )
    interim_results: bool | None = Field(
        default=True,
        description="Return partial transcripts during streaming (required for low-latency agents)",
        title="Interim Results",
    )
    endpointing_ms: int | None = Field(
        default=300,
        description="Silence duration (ms) before Deepgram considers utterance complete",
        ge=10,
        le=5000,
        title="Endpointing Ms",
    )
    filler_words: bool | None = Field(
        default=False,
        description="Include filler words (um, uh) in transcripts",
        title="Filler Words",
    )
    profanity_filter: bool | None = Field(
        default=False,
        description="Filter profanity from transcripts",
        title="Profanity Filter",
    )
    mip_opt_out: bool | None = Field(
        default=False,
        description="Opt out of model improvement program",
        title="Mip Opt Out",
    )


class DialFailureDetail(BaseModel):
    """
    402 body for outbound dial pre-checks.

    Audit fix M2: first-class schema for the structured 402 returned when
    `BillingService.check_call_balance` rejects a call. The frontend keys
    off `code` rather than substring-matching the human `message`, so
    backend wording changes can no longer silently flip the
    override-allowed UI state.

    Codes:
      - dnc_blocked          → number on org's DNC list; admin can override
                                with `force_dnc_override=true` + reason
      - dnc_opted_in_blocked → recipient explicitly opted IN to DNC
                                protection; no override permitted
      - insufficient_credits → ledger short of the call's pre-auth
    """

    code: str = Field(
        ...,
        description="Machine-readable failure category — see class docstring.",
        title="Code",
    )
    can_override: bool = Field(
        ...,
        description="True when the operator can re-submit with force_dnc_override=true.",
        title="Can Override",
    )
    message: str = Field(
        ..., description="Human-readable detail for display.", title="Message"
    )


class CallerIdName(RootModel[str]):
    root: str = Field(
        ...,
        description="Caller ID display name (max 50 chars).",
        max_length=50,
        title="Caller Id Name",
    )


class ForceDncOverrideReason(RootModel[str]):
    root: str = Field(
        ...,
        description="Free-text justification for the DNC override (logged to dnc_check_log for audit). Required when force_dnc_override=True.",
        max_length=500,
        title="Force Dnc Override Reason",
    )


class DialRequest(BaseModel):
    """
    POST /v1/voice-sessions/outbound — initiate a single phone-channel call.
    """

    agent_id: UUID = Field(..., title="Agent Id")
    to_number: str = Field(
        ...,
        description="Destination phone number (E.164 format, e.g., +15551234567)",
        max_length=20,
        min_length=10,
        title="To Number",
    )
    number_id: UUID = Field(
        ..., description="Phone number ID to use for caller ID", title="Number Id"
    )
    caller_id_number: str | None = Field(
        default=None,
        description="Override caller ID number (E.164). Defaults to number_id's DID.",
        title="Caller Id Number",
    )
    caller_id_name: CallerIdName | None = Field(
        default=None,
        description="Caller ID display name (max 50 chars).",
        title="Caller Id Name",
    )
    dynamic_variables: dict[str, Any] | None = Field(
        default=None,
        description="Dynamic variables injected into agent prompts via {{var}} syntax.",
        title="Dynamic Variables",
    )
    agent_override: dict[str, Any] | None = Field(
        default=None,
        description="Per-call deep-merged agent config overrides.",
        title="Agent Override",
    )
    force_dnc_override: bool | None = Field(
        default=False,
        description="When true AND the org has DNC protection_enabled=False, allows the call to proceed even if the destination is on the DNC directory. Requires force_dnc_override_reason. Opt-IN orgs cannot override.",
        title="Force Dnc Override",
    )
    force_dnc_override_reason: ForceDncOverrideReason | None = Field(
        default=None,
        description="Free-text justification for the DNC override (logged to dnc_check_log for audit). Required when force_dnc_override=True.",
        title="Force Dnc Override Reason",
    )


class DialResponse(BaseModel):
    """
    Response from outbound voice-session creation.
    """

    success: bool = Field(..., title="Success")
    call_id: str | None = Field(default=None, title="Call Id")
    to_number: str = Field(..., title="To Number")
    from_number: str | None = Field(default=None, title="From Number")
    agent_id: UUID = Field(..., title="Agent Id")
    created_at: AwareDatetime | None = Field(default=None, title="Created At")
    error: str | None = Field(default=None, title="Error")


class EdgeCondition(BaseModel):
    field: str | None = Field(default=None, title="Field")
    operator: str | None = Field(default=None, title="Operator")
    value: str | None = Field(default=None, title="Value")


class EmailSubscribeRequest(BaseModel):
    """
    Email subscription request
    """

    email: EmailStr = Field(..., title="Email")
    notify_on: list[str] | None = Field(default=None, title="Notify On")


class ExchangeRateResponse(BaseModel):
    """
    Exchange rate for organization's billing currency.
    """

    base_currency: str = Field(..., title="Base Currency")
    target_currency: str = Field(..., title="Target Currency")
    rate: float = Field(..., title="Rate")


class FirstMessageConfig(BaseModel):
    """
    Configuration for agent's first message.
    """

    enabled: bool | None = Field(
        default=True, description="Whether to send a greeting message", title="Enabled"
    )
    text: str | None = Field(
        default="Hello! How can I help you today?",
        description="Greeting message text",
        title="Text",
    )
    delay_ms: int | None = Field(
        default=400,
        description="Delay before speaking (ms)",
        ge=0,
        le=5000,
        title="Delay Ms",
    )
    allow_interruptions: bool | None = Field(
        default=False,
        description="Allow user to interrupt greeting",
        title="Allow Interruptions",
    )


class GroqModel(Enum):
    """
    Groq fast inference models - Updated Apr 2026.
    """

    llama_3_1_8b_instant = "llama-3.1-8b-instant"
    meta_llama_llama_4_scout_17b_16e_instruct = (
        "meta-llama/llama-4-scout-17b-16e-instruct"
    )
    openai_gpt_oss_20b = "openai/gpt-oss-20b"


class ReasoningEffort(Enum):
    """
    Reasoning effort for GPT-OSS reasoning models (openai/gpt-oss-20b, openai/gpt-oss-120b). Only 'low', 'medium', 'high' are valid — 'none' is not supported for these models. None = use API default (medium). Only set when using a reasoning model.
    """

    low = "low"
    medium = "medium"
    high = "high"


class HangupResponse(BaseModel):
    success: bool = Field(..., title="Success")
    call_id: str = Field(..., title="Call Id")
    status: str = Field(..., title="Status")
    timestamp: str = Field(..., title="Timestamp")


class HangupToolConfig(BaseModel):
    """
    Configuration for the hangup tool.
    """

    enabled: bool | None = Field(
        default=True, description="Enable hangup capability", title="Enabled"
    )
    farewell_message: str | None = Field(
        default="Goodbye!",
        description="Message before ending call",
        title="Farewell Message",
    )
    keywords: list[str] | None = Field(
        default=["goodbye", "bye", "end call", "hang up"],
        description="Keywords that trigger hangup consideration",
        title="Keywords",
    )
    confirm_before_hangup: bool | None = Field(
        default=False,
        description="Ask for confirmation before hanging up",
        title="Confirm Before Hangup",
    )
    confirmation_prompt: str | None = Field(
        default="Are you sure you'd like to end the call?",
        description="Confirmation message if enabled",
        title="Confirmation Prompt",
    )


class HealthCheckResult(BaseModel):
    name: str = Field(..., title="Name")
    status: str = Field(..., title="Status")
    response_time_ms: float | None = Field(..., title="Response Time Ms")
    error: str | None = Field(..., title="Error")
    last_checked: AwareDatetime = Field(..., title="Last Checked")


class HourlyDistribution(BaseModel):
    """
    Call distribution by hour of day (for heatmaps).
    """

    hour: int = Field(..., description="Hour of day (0-23)", ge=0, le=23, title="Hour")
    calls: int | None = Field(default=0, description="Call count", ge=0, title="Calls")
    avg_duration_sec: float | None = Field(
        default=0.0, description="Average duration", ge=0.0, title="Avg Duration Sec"
    )


class ImportAccountRequest(BaseModel):
    """
    Received after the Meta Embedded Signup OAuth popup completes.
    The frontend sends the auth code + identifiers from the Meta session event.
    """

    token_code: str = Field(
        ...,
        description="OAuth authorization code from Meta Embedded Signup",
        title="Token Code",
    )
    phone_number_id: str = Field(
        ...,
        description="WhatsApp phone number ID from Meta session event",
        title="Phone Number Id",
    )
    business_account_id: str = Field(
        ..., description="WABA ID from Meta session event", title="Business Account Id"
    )


class IncidentCreate(BaseModel):
    title: str = Field(..., title="Title")
    impact: str | None = Field(default="minor", title="Impact")
    message: str = Field(..., title="Message")
    affected_component_ids: list[UUID] | None = Field(
        default=[], title="Affected Component Ids"
    )
    component_status: str | None = Field(default="degraded", title="Component Status")


class IncidentUpdateCreate(BaseModel):
    status: str = Field(..., title="Status")
    message: str = Field(..., title="Message")


class IncidentUpdateOut(BaseModel):
    id: UUID = Field(..., title="Id")
    status: str = Field(..., title="Status")
    message: str = Field(..., title="Message")
    created_by: str | None = Field(..., title="Created By")
    created_at: AwareDatetime = Field(..., title="Created At")


class TemplateBody1(RootModel[str]):
    root: str = Field(
        ...,
        description="Raw template body string for the permission-request template. Supplied by the frontend after fetching the definition from Meta. When given, server resolves ``{{placeholder}}`` against ``dynamic_variables`` to build ``template_params``.",
        max_length=4096,
        title="Template Body",
    )


class InterruptionConfig(BaseModel):
    """
    Configuration for handling user interruptions.

    Controls when and how the agent stops speaking when the user starts talking.
    Uses VAD (voice activity detection) for interruption detection.
    """

    enabled: bool | None = Field(
        default=True,
        description="Allow user to interrupt while agent is speaking.",
        title="Enabled",
    )
    mode: Literal["vad"] = Field(
        default="vad",
        description="vad: voice-activity detection based interruption.",
        title="Mode",
    )
    discard_audio_if_uninterruptible: bool | None = Field(
        default=True,
        description="Drop buffered audio while agent is speaking and cannot be interrupted.",
        title="Discard Audio If Uninterruptible",
    )
    min_duration: float | None = Field(
        default=0.5,
        description="Minimum seconds of speech before registering as interruption. Default: 0.5",
        ge=0.0,
        le=2.0,
        title="Min Duration",
    )
    min_words: int | None = Field(
        default=0,
        description="Minimum transcribed words to count as interruption. 0 = audio-only (faster). Default: 0",
        ge=0,
        le=10,
        title="Min Words",
    )
    false_interruption_timeout: float | None = Field(
        default=2.0,
        description="Seconds of silence after interruption before deciding it was false. Default: 2.0",
        ge=0.5,
        le=10.0,
        title="False Interruption Timeout",
    )
    resume_false_interruption: bool | None = Field(
        default=True,
        description="Resume agent speech from where it stopped after a false interruption. Default: True",
        title="Resume False Interruption",
    )


class InvitationResponse(BaseModel):
    """
    A pending invitation.
    """

    id: str = Field(..., title="Id")
    email: str = Field(..., title="Email")
    role: str = Field(..., title="Role")
    status: str = Field(..., title="Status")
    created_at: str = Field(..., title="Created At")
    expires_at: str | None = Field(default=None, title="Expires At")


class InvitationsListResponse(BaseModel):
    """
    List of pending invitations.
    """

    data: list[InvitationResponse] = Field(..., title="Data")
    total_count: int = Field(..., title="Total Count")


class Role(Enum):
    admin = "admin"
    operator = "operator"
    viewer = "viewer"


class InviteMemberRequest(BaseModel):
    """
    Request to invite a member to an organization.

    Roles: admin, operator, viewer. Permissions come from role.
    """

    email: EmailStr = Field(..., title="Email")
    role: Role | None = Field(default="operator", title="Role")


class InvoiceResponse(BaseModel):
    """
    Credit transaction (invoice) details for prepaid billing.
    """

    id: str = Field(..., title="Id")
    number: str | None = Field(default=None, title="Number")
    amount_due: float | None = Field(default=0, title="Amount Due")
    amount_paid: float = Field(..., title="Amount Paid")
    amount_remaining: float | None = Field(default=0, title="Amount Remaining")
    status: str = Field(..., title="Status")
    billing_reason: str | None = Field(..., title="Billing Reason")
    currency: str = Field(..., title="Currency")
    created: int = Field(..., title="Created")
    period_start: int | None = Field(default=None, title="Period Start")
    period_end: int | None = Field(default=None, title="Period End")
    due_date: int | None = Field(default=None, title="Due Date")
    pdf_url: str | None = Field(default=None, title="Pdf Url")
    hosted_invoice_url: str | None = Field(default=None, title="Hosted Invoice Url")
    description: str | None = Field(default=None, title="Description")


class KPIMetric(BaseModel):
    """
    A single KPI metric with value, trend, and optional formatting.
    """

    value: float = Field(..., description="The numeric value", title="Value")
    formatted: str = Field(
        ...,
        description="Human-readable formatted value (e.g., '3:42', '85.5%')",
        title="Formatted",
    )
    trend_percent: float | None = Field(
        default=None,
        description="Percent change vs previous period",
        title="Trend Percent",
    )
    trend_direction: str | None = Field(
        default=None, description="'up', 'down', or 'flat'", title="Trend Direction"
    )
    previous_value: float | None = Field(
        default=None,
        description="Previous period value for comparison",
        title="Previous Value",
    )


class KeyType(Enum):
    """
    Type of API key.
    """

    master = "master"
    organization = "organization"


class Description2(RootModel[str]):
    root: str = Field(..., max_length=1000, title="Description")


class KnowledgeBaseCreateFromText(BaseModel):
    """
    Create knowledge base from direct text input.
    """

    name: str = Field(
        ..., description="Display name", max_length=255, min_length=1, title="Name"
    )
    content: str = Field(
        ...,
        description="Text content (up to 500KB)",
        max_length=500000,
        min_length=1,
        title="Content",
    )
    description: Description2 | None = Field(default=None, title="Description")


class KnowledgeBaseCreateFromURL(BaseModel):
    """
    Create knowledge base from URL (web scraping).
    """

    name: str = Field(
        ..., description="Display name", max_length=255, min_length=1, title="Name"
    )
    url: AnyUrl = Field(..., description="URL to scrape content from", title="Url")
    description: Description2 | None = Field(default=None, title="Description")


class KnowledgeBaseStatus(Enum):
    """
    Processing status.
    """

    pending = "pending"
    processing = "processing"
    ready = "ready"
    error = "error"


class KnowledgeBaseType(Enum):
    """
    Type of knowledge base source.
    """

    url = "url"
    file = "file"
    text = "text"


class Name3(RootModel[str]):
    root: str = Field(..., max_length=255, min_length=1, title="Name")


class KnowledgeBaseUpdate(BaseModel):
    """
    Update knowledge base metadata and content.
    """

    name: Name3 | None = Field(default=None, title="Name")
    description: Description2 | None = Field(default=None, title="Description")
    content: str | None = Field(
        default=None,
        description="Updated content for text-based documents",
        title="Content",
    )


class LatencyMetrics(BaseModel):
    """
    Latency measurements for AI components.
    """

    ttft_ms: float | None = Field(
        default=0.0,
        description="Time to First Token (LLM) in milliseconds",
        ge=0.0,
        title="Ttft Ms",
    )
    ttfb_ms: float | None = Field(
        default=0.0,
        description="Time to First Byte (TTS) in milliseconds",
        ge=0.0,
        title="Ttfb Ms",
    )
    eou_delay_ms: float | None = Field(
        default=0.0,
        description="End-of-utterance VAD delay (silence confirmation after user stops speaking) in milliseconds",
        ge=0.0,
        title="Eou Delay Ms",
    )
    asr_p50_ms: float | None = Field(
        default=0.0,
        description="Median ASR latency in milliseconds",
        ge=0.0,
        title="Asr P50 Ms",
    )
    total_response_ms: float | None = Field(
        default=None,
        description="Total end-to-end response time",
        title="Total Response Ms",
    )


class MaintenanceCreate(BaseModel):
    """
    Request body for creating maintenance
    """

    title: str = Field(..., title="Title")
    description: str | None = Field(default=None, title="Description")
    scheduled_start: AwareDatetime = Field(..., title="Scheduled Start")
    scheduled_end: AwareDatetime = Field(..., title="Scheduled End")
    affected_components: list[UUID] | None = Field(
        default=None, title="Affected Components"
    )


class MaintenanceOut(BaseModel):
    id: UUID = Field(..., title="Id")
    title: str = Field(..., title="Title")
    description: str | None = Field(..., title="Description")
    scheduled_start: AwareDatetime = Field(..., title="Scheduled Start")
    scheduled_end: AwareDatetime = Field(..., title="Scheduled End")
    is_active: bool = Field(..., title="Is Active")
    is_completed: bool = Field(..., title="Is Completed")
    affected_component_ids: list[UUID] | None = Field(
        default=None, title="Affected Component Ids"
    )
    affected_components: list[str] = Field(..., title="Affected Components")


class MaintenanceUpdate(BaseModel):
    """
    Request body for updating maintenance
    """

    title: str | None = Field(default=None, title="Title")
    description: str | None = Field(default=None, title="Description")
    scheduled_start: AwareDatetime | None = Field(default=None, title="Scheduled Start")
    scheduled_end: AwareDatetime | None = Field(default=None, title="Scheduled End")
    affected_components: list[UUID] | None = Field(
        default=None, title="Affected Components"
    )


class ManualImportRequest(BaseModel):
    """
    Manual account import using a System User access token.
    Used when Embedded Signup is unavailable (e.g., App Review pending)
    or by power users who already have Cloud API configured.
    """

    access_token: str = Field(
        ...,
        description="System User access token from Meta Business Settings",
        title="Access Token",
    )
    phone_number_id: str = Field(
        ...,
        description="WhatsApp phone number ID from API Setup",
        title="Phone Number Id",
    )
    business_account_id: str = Field(
        ...,
        description="WhatsApp Business Account (WABA) ID",
        title="Business Account Id",
    )


class MarkReadResponse(BaseModel):
    """
    Response for marking notifications as read
    """

    success: bool = Field(..., title="Success")
    marked_count: int = Field(..., title="Marked Count")


class McpExecuteRequest(BaseModel):
    arguments: dict[str, Any] | None = Field(default=None, title="Arguments")


class McpExecuteResult(BaseModel):
    success: bool = Field(..., title="Success")
    tool_name: str = Field(..., title="Tool Name")
    arguments: dict[str, Any] | None = Field(default=None, title="Arguments")
    content: list[Any] | None = Field(default=None, title="Content")
    is_error: bool | None = Field(default=False, title="Is Error")
    error: str | None = Field(default=None, title="Error")
    error_type: str | None = Field(default=None, title="Error Type")


class Description5(RootModel[str]):
    root: str = Field(..., max_length=2000, title="Description")


class McpServerCreate(BaseModel):
    name: str = Field(..., max_length=255, min_length=1, title="Name")
    description: Description5 | None = Field(default=None, title="Description")
    server_url: AnyUrl = Field(..., title="Server Url")
    timeout_seconds: int | None = Field(
        default=30, ge=1, le=300, title="Timeout Seconds"
    )
    auth_connection_id: UUID | None = Field(default=None, title="Auth Connection Id")


class McpServerRef(BaseModel):
    """
    Per-agent reference to an MCP server registration.

    Stored on ``agents.config.tools.mcp_servers``. The agent owns only an
    ID + per-attachment allowlist; URL/headers/auth live on the
    ``mcp_servers`` table and are resolved at dispatch time. ``integration_id``
    is the legacy name (pre-rebuild) and is accepted as an alias so older
    saved agent configs keep loading.
    """

    server_id: str = Field(
        ..., description="ID of the MCP server registration", title="Server Id"
    )
    allowed_tools: list[str] | None = Field(
        default=None,
        description="Specific tool names to expose to this agent (None = all)",
        title="Allowed Tools",
    )


class McpServerResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(default=None, title="Description")
    server_url: str = Field(..., title="Server Url")
    timeout_seconds: int = Field(..., title="Timeout Seconds")
    auth_connection_id: UUID | None = Field(default=None, title="Auth Connection Id")
    last_test_status: str | None = Field(default=None, title="Last Test Status")
    last_test_at: str | None = Field(default=None, title="Last Test At")
    last_test_error: str | None = Field(default=None, title="Last Test Error")
    created_at: str | None = Field(default=None, title="Created At")
    updated_at: str | None = Field(default=None, title="Updated At")


class ServerUrl(RootModel[AnyUrl]):
    root: AnyUrl = Field(..., title="Server Url")


class TimeoutSeconds(RootModel[int]):
    root: int = Field(..., ge=1, le=300, title="Timeout Seconds")


class McpServerUpdate(BaseModel):
    name: Name3 | None = Field(default=None, title="Name")
    description: Description5 | None = Field(default=None, title="Description")
    server_url: ServerUrl | None = Field(default=None, title="Server Url")
    timeout_seconds: TimeoutSeconds | None = Field(
        default=None, title="Timeout Seconds"
    )
    auth_connection_id: UUID | None = Field(default=None, title="Auth Connection Id")


class McpTool(BaseModel):
    name: str = Field(..., title="Name")
    description: str | None = Field(default="", title="Description")
    input_schema: dict[str, Any] | None = Field(default=None, title="Input Schema")


class McpValidateRequest(BaseModel):
    """
    Probe a server config WITHOUT persisting it.

    Use either ``auth_connection_id`` to reuse a stored credential, OR
    ``inline_headers`` for a one-shot test (the create modal uses inline
    headers before the auth connection has been created). If both are
    supplied ``inline_headers`` takes priority.
    """

    server_url: AnyUrl = Field(..., title="Server Url")
    timeout_seconds: int | None = Field(
        default=20, ge=1, le=300, title="Timeout Seconds"
    )
    auth_connection_id: UUID | None = Field(default=None, title="Auth Connection Id")
    inline_headers: dict[str, str] | None = Field(default=None, title="Inline Headers")


class MemberResponse(BaseModel):
    """
    A team member in the organization.
    """

    id: str = Field(..., title="Id")
    email: str = Field(..., title="Email")
    first_name: str | None = Field(default=None, title="First Name")
    last_name: str | None = Field(default=None, title="Last Name")
    image_url: str | None = Field(default=None, title="Image Url")
    role: str = Field(..., title="Role")
    joined_at: str | None = Field(default=None, title="Joined At")
    permissions: dict[str, Any] | None = Field(default=None, title="Permissions")


class MembersListResponse(BaseModel):
    """
    List of organization members.
    """

    data: list[MemberResponse] = Field(..., title="Data")
    total_count: int = Field(..., title="Total Count")


class MessageResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    conversation_id: UUID = Field(..., title="Conversation Id")
    organization_id: UUID = Field(..., title="Organization Id")
    channel: str = Field(..., title="Channel")
    direction: str = Field(..., title="Direction")
    external_message_id: str = Field(..., title="External Message Id")
    client_temp_id: str | None = Field(default=None, title="Client Temp Id")
    message_type: str = Field(..., title="Message Type")
    body: str | None = Field(default=None, title="Body")
    media_id: str | None = Field(default=None, title="Media Id")
    media_url: str | None = Field(default=None, title="Media Url")
    media_mime_type: str | None = Field(default=None, title="Media Mime Type")
    template_name: str | None = Field(default=None, title="Template Name")
    template_params: list[dict[str, Any]] | None = Field(
        default=None, title="Template Params"
    )
    interactive_type: str | None = Field(default=None, title="Interactive Type")
    interactive_payload: dict[str, Any] | None = Field(
        default=None, title="Interactive Payload"
    )
    status: str = Field(..., title="Status")
    error_message: str | None = Field(default=None, title="Error Message")
    sent_at: AwareDatetime = Field(..., title="Sent At")
    delivered_at: AwareDatetime | None = Field(default=None, title="Delivered At")
    read_at: AwareDatetime | None = Field(default=None, title="Read At")


class NodePosition(BaseModel):
    x: float = Field(..., title="X")
    y: float = Field(..., title="Y")


class NodeType(Enum):
    conversation = "conversation"
    branch = "branch"
    transfer = "transfer"
    end_call = "end_call"
    sms_send = "sms_send"
    webhook_call = "webhook_call"
    wait = "wait"
    set_variable = "set_variable"
    knowledge_base = "knowledge_base"
    global_ = "global"


class NotFoundError(BaseModel):
    """
    404 Not Found error response
    """

    detail: str = Field(..., title="Detail")


class NotificationOut(BaseModel):
    """
    Notification response schema
    """

    id: UUID = Field(..., title="Id")
    notification_type: str = Field(..., title="Notification Type")
    title: str = Field(..., title="Title")
    message: str = Field(..., title="Message")
    severity: str = Field(..., title="Severity")
    source_type: str | None = Field(default=None, title="Source Type")
    source_id: UUID | None = Field(default=None, title="Source Id")
    is_read: bool = Field(..., title="Is Read")
    read_at: AwareDatetime | None = Field(default=None, title="Read At")
    created_at: AwareDatetime = Field(..., title="Created At")
    extra_data: dict[str, Any] | None = Field(default=None, title="Extra Data")


class NumberAssignResponse(BaseModel):
    message: str = Field(..., title="Message")
    status: str = Field(..., title="Status")


class NumberCapRow(BaseModel):
    """
    One row in the per-region number-cap panel.
    """

    region_tier: str = Field(..., title="Region Tier")
    region_label: str = Field(..., title="Region Label")
    cap: int = Field(..., title="Cap")
    used: int = Field(..., title="Used")
    above_cap_rate_usd: float | None = Field(default=None, title="Above Cap Rate Usd")


class NumberCapsResponse(BaseModel):
    sku: str = Field(..., title="Sku")
    rows: list[NumberCapRow] = Field(..., title="Rows")


class NumberUnassignResponse(BaseModel):
    message: str = Field(..., title="Message")
    status: str = Field(..., title="Status")


class OnboardingStatusResponse(BaseModel):
    """
    Used by the FE to decide whether /outbound should redirect into
    the first-run wizard. ``completed_at`` is null until the user has
    either completed or explicitly skipped onboarding.
    """

    completed_at: str | None = Field(default=None, title="Completed At")


class OpenAIModel(Enum):
    """
    OpenAI chat models - Updated Apr 2026.
    """

    gpt_5_4_mini = "gpt-5.4-mini"
    gpt_5_4_nano = "gpt-5.4-nano"
    gpt_4_1_mini = "gpt-4.1-mini"
    gpt_4_1_nano = "gpt-4.1-nano"


class MaxCompletionTokens(RootModel[int]):
    root: int = Field(
        4096,
        description="Maximum tokens in response",
        ge=1,
        le=128000,
        title="Max Completion Tokens",
    )


class ReasoningEffort1(Enum):
    """
    Reasoning effort for OpenAI reasoning models. Only 'none', 'minimal', 'low', 'medium', 'high', 'max' are valid.
    """

    none = "none"
    minimal = "minimal"
    low = "low"
    medium = "medium"
    high = "high"
    max = "max"


class OrgUsageItem(BaseModel):
    """
    Usage summary for a single organization.
    """

    organization_id: str = Field(..., title="Organization Id")
    call_count: int = Field(..., title="Call Count")
    total_minutes: float = Field(..., title="Total Minutes")
    total_billed: float = Field(..., title="Total Billed")


class Slug(RootModel[str]):
    root: str = Field(..., max_length=100, min_length=1, title="Slug")


class LogoUrl(RootModel[str]):
    root: str = Field(..., max_length=500, title="Logo Url")


class Sku(Enum):
    pilot = "pilot"
    launch = "launch"
    scale = "scale"


class Website(RootModel[str]):
    root: str = Field(..., max_length=500, title="Website")


class Email(RootModel[str]):
    root: str = Field(..., max_length=255, title="Email")


class OrganizationCreate(BaseModel):
    """
    Schema for creating a new organization
    """

    name: str = Field(..., max_length=255, min_length=1, title="Name")
    slug: Slug | None = Field(default=None, title="Slug")
    logo_url: LogoUrl | None = Field(default=None, title="Logo Url")
    sku: Sku | None = Field(default="pilot", title="Sku")
    website: Website | None = Field(default=None, title="Website")
    email: Email | None = Field(default=None, title="Email")


class OpenaiApiKey(RootModel[str]):
    root: str = Field(..., max_length=500, title="Openai Api Key")


class DeepgramApiKey(RootModel[str]):
    root: str = Field(..., max_length=500, title="Deepgram Api Key")


class SonioxApiKey(RootModel[str]):
    root: str = Field(..., max_length=500, title="Soniox Api Key")


class ElevenlabsApiKey(RootModel[str]):
    root: str = Field(..., max_length=500, title="Elevenlabs Api Key")


class GroqApiKey(RootModel[str]):
    root: str = Field(..., max_length=500, title="Groq Api Key")


class CartesiaApiKey(RootModel[str]):
    root: str = Field(..., max_length=500, title="Cartesia Api Key")


class OrganizationCredentialsUpdate(BaseModel):
    """
    Schema for updating organization API credentials only
    """

    openai_api_key: OpenaiApiKey | None = Field(default=None, title="Openai Api Key")
    deepgram_api_key: DeepgramApiKey | None = Field(
        default=None, title="Deepgram Api Key"
    )
    soniox_api_key: SonioxApiKey | None = Field(default=None, title="Soniox Api Key")
    elevenlabs_api_key: ElevenlabsApiKey | None = Field(
        default=None, title="Elevenlabs Api Key"
    )
    groq_api_key: GroqApiKey | None = Field(default=None, title="Groq Api Key")
    cartesia_api_key: CartesiaApiKey | None = Field(
        default=None, title="Cartesia Api Key"
    )


class PilotIncludedMinutesUsed(RootModel[str]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: str = Field(
        ...,
        pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
        title="Pilot Included Minutes Used",
    )


class OrganizationResponse(BaseModel):
    """
    Schema for organization response
    """

    model_config = ConfigDict(
        regex_engine="python-re",
    )
    id: UUID = Field(..., title="Id")
    supertokens_tenant_id: str | None = Field(
        default=None, title="Supertokens Tenant Id"
    )
    name: str = Field(..., title="Name")
    slug: str = Field(..., title="Slug")
    owner_email: EmailStr = Field(..., title="Owner Email")
    logo_url: str | None = Field(default=None, title="Logo Url")
    max_agents: int | None = Field(default=3, title="Max Agents")
    max_members: int | None = Field(default=5, title="Max Members")
    max_concurrent_calls: int | None = Field(default=5, title="Max Concurrent Calls")
    billing_currency: str | None = Field(default="USD", title="Billing Currency")
    stripe_customer_id: str | None = Field(default=None, title="Stripe Customer Id")
    stripe_subscription_id: str | None = Field(
        default=None, title="Stripe Subscription Id"
    )
    auto_reload_enabled: bool | None = Field(default=False, title="Auto Reload Enabled")
    auto_reload_threshold_cents: int | None = Field(
        default=None, title="Auto Reload Threshold Cents"
    )
    auto_reload_amount_cents: int | None = Field(
        default=None, title="Auto Reload Amount Cents"
    )
    sku: str | None = Field(default="pilot", title="Sku")
    contract_term: str | None = Field(default="month", title="Contract Term")
    payment_method: str | None = Field(default="stripe_card", title="Payment Method")
    stripe_balance_mirror_enabled: bool | None = Field(
        default=True, title="Stripe Balance Mirror Enabled"
    )
    invoice_billing_email: str | None = Field(
        default=None, title="Invoice Billing Email"
    )
    bank_payment_terms_days: int | None = Field(
        default=15, title="Bank Payment Terms Days"
    )
    low_balance_manual_alert_threshold_cents: int | None = Field(
        default=None, title="Low Balance Manual Alert Threshold Cents"
    )
    payment_failed: bool | None = Field(default=False, title="Payment Failed")
    payment_failed_reason: str | None = Field(
        default=None, title="Payment Failed Reason"
    )
    india_dlt_registered: bool | None = Field(
        default=False, title="India Dlt Registered"
    )
    custom_rate_overrides: dict[str, Any] | None = Field(
        default=None, title="Custom Rate Overrides"
    )
    month_to_date_billable_minutes_cache: str | None = Field(
        default="0",
        pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
        title="Month To Date Billable Minutes Cache",
    )
    month_to_date_whatsapp_call_minutes_cache: str | None = Field(
        default="0",
        pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
        title="Month To Date Whatsapp Call Minutes Cache",
    )
    pilot_started_at: AwareDatetime | None = Field(
        default=None, title="Pilot Started At"
    )
    pilot_go_live_at: AwareDatetime | None = Field(
        default=None, title="Pilot Go Live At"
    )
    pilot_status: str | None = Field(default=None, title="Pilot Status")
    pilot_included_minutes_used: PilotIncludedMinutesUsed | None = Field(
        default=None, title="Pilot Included Minutes Used"
    )
    pilot_included_messages_used: int | None = Field(
        default=None, title="Pilot Included Messages Used"
    )
    pilot_conversion_call_alerted_at: AwareDatetime | None = Field(
        default=None, title="Pilot Conversion Call Alerted At"
    )
    setup_fee_invoice_id: UUID | None = Field(
        default=None, title="Setup Fee Invoice Id"
    )
    scale_waiver_applied_at: AwareDatetime | None = Field(
        default=None, title="Scale Waiver Applied At"
    )
    scale_cap_override: bool | None = Field(default=False, title="Scale Cap Override")
    website: str | None = Field(default=None, title="Website")
    email: str | None = Field(default=None, title="Email")
    openai_api_key: str | None = Field(default=None, title="Openai Api Key")
    deepgram_api_key: str | None = Field(default=None, title="Deepgram Api Key")
    soniox_api_key: str | None = Field(default=None, title="Soniox Api Key")
    elevenlabs_api_key: str | None = Field(default=None, title="Elevenlabs Api Key")
    groq_api_key: str | None = Field(default=None, title="Groq Api Key")
    cartesia_api_key: str | None = Field(default=None, title="Cartesia Api Key")
    permissions: dict[str, Any] | None = Field(default=None, title="Permissions")
    status: str = Field(..., title="Status")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class BillingCurrency(RootModel[str]):
    root: str = Field(..., max_length=3, min_length=3, title="Billing Currency")


class ContractTerm(Enum):
    month = "month"
    annual = "annual"


class PaymentMethod(Enum):
    stripe_card = "stripe_card"
    manual_invoice = "manual_invoice"


class BankPaymentTermsDays(RootModel[int]):
    root: int = Field(..., ge=1, le=90, title="Bank Payment Terms Days")


class LowBalanceManualAlertThresholdCents(RootModel[int]):
    root: int = Field(..., ge=0, title="Low Balance Manual Alert Threshold Cents")


class InvoiceBillingEmail(RootModel[str]):
    root: str = Field(..., max_length=255, title="Invoice Billing Email")


class OrganizationUpdate(BaseModel):
    """
    Schema for updating organization settings and credentials
    """

    name: Name3 | None = Field(default=None, title="Name")
    max_agents: int | None = Field(default=None, title="Max Agents")
    max_members: int | None = Field(default=None, title="Max Members")
    max_concurrent_calls: int | None = Field(default=None, title="Max Concurrent Calls")
    billing_currency: BillingCurrency | None = Field(
        default=None, title="Billing Currency"
    )
    sku: Sku | None = Field(default=None, title="Sku")
    contract_term: ContractTerm | None = Field(default=None, title="Contract Term")
    payment_method: PaymentMethod | None = Field(default=None, title="Payment Method")
    bank_payment_terms_days: BankPaymentTermsDays | None = Field(
        default=None, title="Bank Payment Terms Days"
    )
    low_balance_manual_alert_threshold_cents: (
        LowBalanceManualAlertThresholdCents | None
    ) = Field(default=None, title="Low Balance Manual Alert Threshold Cents")
    invoice_billing_email: InvoiceBillingEmail | None = Field(
        default=None, title="Invoice Billing Email"
    )
    stripe_balance_mirror_enabled: bool | None = Field(
        default=None, title="Stripe Balance Mirror Enabled"
    )
    website: Website | None = Field(default=None, title="Website")
    email: Email | None = Field(default=None, title="Email")
    openai_api_key: OpenaiApiKey | None = Field(default=None, title="Openai Api Key")
    deepgram_api_key: DeepgramApiKey | None = Field(
        default=None, title="Deepgram Api Key"
    )
    soniox_api_key: SonioxApiKey | None = Field(default=None, title="Soniox Api Key")
    elevenlabs_api_key: ElevenlabsApiKey | None = Field(
        default=None, title="Elevenlabs Api Key"
    )
    groq_api_key: GroqApiKey | None = Field(default=None, title="Groq Api Key")
    cartesia_api_key: CartesiaApiKey | None = Field(
        default=None, title="Cartesia Api Key"
    )


class OutboundCampaignCreate(BaseModel):
    """
    Create an outbound campaign.

    Organization is determined from your API key - no need to specify.
    """

    name: str = Field(..., description="Campaign name", title="Name")
    agent_id: UUID = Field(
        ..., description="Agent ID to use for making calls", title="Agent Id"
    )
    phone_number_id: UUID = Field(
        ..., description="Phone number ID for caller ID", title="Phone Number Id"
    )
    call_list_id: UUID | None = Field(
        default=None,
        description="Call list ID for contacts to call",
        title="Call List Id",
    )
    description: str | None = Field(
        default=None, description="Campaign description", title="Description"
    )
    status_webhook: str | None = Field(
        default=None,
        description="URL to POST when campaign completes or stops. Receives JSON payload with campaign stats.",
        title="Status Webhook",
    )
    call_schedule: CallSchedule | None = Field(
        default=None, description="Call scheduling configuration"
    )
    campaign_config: CampaignConfig | None = Field(
        default=None, description="Campaign configuration"
    )


class OutboundCampaignResponse(BaseModel):
    """
    Schema for outbound campaign responses.

    Phase 1 dropped the dead `calls_made/completed/successful` denormalized
    counters from the model. Aggregated stats are exposed via
    GET /v1/campaigns/{id}/stats (CampaignStats below) which sources from
    campaign_attempts.
    """

    name: str = Field(
        ..., description="Campaign name", max_length=255, min_length=1, title="Name"
    )
    description: str | None = Field(
        default=None, description="Campaign description", title="Description"
    )
    call_schedule: CallSchedule | None = Field(
        default=None, description="Call scheduling configuration"
    )
    campaign_config: CampaignConfig | None = Field(
        default=None, description="Campaign configuration"
    )
    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    agent_id: UUID = Field(..., title="Agent Id")
    phone_number_id: UUID = Field(..., title="Phone Number Id")
    call_list_id: UUID | None = Field(default=None, title="Call List Id")
    status: str = Field(..., title="Status")
    error_message: str | None = Field(default=None, title="Error Message")
    status_webhook: str | None = Field(default=None, title="Status Webhook")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")
    scheduled_start: AwareDatetime | None = Field(default=None, title="Scheduled Start")
    actual_start: AwareDatetime | None = Field(default=None, title="Actual Start")
    completed_at: AwareDatetime | None = Field(default=None, title="Completed At")
    last_progress_at: AwareDatetime | None = Field(
        default=None, title="Last Progress At"
    )
    last_pause_at: AwareDatetime | None = Field(default=None, title="Last Pause At")


class Name6(RootModel[str]):
    root: str = Field(
        ..., description="Campaign name", max_length=255, min_length=1, title="Name"
    )


class OutboundCampaignUpdate(BaseModel):
    """
    Schema for updating outbound campaigns.

    Phase 3 removed the `status` field from this schema. State changes
    happen ONLY through the dedicated lifecycle endpoints (/start,
    /pause, /resume, /stop, /cancel) which funnel through the state
    machine in `app/domains/campaigns/state.py`. PUT /campaigns/{id}
    is for editing config (name, schedule, pacing, etc.) only.
    """

    name: Name6 | None = Field(default=None, description="Campaign name", title="Name")
    description: str | None = Field(
        default=None, description="Campaign description", title="Description"
    )
    status_webhook: str | None = Field(
        default=None,
        description="URL to POST on campaign completion/stop",
        title="Status Webhook",
    )
    agent_id: UUID | None = Field(
        default=None, description="Agent ID for the campaign", title="Agent Id"
    )
    phone_number_id: UUID | None = Field(
        default=None,
        description="Phone number ID for caller ID",
        title="Phone Number Id",
    )
    call_list_id: UUID | None = Field(
        default=None,
        description="Call list ID for contacts to call",
        title="Call List Id",
    )
    call_schedule: CallSchedule | None = Field(
        default=None, description="Call scheduling configuration"
    )
    campaign_config: CampaignConfig | None = Field(
        default=None, description="Campaign configuration"
    )


class PaginationMetadata(BaseModel):
    """
    Pagination metadata in API responses.
    """

    skip: int = Field(..., description="Number of records skipped", ge=0, title="Skip")
    limit: int = Field(
        ..., description="Maximum records requested", ge=1, title="Limit"
    )
    total: int = Field(..., description="Total records available", ge=0, title="Total")
    has_more: bool = Field(
        ..., description="Whether more records exist", title="Has More"
    )
    count: int = Field(
        ..., description="Number of records in this page", ge=0, title="Count"
    )


class ParticipantInfo(BaseModel):
    participant_identity: str = Field(..., title="Participant Identity")
    participant_type: str = Field(..., title="Participant Type")
    joined_at: AwareDatetime = Field(..., title="Joined At")
    left_at: AwareDatetime | None = Field(default=None, title="Left At")
    duration_seconds: int | None = Field(default=0, title="Duration Seconds")


class PaymentMethodResponse(BaseModel):
    """
    Payment method details.
    """

    id: str = Field(..., title="Id")
    brand: str = Field(..., title="Brand")
    last4: str = Field(..., title="Last4")
    exp_month: int = Field(..., title="Exp Month")
    exp_year: int = Field(..., title="Exp Year")
    is_default: bool = Field(..., title="Is Default")


class Permission(Enum):
    """
    All 63 permissions in the system.
    Format: resource:action (flat strings, no nesting)

    These are used by:
    - Backend: RequirePermission(Permission.AGENTS_CREATE)
    - Frontend: can("agents:create")
    - API Keys: scopes = ["agents:view", "agents:create"]
    """

    admin_all = "admin:all"
    admin_organizations = "admin:organizations"
    dashboard_view = "dashboard:view"
    agents_view = "agents:view"
    agents_create = "agents:create"
    agents_edit = "agents:edit"
    agents_delete = "agents:delete"
    agents_duplicate = "agents:duplicate"
    agents_talk = "agents:talk"
    agents_call = "agents:call"
    numbers_view = "numbers:view"
    numbers_create = "numbers:create"
    numbers_edit = "numbers:edit"
    numbers_delete = "numbers:delete"
    campaigns_view = "campaigns:view"
    campaigns_create = "campaigns:create"
    campaigns_edit = "campaigns:edit"
    campaigns_delete = "campaigns:delete"
    campaigns_start = "campaigns:start"
    campaigns_pause = "campaigns:pause"
    campaigns_stop = "campaigns:stop"
    campaigns_cancel = "campaigns:cancel"
    call_lists_view = "call_lists:view"
    call_lists_create = "call_lists:create"
    call_lists_edit = "call_lists:edit"
    call_lists_delete = "call_lists:delete"
    call_lists_import = "call_lists:import"
    contacts_view = "contacts:view"
    contacts_create = "contacts:create"
    contacts_edit = "contacts:edit"
    contacts_delete = "contacts:delete"
    integrations_view = "integrations:view"
    integrations_create = "integrations:create"
    integrations_edit = "integrations:edit"
    integrations_delete = "integrations:delete"
    integrations_test = "integrations:test"
    knowledge_view = "knowledge:view"
    knowledge_create = "knowledge:create"
    knowledge_edit = "knowledge:edit"
    knowledge_delete = "knowledge:delete"
    analytics_view = "analytics:view"
    analytics_view_details = "analytics:view_details"
    analytics_play_recording = "analytics:play_recording"
    analytics_listen = "analytics:listen"
    analytics_hangup = "analytics:hangup"
    analytics_export = "analytics:export"
    team_view = "team:view"
    team_invite = "team:invite"
    team_change_role = "team:change_role"
    team_remove = "team:remove"
    api_keys_view = "api_keys:view"
    api_keys_create = "api_keys:create"
    api_keys_revoke = "api_keys:revoke"
    billing_view = "billing:view"
    billing_add_payment = "billing:add_payment"
    billing_remove_payment = "billing:remove_payment"
    billing_topup = "billing:topup"
    billing_download_invoice = "billing:download_invoice"
    messaging_view = "messaging:view"
    whatsapp_view = "whatsapp:view"
    whatsapp_send = "whatsapp:send"
    whatsapp_manage = "whatsapp:manage"


class MaxCompletionTokens1(RootModel[int]):
    root: int = Field(
        4096,
        description="Maximum tokens in response",
        ge=1,
        le=32768,
        title="Max Completion Tokens",
    )


class PhantomTranscriberConfig(BaseModel):
    """
    Phantom STT provider configuration.
    """

    provider: Literal["phantom"] = Field(default="phantom", title="Provider")
    model: str | None = Field(default="phantom-stt-v1", title="Model")
    language: str | None = Field(default="auto", title="Language")


class PhantomVoiceConfig(BaseModel):
    """
    Neuratel Phantom TTS — proprietary voice synthesis.
    """

    provider: Literal["phantom"] = Field(default="phantom", title="Provider")
    model: str | None = Field(
        default="phantom-english-speech-preview",
        description="Phantom Speech model (phantom-english-speech-preview or phantom-arabic-speech-preview)",
        title="Model",
    )
    voice: str | None = Field(
        default="aria",
        description="Phantom preset voice. English: aria, bella, claire, alex, david, marcus. Arabic: omar, tariq, layla, nour.",
        title="Voice",
    )


class PhoneNumberCreate(BaseModel):
    """
    Create phone number request
    """

    did: str = Field(..., title="Did")
    name: str = Field(..., title="Name")
    agent_id: UUID | None = Field(default=None, title="Agent Id")


class PhoneNumberResponse(BaseModel):
    """
    Phone number details
    """

    id: UUID = Field(..., title="Id")
    did: str = Field(..., title="Did")
    name: str = Field(..., title="Name")
    organization_id: UUID = Field(..., title="Organization Id")
    agent_id: UUID | None = Field(..., title="Agent Id")
    capabilities: list[str] | None = Field(default=None, title="Capabilities")
    tags: list[str] | None = Field(default=None, title="Tags")
    is_active: bool = Field(..., title="Is Active")
    formatted_number: str = Field(..., title="Formatted Number")
    created_at: str | None = Field(..., title="Created At")
    updated_at: str | None = Field(..., title="Updated At")
    agent_tool_overrides: dict[str, Any] | None = Field(
        default=None, title="Agent Tool Overrides"
    )
    inbound_webhook_url: str | None = Field(default=None, title="Inbound Webhook Url")
    inbound_webhook_secret_set: bool | None = Field(
        default=False, title="Inbound Webhook Secret Set"
    )


class InboundWebhookUrl1(RootModel[str]):
    root: str = Field(..., max_length=2048, title="Inbound Webhook Url")


class InboundWebhookSecret1(RootModel[str]):
    root: str = Field(..., max_length=255, title="Inbound Webhook Secret")


class PhoneNumberUpdate(BaseModel):
    """
    Update phone number request
    """

    name: str | None = Field(default=None, title="Name")
    agent_id: UUID | None = Field(default=None, title="Agent Id")
    agent_tool_overrides: dict[str, Any] | None = Field(
        default=None, title="Agent Tool Overrides"
    )
    inbound_webhook_url: InboundWebhookUrl1 | None = Field(
        default=None, title="Inbound Webhook Url"
    )
    inbound_webhook_secret: InboundWebhookSecret1 | None = Field(
        default=None, title="Inbound Webhook Secret"
    )


class MinDelay(RootModel[float]):
    root: float = Field(
        0.5,
        description="Minimum seconds after end-of-utterance before responding. Default: 0.5",
        ge=0.0,
        le=5.0,
        title="Min Delay",
    )


class MaxDelay(RootModel[float]):
    root: float = Field(
        3.0,
        description="Ceiling — agent commits the turn after this long even if detector is uncertain. Default: 3.0",
        ge=0.5,
        le=15.0,
        title="Max Delay",
    )


class EndpointingMode(Enum):
    """
    fixed: agent waits min_delay; extends up to max_delay only if turn-detector is uncertain. dynamic: adapts effective wait within [min_delay, max_delay] based on this caller's pause patterns.
    """

    fixed = "fixed"
    dynamic = "dynamic"


class PipelineTurnDetectionMode(Enum):
    """
    Turn detection modes for pipeline agents.
    """

    vad = "vad"
    semantic_vad = "semantic_vad"
    semantic_vad_en = "semantic_vad_en"
    stt = "stt"


class PlaceOutboundCallConfig(BaseModel):
    """
    Configuration for the place_outbound_call tool.

    Lets the LLM initiate an outbound call to a phone number on demand —
    works from voice calls (cross-channel) or WhatsApp chat sessions.
    """

    enabled: bool | None = Field(
        default=False,
        description="Enable place_outbound_call capability",
        title="Enabled",
    )
    permission_request_template_name: str | None = Field(
        default="call_permission_request",
        description="WhatsApp template name for permission requests (when channel='whatsapp')",
        title="Permission Request Template Name",
    )
    permission_request_template_language_code: str | None = Field(
        default="en_US",
        description="Language code for the permission template",
        title="Permission Request Template Language Code",
    )


class PlatformRevenueResponse(BaseModel):
    """
    Platform-wide revenue summary (admin only).
    """

    call_count: int = Field(..., title="Call Count")
    total_minutes: float = Field(..., title="Total Minutes")
    total_revenue: float = Field(..., title="Total Revenue")
    total_cost: float = Field(..., title="Total Cost")
    total_margin: float = Field(..., title="Total Margin")
    margin_percentage: float = Field(..., title="Margin Percentage")


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, title="Name")
    avatar: str | None = Field(default=None, title="Avatar")


class PublicIncidentReport(BaseModel):
    email: EmailStr = Field(..., title="Email")
    template_id: str = Field(..., title="Template Id")
    affected_component_ids: list[UUID] | None = Field(
        default=None, title="Affected Component Ids"
    )


class PublishRequest(BaseModel):
    version_number: int = Field(..., title="Version Number")


class RAGQueryRequest(BaseModel):
    """
    RAG query request from worker.
    """

    query: str = Field(
        ...,
        description="User's question/query",
        max_length=2000,
        min_length=1,
        title="Query",
    )
    knowledge_base_ids: list[UUID] = Field(
        ..., description="KB IDs to search", min_length=1, title="Knowledge Base Ids"
    )
    top_k: int | None = Field(
        default=3, description="Number of results to return", ge=1, le=10, title="Top K"
    )


class RAGResult(BaseModel):
    """
    Single RAG result chunk.
    """

    text: str = Field(..., title="Text")
    score: float = Field(
        ..., description="Relevance score", ge=0.0, le=1.0, title="Score"
    )
    knowledge_base_id: UUID = Field(..., title="Knowledge Base Id")
    knowledge_base_name: str = Field(..., title="Knowledge Base Name")
    chunk_index: int = Field(..., title="Chunk Index")


class RagConfig(BaseModel):
    """
    Configuration for RAG (Retrieval-Augmented Generation).
    """

    enabled: bool | None = Field(
        default=False, description="Enable RAG capability", title="Enabled"
    )
    knowledge_base_ids: list[str] | None = Field(
        default=None,
        description="Knowledge base IDs to query",
        title="Knowledge Base Ids",
    )
    top_k: int | None = Field(
        default=5,
        description="Maximum chunks to retrieve per query",
        ge=1,
        le=20,
        title="Top K",
    )
    score_threshold: float | None = Field(
        default=0.7,
        description="Minimum relevance score",
        ge=0.0,
        le=1.0,
        title="Score Threshold",
    )
    include_metadata: bool | None = Field(
        default=True,
        description="Include chunk metadata in context",
        title="Include Metadata",
    )
    context_template: str | None = Field(
        default="Here is relevant information:\n{chunks}",
        description="Template for injecting context",
        title="Context Template",
    )


class RetentionDays(IntEnum):
    """
    Days to retain recordings. -1 = forever
    """

    integer_7 = 7
    integer_30 = 30
    integer__1 = -1


class RecordingConfig(BaseModel):
    """
    Configuration for call recording.
    """

    enabled: bool | None = Field(
        default=False, description="Enable call recording", title="Enabled"
    )
    retention_days: RetentionDays | None = Field(
        default=30,
        description="Days to retain recordings. -1 = forever",
        title="Retention Days",
    )


class RecordingResponse(BaseModel):
    """
    Recording for a voice session.
    """

    id: UUID = Field(..., title="Id")
    recording_url: str | None = Field(default=None, title="Recording Url")
    status: str | None = Field(default="pending", title="Status")
    duration_seconds: float | None = Field(default=None, title="Duration Seconds")
    file_size_bytes: int | None = Field(default=None, title="File Size Bytes")
    format: str | None = Field(default=None, title="Format")
    error_message: str | None = Field(default=None, title="Error Message")
    created_at: AwareDatetime = Field(..., title="Created At")


class RegisterAndAcceptRequest(BaseModel):
    """
    Request body for registering a new user and accepting invitation.
    """

    name: str = Field(
        ...,
        description="User's display name",
        max_length=128,
        min_length=1,
        title="Name",
    )
    password: str = Field(
        ...,
        description="Account password",
        max_length=128,
        min_length=8,
        title="Password",
    )


class RoleType(Enum):
    """
    Role hierarchy for the platform.

    Hierarchy (highest to lowest):
    - super_admin: God mode, full platform access, system-wide operations
    - admin: Full organization access, can manage members and settings
    - operator: Can view/edit/test resources, cannot create/delete/manage
    - viewer: Read-only access to organization resources
    """

    super_admin = "super_admin"
    admin = "admin"
    operator = "operator"
    viewer = "viewer"


class SendAudioMessageConfig(BaseModel):
    """
    Configuration for the send_audio_message tool.

    Lets the LLM send a TTS-generated voice note to the current contact via
    WhatsApp. Uses the agent's configured voice provider.
    """

    enabled: bool | None = Field(
        default=False,
        description="Enable send_audio_message capability",
        title="Enabled",
    )
    max_text_length: int | None = Field(
        default=500,
        description="Maximum text length for TTS generation",
        ge=50,
        le=2000,
        title="Max Text Length",
    )


class SendDtmfConfig(BaseModel):
    """
    Configuration for sending DTMF tones.
    """

    enabled: bool | None = Field(
        default=False, description="Enable DTMF sending", title="Enabled"
    )
    tone_duration_ms: int | None = Field(
        default=100,
        description="Duration of each tone in ms",
        ge=50,
        le=500,
        title="Tone Duration Ms",
    )
    gap_duration_ms: int | None = Field(
        default=100,
        description="Gap between tones in ms",
        ge=50,
        le=500,
        title="Gap Duration Ms",
    )


class SendMessageResponse(BaseModel):
    wa_message_id: str = Field(..., title="Wa Message Id")
    status: str = Field(..., title="Status")
    conversation_id: UUID = Field(..., title="Conversation Id")
    client_temp_id: str | None = Field(default=None, title="Client Temp Id")
    message_id: UUID | None = Field(default=None, title="Message Id")


class TemplateBody2(RootModel[str]):
    root: str = Field(
        ...,
        description="Raw template body string (with ``{{placeholder}}`` markers) — supplied by the frontend after fetching the template definition from Meta's registry. When provided alongside ``dynamic_variables`` and an empty ``template_params``, the server resolves placeholders from the agent variable map (named OR positional templates). Bridges the agent-side and Meta-side substitution moments.",
        max_length=4096,
        title="Template Body",
    )


class TemplateCategory(RootModel[str]):
    root: str = Field(
        ...,
        description="Meta WABA category of this template — one of MARKETING, UTILITY, AUTHENTICATION, AUTHENTICATION_INTERNATIONAL, SERVICE, MARKETING_LITE. Pulled from Meta's template registry by the frontend before send. Used to bill the right rate at send time (per-category passthrough) and grouped by the daily true-up cron. Defaults to MARKETING (most expensive bucket) when omitted; truesup reconciles via manual_adjustment ledger.",
        max_length=40,
        title="Template Category",
    )


class ClientTempId1(RootModel[str]):
    root: str = Field(
        ...,
        description="Client-supplied ID for optimistic UI reconciliation",
        max_length=64,
        title="Client Temp Id",
    )


class SendTextRequest(BaseModel):
    """
    Send a free-form text message inside the active 24h session window.
    """

    whatsapp_phone_number_id: str = Field(
        ...,
        description="Our WhatsApp phone number ID",
        title="Whatsapp Phone Number Id",
    )
    whatsapp_user_id: str = Field(
        ...,
        description="Recipient's WhatsApp E.164 ID",
        max_length=20,
        min_length=7,
        title="Whatsapp User Id",
    )
    body: str = Field(..., max_length=4096, min_length=1, title="Body")
    client_temp_id: ClientTempId1 | None = Field(
        default=None,
        description="Client-supplied ID for optimistic UI reconciliation",
        title="Client Temp Id",
    )


class SentimentTurn(BaseModel):
    turn: int = Field(..., title="Turn")
    role: str = Field(..., title="Role")
    text: str = Field(..., title="Text")
    sentiment: float = Field(..., title="Sentiment")
    emotion: str = Field(..., title="Emotion")


class SetupIntentResponse(BaseModel):
    """
    Setup intent for adding payment method.
    """

    client_secret: str = Field(..., title="Client Secret")
    setup_intent_id: str = Field(..., title="Setup Intent Id")


class SlackSubscribeRequest(BaseModel):
    """
    Slack webhook subscription request
    """

    webhook_url: str = Field(
        ..., description="Slack Incoming Webhook URL", title="Webhook Url"
    )
    channel_name: str | None = Field(
        default=None,
        description="Channel name for display (e.g. #status-alerts)",
        title="Channel Name",
    )
    notify_on: list[str] | None = Field(default=None, title="Notify On")


class SonioxModel(Enum):
    """
    Soniox real-time STT models.

    SDK Default: model="stt-rt-v4". Single unified model handles 60+ languages
    including English + Arabic with native code-switching and built-in semantic EOU.
    """

    stt_rt_v5 = "stt-rt-v5"
    stt_rt_v4 = "stt-rt-v4"


class SonioxTranscriberConfig(BaseModel):
    """
    Soniox v4 STT provider configuration.

    Soniox owns end-of-utterance detection internally via semantic endpointing,
    so the worker auto-routes turn_detection.mode to "stt" when this provider is
    selected. The platform's standalone semantic turn-detection model is bypassed.
    """

    provider: Literal["soniox"] = Field(default="soniox", title="Provider")
    model: SonioxModel | None = "stt-rt-v4"
    language_hints: list[str] | None = Field(
        default=None,
        description="ISO codes Soniox should bias toward (e.g. ['en', 'ar']). If None, Soniox auto-detects across all supported languages.",
        title="Language Hints",
    )
    language_hints_strict: bool | None = Field(
        default=False,
        description="When True, restrict transcription to only the hinted languages",
        title="Language Hints Strict",
    )
    enable_speaker_diarization: bool | None = Field(
        default=False,
        description="Identify and label different speakers in the transcript",
        title="Enable Speaker Diarization",
    )
    enable_language_identification: bool | None = Field(
        default=True,
        description="Tag each token with its detected language (useful for multilingual)",
        title="Enable Language Identification",
    )
    interim_results: bool | None = Field(
        default=True,
        description="Return partial transcripts while user is speaking (always on for Soniox)",
        title="Interim Results",
    )


class SortOrder(Enum):
    """
    Sort order for list endpoints
    """

    ASC = "ASC"
    DESC = "DESC"


class StripeCustomerRequest(BaseModel):
    """
    Request to create a Stripe customer.
    """

    email: str = Field(..., title="Email")
    name: str = Field(..., title="Name")


class StripeCustomerResponse(BaseModel):
    """
    Stripe customer creation response.
    """

    customer_id: str = Field(..., title="Customer Id")
    subscription_id: str | None = Field(default=None, title="Subscription Id")


class SuccessEvaluationRubric(Enum):
    """
    Rubric types for success evaluation.
    """

    NumericScale = "NumericScale"
    DescriptiveScale = "DescriptiveScale"
    Checklist = "Checklist"
    Matrix = "Matrix"
    PercentageScale = "PercentageScale"
    LikertScale = "LikertScale"
    AutomaticRubric = "AutomaticRubric"
    PassFail = "PassFail"


class Mode(Enum):
    listen = "listen"
    whisper = "whisper"
    barge = "barge"


class SupervisorPermissions(BaseModel):
    can_hear: bool | None = Field(default=True, title="Can Hear")
    can_speak: bool | None = Field(default=False, title="Can Speak")
    can_speak_to_agent: bool | None = Field(default=False, title="Can Speak To Agent")
    can_speak_to_customer: bool | None = Field(
        default=False, title="Can Speak To Customer"
    )
    visible_to_participants: bool | None = Field(
        default=False, title="Visible To Participants"
    )


class TTSTextTransform(Enum):
    """
    TTS text transforms.

    Transforms to apply to TTS input text before sending to provider.
    Set to None to disable all transforms.
    """

    filter_markdown = "filter_markdown"
    filter_emoji = "filter_emoji"


class TemplateComponentResponse(BaseModel):
    type: str = Field(..., title="Type")
    format: str | None = Field(default=None, title="Format")
    text: str | None = Field(default=None, title="Text")
    buttons: list[dict[str, Any]] | None = Field(default=None, title="Buttons")
    example: dict[str, Any] | None = Field(default=None, title="Example")


class TemplateParam(BaseModel):
    """
    Single body parameter for a WhatsApp template.

    `name` is the placeholder identifier from the template body:
      - "1", "2", ...  for positional templates ("Hi {{1}}, ...")
      - "customer_name" for named templates ("Hi {{customer_name}}, ...")
    `value` is the substituted text.

    Per Meta Cloud API: positional templates send `[{type:"text",text}]`;
    named templates send `[{type:"text",text,parameter_name}]`.
    """

    name: str = Field(..., max_length=64, min_length=1, title="Name")
    value: str = Field(..., max_length=1024, title="Value")


class TemplateResponse(BaseModel):
    id: str = Field(..., title="Id")
    name: str = Field(..., title="Name")
    language: str = Field(..., title="Language")
    status: str = Field(..., title="Status")
    category: str = Field(..., title="Category")
    parameter_format: str | None = Field(default=None, title="Parameter Format")
    components: list[TemplateComponentResponse] | None = Field(
        default=[], title="Components", validate_default=True
    )
    has_call_permission: bool | None = Field(default=False, title="Has Call Permission")


class ThinkingAudioConfig(BaseModel):
    """
    Configuration for thinking/processing audio.

    Thinking sound plays while the agent is in the "thinking" state.
    Use BuiltinAudioClip presets (KEYBOARD_TYPING, KEYBOARD_TYPING_2) or custom URL/path.
    """

    enabled: bool | None = Field(
        default=False, description="Enable thinking sounds", title="Enabled"
    )
    source: BuiltinAudioClip | str | None = Field(
        default="keyboard_typing",
        description="Built-in audio clip or custom URL/path to audio file",
        title="Source",
    )
    volume: float | None = Field(
        default=0.8, description="Thinking audio volume", ge=0.0, le=1.0, title="Volume"
    )


class TimeRange(Enum):
    """
    Predefined time ranges.
    """

    today = "today"
    yesterday = "yesterday"
    this_week = "this_week"
    last_week = "last_week"
    this_month = "this_month"
    last_month = "last_month"
    last_7_days = "last_7_days"
    last_30_days = "last_30_days"
    last_90_days = "last_90_days"
    all_time = "all_time"


class TimeoutConfig(BaseModel):
    """
    Configuration for user silence timeouts.
    """

    enabled: bool | None = Field(
        default=True, description="Enable timeout handling", title="Enabled"
    )
    trigger_seconds: float | None = Field(
        default=15.0,
        description="Seconds of silence before triggering",
        ge=5.0,
        le=120.0,
        title="Trigger Seconds",
    )
    warning_count: int | None = Field(
        default=2,
        description="Number of warning messages before ending",
        ge=0,
        le=5,
        title="Warning Count",
    )
    warning_messages: list[str] | None = Field(
        default=["Are you still there?", "Hello?"],
        description="Messages to prompt user",
        title="Warning Messages",
    )
    final_message: str | None = Field(
        default="I'll end the call now. Goodbye!",
        description="Message before ending call",
        title="Final Message",
    )


class TokenHealthResponse(BaseModel):
    phone_number_id: str = Field(..., title="Phone Number Id")
    healthy: bool = Field(..., title="Healthy")


class ToolChoice(Enum):
    """
    Tool calling modes.
    """

    auto = "auto"
    required = "required"
    none = "none"


class TopUpIntentResponse(BaseModel):
    """
    Response with PaymentIntent details for frontend.
    """

    payment_intent_id: str | None = Field(default=None, title="Payment Intent Id")
    client_secret: str | None = Field(default=None, title="Client Secret")
    amount_cents: int | None = Field(default=0, title="Amount Cents")
    amount_dollars: float | None = Field(default=0.0, title="Amount Dollars")
    currency: str | None = Field(default="USD", title="Currency")
    requires_action: bool | None = Field(default=False, title="Requires Action")
    succeeded: bool | None = Field(default=False, title="Succeeded")
    payment_method_id: str | None = Field(default=None, title="Payment Method Id")
    error: bool | None = Field(default=False, title="Error")
    error_code: str | None = Field(default=None, title="Error Code")
    error_message: str | None = Field(default=None, title="Error Message")


class TopUpRequest(BaseModel):
    """
    Request to create a top-up payment.
    """

    amount: float = Field(..., title="Amount")


class TransferMode(Enum):
    """
    Transfer mode types.
    """

    blind = "blind"
    warm = "warm"


class TransferOnFail(Enum):
    """
    Actions when transfer fails.
    """

    hangup = "hangup"
    return_ = "return"
    voicemail = "voicemail"


class UnreadCountResponse(BaseModel):
    """
    Unread notification count response
    """

    unread_count: int = Field(..., title="Unread Count")


class UpdateAccountRequest(BaseModel):
    """
    Partial update — all fields optional.
    """

    agent_id: UUID | None = Field(default=None, title="Agent Id")
    enable_messaging: bool | None = Field(default=None, title="Enable Messaging")
    enable_audio_message_response: bool | None = Field(
        default=None, title="Enable Audio Message Response"
    )
    enable_calling: bool | None = Field(default=None, title="Enable Calling")
    timeout_message: str | None = Field(default=None, title="Timeout Message")
    agent_tool_overrides: dict[str, Any] | None = Field(
        default=None, title="Agent Tool Overrides"
    )
    default_call_template_name: str | None = Field(
        default=None, title="Default Call Template Name"
    )
    default_call_template_language: str | None = Field(
        default=None, title="Default Call Template Language"
    )
    inbound_webhook_url: InboundWebhookUrl1 | None = Field(
        default=None, title="Inbound Webhook Url"
    )
    inbound_webhook_secret: InboundWebhookSecret1 | None = Field(
        default=None, title="Inbound Webhook Secret"
    )


class UpdateMemberPermissionsRequest(BaseModel):
    """
    Request to update a member's custom permissions.
    """

    permissions: dict[str, Any] = Field(..., title="Permissions")


class UpdateRoleRequest(BaseModel):
    """
    Request to update a member's role.
    """

    role: Role = Field(..., title="Role")


class Name7(RootModel[str]):
    root: str = Field(..., max_length=255, min_length=1, title="Name")


class UpdateWorkflowRequest(BaseModel):
    name: Name7 | None = Field(default=None, title="Name")
    description: str | None = Field(default=None, title="Description")
    agent_id: UUID | None = Field(default=None, title="Agent Id")


class UsageMetrics(BaseModel):
    stt: dict[str, Any] | None = Field(default=None, title="Stt")
    llm: dict[str, Any] | None = Field(default=None, title="Llm")
    tts: dict[str, Any] | None = Field(default=None, title="Tts")
    realtime: dict[str, Any] | None = Field(default=None, title="Realtime")


class UsageSummaryResponse(BaseModel):
    """
    Usage summary for an organization.
    """

    call_count: int = Field(..., title="Call Count")
    total_seconds: int = Field(..., title="Total Seconds")
    total_minutes: float = Field(..., title="Total Minutes")
    total_billed: float = Field(..., title="Total Billed")
    period_start: AwareDatetime | None = Field(default=None, title="Period Start")
    period_end: AwareDatetime | None = Field(default=None, title="Period End")


class ValidationError(BaseModel):
    loc: list[str | int] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")
    input: Any | None = Field(default=None, title="Input")
    ctx: dict[str, Any] | None = Field(default=None, title="Context")


class VariableCoverageStat(BaseModel):
    filled: int = Field(..., title="Filled")
    total: int = Field(..., title="Total")
    pct: float = Field(..., title="Pct")


class VoiceFilterOptions(BaseModel):
    """
    Available filter options for dropdowns.
    """

    providers: list[str] = Field(..., title="Providers")
    categories: list[str] = Field(..., title="Categories")
    genders: list[str] = Field(..., title="Genders")
    languages: list[str] = Field(..., title="Languages")
    accents: list[str] = Field(..., title="Accents")
    ages: list[str] = Field(..., title="Ages")
    use_cases: list[str] = Field(..., title="Use Cases")


class VoiceResponse(BaseModel):
    """
    Single voice response with all metadata.
    """

    id: str = Field(..., title="Id")
    display_id: str = Field(..., title="Display Id")
    provider: str = Field(..., title="Provider")
    provider_voice_id: str = Field(..., title="Provider Voice Id")
    provider_voice_name: str = Field(..., title="Provider Voice Name")
    description: str | None = Field(default=None, title="Description")
    language: str | None = Field(default=None, title="Language")
    language_name: str | None = Field(default=None, title="Language Name")
    gender: str | None = Field(default=None, title="Gender")
    accent: str | None = Field(default=None, title="Accent")
    age: str | None = Field(default=None, title="Age")
    use_case: str | None = Field(default=None, title="Use Case")
    category: str | None = Field(default=None, title="Category")
    labels: dict[str, Any] | None = Field(default=None, title="Labels")
    preview_url: str | None = Field(default=None, title="Preview Url")
    is_premium: bool | None = Field(default=False, title="Is Premium")
    is_cloned: bool | None = Field(default=False, title="Is Cloned")


class VoiceSessionUpdate(BaseModel):
    """
    Partial update for a voice session.

    Only `call_metadata` is mutable today: operators attach CRM IDs / ticket
    numbers / post-call notes after the call ends. The dict is JSONB-merged
    into the existing column (not replaced wholesale).

    Other fields are either auto-managed (status, timing — written by
    the media-server webhook receiver) or don't exist on the schema
    (no `tags` column).
    """

    call_metadata: dict[str, Any] = Field(
        ...,
        description="Keys to merge into the existing call_metadata JSONB column.",
        title="Call Metadata",
    )


class VoiceSyncResponse(BaseModel):
    """
    Response from voice sync operation.
    """

    success: bool = Field(..., title="Success")
    message: str = Field(..., title="Message")
    elevenlabs_synced: int = Field(..., title="Elevenlabs Synced")
    cartesia_synced: int = Field(..., title="Cartesia Synced")
    total_synced: int = Field(..., title="Total Synced")


class VoicemailAction(Enum):
    """
    Actions when voicemail is detected.
    """

    hangup = "hangup"
    leave_message = "leave_message"
    continue_ = "continue"


class VoicemailToolConfig(BaseModel):
    """
    Configuration for voicemail/answering machine detection.

    The LLM detects voicemail patterns (greetings, beeps) and triggers
    configured actions. This is LLM-based detection, not carrier AMD.
    """

    enabled: bool | None = Field(
        default=True, description="Enable voicemail detection", title="Enabled"
    )
    action: VoicemailAction | None = Field(
        default="hangup", description="Action when voicemail is detected"
    )
    message: str | None = Field(
        default="Hi, this is a message from your assistant. I'll try calling back later.",
        description="Message to leave if action is leave_message",
        title="Message",
    )
    wait_for_beep: bool | None = Field(
        default=True,
        description="Wait for the beep before leaving message",
        title="Wait For Beep",
    )
    post_message_delay_ms: int | None = Field(
        default=500,
        description="Delay after message before hanging up (ms)",
        ge=0,
        le=2000,
        title="Post Message Delay Ms",
    )


class Description7(RootModel[str]):
    root: str = Field(
        ..., description="Optional description", max_length=1000, title="Description"
    )


class AuthHeader(RootModel[str]):
    root: str = Field(
        ...,
        description="Optional custom header name for authentication (e.g., 'X-Api-Key')",
        max_length=100,
        title="Auth Header",
    )


class AuthValue(RootModel[str]):
    root: str = Field(
        ..., description="Value for the auth header", max_length=500, title="Auth Value"
    )


class WebhookCreateResponse(BaseModel):
    """
    Response when creating a webhook - includes secret
    """

    id: UUID = Field(..., description="Unique webhook identifier", title="Id")
    organization_id: UUID = Field(
        ..., description="Organization this webhook belongs to", title="Organization Id"
    )
    name: str = Field(..., description="Display name for this webhook", title="Name")
    description: str | None = Field(
        default=None, description="Optional description", title="Description"
    )
    url: str = Field(
        ..., description="HTTPS endpoint that receives event payloads", title="Url"
    )
    events: list[str] = Field(
        ..., description="Event types this webhook subscribes to", title="Events"
    )
    auth_header: str | None = Field(
        default=None,
        description="Custom header name sent with each request (e.g. X-Api-Key)",
        title="Auth Header",
    )
    is_active: bool = Field(
        ...,
        description="Whether this webhook is enabled. Auto-disabled after 10 consecutive delivery failures",
        title="Is Active",
    )
    timeout_seconds: int = Field(
        ...,
        description="Request timeout per delivery attempt in seconds",
        title="Timeout Seconds",
    )
    max_retries: int = Field(
        ...,
        description="Maximum retry attempts on delivery failure",
        title="Max Retries",
    )
    failure_count: int = Field(
        ...,
        description="Consecutive delivery failures since last success",
        title="Failure Count",
    )
    disabled_reason: str | None = Field(
        default=None,
        description="Reason this webhook was auto-disabled, if applicable",
        title="Disabled Reason",
    )
    last_success_at: AwareDatetime | None = Field(
        default=None,
        description="Timestamp of last successful delivery",
        title="Last Success At",
    )
    last_failure_at: AwareDatetime | None = Field(
        default=None,
        description="Timestamp of last failed delivery attempt",
        title="Last Failure At",
    )
    created_at: AwareDatetime = Field(
        ..., description="Creation timestamp", title="Created At"
    )
    updated_at: AwareDatetime = Field(
        ..., description="Last update timestamp", title="Updated At"
    )
    secret: str = Field(
        ...,
        description="HMAC secret for validating webhook signatures. Store securely - only shown once!",
        title="Secret",
    )


class WebhookDeliveryLogResponse(BaseModel):
    """
    Webhook delivery attempt log
    """

    id: UUID = Field(..., title="Id")
    webhook_id: UUID = Field(..., title="Webhook Id")
    event_type: str = Field(..., title="Event Type")
    event_id: str | None = Field(..., title="Event Id")
    resource_id: str | None = Field(..., title="Resource Id")
    resource_type: str | None = Field(..., title="Resource Type")
    request_url: str = Field(..., title="Request Url")
    response_status: int | None = Field(..., title="Response Status")
    response_body: str | None = Field(..., title="Response Body")
    duration_ms: int | None = Field(..., title="Duration Ms")
    success: bool = Field(..., title="Success")
    error_message: str | None = Field(..., title="Error Message")
    attempt_number: int = Field(..., title="Attempt Number")
    created_at: AwareDatetime = Field(..., title="Created At")


class WebhookDeliveryLogsResponse(BaseModel):
    """
    Paginated delivery logs
    """

    items: list[WebhookDeliveryLogResponse] = Field(..., title="Items")
    total: int = Field(..., title="Total")
    skip: int = Field(..., title="Skip")
    limit: int = Field(..., title="Limit")


class WebhookEvent(Enum):
    """
    Per-agent webhook event types — only events the worker actually fires.

    Org-level webhooks live in `app.schemas.webhook.WebhookEventType` (dot-
    notation values like 'recording.ready'); they are sent by Platform, not
    by the worker, and are out of scope for this enum.
    """

    session_report = "session_report"
    call_ended = "call_ended"
    analysis_complete = "analysis_complete"
    error = "error"


class WebhookEventTypeEnum(Enum):
    """
    Available webhook event types
    """

    call_started = "call.started"
    call_ended = "call.ended"
    call_ringing = "call.ringing"
    call_answered = "call.answered"
    call_failed = "call.failed"
    call_transferred = "call.transferred"
    transcript_partial = "transcript.partial"
    transcript_final = "transcript.final"
    transcript_ready = "transcript.ready"
    recording_ready = "recording.ready"
    agent_turn_started = "agent.turn.started"
    agent_turn_ended = "agent.turn.ended"
    agent_tool_called = "agent.tool.called"
    call_summary_ready = "call.summary.ready"
    campaign_started = "campaign.started"
    campaign_paused = "campaign.paused"
    campaign_resumed = "campaign.resumed"
    campaign_stopped = "campaign.stopped"
    campaign_cancelled = "campaign.cancelled"
    campaign_completed = "campaign.completed"
    campaign_retry_scheduled = "campaign.retry_scheduled"
    dnc_added = "dnc.added"


class WebhookResponse(BaseModel):
    """
    Webhook subscription response
    """

    id: UUID = Field(..., description="Unique webhook identifier", title="Id")
    organization_id: UUID = Field(
        ..., description="Organization this webhook belongs to", title="Organization Id"
    )
    name: str = Field(..., description="Display name for this webhook", title="Name")
    description: str | None = Field(
        default=None, description="Optional description", title="Description"
    )
    url: str = Field(
        ..., description="HTTPS endpoint that receives event payloads", title="Url"
    )
    events: list[str] = Field(
        ..., description="Event types this webhook subscribes to", title="Events"
    )
    auth_header: str | None = Field(
        default=None,
        description="Custom header name sent with each request (e.g. X-Api-Key)",
        title="Auth Header",
    )
    is_active: bool = Field(
        ...,
        description="Whether this webhook is enabled. Auto-disabled after 10 consecutive delivery failures",
        title="Is Active",
    )
    timeout_seconds: int = Field(
        ...,
        description="Request timeout per delivery attempt in seconds",
        title="Timeout Seconds",
    )
    max_retries: int = Field(
        ...,
        description="Maximum retry attempts on delivery failure",
        title="Max Retries",
    )
    failure_count: int = Field(
        ...,
        description="Consecutive delivery failures since last success",
        title="Failure Count",
    )
    disabled_reason: str | None = Field(
        default=None,
        description="Reason this webhook was auto-disabled, if applicable",
        title="Disabled Reason",
    )
    last_success_at: AwareDatetime | None = Field(
        default=None,
        description="Timestamp of last successful delivery",
        title="Last Success At",
    )
    last_failure_at: AwareDatetime | None = Field(
        default=None,
        description="Timestamp of last failed delivery attempt",
        title="Last Failure At",
    )
    created_at: AwareDatetime = Field(
        ..., description="Creation timestamp", title="Created At"
    )
    updated_at: AwareDatetime = Field(
        ..., description="Last update timestamp", title="Updated At"
    )


class WebhookRotateSecretResponse(BaseModel):
    secret: str = Field(..., title="Secret")
    message: str = Field(..., title="Message")


class WebhookTestRequest(BaseModel):
    """
    Test a webhook with a sample payload
    """

    event_type: WebhookEventTypeEnum | None = Field(
        default="call.started", description="Event type to simulate"
    )


class WebhookTestResponse(BaseModel):
    """
    Result of webhook test
    """

    success: bool = Field(..., title="Success")
    status_code: int | None = Field(..., title="Status Code")
    response_body: str | None = Field(..., title="Response Body")
    error_message: str | None = Field(..., title="Error Message")
    duration_ms: int = Field(..., title="Duration Ms")


class Description8(RootModel[str]):
    root: str = Field(..., max_length=1000, title="Description")


class AuthHeader1(RootModel[str]):
    root: str = Field(..., max_length=100, title="Auth Header")


class AuthValue1(RootModel[str]):
    root: str = Field(..., max_length=500, title="Auth Value")


class TimeoutSeconds1(RootModel[int]):
    root: int = Field(..., ge=1, le=60, title="Timeout Seconds")


class MaxRetries(RootModel[int]):
    root: int = Field(..., ge=0, le=5, title="Max Retries")


class WebhookUpdate(BaseModel):
    """
    Update an existing webhook subscription
    """

    name: Name7 | None = Field(default=None, title="Name")
    description: Description8 | None = Field(default=None, title="Description")
    url: str | None = Field(default=None, title="Url")
    events: list[WebhookEventTypeEnum] | None = Field(default=None, title="Events")
    auth_header: AuthHeader1 | None = Field(default=None, title="Auth Header")
    auth_value: AuthValue1 | None = Field(default=None, title="Auth Value")
    timeout_seconds: TimeoutSeconds1 | None = Field(
        default=None, title="Timeout Seconds"
    )
    max_retries: MaxRetries | None = Field(default=None, title="Max Retries")
    is_active: bool | None = Field(default=None, title="Is Active")


class WorkflowEdge(BaseModel):
    id: str = Field(..., title="Id")
    source: str = Field(..., title="Source")
    target: str = Field(..., title="Target")
    sourceHandle: str | None = Field(default=None, title="Sourcehandle")
    label: str | None = Field(default=None, title="Label")
    condition: EdgeCondition | None = None


class WorkflowNode(BaseModel):
    id: str = Field(..., title="Id")
    type: NodeType
    position: NodePosition
    data: dict[str, Any] | None = Field(default=None, title="Data")


class WorkflowResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    agent_id: UUID | None = Field(default=None, title="Agent Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(default=None, title="Description")
    is_active: bool = Field(..., title="Is Active")
    current_version: int = Field(..., title="Current Version")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class WorkflowRevisionStatus(Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class WorkingHoursConfig(BaseModel):
    """
    Configuration for destination working hours.
    """

    enabled: bool | None = Field(
        default=False, description="Enable working hours restrictions", title="Enabled"
    )
    days: list[int] | None = Field(
        default=[1, 2, 3, 4, 5],
        description="Days available (0=Sunday, 1=Monday, ...)",
        title="Days",
    )
    start_time: str | None = Field(
        default="09:00", description="HH:MM format", title="Start Time"
    )
    end_time: str | None = Field(
        default="17:00", description="End time (HH:MM format)", title="End Time"
    )
    timezone: str | None = Field(
        default="America/New_York",
        description="Timezone for working hours",
        title="Timezone",
    )
    unavailable_message: str | None = Field(
        default="This team is currently unavailable. Please try again during business hours.",
        description="Message when outside working hours",
        title="Unavailable Message",
    )


class KnowledgeBaseFileUpload(BaseModel):
    """
    Upload a file to create a knowledge base.
    """

    name: str = Field(
        ..., description="Display name for the knowledge base", title="Name"
    )
    description: str | None = Field(
        default=None, description="Optional description", title="Description"
    )
    file: bytes = Field(
        ..., description="File to upload (txt, md, html, pdf, docx, epub)", title="File"
    )


class APIKeyCreate(BaseModel):
    """
    Request to create an API key.
    """

    name: str = Field(..., max_length=100, min_length=1, title="Name")
    description: str | None = Field(default=None, title="Description")
    key_type: KeyType | None = "organization"
    scopes: list[Permission] | None = Field(default=None, title="Scopes")
    scope_preset: str | None = Field(
        default=None,
        description="Use preset: read_only, standard, full_access",
        title="Scope Preset",
    )
    expires_at: AwareDatetime | None = Field(default=None, title="Expires At")
    rate_limit_per_minute: int | None = Field(
        default=60, ge=1, le=10000, title="Rate Limit Per Minute"
    )
    allowed_ips: list[str] | None = Field(
        default=None, description="IP whitelist", title="Allowed Ips"
    )
    metadata: dict[str, Any] | None = Field(default=None, title="Metadata")


class APIKeyResponse(BaseModel):
    """
    API key response (without secret).
    """

    id: str = Field(..., title="Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(..., title="Description")
    key_type: KeyType
    prefix: str = Field(
        ..., description="Key prefix for identification (first 8 chars)", title="Prefix"
    )
    scopes: list[Permission] = Field(..., title="Scopes")
    created_at: AwareDatetime = Field(..., title="Created At")
    expires_at: AwareDatetime | None = Field(..., title="Expires At")
    last_used_at: AwareDatetime | None = Field(..., title="Last Used At")
    is_active: bool = Field(..., title="Is Active")
    rate_limit_per_minute: int = Field(..., title="Rate Limit Per Minute")
    allowed_ips: list[str] | None = Field(..., title="Allowed Ips")
    organization_id: str | None = Field(..., title="Organization Id")
    created_by: str = Field(..., title="Created By")
    metadata: dict[str, Any] | None = Field(default=None, title="Metadata")
    revoked_at: AwareDatetime | None = Field(default=None, title="Revoked At")


class APIKeyWithSecret(BaseModel):
    """
    API key response with secret (only on creation).
    """

    id: str = Field(..., title="Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(..., title="Description")
    key_type: KeyType
    prefix: str = Field(
        ..., description="Key prefix for identification (first 8 chars)", title="Prefix"
    )
    scopes: list[Permission] = Field(..., title="Scopes")
    created_at: AwareDatetime = Field(..., title="Created At")
    expires_at: AwareDatetime | None = Field(..., title="Expires At")
    last_used_at: AwareDatetime | None = Field(..., title="Last Used At")
    is_active: bool = Field(..., title="Is Active")
    rate_limit_per_minute: int = Field(..., title="Rate Limit Per Minute")
    allowed_ips: list[str] | None = Field(..., title="Allowed Ips")
    organization_id: str | None = Field(..., title="Organization Id")
    created_by: str = Field(..., title="Created By")
    metadata: dict[str, Any] | None = Field(default=None, title="Metadata")
    revoked_at: AwareDatetime | None = Field(default=None, title="Revoked At")
    key: str = Field(..., description="Full API key (only shown once)", title="Key")


class AccountListResponse(BaseModel):
    results: list[AccountResponse] = Field(..., title="Results")


class ActiveCallInfo(BaseModel):
    """
    Active call info for the supervisor dashboard.
    """

    id: str = Field(..., title="Id")
    channel: str = Field(..., title="Channel")
    direction: str | None = Field(default=None, title="Direction")
    phone_number: str | None = Field(default=None, title="Phone Number")
    agent_name: str | None = Field(default=None, title="Agent Name")
    agent_id: str | None = Field(default=None, title="Agent Id")
    status: str = Field(..., title="Status")
    connection_status: str | None = Field(default=None, title="Connection Status")
    participants: list[ActiveCallParticipant] | None = Field(
        default=None, title="Participants"
    )
    started_at: str | None = Field(default=None, title="Started At")
    duration_seconds: int | None = Field(default=None, title="Duration Seconds")


class ActiveCallsResponse(BaseModel):
    success: bool = Field(..., title="Success")
    calls: list[ActiveCallInfo] = Field(..., title="Calls")
    total_active: int = Field(..., title="Total Active")
    timestamp: str = Field(..., title="Timestamp")


class AgentListResponse(BaseModel):
    """
    API response for agent list.

    Standardized pagination format:
    - results: List of items
    - metadata: Pagination info (skip, limit, total, has_more, count)
    """

    results: list[AgentResponse] = Field(
        ..., description="List of agents", title="Results"
    )
    metadata: PaginationMetadata = Field(..., description="Pagination metadata")


class AllOrgsUsageResponse(BaseModel):
    """
    Usage summary for all organizations.
    """

    items: list[OrgUsageItem] = Field(..., title="Items")
    period_days: int = Field(..., title="Period Days")


class AmbientAudioConfig(BaseModel):
    """
    Configuration for ambient background audio.

    Ambient sound plays on a loop in the background during the agent session.
    Use a BuiltinAudioClip preset or provide a custom audio URL/path.
    """

    enabled: bool | None = Field(
        default=False, description="Enable ambient audio", title="Enabled"
    )
    source: BuiltinAudioClip | str | None = Field(
        default="office_ambience",
        description="Built-in audio clip or custom URL/path to audio file",
        title="Source",
    )
    volume: float | None = Field(
        default=0.8, description="Ambient audio volume", ge=0.0, le=1.0, title="Volume"
    )


class AnalysisPlan(BaseModel):
    """
    Post-call analysis configuration.

    Per-feature presence-based gating: each analysis runs only when its
    prompt / schema / flag is populated. The previous master ``enabled``
    toggle was removed in May 2026 — it was a footgun (users would set
    summaryPrompt and still get nothing because they didn't notice the
    master switch was off).
    """

    summaryPrompt: str | None = Field(
        default=None,
        description="Custom prompt for call summary. Empty string disables summary.",
        title="Summaryprompt",
    )
    structuredDataPrompt: str | None = Field(
        default=None,
        description="Custom prompt for structured data extraction",
        title="Structureddataprompt",
    )
    structuredDataSchema: dict[str, Any] | None = Field(
        default=None,
        description="JSON Schema defining the format of extracted data",
        title="Structureddataschema",
    )
    successEvaluationPrompt: str | None = Field(
        default=None,
        description="Custom prompt for success evaluation. Empty string disables evaluation.",
        title="Successevaluationprompt",
    )
    successEvaluationRubric: SuccessEvaluationRubric | None = Field(
        default="PassFail", description="Rubric type for evaluation"
    )
    extract_topics: bool | None = Field(
        default=False,
        description="Auto-extract topics discussed during the call",
        title="Extract Topics",
    )
    extract_action_items: bool | None = Field(
        default=False,
        description="Auto-extract action items mentioned during the call",
        title="Extract Action Items",
    )
    compute_user_sentiment: bool | None = Field(
        default=False,
        description="Compute categorical user sentiment from the per-turn sentiment timeline",
        title="Compute User Sentiment",
    )
    minMessagesThreshold: int | None = Field(
        default=2,
        description="Skip analysis if conversation has fewer messages than this",
        ge=0,
        le=20,
        title="Minmessagesthreshold",
    )


class AuthConnectionListResponse(BaseModel):
    results: list[AuthConnectionResponse] = Field(..., title="Results")


class AuthContextResponse(BaseModel):
    """
    Authentication context for the current user.

    This is the main response from /auth/me endpoint.
    Frontend uses scopes to determine UI permissions.
    """

    email: str = Field(..., title="Email")
    user_id: str = Field(
        ..., description="User identifier from auth provider", title="User Id"
    )
    tenant_id: str | None = Field(default=None, title="Tenant Id")
    organization_id: str | None = Field(default=None, title="Organization Id")
    organization_name: str | None = Field(default=None, title="Organization Name")
    role: RoleType | None = Field(default="viewer", description="Effective role")
    effective_role: str | None = Field(
        default="viewer",
        description="String version of effective role for frontend",
        title="Effective Role",
    )
    is_super_admin: bool | None = Field(
        default=False,
        description="Whether user has super admin access",
        title="Is Super Admin",
    )
    scopes: list[str] | None = Field(
        default=None, description="Permission scopes from JWT", title="Scopes"
    )
    session_id: str | None = Field(default=None, title="Session Id")
    authenticated_via: str | None = Field(
        default="jwt", description="jwt or api_key", title="Authenticated Via"
    )


class BackgroundAudioConfig(BaseModel):
    """
    Combined background audio settings.
    """

    ambient: AmbientAudioConfig | None = Field(
        default=None, description="Ambient audio settings"
    )
    thinking: ThinkingAudioConfig | None = Field(
        default=None, description="Thinking audio settings"
    )


class BalanceHistoryResponse(BaseModel):
    """
    List of balance transactions.
    """

    transactions: list[BalanceTransactionResponse] = Field(..., title="Transactions")
    current_balance_cents: int = Field(..., title="Current Balance Cents")
    current_balance_dollars: float = Field(..., title="Current Balance Dollars")


class BatchCallRequest(BaseModel):
    """
    Batch outbound WhatsApp calls — sends permission-request templates to multiple recipients.
    """

    whatsapp_phone_number_id: str = Field(..., title="Whatsapp Phone Number Id")
    recipients: list[str] = Field(
        ...,
        description="List of recipient WhatsApp IDs (E.164 phone numbers)",
        max_length=100,
        min_length=1,
        title="Recipients",
    )
    permission_request_template_name: str = Field(
        ..., title="Permission Request Template Name"
    )
    permission_request_template_language_code: str | None = Field(
        default="en_US", title="Permission Request Template Language Code"
    )
    template_params: list[TemplateParam] | None = Field(
        default=None,
        description="Body parameters for the call permission template (named or positional). Same auto-resolve contract as ``InitiateCallRequest`` — supply ``template_body`` + ``dynamic_variables`` to fill from the agent map.",
        title="Template Params",
    )
    template_body: TemplateBody | None = Field(
        default=None,
        description="Raw template body for placeholder auto-resolution.",
        title="Template Body",
    )
    dynamic_variables: dict[str, str] | None = Field(
        default=None,
        description="Per-conversation runtime variable map applied uniformly to every recipient in the batch. For per-recipient overrides, supply ``template_params`` directly.",
        title="Dynamic Variables",
    )
    agent_id: UUID = Field(..., title="Agent Id")


class BulkPasteContactsResponse(BaseModel):
    """
    Result of /contacts/bulk.
    """

    imported_count: int | None = Field(default=0, title="Imported Count")
    skipped_count: int | None = Field(default=0, title="Skipped Count")
    dnc_blocked_count: int | None = Field(default=0, title="Dnc Blocked Count")
    errors: list[ContactImportProgressError] | None = Field(
        default=None, title="Errors"
    )


class CallListsListResponse(BaseModel):
    """
    Paginated list of call lists.

    Standardized pagination format:
    - results: List of call lists
    - metadata: Pagination info (skip, limit, total, has_more, count)
    """

    results: list[CallListResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class CampaignAttemptListResponse(BaseModel):
    """
    Paginated list of CampaignAttempt rows for GET /campaigns/{id}/attempts.
    """

    results: list[CampaignAttemptResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class CampaignCoverageResponse(BaseModel):
    """
    Per-required-variable fill rate across a call list's active contacts.

    Powers the wizard Step 1 coverage report and mirrors the math the
    /start hard-block uses. ``blocking_zero_pct`` is the slice that
    would refuse a launch.
    """

    required_variables: list[str] = Field(..., title="Required Variables")
    total_contacts: int = Field(..., title="Total Contacts")
    per_variable: dict[str, VariableCoverageStat] = Field(..., title="Per Variable")
    blocking_zero_pct: list[str] = Field(..., title="Blocking Zero Pct")


class CampaignListResponse(BaseModel):
    """
    Paginated list of campaigns.

    Standardized pagination format:
    - results: List of campaigns
    - metadata: Pagination info (skip, limit, total, has_more, count)
    """

    results: list[OutboundCampaignResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class ChatDashboardResponse(BaseModel):
    """
    Chat-side analytics payload mirroring the voice dashboard contract.
    """

    start_date: str = Field(..., title="Start Date")
    end_date: str = Field(..., title="End Date")
    kpis: ChatKPIs
    by_channel: list[ChatChannelMetrics] | None = Field(
        default=None, title="By Channel"
    )
    volume_series: list[ChatVolumePoint] | None = Field(
        default=None, title="Volume Series"
    )
    delivery_breakdown: list[ChatDeliveryBreakdown] | None = Field(
        default=None, title="Delivery Breakdown"
    )


class ConversationListResponse(BaseModel):
    results: list[ConversationResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class DNCEntryListResponse(BaseModel):
    items: list[DNCEntryResponse] = Field(..., title="Items")
    count: int = Field(..., title="Count")


class DashboardKPIs(BaseModel):
    """
    Primary KPIs displayed on dashboard summary cards.
    Backend provides complete, pre-formatted data - frontend just displays.
    """

    total_calls: KPIMetric = Field(..., description="Total calls in period")
    answered_calls: KPIMetric = Field(
        ..., description="Successfully answered/completed calls"
    )
    error_calls: KPIMetric = Field(..., description="Failed/error calls")
    answer_rate: KPIMetric = Field(..., description="Answered / Total as percentage")
    error_rate: KPIMetric = Field(..., description="Errors / Total as percentage")
    success_rate: KPIMetric = Field(..., description="Completed / Total as percentage")
    avg_handle_time: KPIMetric = Field(..., description="Average call duration")
    total_duration_minutes: KPIMetric = Field(..., description="Total minutes used")
    booking_rate: KPIMetric | None = Field(default=None, description="Bookings / Total")
    latency: LatencyMetrics | None = Field(
        default=None, description="AI component latencies"
    )
    avg_sentiment_score: KPIMetric | None = Field(
        default=None, description="Average sentiment (-1 to 1, formatted as %)"
    )
    avg_quality_score: KPIMetric | None = Field(
        default=None, description="Average audio/conversation quality (0-100%)"
    )
    total_cost: KPIMetric | None = Field(default=None, description="Total cost in USD")


class GraphDataInput(BaseModel):
    nodes: list[WorkflowNode] | None = Field(default=None, title="Nodes")
    edges: list[WorkflowEdge] | None = Field(default=None, title="Edges")
    start_node_id: str | None = Field(default=None, title="Start Node Id")
    global_nodes: list[WorkflowNode] | None = Field(default=None, title="Global Nodes")
    global_config: dict[str, Any] | None = Field(default=None, title="Global Config")


class GraphDataOutput(BaseModel):
    nodes: list[WorkflowNode] | None = Field(default=None, title="Nodes")
    edges: list[WorkflowEdge] | None = Field(default=None, title="Edges")
    start_node_id: str | None = Field(default=None, title="Start Node Id")
    global_nodes: list[WorkflowNode] | None = Field(default=None, title="Global Nodes")
    global_config: dict[str, Any] | None = Field(default=None, title="Global Config")


class GroqModelConfig(BaseModel):
    """
    Groq fast inference model configuration.

    SDK Notes:
    - Parameter is max_completion_tokens (NOT max_tokens)
    - reasoning_effort: only valid for openai/gpt-oss-20b and openai/gpt-oss-120b
      Valid values: 'low', 'medium', 'high'. Default: 'medium'.
      Groq API confirmed — 'none' is NOT valid for gpt-oss models (only for Qwen3).
    """

    provider: Literal["groq"] = Field(default="groq", title="Provider")
    model: GroqModel | None = Field(
        default="meta-llama/llama-4-scout-17b-16e-instruct",
        description="Groq model to use",
    )
    instructions: str | None = Field(
        default="You are a helpful AI assistant.",
        description="System prompt/instructions for the model",
        title="Instructions",
    )
    system_timezone: str | None = Field(
        default="UTC",
        description="Agent's timezone for time-aware responses",
        title="System Timezone",
    )
    temperature: float | None = Field(
        default=0.8,
        description="Randomness in responses",
        ge=0.0,
        le=2.0,
        title="Temperature",
    )
    max_completion_tokens: int | None = Field(
        default=4096,
        description="Maximum tokens in response",
        ge=1,
        le=32768,
        title="Max Completion Tokens",
    )
    tool_choice: ToolChoice | None = Field(
        default="auto", description="How to select tools"
    )
    reasoning_effort: ReasoningEffort | None = Field(
        default=None,
        description="Reasoning effort for GPT-OSS reasoning models (openai/gpt-oss-20b, openai/gpt-oss-120b). Only 'low', 'medium', 'high' are valid — 'none' is not supported for these models. None = use API default (medium). Only set when using a reasoning model.",
        title="Reasoning Effort",
    )
    parallel_tool_calls: bool | None = Field(
        default=True,
        description="Allow the model to call multiple tools in a single response.",
        title="Parallel Tool Calls",
    )
    max_tool_steps: int | None = Field(
        default=3,
        description="Maximum consecutive tool calls per LLM turn.",
        ge=1,
        le=20,
        title="Max Tool Steps",
    )


class HTTPValidationError(BaseModel):
    detail: list[ValidationError] | None = Field(default=None, title="Detail")


class IncidentOut(BaseModel):
    id: UUID = Field(..., title="Id")
    title: str = Field(..., title="Title")
    status: str = Field(..., title="Status")
    impact: str = Field(..., title="Impact")
    started_at: AwareDatetime = Field(..., title="Started At")
    resolved_at: AwareDatetime | None = Field(..., title="Resolved At")
    updates: list[IncidentUpdateOut] = Field(..., title="Updates")
    affected_components: list[str] = Field(..., title="Affected Components")


class InitiateCallRequest(BaseModel):
    """
    Initiate an outbound WhatsApp voice call.
    Mirrors ElevenLabs /whatsapp/outbound-call parameters.
    """

    whatsapp_phone_number_id: str = Field(..., title="Whatsapp Phone Number Id")
    whatsapp_user_id: str = Field(
        ..., max_length=20, min_length=7, title="Whatsapp User Id"
    )
    permission_request_template_name: str = Field(
        ..., title="Permission Request Template Name"
    )
    permission_request_template_language_code: str | None = Field(
        default="en_US", title="Permission Request Template Language Code"
    )
    template_params: list[TemplateParam] | None = Field(
        default=None,
        description="Body parameters for the call permission template (named or positional). Leave empty and supply ``template_body`` + ``dynamic_variables`` to have the server resolve placeholders from the agent variable map.",
        title="Template Params",
    )
    template_body: TemplateBody1 | None = Field(
        default=None,
        description="Raw template body string for the permission-request template. Supplied by the frontend after fetching the definition from Meta. When given, server resolves ``{{placeholder}}`` against ``dynamic_variables`` to build ``template_params``.",
        title="Template Body",
    )
    agent_id: UUID = Field(..., title="Agent Id")
    dynamic_variables: dict[str, str] | None = Field(
        default=None,
        description="Values for {{var}} placeholders in the agent's first_message and instructions. Persisted on the PendingCallIntent and applied at call placement time (which can be up to 24h after the permission request is sent). Same contract as POST /calls/outbound dynamic_variables.",
        examples=[{"company_name": "Acme", "customer_name": "Sarah"}],
        title="Dynamic Variables",
    )


class InvoiceListResponse(BaseModel):
    """
    List of invoices with metadata.
    """

    results: list[InvoiceResponse] = Field(..., title="Results")
    metadata: BillingListMetadata


class KnowledgeBaseListResponse(BaseModel):
    """
    Lightweight response for list views.
    """

    id: UUID = Field(..., title="Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(default=None, title="Description")
    source_type: KnowledgeBaseType
    source_url: str | None = Field(default=None, title="Source Url")
    source_filename: str | None = Field(default=None, title="Source Filename")
    source_mimetype: str | None = Field(default=None, title="Source Mimetype")
    size_bytes: int = Field(..., title="Size Bytes")
    chunk_count: int = Field(..., title="Chunk Count")
    status: KnowledgeBaseStatus
    progress: int | None = Field(default=0, title="Progress")
    error_message: str | None = Field(default=None, title="Error Message")
    created_by: str | None = Field(default=None, title="Created By")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")
    is_active: bool = Field(..., title="Is Active")


class KnowledgeBaseListResult(BaseModel):
    """
    Paginated list of knowledge bases.

    Standardized pagination format:
    - results: List of knowledge bases
    - metadata: Pagination info (skip, limit, total, has_more, count)
    """

    results: list[KnowledgeBaseListResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class KnowledgeBaseResponse(BaseModel):
    """
    Knowledge base response with full details.
    """

    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(default=None, title="Description")
    source_type: KnowledgeBaseType
    source_url: str | None = Field(default=None, title="Source Url")
    source_filename: str | None = Field(default=None, title="Source Filename")
    source_mimetype: str | None = Field(default=None, title="Source Mimetype")
    raw_content: str | None = Field(default=None, title="Raw Content")
    size_bytes: int = Field(..., title="Size Bytes")
    chunk_count: int = Field(..., title="Chunk Count")
    status: KnowledgeBaseStatus
    progress: int | None = Field(default=0, title="Progress")
    error_message: str | None = Field(default=None, title="Error Message")
    created_by: str | None = Field(default=None, title="Created By")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")
    is_active: bool = Field(..., title="Is Active")


class McpProbeResult(BaseModel):
    """
    Outcome of a connect + ``tools/list`` probe.
    """

    success: bool = Field(..., title="Success")
    server_info: dict[str, Any] | None = Field(default=None, title="Server Info")
    tools: list[McpTool] | None = Field(default=None, title="Tools")
    tool_count: int | None = Field(default=0, title="Tool Count")
    error: str | None = Field(default=None, title="Error")
    error_type: str | None = Field(default=None, title="Error Type")


class McpServerListResponse(BaseModel):
    results: list[McpServerResponse] = Field(..., title="Results")


class MessageListResponse(BaseModel):
    results: list[MessageResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class NotificationListResponse(BaseModel):
    """
    Paginated notification list response.

    Standardized pagination format:
    - results: List of notifications
    - metadata: Pagination info (skip, limit, total, has_more, count)
    - unread_count: Additional notification-specific field
    """

    results: list[NotificationOut] = Field(..., title="Results")
    metadata: PaginationMetadata
    unread_count: int = Field(..., title="Unread Count")


class OpenAIModelConfig(BaseModel):
    """
    OpenAI GPT model configuration.

    SDK Notes:
    - Default model in SDK is 'gpt-4.1-mini'
    - Parameter is max_completion_tokens (NOT max_tokens)
    - parallel_tool_calls supported
    """

    provider: Literal["openai"] = Field(default="openai", title="Provider")
    model: OpenAIModel | None = Field(
        default="gpt-4.1-mini", description="OpenAI model to use"
    )
    instructions: str | None = Field(
        default="You are a helpful AI assistant.",
        description="System prompt/instructions for the model",
        title="Instructions",
    )
    system_timezone: str | None = Field(
        default="UTC",
        description="Agent's timezone for time-aware responses (e.g., 'America/New_York', 'Europe/London')",
        title="System Timezone",
    )
    temperature: float | None = Field(
        default=0.8,
        description="Randomness in responses (0=deterministic, 2=creative)",
        ge=0.0,
        le=2.0,
        title="Temperature",
    )
    max_completion_tokens: MaxCompletionTokens | None = Field(
        default=4096,
        description="Maximum tokens in response",
        title="Max Completion Tokens",
        validate_default=True,
    )
    tool_choice: ToolChoice | None = Field(
        default="auto", description="How to select tools"
    )
    parallel_tool_calls: bool | None = Field(
        default=True,
        description="Allow the model to call multiple tools in a single response.",
        title="Parallel Tool Calls",
    )
    max_tool_steps: int | None = Field(
        default=3,
        description="Maximum consecutive tool calls per LLM turn.",
        ge=1,
        le=20,
        title="Max Tool Steps",
    )
    reasoning_effort: ReasoningEffort1 | None = Field(
        default=None,
        description="Reasoning effort for OpenAI reasoning models. Only 'none', 'minimal', 'low', 'medium', 'high', 'max' are valid.",
        title="Reasoning Effort",
    )


class PaymentMethodListResponse(BaseModel):
    """
    List of payment methods with metadata.
    """

    results: list[PaymentMethodResponse] = Field(..., title="Results")
    metadata: BillingListMetadata


class PhantomModelConfig(BaseModel):
    """
    Neuratel Phantom LLM — proprietary inference via phantom.neuratel.ai.
    """

    provider: Literal["phantom"] = Field(default="phantom", title="Provider")
    model: str | None = Field(
        default="phantom", description="Phantom Brain model", title="Model"
    )
    instructions: str | None = Field(
        default="You are a helpful AI assistant.",
        description="System prompt/instructions for the model",
        title="Instructions",
    )
    system_timezone: str | None = Field(
        default="UTC",
        description="Agent's timezone for time-aware responses",
        title="System Timezone",
    )
    temperature: float | None = Field(
        default=0.8,
        description="Randomness in responses",
        ge=0.0,
        le=2.0,
        title="Temperature",
    )
    max_completion_tokens: MaxCompletionTokens1 | None = Field(
        default=4096,
        description="Maximum tokens in response",
        title="Max Completion Tokens",
        validate_default=True,
    )
    tool_choice: ToolChoice | None = Field(
        default="auto", description="How to select tools"
    )
    parallel_tool_calls: bool | None = Field(
        default=True,
        description="Allow the model to call multiple tools in a single response.",
        title="Parallel Tool Calls",
    )
    max_tool_steps: int | None = Field(
        default=3,
        description="Maximum consecutive tool calls per LLM turn.",
        ge=1,
        le=20,
        title="Max Tool Steps",
    )


class PhoneNumberListResponse(BaseModel):
    """
    Paginated list of phone numbers.

    Standardized pagination format:
    - results: List of phone numbers
    - metadata: Pagination info (skip, limit, total, has_more, count)
    """

    results: list[PhoneNumberResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class PipelineTurnDetection(BaseModel):
    """
    Turn detection configuration for voice pipeline agents.

    Modes:
    - semantic_vad: Silero VAD + multilingual context-aware EOU model (60+ languages)
    - semantic_vad_en: Silero VAD + English-only context-aware EOU model — faster
    - vad: Silero VAD only — fast, silence-based detection
    - stt: STT-native EOU (auto-selected for Soniox; Soniox owns turn-end detection)

    All modes still use Silero VAD for barge-in / interruption detection.
    Semantic modes add an ML layer to decide whether a pause means "done" vs "thinking".

    Pair with Interruption mode for coherent behavior:
    - semantic_vad → vad interruptions
    - semantic_vad_en → vad interruptions
    - vad → vad interruptions
    - stt → vad interruptions

    Endpointing timing (EndpointingOptions, applies to vad/semantic_vad/semantic_vad_en):
    - min_delay: minimum wait after end-of-utterance before agent responds
    - max_delay: ceiling — agent commits the turn after this long even if the
      detector model is still uncertain
    - endpointing_mode:
      - "fixed": agent waits min_delay; extends up to max_delay only if turn-detector is uncertain
      - "dynamic": adapts effective wait within [min_delay, max_delay] based on this
        caller's pause patterns (exponential moving average)

    For mode="stt" (Soniox), these knobs are unused — Soniox handles EOU internally
    via its built-in semantic endpointing (no per-call tuning).
    """

    mode: PipelineTurnDetectionMode | None = Field(
        default="semantic_vad", description="Turn detection mode"
    )
    min_delay: MinDelay | None = Field(
        default=0.5,
        description="Minimum seconds after end-of-utterance before responding. Default: 0.5",
        title="Min Delay",
        validate_default=True,
    )
    max_delay: MaxDelay | None = Field(
        default=3.0,
        description="Ceiling — agent commits the turn after this long even if detector is uncertain. Default: 3.0",
        title="Max Delay",
        validate_default=True,
    )
    endpointing_mode: EndpointingMode | None = Field(
        default="dynamic",
        description="fixed: agent waits min_delay; extends up to max_delay only if turn-detector is uncertain. dynamic: adapts effective wait within [min_delay, max_delay] based on this caller's pause patterns.",
        title="Endpointing Mode",
    )


class PostCallConfig(BaseModel):
    """
    Configuration for post-call analysis. AnalysisPlan is the only tree.
    """

    analysisPlan: AnalysisPlan | None = Field(
        default=None, description="Post-call analysis configuration"
    )


class RAGQueryResponse(BaseModel):
    """
    RAG query response with results.
    """

    results: list[RAGResult] = Field(..., title="Results")
    query: str = Field(..., title="Query")
    total_chunks_searched: int = Field(..., title="Total Chunks Searched")


class SaveGraphRequest(BaseModel):
    graph_data: GraphDataInput
    change_description: str | None = Field(default=None, title="Change Description")


class SendTemplateMessageRequest(BaseModel):
    """
    Initiate a conversation by sending an approved template message.
    Mirrors ElevenLabs /whatsapp/outbound-message parameters.
    """

    whatsapp_phone_number_id: str = Field(
        ...,
        description="Our WhatsApp phone number ID",
        title="Whatsapp Phone Number Id",
    )
    whatsapp_user_id: str = Field(
        ...,
        description="Recipient's WhatsApp ID (E.164 phone number)",
        max_length=20,
        min_length=7,
        title="Whatsapp User Id",
    )
    template_name: str = Field(..., max_length=255, min_length=1, title="Template Name")
    template_language_code: str | None = Field(
        default="en_US", max_length=10, title="Template Language Code"
    )
    template_params: list[TemplateParam] | None = Field(
        default=None,
        description="Body parameters for the template. Each item is {name, value}. name is '1'..'N' for positional templates or the placeholder identifier for named templates (e.g. 'customer_name'). Leave empty and supply ``template_body`` + ``dynamic_variables`` to have the server auto-resolve from the agent variable map.",
        title="Template Params",
    )
    template_body: TemplateBody2 | None = Field(
        default=None,
        description="Raw template body string (with ``{{placeholder}}`` markers) — supplied by the frontend after fetching the template definition from Meta's registry. When provided alongside ``dynamic_variables`` and an empty ``template_params``, the server resolves placeholders from the agent variable map (named OR positional templates). Bridges the agent-side and Meta-side substitution moments.",
        title="Template Body",
    )
    dynamic_variables: dict[str, str] | None = Field(
        default=None,
        description="Per-conversation runtime variable map. Used to fill ``template_body`` placeholders when ``template_params`` is empty, AND persisted onto Conversation.dynamic_variables so the agent's reply path picks them up after the contact responds. Mirrors the voice-call dispatch contract (POST /v1/voice-sessions/outbound).",
        examples=[{"customer_name": "Sarah", "order_id": "ABC-123"}],
        title="Dynamic Variables",
    )
    template_category: TemplateCategory | None = Field(
        default=None,
        description="Meta WABA category of this template — one of MARKETING, UTILITY, AUTHENTICATION, AUTHENTICATION_INTERNATIONAL, SERVICE, MARKETING_LITE. Pulled from Meta's template registry by the frontend before send. Used to bill the right rate at send time (per-category passthrough) and grouped by the daily true-up cron. Defaults to MARKETING (most expensive bucket) when omitted; truesup reconciles via manual_adjustment ledger.",
        title="Template Category",
    )
    agent_id: UUID | None = Field(
        default=None,
        description="Agent to associate with the resulting conversation",
        title="Agent Id",
    )


class SentimentTimeline(BaseModel):
    trend: str = Field(..., title="Trend")
    average_sentiment: float = Field(..., title="Average Sentiment")
    high_point: dict[str, Any] | None = Field(default=None, title="High Point")
    low_point: dict[str, Any] | None = Field(default=None, title="Low Point")
    turns: list[SentimentTurn] | None = Field(default=None, title="Turns")


class StatusOverview(BaseModel):
    overall_status: str = Field(..., title="Overall Status")
    uptime_30d: float = Field(..., title="Uptime 30D")
    avg_response_time_ms: float = Field(..., title="Avg Response Time Ms")
    active_incidents_count: int = Field(..., title="Active Incidents Count")
    components: list[ComponentOut] = Field(..., title="Components")
    active_incidents: list[IncidentOut] = Field(..., title="Active Incidents")
    recent_incidents: list[IncidentOut] = Field(..., title="Recent Incidents")
    scheduled_maintenance: list[MaintenanceOut] = Field(
        ..., title="Scheduled Maintenance"
    )


class SupervisorJoinResponse(BaseModel):
    success: bool = Field(..., title="Success")
    mode: Mode = Field(..., title="Mode")
    call_id: str = Field(..., title="Call Id")
    token: str = Field(..., title="Token")
    server_url: str | None = Field(..., title="Server Url")
    supervisor_identity: str = Field(..., title="Supervisor Identity")
    permissions: SupervisorPermissions
    note: str | None = Field(default=None, title="Note")
    warning: str | None = Field(default=None, title="Warning")
    timestamp: str = Field(..., title="Timestamp")


class TemplateListResponse(BaseModel):
    results: list[TemplateResponse] = Field(..., title="Results")


class ToolsConfig(BaseModel):
    """
    Complete tools configuration.

    Enables and configures various agent capabilities
    including built-in tools, RAG, and MCP integrations.
    """

    hangup: HangupToolConfig | None = Field(
        default=None, description="Hangup tool settings"
    )
    collect_dtmf: CollectDtmfConfig | None = Field(
        default=None, description="DTMF collection settings"
    )
    send_dtmf: SendDtmfConfig | None = Field(
        default=None, description="DTMF sending settings"
    )
    voicemail: VoicemailToolConfig | None = Field(
        default=None, description="Voicemail detection settings"
    )
    add_to_dnc: AddToDncConfig | None = Field(
        default=None, description="In-call do-not-call opt-out tool"
    )
    place_outbound_call: PlaceOutboundCallConfig | None = Field(
        default=None, description="Outbound call initiation tool"
    )
    send_audio_message: SendAudioMessageConfig | None = Field(
        default=None, description="WhatsApp voice note sending tool"
    )
    rag: RagConfig | None = Field(default=None, description="RAG settings")
    mcp_servers: list[McpServerRef] | None = Field(
        default=None, description="MCP server integrations", title="Mcp Servers"
    )


class TransferDestination(BaseModel):
    """
    Configuration for a transfer destination.
    """

    id: str = Field(
        ..., description="Unique identifier for this destination", title="Id"
    )
    name: str = Field(
        ..., description="Display name (e.g., 'Sales Team', 'Support')", title="Name"
    )
    number: str = Field(..., description="Phone number in E.164 format", title="Number")
    keywords: list[str] | None = Field(
        default=None,
        description="Keywords that trigger this destination",
        title="Keywords",
    )
    description: str | None = Field(
        default=None,
        description="Description for LLM context (when to use this)",
        title="Description",
    )
    message: str | None = Field(
        default="Transferring you now.",
        description="Message before transferring",
        title="Message",
    )
    timeout_seconds: int | None = Field(
        default=30,
        description="Ring timeout before giving up",
        ge=10,
        le=120,
        title="Timeout Seconds",
    )
    priority: int | None = Field(
        default=0,
        description="Priority when multiple match (higher = preferred)",
        ge=0,
        le=100,
        title="Priority",
    )
    working_hours: WorkingHoursConfig | None = Field(
        default=None, description="Working hours for this destination"
    )


class VoiceListResponse(BaseModel):
    """
    Response with voices and filter metadata.
    """

    voices: list[VoiceResponse] = Field(..., title="Voices")
    by_provider: dict[str, list[VoiceResponse]] = Field(..., title="By Provider")
    total: int = Field(..., title="Total")
    counts: dict[str, int] = Field(..., title="Counts")
    filters: dict[str, list[str]] = Field(..., title="Filters")


class VoiceSessionResponse(BaseModel):
    """
    One voice session — phone, web, or WhatsApp voice.
    """

    id: UUID = Field(..., title="Id")
    channel: str = Field(..., title="Channel")
    direction: str | None = Field(default=None, title="Direction")
    organization_id: UUID | None = Field(default=None, title="Organization Id")
    agent_id: UUID | None = Field(default=None, title="Agent Id")
    agent_name: str | None = Field(default=None, title="Agent Name")
    campaign_id: UUID | None = Field(default=None, title="Campaign Id")
    phone_number_id: UUID | None = Field(default=None, title="Phone Number Id")
    whatsapp_account_id: UUID | None = Field(default=None, title="Whatsapp Account Id")
    from_number: str | None = Field(default=None, title="From Number")
    to_number: str | None = Field(default=None, title="To Number")
    participant_address: str | None = Field(default=None, title="Participant Address")
    business_address: str | None = Field(default=None, title="Business Address")
    caller_id: str | None = Field(default=None, title="Caller Id")
    status: str = Field(..., title="Status")
    analysis_status: str | None = Field(default="pending", title="Analysis Status")
    call_result: str | None = Field(default=None, title="Call Result")
    failure_reason: str | None = Field(default=None, title="Failure Reason")
    error_message: str | None = Field(default=None, title="Error Message")
    end_reason: str | None = Field(default=None, title="End Reason")
    retry_count: int | None = Field(default=0, title="Retry Count")
    started_at: AwareDatetime | None = Field(default=None, title="Started At")
    answered_at: AwareDatetime | None = Field(default=None, title="Answered At")
    ended_at: AwareDatetime | None = Field(default=None, title="Ended At")
    duration_seconds: int | None = Field(default=0, title="Duration Seconds")
    billed_amount: float | None = Field(default=None, title="Billed Amount")
    billing_currency: str | None = Field(default=None, title="Billing Currency")
    billable_minutes: float | None = Field(default=None, title="Billable Minutes")
    billing_rate_per_minute: float | None = Field(
        default=None, title="Billing Rate Per Minute"
    )
    participants: list[ParticipantInfo] | None = Field(
        default=None, title="Participants"
    )
    agent_metrics: AgentMetricsSummary | None = None
    conversation_preview: list[ConversationTurnSummary] | None = Field(
        default=None, max_length=5, title="Conversation Preview"
    )
    conversation_turn_count: int | None = Field(
        default=0, title="Conversation Turn Count"
    )
    conversation: list[ConversationTurnSummary] | None = Field(
        default=None, title="Conversation"
    )
    sentiment_trend: list[float] | None = Field(default=None, title="Sentiment Trend")
    topics_discussed: list[str] | None = Field(default=None, title="Topics Discussed")
    keywords_extracted: list[str] | None = Field(
        default=None, title="Keywords Extracted"
    )
    extracted_data: dict[str, Any] | None = Field(default=None, title="Extracted Data")
    usage_metrics: UsageMetrics | None = None
    estimated_cost_usd: float | None = Field(default=None, title="Estimated Cost Usd")
    tool_calls: list[dict[str, Any]] | None = Field(default=None, title="Tool Calls")
    latency: dict[str, Any] | None = Field(default=None, title="Latency")
    call_summary: str | None = Field(default=None, title="Call Summary")
    success_evaluation: dict[str, Any] | None = Field(
        default=None, title="Success Evaluation"
    )
    sentiment_timeline: SentimentTimeline | None = None
    audio_quality: dict[str, Any] | None = Field(default=None, title="Audio Quality")
    topics: list[str] | None = Field(default=None, title="Topics")
    action_items: list[str] | None = Field(default=None, title="Action Items")
    user_sentiment: str | None = Field(default=None, title="User Sentiment")
    user_sentiment_score: float | None = Field(
        default=None, title="User Sentiment Score"
    )
    call_successful: str | None = Field(default=None, title="Call Successful")
    call_successful_rationale: str | None = Field(
        default=None, title="Call Successful Rationale"
    )
    evaluation_score: dict[str, Any] | None = Field(
        default=None, title="Evaluation Score"
    )
    recording: RecordingResponse | None = None
    session_id: str | None = Field(default=None, title="Session Id")
    call_metadata: dict[str, Any] | None = Field(default=None, title="Call Metadata")
    contact_data: dict[str, Any] | None = Field(default=None, title="Contact Data")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")


class WebhookConfig(BaseModel):
    """
    Configuration for webhook notifications.
    """

    enabled: bool | None = Field(
        default=False, description="Enable webhook notifications", title="Enabled"
    )
    url: str | None = Field(default=None, description="HTTPS endpoint URL", title="Url")
    events: list[WebhookEvent] | None = Field(
        default=["session_report", "call_ended", "error"],
        description="Events to send webhooks for",
        title="Events",
    )
    include_transcript: bool | None = Field(
        default=True,
        description="Include transcript in webhook payload",
        title="Include Transcript",
    )
    include_analytics: bool | None = Field(
        default=True,
        description="Include analytics in webhook payload",
        title="Include Analytics",
    )
    include_recording_url: bool | None = Field(
        default=True,
        description="Include recording URL when available (always included by default)",
        title="Include Recording Url",
    )
    auth_header: str | None = Field(
        default="Authorization",
        description="Authentication header name",
        title="Auth Header",
    )
    auth_token: str | None = Field(
        default=None,
        description="Authentication token (Bearer format)",
        title="Auth Token",
    )
    retry_count: int | None = Field(
        default=3,
        description="Number of retry attempts",
        ge=0,
        le=10,
        title="Retry Count",
    )
    timeout_seconds: float | None = Field(
        default=30.0,
        description="Webhook request timeout",
        ge=5.0,
        le=120.0,
        title="Timeout Seconds",
    )


class WebhookCreate(BaseModel):
    """
    Create a new webhook subscription
    """

    name: str = Field(
        ...,
        description="Human-readable name for the webhook",
        max_length=255,
        min_length=1,
        title="Name",
    )
    description: Description7 | None = Field(
        default=None, description="Optional description", title="Description"
    )
    url: str = Field(
        ..., description="HTTPS endpoint URL to receive webhook events", title="Url"
    )
    events: list[WebhookEventTypeEnum] | None = Field(
        default=None,
        description="List of event types to subscribe to. Empty = all events",
        title="Events",
    )
    auth_header: AuthHeader | None = Field(
        default=None,
        description="Optional custom header name for authentication (e.g., 'X-Api-Key')",
        title="Auth Header",
    )
    auth_value: AuthValue | None = Field(
        default=None, description="Value for the auth header", title="Auth Value"
    )
    timeout_seconds: int | None = Field(
        default=30,
        description="Request timeout in seconds (1-60)",
        ge=1,
        le=60,
        title="Timeout Seconds",
    )
    max_retries: int | None = Field(
        default=3,
        description="Maximum retry attempts on failure (0-5)",
        ge=0,
        le=5,
        title="Max Retries",
    )
    is_active: bool | None = Field(
        default=True, description="Whether the webhook is active", title="Is Active"
    )


class WebhookListResponse(BaseModel):
    """
    Paginated list of webhooks.

    Standardized pagination format:
    - results: List of webhooks
    - metadata: Pagination info (skip, limit, total, has_more, count)
    """

    results: list[WebhookResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class WorkflowListResponse(BaseModel):
    results: list[WorkflowResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class WorkflowRevisionResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    workflow_id: UUID = Field(..., title="Workflow Id")
    version_number: int = Field(..., title="Version Number")
    status: WorkflowRevisionStatus
    graph_data: GraphDataOutput
    change_description: str | None = Field(default=None, title="Change Description")
    published_at: AwareDatetime | None = Field(default=None, title="Published At")
    created_at: AwareDatetime = Field(..., title="Created At")


class APIKeyListResponse(BaseModel):
    """
    Paginated list of API keys.
    """

    results: list[APIKeyResponse] = Field(..., title="Results")
    metadata: APIKeyListMetadata


class APIKeyRotateResponse(BaseModel):
    """
    Response from key rotation.
    """

    old_key_id: str = Field(..., title="Old Key Id")
    new_key: APIKeyWithSecret
    grace_period_ends: AwareDatetime = Field(
        ...,
        description="Old key remains valid until this time",
        title="Grace Period Ends",
    )


class AgentKnowledgeBaseListResponse(BaseModel):
    """
    List of knowledge bases assigned to an agent.
    """

    agent_id: UUID = Field(..., title="Agent Id")
    knowledge_bases: list[KnowledgeBaseListResponse] = Field(
        ..., title="Knowledge Bases"
    )


class AnalyticsConfig(BaseModel):
    """
    Complete analytics configuration.

    Controls all observability features including metrics,
    webhooks, recording, and post-call analysis.
    """

    enabled: bool | None = Field(
        default=True, description="Enable analytics overall", title="Enabled"
    )
    track_sentiment: bool | None = Field(
        default=True,
        description="Track emotional tone/sentiment throughout calls in real-time",
        title="Track Sentiment",
    )
    webhook: WebhookConfig | None = Field(
        default=None, description="Webhook notification settings"
    )
    recording: RecordingConfig | None = Field(
        default=None, description="Call recording settings"
    )
    post_call: PostCallConfig | None = Field(
        default=None, description="Post-call analysis settings"
    )


class AnalyticsDashboardResponse(BaseModel):
    """
    COMPREHENSIVE ANALYTICS RESPONSE - Single Source of Truth

    This is the primary analytics endpoint. Backend returns everything
    the frontend needs - no client-side calculations required.
    """

    start_date: str = Field(
        ..., description="Start date YYYY-MM-DD", title="Start Date"
    )
    end_date: str = Field(..., description="End date YYYY-MM-DD", title="End Date")
    time_range: TimeRange | None = Field(
        default=None, description="Named time range if applicable"
    )
    kpis: DashboardKPIs = Field(..., description="Primary KPI metrics")
    call_volume: list[CallVolumeDataPoint] | None = Field(
        default=None, description="Call volume over time", title="Call Volume"
    )
    contribution_data: list[ContributionDataPoint] | None = Field(
        default=None, description="Activity heatmap data", title="Contribution Data"
    )
    call_outcomes: CallOutcomeBreakdown | None = Field(
        default=None, description="Call outcome breakdown"
    )
    hourly_distribution: list[HourlyDistribution] | None = Field(
        default=None, description="By hour of day", title="Hourly Distribution"
    )
    daily_distribution: list[DayOfWeekDistribution] | None = Field(
        default=None, description="By day of week", title="Daily Distribution"
    )
    agents: list[AgentPerformance] | None = Field(
        default=None, description="Per-agent performance", title="Agents"
    )
    campaigns: list[CampaignPerformance] | None = Field(
        default=None, description="Per-campaign performance", title="Campaigns"
    )
    latency: LatencyMetrics | None = Field(
        default=None, description="Average latency metrics"
    )


class CombinedDashboardResponse(BaseModel):
    """
    Voice + chat dashboard returned by `/v1/analytics/dashboard`.
    """

    start_date: str = Field(..., title="Start Date")
    end_date: str = Field(..., title="End Date")
    voice: AnalyticsDashboardResponse
    chat: ChatDashboardResponse
    combined_cost: CombinedCost


class TransferConfig(BaseModel):
    """
    Complete transfer configuration.

    Controls how calls are transferred to other destinations
    including agents, teams, or external numbers.
    """

    enabled: bool | None = Field(
        default=False, description="Enable transfer capability", title="Enabled"
    )
    mode: TransferMode | None = Field(
        default="blind",
        description="Transfer type: blind (immediate) or warm (with intro)",
    )
    destinations: list[TransferDestination] | None = Field(
        default=None,
        description="Available transfer destinations",
        title="Destinations",
    )
    fallback_destination: TransferDestination | None = Field(
        default=None, description="Default destination if no match"
    )
    warm_intro_template: str | None = Field(
        default="Hi, I'm transferring a caller who needs help with {reason}. They said: {summary}",
        description="Template for warm transfer introduction",
        title="Warm Intro Template",
    )
    warm_intro_timeout_seconds: int | None = Field(
        default=60,
        description="Time to wait for warm intro before falling back",
        ge=10,
        le=180,
        title="Warm Intro Timeout Seconds",
    )
    on_fail: TransferOnFail | None = Field(
        default="return", description="What to do if transfer fails"
    )
    fail_message: str | None = Field(
        default="I'm sorry, I wasn't able to transfer your call. Let me help you directly.",
        description="Message on transfer failure",
        title="Fail Message",
    )
    max_retries: int | None = Field(
        default=2,
        description="Maximum transfer retry attempts",
        ge=0,
        le=5,
        title="Max Retries",
    )
    hold_music: bool | None = Field(
        default=True, description="Play hold music during transfer", title="Hold Music"
    )
    hold_music_url: str | None = Field(
        default=None, description="Custom hold music URL", title="Hold Music Url"
    )
    announce_position: bool | None = Field(
        default=False,
        description="Announce queue position if applicable",
        title="Announce Position",
    )


class VoiceSessionListResponse(BaseModel):
    results: list[VoiceSessionResponse] = Field(..., title="Results")
    metadata: PaginationMetadata


class WorkflowDetailResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    organization_id: UUID = Field(..., title="Organization Id")
    agent_id: UUID | None = Field(default=None, title="Agent Id")
    name: str = Field(..., title="Name")
    description: str | None = Field(default=None, title="Description")
    is_active: bool = Field(..., title="Is Active")
    current_version: int = Field(..., title="Current Version")
    created_at: AwareDatetime = Field(..., title="Created At")
    updated_at: AwareDatetime = Field(..., title="Updated At")
    versions: list[WorkflowRevisionResponse] | None = Field(
        default=[], title="Versions", validate_default=True
    )


class AgentCreate(BaseModel):
    """
    Request schema for creating a new agent.

    Only `name` is required - all other fields have production-ready defaults.
    Users can override any field with their own values.

    The service layer applies defaults via deep_merge_config().
    """

    name: str = Field(
        ...,
        description="Agent display name (required)",
        max_length=255,
        min_length=1,
        title="Name",
    )
    agent_type: AgentType | None = Field(
        default="advanced",
        description="Agent type: advanced (form-based) or workflow (graph-based)",
        title="Agent Type",
    )
    template_id: str | None = Field(
        default=None,
        description="Template ID to apply preset instructions and config. See GET /v1/templates for available templates.",
        title="Template Id",
    )
    tags: list[str] | None = Field(
        default=None, description="Tags for organization", max_length=20, title="Tags"
    )
    description: Description | None = Field(
        default=None, description="Agent description", title="Description"
    )
    brain: OpenAIModelConfig | GroqModelConfig | PhantomModelConfig | None = Field(
        default=None,
        description="LLM configuration. Default: OpenAI GPT-4.1",
        title="Brain",
    )
    voice: CartesiaVoiceConfig | PhantomVoiceConfig | None = Field(
        default=None,
        description="TTS configuration. Default: ElevenLabs Flash v2.5",
        title="Voice",
    )
    transcriber: (
        DeepgramTranscriberConfig
        | SonioxTranscriberConfig
        | PhantomTranscriberConfig
        | None
    ) = Field(
        default=None,
        description="STT configuration. Default: ElevenLabs Scribe v2",
        title="Transcriber",
    )
    turn_detection: PipelineTurnDetection | None = None
    first_message: FirstMessageConfig | None = None
    interruption: InterruptionConfig | None = None
    timeout: TimeoutConfig | None = None
    call_duration: CallDurationConfig | None = None
    background_audio: BackgroundAudioConfig | None = None
    tts_text_transforms: list[TTSTextTransform] | None = Field(
        default=None, title="Tts Text Transforms"
    )
    preemptive_generation: bool | None = Field(
        default=None, title="Preemptive Generation"
    )
    min_consecutive_speech_delay: float | None = Field(
        default=None, title="Min Consecutive Speech Delay"
    )
    tools: ToolsConfig | None = Field(
        default=None, description="Tool and capability settings"
    )
    transfer: TransferConfig | None = Field(
        default=None, description="Call transfer settings"
    )
    analytics: AnalyticsConfig | None = Field(
        default=None, description="Analytics and monitoring settings"
    )


class AgentUpdate(BaseModel):
    """
    Request schema for updating an agent.

    All fields are optional - only provided fields are updated.
    """

    name: Name | None = Field(
        default=None, description="Agent display name", title="Name"
    )
    tags: Tags | None = Field(
        default=None, description="Tags for organization", title="Tags"
    )
    description: Description | None = Field(
        default=None, description="Agent description", title="Description"
    )
    is_active: bool | None = Field(
        default=None, description="Whether agent is active", title="Is Active"
    )
    brain: OpenAIModelConfig | GroqModelConfig | PhantomModelConfig | None = Field(
        default=None,
        description="LLM configuration (brain - what thinks)",
        title="Brain",
    )
    voice: CartesiaVoiceConfig | PhantomVoiceConfig | None = Field(
        default=None, description="TTS configuration", title="Voice"
    )
    transcriber: (
        DeepgramTranscriberConfig
        | SonioxTranscriberConfig
        | PhantomTranscriberConfig
        | None
    ) = Field(default=None, description="STT configuration", title="Transcriber")
    turn_detection: PipelineTurnDetection | None = None
    first_message: FirstMessageConfig | None = None
    interruption: InterruptionConfig | None = None
    timeout: TimeoutConfig | None = None
    call_duration: CallDurationConfig | None = None
    background_audio: BackgroundAudioConfig | None = None
    tts_text_transforms: list[TTSTextTransform] | None = Field(
        default=None, title="Tts Text Transforms"
    )
    preemptive_generation: bool | None = Field(
        default=None, title="Preemptive Generation"
    )
    min_consecutive_speech_delay: float | None = Field(
        default=None, title="Min Consecutive Speech Delay"
    )
    tools: ToolsConfig | None = Field(
        default=None, description="Tool and capability settings"
    )
    transfer: TransferConfig | None = Field(
        default=None, description="Call transfer settings"
    )
    analytics: AnalyticsConfig | None = Field(
        default=None, description="Analytics and monitoring settings"
    )
    expected_version: int | None = Field(
        default=None,
        description="If provided, the update will fail with 409 if the agent's current version does not match. Prevents concurrent overwrites.",
        title="Expected Version",
    )
    inbound_webhook_url: InboundWebhookUrl | None = Field(
        default=None,
        description="HTTPS URL invoked at call/message connect to fetch per-call dynamic_variables and (optional) prompt overrides. Empty/null disables the fetch. Phone-number-level URLs (when configured) take precedence for inbound voice — agent URL is the fallback.",
        title="Inbound Webhook Url",
    )
    inbound_webhook_secret: InboundWebhookSecret | None = Field(
        default=None,
        description="Shared secret used to sign every webhook request with HMAC-SHA256 in the X-Neuratel-Signature header. Optional — null means no signature is sent (acceptable for internal/dev endpoints only).",
        title="Inbound Webhook Secret",
    )
