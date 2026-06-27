# gateway 模块详细说明

本组件包含 65 个模块。

---

## __init__.py

**路径**: `gateway\__init__.py`
**行数**: 36

### 功能描述

Hermes Gateway - Multi-platform messaging integration.

This module provides a unified gateway for connecting the Hermes agent
to various messaging platforms (Telegram, Discord, WhatsApp, Weixin, and more) with:
- Session management (persistent conversations with reset policies)
- Dynamic context in

### 依赖关系

**依赖组件**: acp-adapter, cli
**跨组件调用**: 是

---

## authz_mixin.py

**路径**: `gateway\authz_mixin.py`
**行数**: 604

### 功能描述

User-authorization methods for ``GatewayRunner``.

Extracted from ``gateway/run.py`` as part of the god-file decomposition campaign
(``~/.hermes/plans/god-file-decomposition.md``, Phase 3 mechanical mixin lifts).
This mixin holds the inbound-message authorization cluster: whether a user/chat
is allo

### 核心类

- `GatewayAuthorizationMixin`: User/chat authorization methods for ``GatewayRunner``.

### 依赖关系

**依赖组件**: acp-adapter, cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `gateway\builtin_hooks\__init__.py`
**行数**: 2

### 功能描述

Built-in gateway hooks that are always registered.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## channel_directory.py

**路径**: `gateway\channel_directory.py`
**行数**: 424

### 功能描述

Channel directory -- cached map of reachable channels/contacts per platform.

Built on gateway startup, refreshed periodically (every 5 min), and saved to
~/.hermes/channel_directory.json.  The send_message tool reads this file for
action="list" and for resolving human-friendly channel names to nume

### 核心函数

- `load_directory()`: Load the cached channel directory from disk.
- `lookup_channel_type()`: Return the channel ``type`` string (e.g. ``"channel"``, ``"forum"``) for *chat_id*, or *None* if unk
- `resolve_channel_name()`: Resolve a human-friendly channel name to a numeric ID.

    Matching strategy (case-insensitive, fir
- `format_directory_for_display()`: Format the channel directory as a human-readable list for the model.

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## code_skew.py

**路径**: `gateway\code_skew.py`
**行数**: 65

### 功能描述

Detect when the gateway is running stale code after a hot ``git pull``.

The gateway is a single long-lived process; its ``sys.modules`` is frozen at
boot. If the checkout is updated underneath it (a manual ``git pull``, or the
window before ``hermes update``'s graceful restart fires), a first-time 

### 核心函数

- `record_boot_fingerprint()`: Snapshot the checkout revision at gateway startup (idempotent).
- `detect_code_skew()`: Return ``(boot_rev, disk_rev)`` short labels if the checkout drifted
    since boot, else ``None``.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## config.py

**路径**: `gateway\config.py`
**行数**: 2068

### 功能描述

Gateway configuration management.

Handles loading and validating configuration for:
- Connected platforms (Telegram, Discord, WhatsApp, Weixin, and more)
- Home channels for each platform
- Session reset policies
- Delivery preferences

### 核心类

- `Platform`: Supported messaging platforms.

    Built-in platforms have explicit members.  Plugin platforms use 
- `HomeChannel`: Default destination for a platform.
    
    When a cron job specifies deliver="telegram" without a 
- `SessionResetPolicy`: Controls when sessions reset (lose context).
    
    Modes:
    - "daily": Reset at a specific hour
- `PlatformConfig`: Configuration for a single messaging platform.
- `StreamingConfig`: Configuration for real-time token streaming to messaging platforms.
- `GatewayConfig`: Main gateway configuration.
    
    Manages all platform connections, session policies, and deliver

### 核心函数

- `load_gateway_config()`: Load gateway configuration from multiple sources.

    Priority (highest to lowest):
    1. Environm

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points
**跨组件调用**: 是

---

## delivery.py

**路径**: `gateway\delivery.py`
**行数**: 479

### 功能描述

Delivery routing for cron job outputs and agent responses.

Routes messages to the appropriate destination based on:
- Explicit targets (e.g., "telegram:123456789")
- Platform home channels (e.g., "telegram" → home channel)
- Origin (back to where the job was created)
- Local (always saved to files)

### 核心类

- `DeliveryTarget`: A single delivery target.
    
    Represents where a message should be sent:
    - "origin" → back 
- `DeliveryRouter`: Routes messages to appropriate destinations.
    
    Handles the logic of resolving delivery target

### 依赖关系

**依赖组件**: acp-adapter, cli
**跨组件调用**: 是

---

## display_config.py

**路径**: `gateway\display_config.py`
**行数**: 263

### 功能描述

Per-platform display/verbosity configuration resolver.

Provides ``resolve_display_setting()`` — the single entry-point for reading
display settings with platform-specific overrides and sensible defaults.

Resolution order (first non-None wins):
    1. ``display.platforms.<platform>.<key>``  — expli

### 核心函数

- `resolve_display_setting()`: Resolve a display setting with per-platform override support.

    Parameters
    ----------
    use

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## drain_control.py

**路径**: `gateway\drain_control.py`
**行数**: 234

### 功能描述

External drain-control marker contract (dashboard → gateway).

Task 2.2 of the safe-shutdown plan (decisions.md Q-B, option A): the dashboard
has no way to call into a running gateway — there is no HTTP control channel
into the gateway process (guardrails: "there is NO external control channel
into 

### 核心函数

- `current_instantiation_epoch()`: Identity of THIS container / VM instantiation.

    Stable for the life of the PID-1 init process — 
- `drain_request_path()`: Absolute path to the drain-request marker, respecting HERMES_HOME.
- `write_drain_request()`: Write the begin-drain marker. Returns the payload written.

    Atomic write so the gateway watcher 
- `clear_drain_request()`: Remove the drain marker (cancel-drain). Returns True if one existed.

    Best-effort: a missing fil
- `drain_requested()`: True iff a begin-drain marker for THIS instantiation is present.

    A marker whose ``epoch`` does 
- `read_drain_request()`: Return the marker payload, or ``None`` if absent.

    A present-but-unparseable marker returns ``{}

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## hooks.py

**路径**: `gateway\hooks.py`
**行数**: 228

### 功能描述

Event Hook System

A lightweight event-driven system that fires handlers at key lifecycle points.
Hooks are discovered from ~/.hermes/hooks/ directories, each containing:
  - HOOK.yaml  (metadata: name, description, events list)
  - handler.py (Python handler with async def handle(event_type, contex

### 核心类

- `HookRegistry`: Discovers, loads, and fires event hooks.

    Usage:
        registry = HookRegistry()
        regis

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## kanban_watchers.py

**路径**: `gateway\kanban_watchers.py`
**行数**: 1186

### 功能描述

Kanban board watcher methods for GatewayRunner.

Extracted verbatim from ``gateway/run.py`` (god-file decomposition Phase 3).
These are the background-loop methods that subscribe to kanban boards, deliver
notifications/artifacts, and drive the multi-agent dispatcher. They use only
``self`` state, so

### 核心类

- `GatewayKanbanWatchersMixin`: Kanban watcher / notifier / dispatcher loops for GatewayRunner.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## memory_monitor.py

**路径**: `gateway\memory_monitor.py`
**行数**: 231

### 功能描述

Periodic process memory usage logging for the gateway.

Ported from cline/cline#10343 (src/standalone/memory-monitor.ts).

The gateway is a long-lived process that accumulates memory as it caches
agent instances, session transcripts, tool schemas, memory providers, MCP
connections, etc.  A slow leak

### 核心函数

- `log_memory_usage()`: Log current memory usage in a grep-friendly ``[MEMORY] ...`` line.

    Safe to call on-demand from 
- `start_memory_monitoring()`: Start periodic memory usage logging in a daemon thread.

    Logs immediately to capture a baseline,
- `stop_memory_monitoring()`: Stop the monitor thread and log a final snapshot.

    Safe to call even if ``start_memory_monitorin
- `is_running()`: True if the background monitor thread is alive.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## message_timestamps.py

**路径**: `gateway\message_timestamps.py`
**行数**: 167

### 功能描述

Helpers for rendering gateway message timestamps exactly once.

Gateway messages need timestamps in the LLM context for temporal awareness, but
persisted message content should stay clean so replay does not accumulate
``[timestamp] [timestamp] ...`` prefixes across turns.

### 核心函数

- `coerce_message_timestamp()`: Coerce a timestamp-like value to Unix epoch seconds.

    Accepts Unix epoch numbers, datetime objec
- `format_message_timestamp()`: Format a timestamp value as ``[Tue 2026-04-28 13:40:53 CEST]``.
- `strip_leading_message_timestamps()`: Strip one or more leading gateway timestamp prefixes from ``content``.

    Returns ``(clean_content
- `render_user_content_with_timestamp()`: Render a user message for LLM context with exactly one timestamp prefix.

    Existing leading times

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## mirror.py

**路径**: `gateway\mirror.py`
**行数**: 185

### 功能描述

Session mirroring for cross-platform message delivery.

When a message is sent to a platform (via send_message or cron delivery),
this module appends a "delivery-mirror" record to the target session's
transcript so the receiving-side agent has context about what was sent.

Standalone -- works from C

### 核心函数

- `mirror_to_session()`: Append a delivery-mirror message to the target session's transcript.

    Finds the gateway session 

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## pairing.py

**路径**: `gateway\pairing.py`
**行数**: 451

### 功能描述

DM Pairing System

Code-based approval flow for authorizing new users on messaging platforms.
Instead of static allowlists with user IDs, unknown users receive a one-time
pairing code that the bot owner approves via the CLI.

Security features (based on OWASP + NIST SP 800-63-4 guidance):
  - 8-char

### 核心类

- `PairingStore`: Manages pairing codes and approved user lists.

    Data files per platform:
      - {platform}-pend

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## platform_registry.py

**路径**: `gateway\platform_registry.py`
**行数**: 261

### 功能描述

Platform Adapter Registry

Allows platform adapters (built-in and plugin) to self-register so the gateway
can discover and instantiate them without hardcoded if/elif chains.

Built-in adapters continue to use the existing if/elif in _create_adapter()
for now.  Plugin adapters register here via Plugi

### 核心类

- `PlatformEntry`: Metadata and factory for a single platform adapter.
- `PlatformRegistry`: Central registry of platform adapters.

    Thread-safe for reads (dict lookups are atomic under GIL

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `gateway\platforms\__init__.py`
**行数**: 46

### 功能描述

Platform adapters for messaging integrations.

Each adapter handles:
- Receiving messages from a platform
- Sending messages/responses back
- Platform-specific authentication
- Message formatting and media handling

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## _http_client_limits.py

**路径**: `gateway\platforms\_http_client_limits.py`
**行数**: 85

### 功能描述

Shared HTTP client factory for long-lived platform adapters.

Gateway messaging platforms (QQ Bot, Feishu, WeCom, DingTalk, Signal,
BlueBubbles, WeCom-callback) keep a persistent ``httpx.AsyncClient``
alive for the adapter's lifetime.  That amortises TLS/connection setup
across many API calls, but i

### 核心函数

- `platform_httpx_limits()`: Return ``httpx.Limits`` tuned for persistent platform-adapter clients.

    Returns ``None`` when ht

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## api_server.py

**路径**: `gateway\platforms\api_server.py`
**行数**: 4577

### 功能描述

OpenAI-compatible API server platform adapter.

Exposes an HTTP server with endpoints:
- POST /v1/chat/completions        — OpenAI Chat Completions format (stateless; opt-in session continuity via X-Hermes-Session-Id header; opt-in long-term memory scoping via X-Hermes-Session-Key header)
- POST /v1

### 核心类

- `ResponseStore`: SQLite-backed LRU store for Responses API state.

    Each stored response includes the full interna
- `_IdempotencyCache`: In-memory idempotency cache with TTL and basic LRU semantics.
- `APIServerAdapter`: OpenAI-compatible HTTP API server adapter.

    Runs an aiohttp web server that accepts OpenAI-forma

### 核心函数

- `check_api_server_requirements()`: Check if API server dependencies are available.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, cron, entry-points, llm-client, plugin-system, state-management, tool-system
**跨组件调用**: 是

---

## base.py

**路径**: `gateway\platforms\base.py`
**行数**: 5311

### 功能描述

Base platform adapter interface.

All platform adapters (Telegram, Discord, WhatsApp, Weixin, and more) inherit from this
and implement the required methods.

### 核心类

- `CachedMedia`: Result of caching one attachment's bytes.
- `MessageType`: Types of incoming messages.
- `ProcessingOutcome`: Result classification for message-processing lifecycle hooks.
- `MessageEvent`: Incoming message from a platform.
    
    Normalized representation that all adapters produce.
- `TextDebounceState`
- `SendResult`: Result of sending a message.
- `EphemeralReply`: System-notice reply that auto-deletes after a TTL.

    Slash-command handlers in ``gateway/run.py``
- `BasePlatformAdapter`: Base class for platform adapters.
    
    Subclasses implement platform-specific logic for:
    - C

### 核心函数

- `should_send_media_as_audio()`: Return True when a media file should use the platform's audio sender.

    Other platforms: every re
- `utf16_len()`: Count UTF-16 code units in *s*.

    Telegram's message-length limit (4 096) is measured in UTF-16 c
- `is_network_accessible()`: Return True if *host* would expose the server beyond loopback.

    Loopback addresses (127.0.0.1, :
- `should_bypass_proxy()`: Return True when NO_PROXY/no_proxy matches at least one target host.

    Supports exact hosts, doma
- `resolve_proxy_url()`: Return a proxy URL from env vars, or macOS system proxy.

    Check order:
      0. *platform_env_va
- `proxy_kwargs_for_bot()`: Build kwargs for ``commands.Bot()`` / ``discord.Client()`` with proxy.

    Returns:
      - SOCKS U
- `proxy_kwargs_for_aiohttp()`: Build kwargs for standalone ``aiohttp.ClientSession`` with proxy.

    Returns ``(session_kwargs, re
- `is_host_excluded_by_no_proxy()`: Return True when ``hostname`` matches a ``NO_PROXY`` entry.

    Supports comma- or whitespace-separ
- `safe_url_for_log()`: Return a URL string safe for logs (no query/fragment/userinfo).
- `get_inbound_media_max_bytes()`: Return the max inbound image/audio/video bytes allowed in memory.

    Reads ``gateway.max_inbound_m
- `validate_inbound_media_size()`: Raise ``ValueError`` if an inbound media payload exceeds the cap.

    A ``max_bytes`` of ``0`` (or 
- `get_image_cache_dir()`: Return the image cache directory, creating it if it doesn't exist.
- `cache_image_from_bytes()`: Save raw image bytes to the cache and return the absolute file path.

    Args:
        data: Raw im
- `cleanup_image_cache()`: Delete cached images older than *max_age_hours*.

    Returns the number of files removed.
- `get_audio_cache_dir()`: Return the audio cache directory, creating it if it doesn't exist.
- ... 还有 13 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## bluebubbles.py

**路径**: `gateway\platforms\bluebubbles.py`
**行数**: 1040

### 功能描述

BlueBubbles iMessage platform adapter.

Uses the local BlueBubbles macOS server for outbound REST sends and inbound
webhooks.  Supports text messaging, media attachments (images, voice, video,
documents), tapback reactions, typing indicators, and read receipts.

Architecture based on PR #5869 (benja

### 核心类

- `BlueBubblesAdapter`

### 核心函数

- `check_bluebubbles_requirements()`

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## helpers.py

**路径**: `gateway\platforms\helpers.py`
**行数**: 279

### 功能描述

Shared helper classes for gateway platform adapters.

Extracts common patterns that were duplicated across 5-7 adapters:
message deduplication, text batch aggregation, markdown stripping,
and thread participation tracking.

### 核心类

- `MessageDeduplicator`: TTL-based message deduplication cache.

    Replaces the identical ``_seen_messages`` / ``_is_duplic
- `TextBatchAggregator`: Aggregates rapid-fire text events into single messages.

    Replaces the ``_enqueue_text_event`` / 
- `ThreadParticipationTracker`: Persistent tracking of threads the bot has participated in.

    Replaces the identical ``_load/_sav

### 核心函数

- `strip_markdown()`: Strip markdown formatting for plain-text platforms (SMS, iMessage, etc.).

    Replaces the identica
- `redact_phone()`: Redact a phone number for logging, preserving country code and last 4.

    Replaces the identical `

### 依赖关系

**依赖组件**: entry-points, llm-client, state-management
**跨组件调用**: 是

---

## msgraph_webhook.py

**路径**: `gateway\platforms\msgraph_webhook.py`
**行数**: 422

### 功能描述

Microsoft Graph webhook adapter for change-notification ingress.

### 核心类

- `MSGraphWebhookAdapter`: Receive Microsoft Graph change notifications and surface them internally.

### 核心函数

- `check_msgraph_webhook_requirements()`: Return whether required webhook dependencies are available.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `gateway\platforms\qqbot\__init__.py`
**行数**: 92

### 功能描述

QQBot platform package.

Re-exports the main adapter symbols from ``adapter.py`` (the original
``qqbot.py``) so that **all existing import paths remain unchanged**::

    from gateway.platforms.qqbot import QQAdapter          # works
    from gateway.platforms.qqbot import check_qq_requirements  # w

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## adapter.py

**路径**: `gateway\platforms\qqbot\adapter.py`
**行数**: 3197

### 功能描述

QQ Bot platform adapter using the Official QQ Bot API (v2).

Connects to the QQ Bot WebSocket Gateway for inbound events and uses the
REST API (``api.sgroup.qq.com``) for outbound messages and media uploads.

Configuration in config.yaml:
    platforms:
      qq:
        enabled: true
        extra:

### 核心类

- `QQCloseError`: Raised when QQ WebSocket closes with a specific code.

    Carries the close code and reason for pro
- `QQAdapter`: QQ Bot adapter backed by the official QQ Bot WebSocket Gateway + REST API.

### 核心函数

- `check_qq_requirements()`: Check if QQ runtime dependencies are available.

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## chunked_upload.py

**路径**: `gateway\platforms\qqbot\chunked_upload.py`
**行数**: 603

### 功能描述

QQ Bot chunked upload flow.

The QQ v2 API caps inline base64 uploads (``file_data`` / ``url``) at ~10 MB.
For files between 10 MB and ~100 MB we have to use the three-step chunked
upload flow::

    1. POST /v2/{users|groups}/{id}/upload_prepare
       → returns upload_id, block_size, and an array 

### 核心类

- `UploadDailyLimitExceededError`: Raised when ``upload_prepare`` returns biz_code 40093002.

    The daily cumulative upload quota for
- `UploadFileTooLargeError`: Raised when a file exceeds the platform per-file size limit.
- `_UploadProgress`
- `_PreparePart`
- `_PrepareResult`
- `ChunkedUploader`: Run the prepare → PUT parts → complete sequence.

    :param api_request: Bound ``_api_request(metho

### 核心函数

- `format_size()`: Return a human-readable file size string (e.g. ``'12.3 MB'``).

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## constants.py

**路径**: `gateway\platforms\qqbot\constants.py`
**行数**: 75

### 功能描述

QQBot package-level constants shared across adapter, onboard, and other modules.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## crypto.py

**路径**: `gateway\platforms\qqbot\crypto.py`
**行数**: 46

### 功能描述

AES-256-GCM utilities for QQBot scan-to-configure credential decryption.

### 核心函数

- `generate_bind_key()`: Generate a 256-bit random AES key and return it as base64.

    The key is passed to ``create_bind_t
- `decrypt_secret()`: Decrypt a base64-encoded AES-256-GCM ciphertext.

    Ciphertext layout (after base64-decoding)::

 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## keyboards.py

**路径**: `gateway\platforms\qqbot\keyboards.py`
**行数**: 474

### 功能描述

QQ Bot inline keyboards + approval / update-prompt senders.

QQ Bot v2 supports attaching inline keyboards to outbound messages. When a
user clicks a button, the platform dispatches an ``INTERACTION_CREATE``
gateway event containing the button's ``data`` payload. The bot must ACK the
interaction pro

### 核心类

- `KeyboardButtonPermission`: Button permission metadata. ``type=2`` means all users can click.
- `KeyboardButtonAction`: What happens when the button is clicked.

    :param type: ``1`` (Callback — triggers ``INTERACTION_
- `KeyboardButtonRenderData`: Visual rendering of a button.

    :param label: Pre-click label.
    :param visited_label: Post-cli
- `KeyboardButton`: One button in a keyboard.

    :param group_id: Buttons sharing a ``group_id`` are mutually exclusiv
- `KeyboardRow`
- `KeyboardContent`
- `InlineKeyboard`: Top-level keyboard payload — goes into ``MessageToCreate.keyboard``.
- `ApprovalRequest`: Structured approval-request display data.

    :param session_key: Routes the decision back to the w
- `ApprovalSender`: Send an approval-request message with an inline keyboard.

    Decoupled from the adapter via callab
- `InteractionEvent`: Parsed ``INTERACTION_CREATE`` event payload.

    See https://bot.q.qq.com/wiki/develop/api-v2/dev-p

### 核心函数

- `parse_approval_button_data()`: Parse approval ``button_data`` into ``(session_key, decision)``.

    :param button_data: Raw ``data
- `parse_update_prompt_button_data()`: Parse update-prompt ``button_data`` into ``'y'`` or ``'n'``.
- `build_approval_keyboard()`: Build the 3-button approval keyboard.

    Layout: ``[✅ 允许一次] [⭐ 始终允许] [❌ 拒绝]`` — all three share
  
- `build_update_prompt_keyboard()`: Build a Yes/No keyboard for update confirmation prompts.
- `build_approval_text()`: Render an :class:`ApprovalRequest` into the message body (markdown).
- `parse_interaction_event()`: Parse a raw ``INTERACTION_CREATE`` dispatch payload (``d``).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## onboard.py

**路径**: `gateway\platforms\qqbot\onboard.py`
**行数**: 221

### 功能描述

QQBot scan-to-configure (QR code onboard) module.

Mirrors the Feishu onboarding pattern: synchronous HTTP + a single public
entry-point ``qr_register()`` that handles the full flow (create task →
display QR code → poll → decrypt credentials).

Calls the ``q.qq.com`` ``create_bind_task`` / ``poll_bi

### 核心类

- `BindStatus`: Status codes returned by ``_poll_bind_result``.

### 核心函数

- `build_connect_url()`: Build the QR-code target URL for a given *task_id*.
- `qr_register()`: Run the QQBot scan-to-configure QR registration flow.

    Mirrors ``feishu.qr_register()``: handles

### 依赖关系

**依赖组件**: agent-engine, entry-points
**跨组件调用**: 是

---

## utils.py

**路径**: `gateway\platforms\qqbot\utils.py`
**行数**: 72

### 功能描述

QQBot shared utilities — User-Agent, HTTP helpers, config coercion.

### 核心函数

- `build_user_agent()`: Build a descriptive User-Agent string.

    Format::

        QQBotAdapter/<qqbot_version> (Python/<
- `get_api_headers()`: Return standard HTTP headers for QQBot API requests.

    Includes ``Content-Type``, ``Accept``, and
- `coerce_list()`: Coerce config values into a trimmed string list.

    Accepts comma-separated strings, lists, tuples

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## signal.py

**路径**: `gateway\platforms\signal.py`
**行数**: 1702

### 功能描述

Signal messenger platform adapter.

Connects to a signal-cli daemon running in HTTP mode.
Inbound messages arrive via SSE (Server-Sent Events) streaming.
Outbound messages and actions use JSON-RPC 2.0 over HTTP.

Based on PR #268 by ibhagwan, rebuilt with bug fixes.

Requires:
  - signal-cli install

### 核心类

- `SignalAdapter`: Signal messenger adapter using signal-cli HTTP daemon.

### 核心函数

- `check_signal_requirements()`: Check if Signal is configured (has URL and account).

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## signal_format.py

**路径**: `gateway\platforms\signal_format.py`
**行数**: 141

### 功能描述

Shared Signal formatting helpers.

Keep markdown → Signal native formatting conversion in one place so both the
live Signal adapter and standalone send paths emit the same bodyRanges.

### 核心函数

- `markdown_to_signal()`: Convert markdown to plain text + Signal textStyles list.

    Signal doesn't render markdown. Instea

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## signal_rate_limit.py

**路径**: `gateway\platforms\signal_rate_limit.py`
**行数**: 370

### 功能描述

Signal attachment rate-limit scheduler.

Process-wide token-bucket simulator that mirrors the per-account
attachment rate limit signal-cli/Signal-Server enforce. Producers
(``SignalAdapter.send_multiple_images`` and the ``send_message`` tool's
Signal path) call ``acquire(n)`` before an attachment se

### 核心类

- `SignalRateLimitError`: Raised by ``SignalAdapter._rpc`` for rate-limit responses when the
    caller has opted in via ``rai
- `SignalSchedulerError`
- `SignalAttachmentScheduler`: Process-wide token-bucket simulator for Signal attachment sends.

    The bucket holds up to ``capac

### 核心函数

- `get_scheduler()`: Return the process-wide scheduler, creating it on first access.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## webhook.py

**路径**: `gateway\platforms\webhook.py`
**行数**: 1023

### 功能描述

Generic webhook platform adapter.

Runs an aiohttp HTTP server that receives webhook POSTs from external
services (GitHub, GitLab, JIRA, Stripe, etc.), validates HMAC signatures,
transforms payloads into agent prompts, and routes responses back to the
source or to another configured platform.

Confi

### 核心类

- `WebhookAdapter`: Generic webhook receiver that triggers agent runs from HTTP POSTs.

### 核心函数

- `check_webhook_requirements()`: Check if webhook adapter dependencies are available.

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client, state-management
**跨组件调用**: 是

---

## weixin.py

**路径**: `gateway\platforms\weixin.py`
**行数**: 2360

### 功能描述

Weixin platform adapter.

Connects Hermes Agent to WeChat personal accounts via Tencent's iLink Bot API.

Design notes:
- Long-poll ``getupdates`` drives inbound delivery.
- Every outbound reply must echo the latest ``context_token`` for the peer.
- Media files move through an AES-128-ECB encrypted 

### 核心类

- `ContextTokenStore`: Disk-backed ``context_token`` cache keyed by account + peer.
- `TypingTicketCache`: Short-lived typing ticket cache from ``getconfig``.
- `WeixinAdapter`: Native Hermes adapter for Weixin personal accounts.

### 核心函数

- `check_weixin_requirements()`: Return True when runtime dependencies for Weixin are available.
- `save_weixin_account()`: Persist account credentials for later reuse.
- `load_weixin_account()`: Load persisted account credentials.

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## whatsapp_cloud.py

**路径**: `gateway\platforms\whatsapp_cloud.py`
**行数**: 1993

### 功能描述

WhatsApp Cloud API adapter — official Meta WhatsApp Business Platform.

This adapter is a *complement* to ``whatsapp.py`` (the Baileys bridge), not
a replacement. The two are independent:

- ``whatsapp.py``      — unofficial Baileys bridge, personal accounts, no
                         public URL n

### 核心类

- `WhatsAppCloudAdapter`: WhatsApp Business Cloud API adapter.

    Outbound: HTTPS POST to ``graph.facebook.com/<api_version>

### 核心函数

- `check_whatsapp_cloud_requirements()`: Return whether transport dependencies are available.

    aiohttp is needed for the webhook server (

### 依赖关系

**依赖组件**: acp-adapter, cli, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## whatsapp_common.py

**路径**: `gateway\platforms\whatsapp_common.py`
**行数**: 421

### 功能描述

Transport-agnostic WhatsApp behavior shared by the Baileys bridge adapter
and the official WhatsApp Cloud API adapter.

The mixin provides:
- Allow-list / DM / group gating
- Mention detection (explicit @-mentions + configurable regex patterns)
- Quoted-reply-to-bot detection
- Broadcast / Channel /

### 核心类

- `WhatsAppBehaviorMixin`: Shared behavior for all WhatsApp adapters (Baileys + Cloud API).

    See module docstring for the a

### 核心函数

- `resolve_whatsapp_bridge_dir()`: Resolve the WhatsApp bridge directory, mirroring to HERMES_HOME if needed.

    When the install tre

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## yuanbao.py

**路径**: `gateway\platforms\yuanbao.py`
**行数**: 5360

### 功能描述

Yuanbao platform adapter.

Connects to the Yuanbao WebSocket gateway, handles authentication (AUTH_BIND),
heartbeat, reconnection, message receive (T05) and send (T06).

Configuration in config.yaml (or via env vars):
    platforms:
      yuanbao:
        extra:
          app_id: "..."              

### 核心类

- `MarkdownProcessor`: Encapsulates all Markdown-related utilities for the Yuanbao platform.

    Provides static methods f
- `SignManager`: Encapsulates all sign-token related logic for the Yuanbao platform.

    Manages token acquisition, 
- `InboundContext`: Mutable context flowing through the inbound middleware pipeline.

    Each middleware reads/writes f
- `InboundMiddleware`: Abstract base class for all inbound pipeline middlewares.

    Subclasses must:
      - Set ``name``
- `InboundPipeline`: Onion-model middleware pipeline engine for inbound message processing.

    Inspired by OpenClaw's M
- `DecodeMiddleware`: Decode raw inbound frames from JSON or Protobuf into ctx.push.

    Encapsulates JSON push parsing (
- `ExtractFieldsMiddleware`: Extract common fields from ctx.push into ctx attributes.
- `DedupMiddleware`: Inbound message deduplication.
- `RecallGuardMiddleware`: Intercept Group.CallbackAfterRecallMsg / C2C.CallbackAfterMsgWithDraw.

    Branch A: message in tra
- `SkipSelfMiddleware`: Filter out bot's own messages.
- ... 还有 31 个类

### 核心函数

- `get_active_adapter()`: Delegate to ``YuanbaoAdapter.get_active()``.

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, llm-client, state-management
**跨组件调用**: 是

---

## yuanbao_media.py

**路径**: `gateway\platforms\yuanbao_media.py`
**行数**: 646

### 功能描述

yuanbao_media.py — 元宝平台媒体处理模块

提供 COS 上传、文件下载、TIM 媒体消息构建等功能。
移植自 TypeScript 版 media.ts（yuanbao-openclaw-plugin），
使用 httpx 替代 cos-nodejs-sdk-v5，避免引入额外 SDK 依赖。

COS 上传流程：
  1. 调用 genUploadInfo 获取临时凭证（tmpSecretId/tmpSecretKey/sessionToken）
  2. 用临时凭证通过 HMAC-SHA1 签名构建 Authorization 头
  3. HTTP PUT 上传到 C

### 核心函数

- `guess_mime_type()`: 根据文件扩展名猜测 MIME 类型。
- `is_image()`: 判断是否为图片类型。
- `get_image_format()`: 获取 TIM 图片格式编号。
- `md5_hex()`: 计算 MD5 十六进制摘要。
- `generate_file_id()`: 生成随机文件 ID（32 位 hex）。
- `parse_image_size()`: 解析图片宽高（支持 JPEG/PNG/GIF/WebP），无需第三方依赖。
    返回 {"width": w, "height": h} 或 None（无法识别）。
- `build_image_msg_body()`: 构建腾讯 IM TIMImageElem 消息体。
    参考：https://cloud.tencent.com/document/product/269/2720

    Args:
    
- `build_file_msg_body()`: 构建腾讯 IM TIMFileElem 消息体。
    参考：https://cloud.tencent.com/document/product/269/2720

    Args:
     

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## yuanbao_proto.py

**路径**: `gateway\platforms\yuanbao_proto.py`
**行数**: 1419

### 功能描述

yuanbao_proto.py - Yuanbao WebSocket 协议编解码（纯 Python 实现）

协议层级：
  WebSocket frame
    └── ConnMsg (protobuf: trpc.yuanbao.conn_common.ConnMsg)
          ├── head: Head  (cmd_type, cmd, seq_no, msg_id, module, ...)
          └── data: bytes  (业务 payload，标准 protobuf)
                └── InboundMessageP

### 核心函数

- `next_seq_no()`: 生成递增序列号（线程安全，溢出时归零）
- `encode_conn_msg()`: 编码 ConnMsg（简化接口，对应任务要求的签名）。

    Args:
        msg_type: cmd_type（CMD_TYPE 枚举值）
        seq_no:   序列
- `decode_conn_msg()`: 解码 ConnMsg，返回 {msg_type, seq_no, data, head}。

    Returns:
        {
          "msg_type": int,    
- `encode_conn_msg_full()`: 编码完整的 ConnMsg（含 cmd/msg_id/module 等 head 字段）。
    比 encode_conn_msg 提供更多 head 控制。
- `encode_biz_msg()`: 将业务 payload 包装为 ConnMsg bytes。

    Args:
        service: 模块名（head.module），如 "yuanbao_openclaw_prox
- `decode_biz_msg()`: 解码 ConnMsg bytes，返回业务层信息。

    Returns:
        {
          "service":     str,    # head.module
   
- `decode_inbound_push()`: 解析入站消息推送的 biz payload（InboundMessagePush proto bytes）。

    Args:
        data: ConnMsg.data 字段的 byt
- `decode_forward_msg_data()`: Parse ForwardMsgData protobuf bytes (the base64-decoded ext_map value).

    Args:
        data: For
- `encode_forward_msg_data()`: Encode ForwardMsgData protobuf bytes (inverse of ``decode_forward_msg_data``).

    Mainly used to b
- `encode_send_c2c_message()`: Encode a C2C send-message request and return the full ConnMsg bytes
    (ready to be sent over WebSo
- `encode_send_group_message()`: Encode a group send-message request and return the full ConnMsg bytes
    (ready to be sent over Web
- `encode_auth_bind()`: 构造 auth-bind 请求 ConnMsg bytes。

    AuthBindReq fields:
      1: biz_id (string)
      2: auth_info 
- `encode_ping()`: 构造 ping 请求 ConnMsg bytes（PingReq 为空消息）
- `encode_push_ack()`: 构造 push ACK 回包
- `encode_send_private_heartbeat()`: 编码 SendPrivateHeartbeatReq，返回完整 ConnMsg bytes。

    SendPrivateHeartbeatReq fields:
      1: from_ac
- ... 还有 5 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## yuanbao_sticker.py

**路径**: `gateway\platforms\yuanbao_sticker.py`
**行数**: 559

### 功能描述

Yuanbao sticker (TIMFaceElem) support.

Ported from yuanbao-openclaw-plugin/src/sticker/.

TIMFaceElem wire format:
    {
        "msg_type": "TIMFaceElem",
        "msg_content": {
            "index": 0,          # always 0 per Yuanbao convention
            "data": "<json>",    # serialised stick

### 核心函数

- `get_sticker_by_name()`: 按名称查找贴纸，支持模糊匹配。

    匹配优先级：
      1. 完全相等（name）
      2. name 包含查询词（前缀/子串）
      3. description 包含查询
- `get_random_sticker()`: 随机返回一个贴纸。

    若指定 category，则在 description 中含有该关键词的贴纸里随机选取；
    category 为 None 时从全表随机。
- `get_sticker_by_id()`: 按 sticker_id 精确查找贴纸。
- `search_stickers()`: 在内置贴纸表中按模糊匹配排序返回前 N 条结果。

    评分综合 name/description 字段的子串、字符多重集覆盖、bigram Jaccard、子序列比例。
    name 权重略
- `build_face_msg_body()`: 构造 TIMFaceElem 消息体。

    Yuanbao 约定：
      - index 固定传 0（服务端通过 data 字段识别具体表情）
      - data 为 JSON 字符
- `build_sticker_msg_body()`: 从 STICKER_MAP 中的 sticker dict 直接构造 TIMFaceElem 消息体。

    这是 send_sticker() 的内部辅助，确保 data 字段与原始 JS 插件

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `gateway\relay\__init__.py`
**行数**: 764

### 功能描述

Relay/connector support package for the Hermes gateway.

EXPERIMENTAL. This package implements the gateway side of the "Gateway Gateway"
relay design: a generic ``RelayAdapter`` plus the wire-serializable
``CapabilityDescriptor`` the connector hands it at handshake time, and the
production ``WebSock

### 核心函数

- `relay_url()`: The connector relay endpoint URL, or None when relay is not configured.

    Checks ``GATEWAY_RELAY_
- `relay_platform_identities()`: The (platform, bot_id) pairs this gateway fronts over the relay (Phase 1.5).

    Shape A (multi-pla
- `relay_bot_username()`: The bot's deep-link username/handle for a platform (e.g. Telegram's
    ``@handle`` for ``t.me/<hand
- `relay_platform_identity()`: The PRIMARY (platform, bot_id) — the first identity in the configured set.

    Kept for call sites 
- `relay_connection_auth()`: The (gateway_id, upgrade_secret) this gateway authenticates the WS upgrade with.

    Both come from
- `relay_endpoint()`: The gateway's own PUBLIC inbound URL, asserted to the connector at provision.

    The connector del
- `relay_route_keys()`: Discriminators (guild_ids / chat_ids / paths) this gateway's tenant owns.

    Gateway-provided conf
- `relay_instance_id()`: Stable per-instance id this gateway forwards at provision (Phase 6 Unit α).

    Binds the connector
- `relay_wake_url()`: The gateway's WAKE URL, forwarded at provision (Phase 5 §5.2 wake PRIMITIVE).

    A poke target the
- `relay_relevance_policy()`: Project a fronted platform's RELEVANCE config into the connector's generic vocabulary.

    The conn
- `self_provision_relay()`: Boot-time relay self-provision: mint relay creds in-process, no human, no disk.

    Fires when rela
- `send_relay_policy()`: Declare this gateway's relevance policy to the connector (Phase 6 Unit ζ).

    Runs at boot AFTER t
- `register_relay_adapter()`: Register the generic ``relay`` platform via the platform registry.

    Registers when a relay URL i

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## adapter.py

**路径**: `gateway\relay\adapter.py`
**行数**: 547

### 功能描述

RelayAdapter — one generic gateway adapter fronted by the connector. EXPERIMENTAL.

A single ``BasePlatformAdapter`` subclass that, at handshake, receives a
``CapabilityDescriptor`` from the connector telling it which platform it is
fronting and which capabilities to advertise to the ``GatewayStream

### 核心类

- `RelayAdapter`: Generic relay adapter advertising a connector-negotiated capability profile.

### 依赖关系

**依赖组件**: acp-adapter, cli, llm-client
**跨组件调用**: 是

---

## auth.py

**路径**: `gateway\relay\auth.py`
**行数**: 169

### 功能描述

Gateway-side relay authentication primitives. EXPERIMENTAL.

The connector⇄gateway channel is authenticated because a gateway may be
customer-managed and internet-exposed (see the connector repo
``docs/connector-gateway-auth-design.md``). This module is the **gateway half**
of two HMAC schemes whose

### 核心函数

- `sign()`: HMAC-SHA256 hex digest — the connector's ``sign`` (relayAuthToken.ts).
- `verify_signature()`: Constant-time check that ``sig_hex`` is a valid HMAC of ``payload`` under
    ANY of ``secrets`` (ro
- `make_token()`: Build a signed, optionally-expiring token — the connector's ``makeToken``.

    ``base64url(f"{paylo
- `make_upgrade_token()`: The WS-upgrade bearer token a gateway sends: ``payload = gateway_id``.

    The connector peeks ``ga
- `verify_token()`: Verify a token built by ``make_token``; return the payload or None.

    Splits from the right so a 
- `verify_delivery_signature()`: Verify a connector→gateway inbound delivery signature.

    ``body_json`` MUST be the exact request 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## descriptor.py

**路径**: `gateway\relay\descriptor.py`
**行数**: 119

### 功能描述

CapabilityDescriptor — the relay handshake payload. EXPERIMENTAL.

The connector hands a ``CapabilityDescriptor`` to the gateway's ``RelayAdapter``
at handshake time; it tells the adapter which platform it is fronting and which
capabilities to advertise to the ``GatewayStreamConsumer`` (char limit,


### 核心类

- `CapabilityDescriptor`: Immutable capability descriptor negotiated at relay handshake.

    Frozen so a descriptor cannot be

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## transport.py

**路径**: `gateway\relay\transport.py`
**行数**: 144

### 功能描述

Relay transport protocol — the gateway<->connector wire contract. EXPERIMENTAL.

The ``RelayAdapter`` (gateway side) delegates all wire I/O to a ``RelayTransport``.
The gateway dials OUT to the connector, so a production transport is a WebSocket
client; in tests it is an in-memory stub (``tests/gate

### 核心类

- `RelayTransport`: Full gateway<->connector transport contract.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## ws_transport.py

**路径**: `gateway\relay\ws_transport.py`
**行数**: 710

### 功能描述

Production WebSocket RelayTransport — the gateway's live link to the connector.

The gateway dials OUT to the connector's relay endpoint over a WebSocket and
speaks the newline-delimited JSON frame protocol defined in the connector repo
(``gateway-gateway`` ``src/relay/protocol.ts``) and mirrored in

### 核心类

- `PassthroughForward`: A connector-forwarded passthrough-plane request (Phase 5 §5.1).

    The connector answered the prov
- `WebSocketRelayTransport`: RelayTransport over a WebSocket connection the gateway dials to the connector.

### 依赖关系

**依赖组件**: acp-adapter, cli, llm-client
**跨组件调用**: 是

---

## response_filters.py

**路径**: `gateway\response_filters.py`
**行数**: 54

### 功能描述

Gateway response filtering helpers.

These helpers operate at the gateway boundary: they decide whether a completed
agent turn should be delivered to the chat, not what should be persisted in the
conversation history.

### 核心函数

- `is_intentional_silence_response()`: Return True only when ``response`` is exactly a silence marker.

    Substantive prose that merely m
- `is_intentional_silence_agent_result()`: Silence markers suppress delivery only for successful agent turns.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## restart.py

**路径**: `gateway\restart.py`
**行数**: 27

### 功能描述

Shared gateway restart constants and parsing helpers.

### 核心函数

- `parse_restart_drain_timeout()`: Parse a configured drain timeout, falling back to the shared default.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## rich_sent_store.py

**路径**: `gateway\rich_sent_store.py`
**行数**: 81

### 功能描述

Local index of text we've sent via ``sendRichMessage`` (Bot API 10.1).

Telegram does NOT echo a rich message's content back in ``reply_to_message``
when a user replies to it (verified: ``.text``/``.caption`` empty,
``.api_kwargs`` None). So replies to the launchd briefings / any rich send
arrive wi

### 核心函数

- `record()`: Persist ``text`` for ``(chat_id, message_id)``. No-op on any failure.
- `lookup()`: Return stored text for ``(chat_id, message_id)`` or ``None``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## run.py

**路径**: `gateway\run.py`
**行数**: 18520

### 功能描述

Gateway runner - entry point for messaging platform integrations.

This module provides:
- start_gateway(): Start all configured platform adapters
- GatewayRunner: Main class managing the gateway lifecycle

Usage:
    # Start the gateway
    python -m gateway.run
    
    # Or from CLI
    python cl

### 核心类

- `MultiplexConfigError`: A profile multiplexer config is invalid (fail-fast at startup).

    Distinct from a transient adapt
- `GatewayRunner`: Main gateway controller.

    Manages the lifecycle of all platform adapters and routes
    messages

### 核心函数

- `render_notice_line()`: Render an AgentNotice to a single plaintext line for messaging platforms.

    Messaging has no pers
- `main()`: CLI entry point for the gateway.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, cron, entry-points, llm-client, memory-system, plugin-system, security, state-management, tool-system
**跨组件调用**: 是

---

## runtime_footer.py

**路径**: `gateway\runtime_footer.py`
**行数**: 150

### 功能描述

Gateway runtime-metadata footer.

Renders a compact footer showing runtime state (model, context %, cwd) and
appends it to the FINAL message of an agent turn when enabled.  Off by default
to keep replies minimal.

Config (``~/.hermes/config.yaml``)::

    display:
      runtime_footer:
        enabl

### 核心函数

- `resolve_footer_config()`: Resolve effective runtime-footer config for *platform_key*.

    Merge order (later wins):
        1
- `format_runtime_footer()`: Render the footer line, or return "" if no fields have data.

    Fields are skipped silently when t
- `build_footer_line()`: Top-level entry point used by gateway/run.py.

    Returns the footer text (empty string when disabl

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## scale_to_zero.py

**路径**: `gateway\scale_to_zero.py`
**行数**: 125

### 功能描述

Scale-to-zero idle detection + dormant-quiesce for the gateway (Phase 0).

This is the gateway-side BEHAVIOUR layer that consumes the relay scale-to-zero
PRIMITIVES (gateway-gateway Phase 5: the buffered-flip, the durable per-instance
buffer, the wakeUrl poke, the reconnect supervisor). It owns the 

### 核心函数

- `scale_to_zero_enabled()`: Whether the per-instance Labs toggle is on (the HERMES_SCALE_TO_ZERO stamp).

    D11/Q8=A: this env
- `parse_idle_timeout_seconds()`: Coerce ``scale_to_zero.idle_timeout_minutes`` (config.yaml, D2) to seconds.

    Degrades to the def
- `messaging_is_relay_only_or_absent()`: True iff the only connected messaging platform is RELAY, or there is none
    (a Chronos-only / no-p
- `should_arm()`: Whether to start the idle watcher at all (D1/D11/§3.4(1)).

    ALL must hold: the Labs flag is on, 
- `is_idle()`: The idle predicate (D2/D3/F7). Pure — composes the three conjuncts.

    Idle iff: no in-flight agen

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## session.py

**路径**: `gateway\session.py`
**行数**: 1598

### 功能描述

Session management for the gateway.

Handles:
- Session context tracking (where messages come from)
- Session storage (conversations persisted to disk)
- Reset policy evaluation (when to start fresh)
- Dynamic system prompt injection (agent knows its context)

### 核心类

- `SessionSource`: Describes where a message originated from.
    
    This information is used to:
    1. Route respon
- `SessionContext`: Full context for a session, used for dynamic system prompt injection.
    
    The agent receives th
- `SessionEntry`: Entry in the session store.
    
    Maps a session key to its current session ID and metadata.
- `SessionStore`: Manages session storage and retrieval.
    
    Uses SQLite (via SessionDB) for session metadata and

### 核心函数

- `build_session_context_prompt()`: Build the dynamic system prompt section that tells the agent about its context.

    This is injecte
- `is_shared_multi_user_session()`: Return True when a non-DM session is shared across participants.

    Mirrors the isolation rules in
- `build_session_key()`: Build a deterministic session key from a message source.

    This is the single source of truth for
- `build_session_context()`: Build a full session context from a source and config.
    
    This is used to inject context into 

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## session_context.py

**路径**: `gateway\session_context.py`
**行数**: 255

### 功能描述

Session-scoped context variables for the Hermes gateway.

Replaces the previous ``os.environ``-based session state
(``HERMES_SESSION_PLATFORM``, ``HERMES_SESSION_CHAT_ID``, etc.) with
Python's ``contextvars.ContextVar``.

**Why this matters**

The gateway processes messages concurrently via ``asynci

### 核心函数

- `set_current_session_id()`: Synchronize ``HERMES_SESSION_ID`` across ContextVar and ``os.environ``.

    Long-lived single-proce
- `set_session_vars()`: Set all session context variables and return reset tokens.

    Call ``clear_session_vars(tokens)`` 
- `clear_session_vars()`: Mark session context variables as explicitly cleared.

    Sets all variables to ``""`` so that ``ge
- `get_session_env()`: Read a session context variable by its legacy ``HERMES_SESSION_*`` name.

    Drop-in replacement fo
- `async_delivery_supported()`: Whether the current session can deliver a background completion later.

    Returns ``False`` only w

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## shutdown_forensics.py

**路径**: `gateway\shutdown_forensics.py`
**行数**: 463

### 功能描述

Shutdown forensics — capture context when the gateway receives SIGTERM/SIGINT.

The gateway's ``shutdown_signal_handler`` runs synchronously inside the
asyncio event loop.  We can't safely block it for long, but we DO want a
durable record of who/what triggered the shutdown so that "the gateway
keep

### 核心函数

- `snapshot_shutdown_context()`: Fast (<10ms) snapshot of who/what is asking us to shut down.

    Captures:

    * The signal number
- `spawn_async_diagnostic()`: Fire-and-forget ``ps``-style snapshot written to ``log_path``.

    Runs as a detached subprocess so
- `format_context_for_log()`: Render a shutdown context dict as a single, scannable log line.
- `context_as_json()`: JSON-serialise a context dict for structured ingestion.  Never raises.
- `check_systemd_timing_alignment()`: At startup, sanity-check that systemd's TimeoutStopSec >= drain_timeout.

    When the gateway is ru

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## slash_access.py

**路径**: `gateway\slash_access.py`
**行数**: 230

### 功能描述

Per-platform slash command access control.

This module sits beside the existing per-platform allowlist (``allow_from``)
and adds a second axis: of the users who are *allowed to talk to the
gateway*, which ones can run *which slash commands*.

Two lists per platform scope (DM vs group, mirroring ``a

### 核心类

- `SlashAccessPolicy`: Resolved access policy for a single (platform, scope) pair.

    ``scope`` is ``"dm"`` for direct me

### 核心函数

- `policy_from_extra()`: Build a policy from a platform's ``extra`` dict for one scope.

    DM scope falls back to group sco
- `policy_for_source()`: Resolve the access policy for a SessionSource.

    Returns a "disabled" policy (gating off, allow e

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## slash_commands.py

**路径**: `gateway\slash_commands.py`
**行数**: 4108

### 功能描述

Gateway slash-command handlers for GatewayRunner.

Extracted from ``gateway/run.py`` (god-file decomposition Phase 3b). These are
the in-session slash commands (/model, /reset, /usage, /compress, ...) the
gateway dispatches from ``_handle_message``. There are 42 of them (~3,200 LOC);
lifting them in

### 核心类

- `GatewaySlashCommandsMixin`: In-session slash-command handlers for GatewayRunner.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, llm-client, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## status.py

**路径**: `gateway\status.py`
**行数**: 1373

### 功能描述

Gateway runtime status helpers.

Provides PID-file based detection of whether the gateway daemon is running,
used by send_message's check_fn to gate availability in the CLI.

The PID file lives at ``{HERMES_HOME}/gateway.pid``.  HERMES_HOME defaults to
``~/.hermes`` but can be overridden via the env

### 核心函数

- `terminate_pid()`: Terminate a PID with platform-appropriate force semantics.

    POSIX uses SIGTERM/SIGKILL. Windows 
- `get_process_start_time()`: Public wrapper for retrieving a process start time when available.
- `looks_like_gateway_command_line()`: Return True only for a real ``gateway run`` process command line.
- `looks_like_gateway_runtime_command_line()`: Return True for command lines that can host the gateway runtime.

    ``gateway restart`` is normall
- `acquire_gateway_runtime_lock()`: Claim the cross-process runtime lock for the gateway.

    Unlike the PID file, the lock is owned by
- `release_gateway_runtime_lock()`: Release the gateway runtime lock when owned by this process.
- `is_gateway_runtime_lock_active()`: Return True when some process currently owns the gateway runtime lock.
- `write_pid_file()`: Write the current process PID and metadata to the gateway PID file.

    Uses atomic O_CREAT | O_EXC
- `write_runtime_status()`: Persist gateway runtime health information for diagnostics/status.
- `read_runtime_status()`: Read the persisted gateway runtime health/status information.

    ``path`` is optional so callers t
- `parse_active_agents()`: Coerce a persisted ``active_agents`` value to a clamped non-negative int.

    The shared coercion f
- `derive_gateway_busy()`: Whether the gateway is actively processing in-flight turns.

    The contract NAS gates lifecycle ac
- `derive_gateway_drainable()`: Whether the gateway can accept a begin-drain request right now.

    True iff the gateway is live an
- `get_runtime_status_running_pid()`: Return a live gateway PID from the runtime status record, if valid.

    ``get_running_pid()`` is th
- `remove_pid_file()`: Remove the gateway PID file, but only if it belongs to this process.

    During --replace handoffs,
- ... 还有 12 个函数

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## sticker_cache.py

**路径**: `gateway\sticker_cache.py`
**行数**: 125

### 功能描述

Sticker description cache for Telegram.

When users send stickers, we describe them via the vision tool and cache
the descriptions keyed by file_unique_id so we don't re-analyze the same
sticker image on every send. Descriptions are concise (1-2 sentences).

Cache location: ~/.hermes/sticker_cache.j

### 核心函数

- `get_cached_description()`: Look up a cached sticker description.

    Returns:
        dict with keys {description, emoji, set_
- `cache_sticker_description()`: Store a sticker description in the cache.

    Args:
        file_unique_id: Telegram's stable stick
- `build_sticker_injection()`: Build the warm-style injection text for a sticker description.

    Returns a string like:
      [Th
- `build_animated_sticker_injection()`: Build injection text for animated/video stickers we can't analyze.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## stream_consumer.py

**路径**: `gateway\stream_consumer.py`
**行数**: 1652

### 功能描述

Gateway streaming consumer — bridges sync agent callbacks to async platform delivery.

The agent fires stream_delta_callback(text) synchronously from its worker thread.
GatewayStreamConsumer:
  1. Receives deltas via on_delta() (thread-safe, sync)
  2. Queues them to an asyncio task via queue.Queue


### 核心类

- `StreamConsumerConfig`: Runtime config for a single stream consumer instance.
- `GatewayStreamConsumer`: Async consumer that progressively edits a platform message with streamed tokens.

    Usage::

     

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## stream_dispatch.py

**路径**: `gateway\stream_dispatch.py`
**行数**: 133

### 功能描述

Adapter-driven dispatch of structured stream events to a delivery sink.

``GatewayEventDispatcher`` is the seam Tobi asked for: the agent emits typed
events (gateway/stream_events.py), and the *adapter* decides how each one is
delivered.  The dispatcher holds an adapter + the stream consumer (sink) 

### 核心类

- `GatewayEventDispatcher`: Route typed stream events through an adapter onto a delivery sink.

    Parameters
    ----------
  

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## stream_events.py

**路径**: `gateway\stream_events.py`
**行数**: 172

### 功能描述

Structured streaming events — the agent→gateway delivery contract.

Historically the agent drove gateway delivery through a fan of loosely-typed
callbacks (``stream_delta_callback(text)``, ``tool_progress_callback(event_type,
tool_name, preview, args)``, ``interim_assistant_callback(text)`` …) and e

### 核心类

- `MessageChunk`: A delta of streamed assistant text.

    ``text`` is the incremental content as it arrives from the 
- `MessageStop`: The current assistant message segment is complete.

    Emitted when a contiguous run of assistant t
- `Commentary`: A complete interim assistant message emitted between tool iterations.

    Example: the model says "
- `ToolCallChunk`: A tool invocation has started (or its in-progress state changed).

    Carries the raw facts about t
- `ToolCallFinished`: A tool invocation completed.

    ``duration`` is wall-clock seconds.  ``ok`` reflects whether the t
- `LongToolHint`: One-shot onboarding nudge when a tool runs longer than the threshold.

    The gateway gates this on
- `GatewayNotice`: A gateway-originated control message (restart, online, long-run notice).

    ``kind`` is a stable s

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## whatsapp_identity.py

**路径**: `gateway\whatsapp_identity.py`
**行数**: 207

### 功能描述

Shared helpers for canonicalising WhatsApp sender identity.

WhatsApp's bridge can surface the same human under two different JID shapes
within a single conversation:

- LID form: ``999999999999999@lid``
- Phone form: ``15551234567@s.whatsapp.net``

Both the authorisation path (:mod:`gateway.run`) a

### 核心函数

- `normalize_whatsapp_identifier()`: Strip WhatsApp JID/LID syntax down to its stable numeric identifier.

    Accepts any of the identif
- `to_whatsapp_jid()`: Normalize an *outbound* WhatsApp target to a bridge-safe JID.

    Baileys' ``jidDecode`` crashes on
- `expand_whatsapp_aliases()`: Resolve WhatsApp phone/LID aliases via bridge session mapping files.

    Returns the set of all ide
- `canonical_whatsapp_identifier()`: Return a stable WhatsApp sender identity across phone-JID/LID variants.

    WhatsApp may surface th

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

