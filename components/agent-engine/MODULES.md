# agent-engine 模块详细说明

本组件包含 134 个模块。

---

## __init__.py

**路径**: `agent\__init__.py`
**行数**: 9

### 功能描述

Agent internals -- extracted modules from run_agent.py.

These modules contain pure utility functions and self-contained classes
that were previously embedded in the 3,600-line run_agent.py. Extracting
them makes run_agent.py focused on the AIAgent orchestrator class.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## account_usage.py

**路径**: `agent\account_usage.py`
**行数**: 639

### 功能描述

Surface-agnostic data for the ``/credits`` command.

    One portal fetch, one parse — consumed identically by the CLI panel, the
    gateway button, and any other money surface. Fail-open: when not l

### 核心类

- `AccountUsageWindow`
- `AccountUsageSnapshot`
- `CreditsView`: Surface-agnostic data for the ``/credits`` command.

    One portal fetch, one parse — consumed iden

### 核心函数

- `render_account_usage_lines()`
- `build_nous_credits_snapshot()`: Map a NousPortalAccountInfo into an AccountUsageSnapshot for /usage.

    Shows dollar magnitudes (s
- `nous_credits_lines()`: Return rendered Nous-credits /usage lines, or [] when there's nothing to show.

    Account-independ
- `build_credits_view()`: Build the /credits view: balance block + identity line + top-up URL.

    Reuses the same account fe
- `fetch_account_usage()`

### 依赖关系

**依赖组件**: acp-adapter, cli, llm-client
**跨组件调用**: 是

---

## agent_init.py

**路径**: `agent\agent_init.py`
**行数**: 1835

### 功能描述

Implementation of :meth:`AIAgent.__init__` — extracted as a module function.

``AIAgent.__init__`` is one of the longest methods in the codebase (60+
parameters, ~1,400 lines of attribute initialization, provider
auto-detection, credential resolution, context-engine bootstrap, etc.).
Keeping it in `

### 核心函数

- `init_agent()`: Initialize the AI Agent.

    Args:
        base_url (str): Base URL for the model API (optional)
  

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, gateway, llm-client, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## agent_runtime_helpers.py

**路径**: `agent\agent_runtime_helpers.py`
**行数**: 2651

### 功能描述

Assorted AIAgent runtime helpers — moved out of run_agent.py for clarity.

Each function takes the parent ``AIAgent`` as its first argument
(``agent``) except for the static helpers (``sanitize_tool_call_arguments``,
``drop_thinking_only_and_merge_users``) which are stateless.  AIAgent
keeps thin fo

### 核心函数

- `agent_runtime_owns_post_tool_hook()`: Return True when an agent-level tool path emits its own post hook.
- `convert_to_trajectory_format()`: Convert internal message format to trajectory format for saving.
    
    Args:
        messages (Li
- `sanitize_tool_call_arguments()`: Repair corrupted assistant tool-call argument JSON in-place.
- `repair_message_sequence()`: Collapse malformed role-alternation left in the live history.

    Providers (OpenAI, OpenRouter, An
- `repair_message_sequence_with_cursor()`: Run :func:`repair_message_sequence` and keep the SessionDB flush
    cursor consistent with the comp
- `strip_think_blocks()`: Remove reasoning/thinking blocks from content, returning only visible text.

    Handles four cases:
- `recover_with_credential_pool()`: Attempt credential recovery via pool rotation.

    Returns (recovered, has_retried_429).
    On rat
- `try_recover_primary_transport()`: Attempt one extra primary-provider recovery cycle for transient transport failures.

    After ``max
- `drop_thinking_only_and_merge_users()`: Drop thinking-only assistant turns; merge any adjacent user messages left behind.

    Runs on the p
- `restore_primary_runtime()`: Restore the primary runtime at the start of a new turn.

    In long-lived CLI sessions a single AIA
- `extract_reasoning()`: Extract reasoning/thinking content from an assistant message.
    
    OpenRouter and various provid
- `dump_api_request_debug()`: Dump a debug-friendly HTTP request record for the active inference API.

    Captures the request bo
- `anthropic_prompt_cache_policy()`: Decide whether to apply Anthropic prompt caching and which layout to use.

    Returns ``(should_cac
- `create_openai_client()`
- `switch_model()`: Switch the model/provider in-place for a live agent.

    Called by the /model command handlers (CLI
- ... 还有 10 个函数

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, llm-client, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## anthropic_adapter.py

**路径**: `agent\anthropic_adapter.py`
**行数**: 2661

### 功能描述

Anthropic Messages API adapter for Hermes Agent.

Translates between Hermes's internal OpenAI-style message format and
Anthropic's Messages API. Follows the same pattern as the codex_responses
adapter — all provider-specific logic is isolated here.

Auth supports:
  - Regular API keys (sk-ant-api*) 

### 核心函数

- `build_anthropic_client()`: Create an Anthropic client, auto-detecting setup-tokens vs API keys.

    ``api_key`` accepts either
- `build_anthropic_bedrock_client()`: Create an AnthropicBedrock client for Bedrock Claude models.

    Uses the Anthropic SDK's native Be
- `read_claude_code_credentials()`: Read refreshable Claude Code OAuth credentials.

    Checks two sources in order:
      1. macOS Key
- `is_claude_code_token_valid()`: Check if Claude Code credentials have a non-expired access token.
- `refresh_anthropic_oauth_pure()`: Refresh an Anthropic OAuth token without mutating local credential files.
- `resolve_anthropic_token()`: Resolve an Anthropic token from all available sources.

    Priority:
      1. ANTHROPIC_TOKEN env v
- `run_oauth_setup_token()`: Run 'claude setup-token' interactively and return the resulting token.

    Checks multiple sources 
- `run_hermes_oauth_login_pure()`: Run Hermes-native OAuth PKCE flow and return credential state.
- `read_hermes_oauth_credentials()`: Read Hermes-managed OAuth credentials from ~/.hermes/.anthropic_oauth.json.
- `normalize_model_name()`: Normalize a model name for the Anthropic API.

    - Strips 'anthropic/' prefix (OpenRouter format, 
- `convert_tools_to_anthropic()`: Convert OpenAI tool definitions to Anthropic format.
- `convert_messages_to_anthropic()`: Convert OpenAI-format messages to Anthropic format.

    Returns (system_prompt, anthropic_messages)
- `build_anthropic_kwargs()`: Build kwargs for anthropic.messages.create().

    Naming note — two distinct concepts, easily confu
- `sanitize_anthropic_kwargs()`: Drop Responses-API-only keys before an Anthropic Messages SDK call.

    Defensive boundary guard fo
- `create_anthropic_message()`: Create an Anthropic message, aggregating via stream when available.

    Some Anthropic-compatible g

### 依赖关系

**依赖组件**: acp-adapter, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## async_utils.py

**路径**: `agent\async_utils.py`
**行数**: 69

### 功能描述

Async/sync bridging helpers.

The codebase has ~30 sites that schedule a coroutine onto an event loop from a
worker thread via :func:`asyncio.run_coroutine_threadsafe`.  That function can
raise :class:`RuntimeError` (e.g. the loop was closed during a shutdown race),
and when it does the coroutine ob

### 核心函数

- `safe_schedule_threadsafe()`: Schedule ``coro`` on ``loop`` from a sync context, leak-safe.

    Returns the :class:`concurrent.fu

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## auxiliary_client.py

**路径**: `agent\auxiliary_client.py`
**行数**: 6536

### 功能描述

Shared auxiliary client router for side tasks.

Provides a single resolution chain so every consumer (context compression,
session search, web extraction, vision analysis, browser vision) picks up
the best available backend without duplicating fallback logic.

Resolution order for text tasks (auto m

### 核心类

- `_OpenAIProxy`: Module-level proxy that looks like the ``openai.OpenAI`` class.

    Forwards ``OpenAI(...)`` calls 
- `_CodexCompletionsAdapter`: Drop-in shim that accepts chat.completions.create() kwargs and
    routes them through the Codex Res
- `_CodexChatShim`: Wraps the adapter to provide client.chat.completions.create().
- `CodexAuxiliaryClient`: OpenAI-client-compatible wrapper that routes through Codex Responses API.

    Consumers can call cl
- `_AsyncCodexCompletionsAdapter`: Async version of the Codex Responses adapter.

    Wraps the sync adapter via asyncio.to_thread() so
- `_AsyncCodexChatShim`
- `AsyncCodexAuxiliaryClient`: Async-compatible wrapper matching AsyncOpenAI.chat.completions.create().
- `_AnthropicCompletionsAdapter`: OpenAI-client-compatible adapter for Anthropic Messages API.
- `_AnthropicChatShim`
- `AnthropicAuxiliaryClient`: OpenAI-client-compatible wrapper over a native Anthropic client.
- ... 还有 3 个类

### 核心函数

- `aux_interrupt_protection()`: Mark the current thread's auxiliary LLM call as interrupt-protected.

    Used by atomic aux tasks (
- `build_or_headers()`: Build OpenRouter headers, optionally including response-cache headers.

    Precedence for response 
- `build_nvidia_nim_headers()`: Return NVIDIA NIM cloud attribution headers for build.nvidia.com traffic.
- `set_runtime_main()`: Record the live runtime provider/model/credentials for the current AIAgent.

    Called by ``run_age
- `clear_runtime_main()`: Clear the runtime override (e.g. on session end).
- `resolve_provider_client()`: Central router: given a provider name and optional model, return a
    configured client with the co
- `get_text_auxiliary_client()`: Return (client, default_model_slug) for text-only auxiliary tasks.

    Args:
        task: Optional
- `get_async_text_auxiliary_client()`: Return (async_client, model_slug) for async consumers.

    For standard providers returns (AsyncOpe
- `get_available_vision_backends()`: Return the currently available vision backends in auto-selection order.

    Order: active provider 
- `resolve_vision_provider_client()`: Resolve the client actually used for vision tasks.

    Direct endpoint overrides take precedence ov
- `get_auxiliary_extra_body()`: Return extra_body kwargs for auxiliary API calls.
    
    Includes Nous Portal product tags when th
- `auxiliary_max_tokens_param()`: Return the correct max tokens kwarg for the auxiliary client's provider.

    OpenRouter and local m
- `neuter_async_httpx_del()`: Monkey-patch ``AsyncHttpxClientWrapper.__del__`` to be a no-op.

    The OpenAI SDK's ``AsyncHttpxCl
- `shutdown_cached_clients()`: Close all cached clients (sync and async) to prevent event-loop errors.

    Call this during CLI sh
- `cleanup_stale_async_clients()`: Force-close cached async clients whose event loop is closed.

    Call this after each agent turn to
- ... 还有 2 个函数

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## azure_identity_adapter.py

**路径**: `agent\azure_identity_adapter.py`
**行数**: 556

### 功能描述

Microsoft Entra ID adapter for Microsoft Foundry.

Provides keyless authentication for Microsoft Foundry deployments using the
`azure-identity` SDK's `DefaultAzureCredential` chain (env service principal
→ workload identity → managed identity → VS Code → Azure CLI → azd →
PowerShell → broker).

Arch

### 核心类

- `EntraIdentityConfig`: Serializable Entra ID config.

    Captures the Hermes-managed Entra knobs we need outside Azure SDK

### 核心函数

- `has_azure_identity_installed()`: Return True if `azure-identity` can be imported right now.

    Cheap check — does not walk the cred
- `reset_credential_cache()`: Clear the cached ``DefaultAzureCredential``. Used by tests and
    profile switches.

    Defensive 
- `build_credential()`: Return the cached ``DefaultAzureCredential`` for ``config``.

    Hermes processes use exactly one E
- `build_token_provider()`: Return a zero-arg callable that mints a fresh Entra bearer JWT.

    The returned callable is exactl
- `has_azure_identity_credentials()`: Best-effort probe: can `DefaultAzureCredential` mint a token now?

    Runs ``credential.get_token(s
- `describe_active_credential()`: Return diagnostic info about the active credential chain.

    Best-effort: runs ``get_token()`` and
- `is_token_provider()`: Return True when ``value`` is a callable Entra token provider.

    Used at the seams where a consum
- `materialize_bearer_for_http()`: Return a fresh Bearer JWT for a manual HTTP request.

    Only call this at sites that must construc
- `build_bearer_http_client()`: Return an ``httpx.Client`` that mints a fresh Entra bearer JWT
    per outbound request.

    The An

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## background_review.py

**路径**: `agent\background_review.py`
**行数**: 875

### 功能描述

Background memory/skill review — fork the agent to evaluate the turn.

After every turn, ``AIAgent.run_conversation`` may call
:func:`spawn_background_review` to fire off a daemon thread that replays
the conversation snapshot in a forked :class:`AIAgent` and asks itself
"should any skill/memory be s

### 核心函数

- `summarize_background_review_actions()`: Build the human-facing action summary for a background review pass.

    Walks the review agent's se
- `build_memory_write_metadata()`: Build provenance metadata for external memory-provider mirrors.
- `spawn_background_review_thread()`: Build the review thread target and prompt for a background review.

    Returns a ``(target, prompt)

### 依赖关系

**依赖组件**: cli, entry-points, tool-system
**跨组件调用**: 是

---

## bedrock_adapter.py

**路径**: `agent\bedrock_adapter.py`
**行数**: 1343

### 功能描述

AWS Bedrock Converse API adapter for Hermes Agent.

Provides native integration with Amazon Bedrock using the Converse API,
bypassing the OpenAI-compatible endpoint in favor of direct AWS SDK calls.
This enables full access to the Bedrock ecosystem:

  - **Native Converse API**: Unified interface fo

### 核心函数

- `reset_client_cache()`: Clear cached boto3 clients. Used in tests and profile switches.
- `invalidate_runtime_client()`: Evict the cached ``bedrock-runtime`` client for a single region.

    Per-region counterpart to :fun
- `is_stale_connection_error()`: Return True if ``exc`` indicates a dead/stale Bedrock HTTP connection.

    Matches:
      * ``botoc
- `is_streaming_access_denied_error()`: Return True when AWS denied the ``bedrock:InvokeModelWithResponseStream`` action.

    IAM policies 
- `resolve_aws_auth_env_var()`: Return the name of the AWS auth source that is active, or None.

    Checks environment variables fi
- `has_aws_credentials()`: Return True if any AWS credential source is detected.

    Checks environment variables first (fast,
- `resolve_bedrock_region()`: Resolve the AWS region for Bedrock API calls.

    Priority:
      1. AWS_REGION env var
      2. AW
- `bedrock_model_ids_or_none()`: Live-discover Bedrock model IDs for the active region.

    Returns a list of model ID strings if di
- `is_anthropic_bedrock_model()`: Return True if the model is an Anthropic Claude model on Bedrock.

    These models should use the A
- `convert_tools_to_converse()`: Convert OpenAI-format tool definitions to Bedrock Converse ``toolConfig``.

    OpenAI format::

   
- `convert_messages_to_converse()`: Convert OpenAI-format messages to Bedrock Converse format.

    Returns ``(system_prompt, converse_m
- `normalize_converse_response()`: Convert a Bedrock Converse API response to an OpenAI-compatible object.

    The agent loop in ``run
- `normalize_converse_stream_events()`: Consume a Bedrock ConverseStream event stream and build an OpenAI-compatible response.

    Processe
- `stream_converse_with_callbacks()`: Process a Bedrock ConverseStream event stream with real-time callbacks.

    This is the core stream
- `build_converse_kwargs()`: Build kwargs for ``bedrock-runtime.converse()`` or ``converse_stream()``.

    Converts OpenAI-forma
- ... 还有 7 个函数

### 依赖关系

**依赖组件**: acp-adapter, llm-client, tool-system
**跨组件调用**: 是

---

## billing_view.py

**路径**: `agent\billing_view.py`
**行数**: 296

### 功能描述

Surface-agnostic core for the Phase 2b terminal-billing screens.

One fetch/parse per concern, consumed identically by the CLI handler
(``cli.py::_show_billing``), the TUI JSON-RPC methods
(``tui_gateway/server.py``), and any other surface. Mirrors the proven
``agent/account_usage.py::build_credits_

### 核心类

- `CardInfo`
- `MonthlyCap`
- `AutoReload`
- `BillingState`: Parsed ``GET /api/billing/state`` — the overview screen's data.

    Fail-open: ``logged_in=False`` 
- `AmountValidation`

### 核心函数

- `parse_money()`: Parse a server money value (decimal string) into :class:`Decimal`.

    Returns None for missing/inv
- `format_money()`: Format a Decimal as ``$X`` / ``$X.YY`` for display.

    Whole dollars show no decimals; any fractio
- `billing_state_from_payload()`: Map a raw ``/api/billing/state`` JSON dict into :class:`BillingState`.
- `build_billing_state()`: Fetch + parse ``/api/billing/state``. Fail-open.

    Returns ``BillingState(logged_in=False)`` when
- `new_idempotency_key()`: Fresh UUID for a user-confirmed purchase (reuse on retry of the SAME buy).

    The ``Idempotency-Ke
- `validate_charge_amount()`: Validate a custom charge amount against bounds + 2dp (multipleOf 0.01).

    Mirrors the server's ac

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## browser_provider.py

**路径**: `agent\browser_provider.py`
**行数**: 176

### 功能描述

Browser Provider ABC
====================

Defines the pluggable-backend interface for cloud browser providers
(Browserbase, Browser Use, Firecrawl, …). Providers register instances via
:meth:`PluginContext.register_browser_provider`; the active one (selected via
``browser.cloud_provider`` in ``conf

### 核心类

- `BrowserProvider`: Abstract base class for a cloud browser backend.

    Subclasses must implement :meth:`name`, :meth:

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## browser_registry.py

**路径**: `agent\browser_registry.py`
**行数**: 193

### 功能描述

Browser Provider Registry
=========================

Central map of registered cloud browser providers. Populated by plugins at
import-time via :meth:`PluginContext.register_browser_provider`; consumed by
:func:`tools.browser_tool._get_cloud_provider` to route each cloud-mode
``browser_*`` tool call

### 核心函数

- `register_provider()`: Register a cloud browser provider.

    Re-registration (same ``name``) overwrites the previous entr
- `list_providers()`: Return all registered providers, sorted by name.
- `get_provider()`: Return the provider registered under *name*, or None.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## chat_completion_helpers.py

**路径**: `agent\chat_completion_helpers.py`
**行数**: 2727

### 功能描述

Helper functions for the chat-completions code path.

Extracted from :class:`AIAgent` for cleanliness — bodies of the
non-streaming API call, request kwargs builder, assistant-message
materializer, provider-fallback activator, max-iterations handler,
and per-turn resource cleanup.

Each function tak

### 核心函数

- `estimate_request_context_tokens()`: Estimate context/load tokens from an API payload, dict or messages list.

    The stale-call detecto
- `interruptible_api_call()`: Run the API call in a background thread so the main conversation loop
    can detect interrupts with
- `build_api_kwargs()`: Build the keyword arguments dict for the active API mode.
- `build_assistant_message()`: Build a normalized assistant message dict from an API response message.

    Handles reasoning extra
- `rewrite_prompt_model_identity()`: Point the cached system prompt's ``Model:``/``Provider:`` lines at
    the active runtime after a pr
- `try_activate_fallback()`: Switch to the next fallback model/provider in the chain.

    Called when the current model is faili
- `handle_max_iterations()`: Request a summary when max iterations are reached. Returns the final response text.
- `cleanup_task_resources()`: Clean up VM and browser resources for a given task.

    Skips ``cleanup_vm`` when the active termin
- `interruptible_streaming_api_call()`: Streaming variant of _interruptible_api_call for real-time token delivery.

    Handles all three ap

### 依赖关系

**依赖组件**: cli, entry-points, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## codex_responses_adapter.py

**路径**: `agent\codex_responses_adapter.py`
**行数**: 1337

### 功能描述

Codex Responses API adapter.

Pure format-conversion and normalization logic for the OpenAI Responses API
(used by OpenAI Codex, xAI, GitHub Models, and other Responses-compatible endpoints).

Extracted from run_agent.py to isolate Responses API-specific logic from the
core agent loop. All functions

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## codex_runtime.py

**路径**: `agent\codex_runtime.py`
**行数**: 763

### 功能描述

Codex API runtime — App Server and Responses-API streaming paths.

Extracted from :class:`AIAgent` to keep the agent loop file focused.
Each function takes the parent ``AIAgent`` as its first argument
(``agent``).  AIAgent keeps thin forwarder methods for backward
compatibility.

* ``run_codex_app_s

### 核心函数

- `run_codex_app_server_turn()`: Codex app-server runtime path. Hands the entire turn to a `codex
    app-server` subprocess and proj
- `run_codex_stream()`: Execute one streaming Responses API request and return the final response.

    Uses ``responses.cre
- `run_codex_create_stream_fallback()`: Backward-compatible alias for the unified event-driven path.

    Historically this was the fallback

### 依赖关系

**依赖组件**: entry-points, tool-system
**跨组件调用**: 是

---

## coding_context.py

**路径**: `agent\coding_context.py`
**行数**: 849

### 功能描述

Coding-context awareness — base Hermes, every interactive surface.

When the user runs Hermes inside a code workspace (CLI, TUI, desktop app, or an
editor over ACP), Hermes shifts into a **coding posture**. This module is the
single place that decides whether we're in that posture and what it implie

### 核心类

- `ContextProfile`: A named operating posture. Pure data — consumers read these fields.

    ``toolset``      — collapse
- `RuntimeMode`: The resolved operating posture for a session. Immutable by construction.

    Built once via :func:`
- `ProjectFacts`: Structured project facts — the model's verify loop, detected once.

    The same data that feeds the

### 核心函数

- `get_profile()`: Return a registered profile, falling back to ``general``.
- `resolve_runtime_mode()`: Resolve the operating posture once. Cheap — a handful of ``stat`` calls.

    This is the single ent
- `is_coding_context()`: Whether Hermes should operate in its coding posture right now.
- `coding_selection()`: Toolset selection for the coding posture.

    ``None`` unless the user opted into ``focus`` mode AN
- `coding_system_blocks()`: Stable system-prompt blocks for the current posture (empty when general).

    ``model`` steers the 
- `coding_compact_skill_categories()`: Skill categories the active posture demotes to names-only in the index.

    Empty outside the codin
- `detect_project_facts()`: Detect manifests, package manager(s), verify commands, and context files.

    Cheap: stat calls plu
- `project_facts_for()`: Structured project facts for ``cwd`` — ``None`` outside a workspace.

    Same detection the system-
- `build_coding_workspace_block()`: Workspace snapshot for the system prompt (empty outside a workspace).

    Git state (branch/status/

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## context_compressor.py

**路径**: `agent\context_compressor.py`
**行数**: 2684

### 功能描述

Automatic context window compression for long conversations.

Self-contained class with its own OpenAI client for summarization.
Uses auxiliary model (cheap/fast) to summarize middle turns while
protecting head and tail context.

Improvements over v2:
  - Structured summary template with Resolved/Pe

### 核心类

- `ContextCompressor`: Default context engine — compresses conversation context via lossy summarization.

    Algorithm:
  

### 依赖关系

**依赖组件**: entry-points, llm-client
**跨组件调用**: 是

---

## context_engine.py

**路径**: `agent\context_engine.py`
**行数**: 227

### 功能描述

Abstract base class for pluggable context engines.

A context engine controls how conversation context is managed when
approaching the model's token limit. The built-in ContextCompressor
is the default implementation. Third-party engines (e.g. LCM) can
replace it via the plugin system or by being pl

### 核心类

- `ContextEngine`: Base class all context engines must implement.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## context_references.py

**路径**: `agent\context_references.py`
**行数**: 552

### 功能描述

（需从代码逻辑分析）

### 核心类

- `ContextReference`
- `ContextReferenceResult`

### 核心函数

- `parse_context_references()`
- `preprocess_context_references()`

### 依赖关系

**依赖组件**: state-management, tool-system
**跨组件调用**: 是

---

## conversation_compression.py

**路径**: `agent\conversation_compression.py`
**行数**: 1068

### 功能描述

Context compression — extract the AIAgent methods that drive summarisation.

Three concerns live here:

* :func:`check_compression_model_feasibility` — startup probe of the
  configured auxiliary compression model.  Warns when the aux context
  window can't fit the main model's compression threshold

### 核心函数

- `check_compression_model_feasibility()`: Warn at session start if the auxiliary compression model's context
    window is smaller than the ma
- `replay_compression_warning()`: Re-send the compression warning through ``status_callback``.

    During ``__init__`` the gateway's 
- `compress_context()`: Compress conversation context and split the session in SQLite.

    Args:
        agent: The owning 
- `try_shrink_image_parts_in_messages()`: Re-encode all native image parts at a smaller size to recover from
    image-too-large errors (Anthr

### 依赖关系

**依赖组件**: cli, entry-points, gateway, llm-client, tool-system
**跨组件调用**: 是

---

## conversation_loop.py

**路径**: `agent\conversation_loop.py`
**行数**: 4787

### 功能描述

The agent conversation loop — extracted from ``run_agent.AIAgent``.

This is the biggest single chunk pulled out of ``run_agent.py``: the
roughly 3,900-line :func:`run_conversation` body that drives one user
turn through the agent (model call, tool dispatch, retries, fallbacks,
compression, post-tur

### 核心函数

- `run_conversation()`: Run a complete conversation with tool calling until completion.

    Args:
        user_message (str

### 依赖关系

**依赖组件**: cli, entry-points, llm-client, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## copilot_acp_client.py

**路径**: `agent\copilot_acp_client.py`
**行数**: 680

### 功能描述

OpenAI-compatible shim that forwards Hermes requests to `copilot --acp`.

This adapter lets Hermes treat the GitHub Copilot ACP server as a chat-style
backend. Each request starts a short-lived ACP session, sends the formatted
conversation as a single prompt, collects text chunks, and converts the r

### 核心类

- `_ACPChatCompletions`
- `_ACPChatNamespace`
- `CopilotACPClient`: Minimal OpenAI-client-compatible facade for Copilot ACP.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## credential_persistence.py

**路径**: `agent\credential_persistence.py`
**行数**: 175

### 功能描述

Credential-pool disk-boundary sanitization helpers.

These helpers define which credential-pool entries are references to borrowed
runtime secrets and strip raw values before those entries are written to
``auth.json``.  They intentionally have no dependency on ``hermes_cli.auth`` so
both the pool mo

### 核心函数

- `is_borrowed_credential_source()`: Return True when ``source`` points at a borrowed/reference-only secret.
- `sanitize_borrowed_credential_payload()`: Return a disk-safe credential-pool payload.

    Owned sources (manual entries and Hermes-owned OAut

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## credential_pool.py

**路径**: `agent\credential_pool.py`
**行数**: 2293

### 功能描述

Persistent multi-credential pool for same-provider failover.

### 核心类

- `PooledCredential`
- `CredentialPool`

### 核心函数

- `label_from_token()`
- `get_custom_provider_pool_key()`: Look up the custom_providers list in config.yaml and return 'custom:<name>' for a matching base_url.
- `list_custom_pool_providers()`: Return all 'custom:*' pool keys that have entries in auth.json.
- `get_pool_strategy()`: Return the configured selection strategy for a provider.
- `load_pool()`

### 依赖关系

**依赖组件**: acp-adapter, cli, llm-client, state-management
**跨组件调用**: 是

---

## credential_sources.py

**路径**: `agent\credential_sources.py`
**行数**: 449

### 功能描述

Unified removal contract for every credential source Hermes reads from.

Hermes seeds its credential pool from many places:

    env:<VAR>     — os.environ / ~/.hermes/.env
    claude_code   — ~/.claude/.credentials.json
    hermes_pkce   — ~/.hermes/.anthropic_oauth.json
    device_code   — auth.js

### 核心类

- `RemovalResult`: Outcome of removing a credential source.

    Attributes:
        cleaned: Short strings describing 
- `RemovalStep`: How to remove one specific credential source cleanly.

    Attributes:
        provider: Provider po

### 核心函数

- `register()`
- `find_removal_step()`: Return the first matching RemovalStep, or None if unregistered.

    Unregistered sources fall throu

### 依赖关系

**依赖组件**: acp-adapter, cli, state-management
**跨组件调用**: 是

---

## credits_tracker.py

**路径**: `agent\credits_tracker.py`
**行数**: 795

### 功能描述

Credits tracking for Nous inference API responses.

Parses x-nous-credits-* (and optional x-nous-tool-pool-*) headers from
inference responses into a validated CreditsState dataclass.  Provides
depletion detection (paid_access), subscription-cap used_fraction, and
warn-once schema-version gating.  T

### 核心类

- `CreditsState`: Full credits state parsed from x-nous-credits-* response headers.
- `AgentNotice`: A structured, driver-agnostic out-of-band notice.

    The agent fires these via ``AIAgent.notice_ca

### 核心函数

- `is_free_tier_model()`: Return True when *model* is a Nous free-tier model, using ONLY local data.

    Two signals, both ze
- `evaluate_credits_notices()`: Reconcile credits notices against the latch. Mutates ``latch`` IN PLACE.

    latch = {"active": set
- `parse_credits_headers()`: Parse x-nous-credits-* (and x-nous-tool-pool-*) headers into a CreditsState.

    Returns None (miss
- `dev_fixture_credits_state()`: Return a fixture CreditsState for HERMES_DEV_CREDITS_FIXTURE, or None.

    The env value is a state
- `seed_credits_at_session_start()`: Hydrate agent._credits_state from /api/oauth/account (or a dev fixture) and
    fire the notice poli

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## curator.py

**路径**: `agent\curator.py`
**行数**: 1928

### 功能描述

Curator — background skill maintenance orchestrator.

The curator is an auxiliary-model task that periodically reviews agent-created
skills and maintains the collection. It runs inactivity-triggered (no cron
daemon): when the agent is idle and the last curator run was longer than
``interval_hours`` 

### 核心类

- `_ReviewRuntimeBinding`: Provider/model for the curator review fork plus optional per-slot overrides.

### 核心函数

- `load_state()`
- `save_state()`
- `set_paused()`
- `is_paused()`
- `is_enabled()`: Default ON when no config says otherwise.
- `get_interval_hours()`
- `get_min_idle_hours()`
- `get_stale_after_days()`
- `get_archive_after_days()`
- `get_prune_builtins()`: Whether the curator may prune (archive) bundled built-in skills too.

    ON by default. When on, bu
- `get_consolidate()`: Whether the curator runs its LLM consolidation (umbrella-building) pass.

    OFF by default. When o
- `should_run_now()`: Return True if the curator should run immediately.

    Gates:
      - curator.enabled == True
     
- `apply_automatic_transitions()`: Walk every curator-managed skill and move active/stale/archived based on
    the latest real activit
- `run_curator_review()`: Execute a single curator review pass.

    Steps:
      1. Apply automatic state transitions (pure, 
- `maybe_run_curator()`: Best-effort: run a curator pass if all gates pass. Returns the result
    dict if a pass was started

### 依赖关系

**依赖组件**: acp-adapter, cli, cron, entry-points, state-management
**跨组件调用**: 是

---

## curator_backup.py

**路径**: `agent\curator_backup.py`
**行数**: 712

### 功能描述

Curator snapshot + rollback.

A pre-run snapshot of ``~/.hermes/skills/`` (excluding ``.curator_backups/``
itself) is taken before any mutating curator pass. Snapshots are tar.gz
files under ``~/.hermes/skills/.curator_backups/<utc-iso>/`` with a
companion ``manifest.json`` describing the snapshot (

### 核心函数

- `is_enabled()`: Default ON — the whole point of the backup is safety by default.
- `get_keep()`
- `snapshot_skills()`: Create a tar.gz snapshot of ``~/.hermes/skills/`` and prune old ones.

    Returns the snapshot dire
- `list_backups()`: Return all restorable snapshots, newest first. Only entries with a
    real ``skills.tar.gz`` tarbal
- `rollback()`: Restore ``~/.hermes/skills/`` from a snapshot.

    Strategy:
      1. Resolve the target snapshot (
- `format_size()`
- `summarize_backups()`

### 依赖关系

**依赖组件**: cli, cron, state-management
**跨组件调用**: 是

---

## display.py

**路径**: `agent\display.py`
**行数**: 1311

### 功能描述

CLI presentation -- spinner, kawaii faces, tool preview formatting.

Pure display functions and classes with no AIAgent dependency.
Used by AIAgent._execute_tool_calls for CLI feedback.

### 核心类

- `LocalEditSnapshot`: Pre-tool filesystem snapshot used to render diffs locally after writes.
- `KawaiiSpinner`: Animated spinner with kawaii faces for CLI feedback during tool execution.

### 核心函数

- `set_tool_preview_max_len()`: Set the global max length for tool call previews. 0 = no limit.
- `get_tool_preview_max_len()`: Return the configured max preview length (0 = unlimited).
- `get_skin_tool_prefix()`: Get tool output prefix character from active skin.
- `get_tool_emoji()`: Get the display emoji for a tool.

    Resolution order:
    1. Active skin's ``tool_emojis`` overri
- `summarize_shell_command()`: Compact shell wrapper/plumbing for display while preserving raw command elsewhere.
- `redact_browser_typed_text_for_display()`: Apply secret redaction to browser_type text in display-facing payloads.

    Backends sometimes echo
- `redact_tool_args_for_display()`: Return a copy of tool args safe for logs/progress UI.

    For ``browser_type`` the ``text`` argumen
- `build_tool_preview()`: Build a short preview of a tool call's primary argument for display.

    *max_len* controls truncat
- `capture_local_edit_snapshot()`: Capture before-state for local write previews.
- `extract_edit_diff()`: Extract a unified diff from a file-edit tool result.
- `render_edit_diff_with_delta()`: Render an edit diff inline without taking over the terminal UI.
- `get_cute_tool_message()`: Generate a formatted tool completion line for CLI quiet mode.

    Format: ``| {emoji} {verb:9} {det

### 依赖关系

**依赖组件**: cli, entry-points, tool-system
**跨组件调用**: 是

---

## error_classifier.py

**路径**: `agent\error_classifier.py`
**行数**: 1386

### 功能描述

API error classification for smart failover and recovery.

Provides a structured taxonomy of API errors and a priority-ordered
classification pipeline that determines the correct recovery action
(retry, rotate credential, fallback to another provider, compress
context, or abort).

Replaces scattered

### 核心类

- `FailoverReason`: Why an API call failed — determines recovery strategy.
- `ClassifiedError`: Structured classification of an API error with recovery hints.

### 核心函数

- `classify_api_error()`: Classify an API error into a structured recovery recommendation.

    Priority-ordered pipeline:
   

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## errors.py

**路径**: `agent\errors.py`
**行数**: 4

### 功能描述

Raised when SSL/TLS certificate bundle configuration fails.

### 核心类

- `SSLConfigurationError`: Raised when SSL/TLS certificate bundle configuration fails.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## file_safety.py

**路径**: `agent\file_safety.py`
**行数**: 624

### 功能描述

Shared file safety rules used by both tools and ACP shims.

### 核心函数

- `build_write_denied_paths()`: Return exact sensitive paths that must never be written.
- `build_write_denied_prefixes()`: Return sensitive directory prefixes that must never be written.
- `get_safe_write_root()`: Return the resolved HERMES_WRITE_SAFE_ROOT path, or None if unset.
- `is_write_denied()`: Return True if path is blocked by the write denylist or safe root.
- `get_read_block_error()`: Return an error message when a read targets a denied Hermes path.

    Three categories are blocked:
- `classify_cross_profile_target()`: Classify a write target as cross-profile if it lands in another
    profile's scoped area (skills/pl
- `get_cross_profile_warning()`: Return a model-facing warning string when ``path`` is cross-profile.

    Returns ``None`` when the 
- `classify_sandbox_mirror_target()`: Classify a write target as a sandbox-mirror of authoritative Hermes state.

    Returns ``None`` whe
- `get_sandbox_mirror_warning()`: Return a model-facing warning when ``path`` lands in a sandbox mirror.

    Returns ``None`` when th
- `classify_container_mirror_target()`: Classify a write target as a container-side sandbox mirror.

    ``mirror_prefix`` must be supplied 
- `get_container_mirror_warning()`: Return a model-facing warning when *path* lands in the container's
    sandbox mirror of authoritati

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## gemini_native_adapter.py

**路径**: `agent\gemini_native_adapter.py`
**行数**: 1002

### 功能描述

OpenAI-compatible facade over Google AI Studio's native Gemini API.

Hermes keeps ``api_mode='chat_completions'`` for the ``gemini`` provider so the
main agent loop can keep using its existing OpenAI-shaped message flow.
This adapter is the transport shim that converts those OpenAI-style
``messages[

### 核心类

- `GeminiAPIError`: Error shape compatible with Hermes retry/error classification.
- `_GeminiStreamChunk`
- `_GeminiChatCompletions`
- `_AsyncGeminiChatCompletions`
- `_GeminiChatNamespace`
- `_AsyncGeminiChatNamespace`
- `GeminiNativeClient`: Minimal OpenAI-SDK-compatible facade over Gemini's native REST API.
- `AsyncGeminiNativeClient`: Async wrapper used by auxiliary_client for native Gemini calls.

### 核心函数

- `bare_gemini_model_id()`: Strip Gemini's own provider prefix from an aggregator-style model id.
- `is_native_gemini_base_url()`: Return True when the endpoint speaks Gemini's native REST API.
- `probe_gemini_tier()`: Probe a Google AI Studio API key and return its tier.

    Returns one of:

    - ``"free"``    -- k
- `is_free_tier_quota_error()`: Return True when a Gemini 429 message indicates free-tier exhaustion.
- `build_gemini_request()`
- `translate_gemini_response()`
- `translate_stream_event()`
- `gemini_http_error()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## gemini_schema.py

**路径**: `agent\gemini_schema.py`
**行数**: 100

### 功能描述

Helpers for translating OpenAI-style tool schemas to Gemini's schema subset.

### 核心函数

- `sanitize_gemini_schema()`: Return a Gemini-compatible copy of a tool parameter schema.

    Hermes tool schemas are OpenAI-flav
- `sanitize_gemini_tool_parameters()`: Normalize tool parameters to a valid Gemini object schema.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## i18n.py

**路径**: `agent\i18n.py`
**行数**: 303

### 功能描述

Lightweight internationalization (i18n) for Hermes static user-facing messages.

Scope (thin slice, by design): only the highest-impact static strings shown
to the user by Hermes itself -- approval prompts, a handful of gateway slash
command replies, restart-drain notices.  Agent-generated output, l

### 核心函数

- `reset_language_cache()`: Invalidate cached language resolution and catalogs.

    Call after :func:`hermes_cli.config.save_co
- `get_language()`: Resolve the active language using env > config > default order.
- `t()`: Translate a dotted key to the active language.

    Parameters
    ----------
    key
        Dotted

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## image_gen_provider.py

**路径**: `agent\image_gen_provider.py`
**行数**: 394

### 功能描述

Image Generation Provider ABC
=============================

Defines the pluggable-backend interface for image generation. Providers register
instances via ``PluginContext.register_image_gen_provider()``; the active one
(selected via ``image_gen.provider`` in ``config.yaml``) services every
``image_

### 核心类

- `ImageGenProvider`: Abstract base class for an image generation backend.

    Subclasses must implement :meth:`generate`

### 核心函数

- `resolve_aspect_ratio()`: Clamp an aspect_ratio value to the valid set, defaulting to landscape.

    Invalid values are coerc
- `normalize_reference_images()`: Coerce a reference-image argument into a clean list of URL/path strings.

    Accepts a single strin
- `save_b64_image()`: Decode base64 image data and write it under ``$HERMES_HOME/cache/images/``.

    Returns the absolut
- `save_url_image()`: Download an image URL and write it under ``$HERMES_HOME/cache/images/``.

    Used by providers (xAI
- `success_response()`: Build a uniform success response dict.

    ``image`` may be an HTTP URL or an absolute filesystem p
- `error_response()`: Build a uniform error response dict.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## image_gen_registry.py

**路径**: `agent\image_gen_registry.py`
**行数**: 146

### 功能描述

Image Generation Provider Registry
==================================

Central map of registered providers. Populated by plugins at import-time via
``PluginContext.register_image_gen_provider()``; consumed by the
``image_generate`` tool to dispatch each call to the active backend.

Active selection


### 核心函数

- `register_provider()`: Register an image generation provider.

    Re-registration (same ``name``) overwrites the previous 
- `list_providers()`: Return all registered providers, sorted by name.
- `get_provider()`: Return the provider registered under *name*, or None.
- `get_active_provider()`: Resolve the currently-active provider.

    Reads ``image_gen.provider`` from config.yaml; falls bac

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## image_routing.py

**路径**: `agent\image_routing.py`
**行数**: 541

### 功能描述

Routing helpers for inbound user-attached images.

Two modes:

  native  — attach images as OpenAI-style ``image_url`` content parts on the
            user turn. Provider adapters (Anthropic, Gemini, Bedrock, Codex,
            OpenAI chat.completions) already translate these into their
           

### 核心函数

- `extract_image_refs()`: Scan free-form text for image references the model should see.

    Returns ``(local_paths, urls)``:
- `decide_image_input_mode()`: Return ``"native"`` or ``"text"`` for the given turn.

    Args:
      provider: active inference pr
- `build_native_content_parts()`: Build an OpenAI-style ``content`` list for a user turn.

    Shape:
      [{"type": "text", "text": 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## insights.py

**路径**: `agent\insights.py`
**行数**: 922

### 功能描述

Session Insights Engine for Hermes Agent.

Analyzes historical session data from the SQLite state database to produce
comprehensive usage insights — token consumption, cost estimates, tool usage
patterns, activity trends, model/platform breakdowns, and session metrics.

Inspired by Claude Code's /in

### 核心类

- `InsightsEngine`: Analyzes session history and produces usage insights.

    Works directly with a SessionDB instance 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## iteration_budget.py

**路径**: `agent\iteration_budget.py`
**行数**: 63

### 功能描述

Per-agent iteration budget — thread-safe consume/refund counter.

Extracted from ``run_agent.py``.  Each ``AIAgent`` instance (parent or
subagent) holds an :class:`IterationBudget`; the parent's cap comes from
``max_iterations`` (default 90), each subagent's cap comes from
``delegation.max_iteration

### 核心类

- `IterationBudget`: Thread-safe iteration counter for an agent.

    Each agent (parent or subagent) gets its own ``Iter

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## jiter_preload.py

**路径**: `agent\jiter_preload.py`
**行数**: 40

### 功能描述

Best-effort early import for the OpenAI SDK's native streaming parser.

The OpenAI SDK imports ``jiter`` while constructing streaming chat-completion
responses.  On some Windows installs the native extension can be imported
directly from the Hermes venv, but the first import fails when it happens la

### 核心函数

- `preload_jiter_native_extension()`: Import jiter's native extension early if it is available.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## learn_prompt.py

**路径**: `agent\learn_prompt.py`
**行数**: 137

### 功能描述

``/learn`` — build the standards-guided prompt that turns whatever the user
described into a reusable skill.

``/learn`` is open-ended. The user can point it at anything they can describe:
a directory of code, an API doc URL, a workflow they just walked the agent
through in this conversation, or pas

### 核心函数

- `build_learn_prompt()`: Build the agent prompt for an open-ended ``/learn`` request.

    Args:
        user_request: the fr

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## lmstudio_reasoning.py

**路径**: `agent\lmstudio_reasoning.py`
**行数**: 49

### 功能描述

LM Studio reasoning-effort resolution shared by the chat-completions
transport and run_agent's iteration-limit summary path.

LM Studio publishes per-model ``capabilities.reasoning.allowed_options`` (e.g.
``["off","on"]`` for toggle-style models, ``["off","minimal","low"]`` for
graduated models). We

### 核心函数

- `resolve_lmstudio_effort()`: Return the ``reasoning_effort`` string to send to LM Studio, or ``None``.

    ``None`` means "omit 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `agent\lsp\__init__.py`
**行数**: 107

### 功能描述

Language Server Protocol (LSP) integration for Hermes Agent.

Hermes runs full language servers (pyright, gopls, rust-analyzer,
typescript-language-server, etc.) as subprocesses and pipes their
``textDocument/publishDiagnostics`` output into the post-write lint
delta filter used by ``write_file`` an

### 核心函数

- `get_service()`: Return the process-wide LSP service singleton, or None when disabled.

    The service is created la
- `shutdown_service()`: Tear down the LSP service if one was started.

    Safe to call multiple times; safe to call when no

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## cli.py

**路径**: `agent\lsp\cli.py`
**行数**: 300

### 功能描述

``hermes lsp`` CLI subcommand.

Subcommands:

- ``status`` — show service state, configured servers, install status.
- ``install <server_id>`` — eagerly install one server's binary.
- ``install-all`` — try to install every server with a known recipe.
- ``restart`` — tear down running clients so the 

### 核心函数

- `register_subparser()`: Wire the ``hermes lsp`` subcommand tree into the main argparse.
- `run_lsp_command()`: Top-level dispatcher for ``hermes lsp <subcommand>``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## client.py

**路径**: `agent\lsp\client.py`
**行数**: 944

### 功能描述

Async LSP client over stdin/stdout.

One :class:`LSPClient` corresponds to one ``(language_server, workspace_root)``
pair — exactly what OpenCode keys clients on, and the same shape Claude
Code uses.  The client owns a child process, drives the JSON-RPC
exchange, and exposes:

- :meth:`open_file` / 

### 核心类

- `LSPClient`: Async LSP client tied to one server process and one workspace root.

    Lifecycle:

        c = LSP

### 核心函数

- `file_uri()`: Return ``file://`` URI for an absolute filesystem path.

    Mirrors Node's ``pathToFileURL`` — hand
- `uri_to_path()`: Inverse of :func:`file_uri`.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## eventlog.py

**路径**: `agent\lsp\eventlog.py`
**行数**: 214

### 功能描述

Structured logging with steady-state silence for the LSP layer.

The LSP layer fires on every write_file/patch.  In a busy session
that's hundreds of events.  We want users to be able to ``rg`` the
log for "did LSP fire on that edit?" without drowning in noise.

The level model:

- ``DEBUG`` for ste

### 核心函数

- `log_clean()`: No diagnostics emitted for *file_path*.  DEBUG (silent at default).
- `log_disabled()`: LSP intentionally skipped for this file (feature off, ext unmapped,
    backend not local, etc.).  D
- `log_active()`: A new LSP client started for (server_id, workspace_root).

    INFO once per (server_id, workspace_r
- `log_diagnostics()`: Diagnostics arrived for a file.  INFO every time — these are the
    failure signals users actually 
- `log_no_project_root()`: File had no recognised project marker.  INFO once per file,
    DEBUG thereafter.
- `log_server_unavailable()`: The server binary couldn't be resolved.  WARNING once per
    (server_id, binary), DEBUG thereafter 
- `log_no_server_configured()`: No spawn recipe for this language.  WARNING once.
- `log_timeout()`: A request to the server timed out.  WARNING every time — these are
    inherently novel events worth
- `log_server_error()`: An unexpected exception bubbled out of the LSP layer.  WARNING.
- `log_spawn_failed()`: The LSP server failed to spawn or initialize.  WARNING.
- `reset_announce_caches()`: Test-only: clear the dedup caches.  Production code never calls this.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## install.py

**路径**: `agent\lsp\install.py`
**行数**: 404

### 功能描述

Auto-installation of LSP server binaries.

Tries to install missing servers using whatever package manager is
appropriate.  All installs go to a Hermes-owned bin staging dir,
``<HERMES_HOME>/lsp/bin/``, so we don't pollute the user's global
toolchain.

Strategies:

- ``auto`` — attempt to install wi

### 核心函数

- `hermes_lsp_bin_dir()`: Return the Hermes-owned bin staging dir for LSP servers.
- `try_install()`: Try to install ``pkg`` and return the binary path if successful.

    ``strategy`` is ``"auto"``, ``
- `detect_status()`: Return ``installed``, ``missing``, or ``manual-only`` for a package.

    Used by the ``hermes lsp s

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## manager.py

**路径**: `agent\lsp\manager.py`
**行数**: 640

### 功能描述

Service-level orchestration for LSP clients.

The :class:`LSPService` is the bridge between the synchronous
file_operations layer and the async :class:`agent.lsp.client.LSPClient`.

Design choices:

- A **single asyncio event loop** runs in a background thread.  All
  client work happens on that loo

### 核心类

- `_BackgroundLoop`: A daemon thread that owns one asyncio event loop.

    Provides :meth:`run` for synchronous callers 
- `LSPService`: The process-wide LSP service.

    Created once via :meth:`create_from_config`; the
    :func:`agent

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## protocol.py

**路径**: `agent\lsp\protocol.py`
**行数**: 197

### 功能描述

Minimal LSP JSON-RPC 2.0 framer over async streams.

LSP wire format:

    Content-Length: <bytes>\r\n
    \r\n
    <utf-8 JSON body>

The body is a JSON-RPC 2.0 envelope: request, response, or notification.

This module replaces what ``vscode-jsonrpc/node`` would do in a
TypeScript implementation. 

### 核心类

- `LSPProtocolError`: Raised when the wire protocol is violated.

    Distinct from :class:`LSPRequestError` which represe
- `LSPRequestError`: Raised when an LSP request returns an error response.

    Carries the JSON-RPC ``code``, ``message`

### 核心函数

- `encode_message()`: Encode a JSON-RPC envelope as a Content-Length framed byte string.

    The body is encoded as compa
- `make_request()`: Build a JSON-RPC 2.0 request envelope.
- `make_notification()`: Build a JSON-RPC 2.0 notification envelope (no ``id``).
- `make_response()`: Build a JSON-RPC 2.0 success response envelope.
- `make_error_response()`: Build a JSON-RPC 2.0 error response envelope.
- `classify_message()`: Return ``(kind, key)`` where kind is one of ``request``,
    ``response``, ``notification``, ``inval

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## range_shift.py

**路径**: `agent\lsp\range_shift.py`
**行数**: 150

### 功能描述

Diff-aware line-shift map for cross-edit LSP delta filtering.

When an edit deletes or inserts lines in the middle of a file, every
diagnostic below the edit point shifts to a new line number.  The
LSPService delta filter subtracts the pre-edit baseline from the
post-edit diagnostics keyed on ``(sev

### 核心函数

- `build_line_shift()`: Build a function mapping pre-edit line numbers to post-edit line numbers.

    Lines are 0-indexed t
- `shift_diagnostic_range()`: Return a copy of ``diag`` with its line range remapped through ``shift``.

    Returns ``None`` if t
- `shift_baseline()`: Apply ``shift`` to every diagnostic in ``baseline``, dropping deleted entries.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## reporter.py

**路径**: `agent\lsp\reporter.py`
**行数**: 79

### 功能描述

Format LSP diagnostics for inclusion in tool output.

The model sees a compact, severity-filtered, line-bounded summary of
diagnostics introduced by the latest edit.  Format matches what
OpenCode's ``lsp/diagnostic.ts`` and Claude Code's
``formatDiagnosticsSummary`` produce — ``<diagnostics>`` block

### 核心函数

- `format_diagnostic()`: One-line representation of a single diagnostic.
- `report_for_file()`: Build a ``<diagnostics file=...>`` block for one file.

    Returns an empty string when no diagnost
- `truncate()`: Hard-cap a formatted summary string.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## servers.py

**路径**: `agent\lsp\servers.py`
**行数**: 1041

### 功能描述

Server registry — per-language LSP server definitions.

Each :class:`ServerDef` knows how to:

- match a file by extension (or basename for extensionless files like
  ``Dockerfile``),
- resolve a project root from a file path (often via
  :func:`agent.lsp.workspace.nearest_root`),
- assemble the spa

### 核心类

- `SpawnSpec`: The result of resolving a server for a file.

    Returned by :meth:`ServerDef.resolve` when a serve
- `ServerDef`: Definition of one language server.

    The :func:`resolve_root` callable receives the absolute file
- `ServerContext`: Context passed into :meth:`ServerDef.build_spawn`.

    Carries the user's auto-install policy, any 

### 核心函数

- `find_server_for_file()`: Return the registry entry that handles ``file_path``, or None.
- `language_id_for()`: Return the LSP languageId to send in didOpen for ``path``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## workspace.py

**路径**: `agent\lsp\workspace.py`
**行数**: 224

### 功能描述

Workspace and project-root resolution for LSP.

Two concerns live here:

1. **Workspace gate** — the upper-level "is this directory a project?"
   check.  Hermes only runs LSP when the cwd (or the file being edited)
   sits inside a git worktree.  Files outside any git root never
   trigger LSP, eve

### 核心函数

- `normalize_path()`: Normalize a path for use as a stable map key.

    Resolves ``~``, makes absolute, and collapses ``.
- `find_git_worktree()`: Walk up from ``start`` looking for a ``.git`` entry (file or dir).

    Returns the directory contai
- `is_inside_workspace()`: Return True iff ``path`` is inside (or equal to) ``workspace_root``.

    Uses absolute paths but do
- `nearest_root()`: Walk up from ``start`` looking for any of the given marker files.

    Returns the **directory conta
- `resolve_workspace_for_file()`: Resolve the workspace root for a file.

    Returns ``(workspace_root, gated_in)`` where ``gated_in`
- `clear_cache()`: Clear the workspace-resolution cache.

    Called on service shutdown so a subsequent re-init doesn'

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## manual_compression_feedback.py

**路径**: `agent\manual_compression_feedback.py`
**行数**: 50

### 功能描述

User-facing summaries for manual compression commands.

### 核心函数

- `summarize_manual_compression()`: Return consistent user-facing feedback for manual compression.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## markdown_tables.py

**路径**: `agent\markdown_tables.py`
**行数**: 310

### 功能描述

CJK/wide-character-aware re-alignment of model-emitted markdown tables.

Models pad markdown tables assuming each character occupies one terminal
cell. CJK glyphs and most emoji render as two cells, so the model's
spacing collapses into drift the moment a table reaches a real terminal —
header pipes

### 核心函数

- `split_table_row()`: Split ``| a | b | c |`` into ``["a", "b", "c"]`` with trims.
- `is_table_divider()`: True when ``row`` is a markdown table separator line.
- `looks_like_table_row()`: True when ``row`` could plausibly be a markdown table row.

    Used by streaming callers to decide 
- `realign_markdown_tables()`: Rewrite every ``| ... |`` + divider block with wcwidth-aware padding.

    Lines that are not part o

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## memory_manager.py

**路径**: `agent\memory_manager.py`
**行数**: 1082

### 功能描述

MemoryManager — orchestrates memory providers for the agent.

Single integration point in run_agent.py. Replaces scattered per-backend
code with one manager that delegates to registered providers.

Only ONE external plugin provider is allowed at a time — attempting to
register a second external prov

### 核心类

- `StreamingContextScrubber`: Stateful scrubber for streaming text that may contain split memory-context spans.

    The one-shot 
- `MemoryManager`: Orchestrates the built-in provider plus at most one external provider.

    The builtin provider is 

### 核心函数

- `normalize_tool_schema()`: Return a function-tool dict with a resolvable top-level ``name``.

    Context engines and memory pr
- `memory_provider_tools_enabled()`: Return whether external memory-provider tools should be exposed.
- `inject_memory_provider_tools()`: Append external memory-provider tool schemas to an agent tool surface.
- `sanitize_context()`: Strip fence tags, injected context blocks, and system notes from provider output.
- `build_memory_context_block()`: Wrap prefetched memory in a fenced block with system note.

### 依赖关系

**依赖组件**: cli, entry-points, memory-system, state-management
**跨组件调用**: 是

---

## memory_provider.py

**路径**: `agent\memory_provider.py`
**行数**: 316

### 功能描述

Abstract base class for pluggable memory providers.

Memory providers give the agent persistent recall across sessions.
The MemoryManager enforces a one-external-provider limit to prevent
tool schema bloat and conflicting memory backends.

External providers (Honcho, Hindsight, Mem0, etc.) are regis

### 核心类

- `MemoryProvider`: Abstract base class for memory providers.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## message_content.py

**路径**: `agent\message_content.py`
**行数**: 51

### 功能描述

Return the visible text from common chat/Responses message content shapes.

### 核心函数

- `flatten_message_text()`: Return the visible text from common chat/Responses message content shapes.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## message_sanitization.py

**路径**: `agent\message_sanitization.py`
**行数**: 478

### 功能描述

Message and tool-payload sanitization helpers.

Pure functions extracted from ``run_agent.py`` so the AIAgent module can
stay focused on the conversation loop.  These walk OpenAI-format message
lists and structured payloads, repairing or stripping problematic
characters that would otherwise crash ``

### 核心函数

- `close_interrupted_tool_sequence()`: Append a synthetic assistant turn when an interrupted tail is a tool result.

    A turn cut short b

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## moa_loop.py

**路径**: `agent\moa_loop.py`
**行数**: 307

### 功能描述

Mixture-of-Agents runtime helpers for /moa turns.

The slash command is deliberately not a model tool. It marks one user turn as
MoA-enabled; the normal Hermes agent loop still owns tool calling and turn
termination, while this module gathers reference-model context before each model
iteration.

### 核心类

- `MoAChatCompletions`: OpenAI-chat-compatible facade where the aggregator is the acting model.
- `MoAClient`

### 核心函数

- `aggregate_moa_context()`: Run configured reference models and synthesize their advice.

    Failures are returned as model-spe

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## model_metadata.py

**路径**: `agent\model_metadata.py`
**行数**: 2091

### 功能描述

Model metadata, context lengths, and token estimation utilities.

Pure utility functions with no AIAgent dependency. Used by ContextCompressor
and run_agent.py for pre-flight context checks.

### 核心函数

- `grok_supports_reasoning_effort()`: Return True when an xAI Grok model accepts ``reasoning.effort``.

    Allowlist by substring (matche
- `is_local_endpoint()`: Return True if base_url points to a local machine.

    Recognises loopback (``localhost``, ``127.0.
- `detect_local_server_type()`: Detect which local server is running at base_url by probing known endpoints.

    Returns one of: "o
- `fetch_model_metadata()`: Fetch model metadata from OpenRouter (cached for 1 hour).
- `fetch_endpoint_model_metadata()`: Fetch model metadata from an OpenAI-compatible ``/models`` endpoint.

    This is used for explicit 
- `save_context_length()`: Persist a discovered context length for a model+provider combo.

    Cache key is ``model@base_url``
- `get_cached_context_length()`: Look up a previously discovered context length for model+provider.
- `get_next_probe_tier()`: Return the next lower probe tier, or None if already at minimum.
- `parse_context_limit_from_error()`: Try to extract the actual context limit from an API error message.

    Many providers include the l
- `get_context_length_from_provider_error()`: Return a provider-reported lower context limit, if one is present.

    Context-overflow recovery mu
- `parse_available_output_tokens_from_error()`: Detect an "output cap too large" error and return how many output tokens are available.

    Backgro
- `query_ollama_num_ctx()`: Query an Ollama server for the model's context length.

    Returns the model's maximum context from
- `get_model_context_length()`: Get the context length for a model.

    Resolution order:
    0. Explicit config override (model.co
- `estimate_tokens_rough()`: Rough token estimate (~4 chars/token) for pre-flight checks.

    Uses ceiling division so short tex
- `estimate_messages_tokens_rough()`: Rough token estimate for a message list (pre-flight only).

    Image parts (base64 PNG/JPEG) are co
- ... 还有 1 个函数

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## models_dev.py

**路径**: `agent\models_dev.py`
**行数**: 726

### 功能描述

Models.dev registry integration — primary database for providers and models.

Fetches from https://models.dev/api.json — a community-maintained database
of 4000+ models across 109+ providers.  Provides:

- **Provider metadata**: name, base URL, env vars, documentation link
- **Model metadata**: cont

### 核心类

- `ModelInfo`: Full metadata for a single model from models.dev.
- `ProviderInfo`: Full metadata for a provider from models.dev.
- `ModelCapabilities`: Structured capability metadata for a model from models.dev.

### 核心函数

- `fetch_models_dev()`: Fetch models.dev registry. Cache hierarchy: in-mem → disk → network.

    Returns the full registry 
- `lookup_models_dev_context()`: Look up context_length for a provider+model combo in models.dev.

    Returns the context window in 
- `get_model_capabilities()`: Look up full capability metadata from models.dev cache.

    Uses the existing fetch_models_dev() an
- `list_provider_models()`: Return all model IDs for a provider from models.dev.

    Returns an empty list if the provider is u
- `list_agentic_models()`: Return model IDs suitable for agentic use from models.dev.

    Filters for tool_call=True and exclu
- `get_provider_info()`: Get full provider metadata from models.dev.

    Accepts either a Hermes provider ID (e.g. "kilocode
- `get_model_info()`: Get full model metadata from models.dev.

    Accepts Hermes or models.dev provider ID.  Tries exact

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## moonshot_schema.py

**路径**: `agent\moonshot_schema.py`
**行数**: 239

### 功能描述

Helpers for translating OpenAI-style tool schemas to Moonshot's schema subset.

Moonshot (Kimi) accepts a stricter subset of JSON Schema than standard OpenAI
tool calling.  Requests that violate it fail with HTTP 400:

    tools.function.parameters is not a valid moonshot flavored json schema,
    d

### 核心函数

- `sanitize_moonshot_tool_parameters()`: Normalize tool parameters to a Moonshot-compatible object schema.

    Returns a deep-copied schema 
- `sanitize_moonshot_tools()`: Apply ``sanitize_moonshot_tool_parameters`` to every tool's parameters.
- `is_moonshot_model()`: True for any Kimi / Moonshot model slug, regardless of aggregator prefix.

    Matches bare names (`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## nous_rate_guard.py

**路径**: `agent\nous_rate_guard.py`
**行数**: 326

### 功能描述

Cross-session rate limit guard for Nous Portal.

Writes rate limit state to a shared file so all sessions (CLI, gateway,
cron, auxiliary) can check whether Nous Portal is currently rate-limited
before making requests.  Prevents retry amplification when RPH is tapped.

Each 429 from Nous triggers up 

### 核心函数

- `record_nous_rate_limit()`: Record that Nous Portal is rate-limited.

    Parses the reset time from response headers or error c
- `nous_rate_limit_remaining()`: Check if Nous Portal is currently rate-limited.

    Returns:
        Seconds remaining until reset,
- `clear_nous_rate_limit()`: Clear the rate limit state (e.g., after a successful Nous request).
- `format_remaining()`: Format seconds remaining into human-readable duration.
- `is_genuine_nous_rate_limit()`: Decide whether a 429 from Nous Portal is a real account rate limit.

    Nous Portal multiplexes mul

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## onboarding.py

**路径**: `agent\onboarding.py`
**行数**: 254

### 功能描述

Contextual first-touch onboarding hints.

Instead of blocking first-run questionnaires, show a one-time hint the *first*
time a user hits a behavior fork — message-while-running, first long-running
tool, etc.  Each hint is shown once per install (tracked in ``config.yaml`` under
``onboarding.seen.<f

### 核心函数

- `busy_input_hint_gateway()`: Hint shown the first time a user messages while the agent is busy.

    ``mode`` is the effective bu
- `busy_input_hint_cli()`: CLI version of the busy-input hint (plain text, no markdown).
- `tool_progress_hint_gateway()`
- `tool_progress_hint_cli()`
- `openclaw_residue_hint_cli()`: Banner shown the first time Hermes starts and finds ``~/.openclaw/``.

    Points users at ``hermes 
- `detect_openclaw_residue()`: Return True if an OpenClaw workspace directory is present in ``$HOME``.

    Pure filesystem check —
- `profile_build_mode()`: Resolve the onboarding profile-build mode from config.

    Returns one of:
      ``"ask"``  — on fi
- `profile_build_directive()`: System-note directive appended to the very first message ever.

    Instructs the agent to run a sho
- `is_seen()`: Return True if the user has already been shown this first-touch hint.
- `mark_seen()`: Persist ``onboarding.seen.<flag> = True`` to ``config_path``.

    Uses the atomic YAML writer so a 

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## oneshot.py

**路径**: `agent\oneshot.py`
**行数**: 159

### 功能描述

Shared one-off LLM requests for non-conversational helpers.

A "one-shot" is a single, stateless model call that runs *outside* any
conversation: it never touches a session's history, never breaks prompt
caching, and returns plain text. UI surfaces use it for small generative
chores — a commit messa

### 核心函数

- `render_template()`: Resolve a registered template into (instructions, user_input).

    Raises KeyError if the template 
- `run_oneshot()`: Run a single stateless LLM request and return its text.

    Provide either a registered ``template`

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `agent\pet\__init__.py`
**行数**: 52

### 功能描述

Petdex pet engine — shared core for the CLI, TUI, and desktop surfaces.

Petdex (https://github.com/crafter-station/petdex) is a public gallery of
animated sprite "pets" for coding agents.  Each pet is a ``pet.json`` plus a
``spritesheet.{webp,png}`` of 192×208 px cells. Current Codex/petdex sheets 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## constants.py

**路径**: `agent\pet\constants.py`
**行数**: 168

### 功能描述

Pet sprite geometry + animation-state taxonomy.

These values are the common petdex/Codex pet geometry. The real ``pet.json``
usually only carries ``id``/``displayName``/``description``/``spritesheetPath``;
row taxonomy is inferred from the atlas shape so Hermes can render both legacy
8-row sheets a

### 核心类

- `PetState`: Animation state a pet can be shown in.

    These are Hermes' activity state names. They are not alw

### 核心函数

- `clamp_scale()`: Clamp *scale* to ``[MIN_SCALE, MAX_SCALE]`` (the single validation point).
- `cols_for_scale()`: Half-block width implied by *scale*, clamped to the legibility floor.

    Above the floor it tracks
- `resolve_cols()`: Resolve terminal width: explicit *unicode_cols* override, else from *scale*.
- `state_aliases_for()`: Return accepted row-name aliases for *state* (always non-empty).
- `state_rows_for_grid()`: Return the row taxonomy for a spritesheet with *row_count* rows.
- `state_row_index()`: Return the spritesheet row index for *state* (clamped, never raises).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `agent\pet\generate\__init__.py`
**行数**: 30

### 功能描述

Pet generation — base-draft → hatch pipeline.

Public surface used by the gateway RPCs, the CLI ``hermes pets generate``
command, and tests:

- :func:`generate_base_drafts` / :func:`hatch_pet` — the two-step flow.
- :class:`HatchResult`, :class:`GenerationError`.
- :mod:`atlas` — deterministic frame

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## atlas.py

**路径**: `agent\pet\generate\atlas.py`
**行数**: 1184

### 功能描述

Deterministic spritesheet assembly — generated row strips → Hermes atlas.

Image-generation models are good at *drawing* a row of poses but bad at exact
grid geometry, so the model never owns the atlas layout: it produces one loose
horizontal strip per state, and these deterministic ops slice that s

### 核心函数

- `remove_background()`: Return *image* (RGBA) with its flat background keyed out to transparent.

    If the strip already h
- `extract_strip_frames()`: Turn one generated row strip into *frame_count* frames.

    The background is keyed out, then stric
- `normalize_cells()`: Register every frame into a 192x208 cell — the deterministic anti-jitter math.

    A per-frame "cro
- `single_frame()`: One frame from a standalone image (e.g. the base look).

    Used as an idle fallback so a pet alway
- `mirror_frames()`: Horizontally flip each frame *in place* (RGBA-safe).

    Used to derive ``running-left`` from an ap
- `compose_atlas()`: Pack per-state frame lists into the Hermes atlas (RGBA, residue-cleared).

    Missing/short states 
- `atlas_to_webp_bytes()`: Encode an atlas image to lossless WebP bytes (the on-disk pet format).
- `validate_atlas()`: Check geometry, per-cell occupancy, and transparency invariants.

    Returns ``{ok, width, height, 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## imagegen.py

**路径**: `agent\pet\generate\imagegen.py`
**行数**: 252

### 功能描述

Thin image-generation layer for pet sprites.

Wraps the active :class:`~agent.image_gen_provider.ImageGenProvider` with the
two things sprite generation needs that the agent-facing ``image_generate`` tool
doesn't expose: **N variants** (loop) and **reference-image grounding** (so each
animation row 

### 核心类

- `GenerationError`: Raised on any image-generation failure (no provider, API error, IO).
- `SpriteProvider`: Resolved provider plus whether it can take reference images.

### 核心函数

- `resolve_provider()`: Pick the image provider to use for sprite work.

    Preference: an explicit *prefer* choice (the de
- `list_sprite_providers()`: The reference-capable providers available to pick for pet generation.

    Returns ``[{name, label, 
- `generate()`: Generate *n* sprite images and return their local paths.

    *reference_images* grounds the output 

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## orchestrate.py

**路径**: `agent\pet\generate\orchestrate.py`
**行数**: 359

### 功能描述

Pet generation orchestration — the base-draft → hatch flow.

Two steps, mirroring the UX across every surface:

1. :func:`generate_base_drafts` — a handful of prompt-only "what should this pet
   look like" variants. Cheap; the user picks one (or retries for a fresh set).
2. :func:`hatch_pet` — take

### 核心类

- `HatchResult`: Outcome of a successful :func:`hatch_pet`.

### 核心函数

- `generate_base_drafts()`: Generate *n* candidate base looks for *concept*; returns image paths.

    Each draft is hardened to
- `hatch_pet()`: Turn an approved base image into a full, installed Hermes pet.

    Generates a grounded row strip p

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## prompts.py

**路径**: `agent\pet\generate\prompts.py`
**行数**: 184

### 功能描述

Prompt builders for pet generation.

Two prompt shapes: a *base* prompt (prompt-only, produces the canonical look the
user picks between) and per-*state* *row* prompts (grounded on the chosen base,
produce one horizontal strip of N poses). Prompts stay concise and
sprite-production oriented; the ide

### 核心函数

- `style_hint()`
- `build_base_prompt()`: The base look: a single, clean, centered full-body mascot.

    *variation* differentiates one draft
- `build_row_prompt()`: A row strip: *frame_count* poses of the SAME character, left→right.

    The attached base image is 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## manifest.py

**路径**: `agent\pet\manifest.py`
**行数**: 166

### 功能描述

Fetch the public petdex manifest.

``https://petdex.dev/api/manifest`` 307-redirects to a JSON document on R2:

    {
      "generatedAt": "...",
      "total": 2926,
      "pets": [
        {"slug": "boba", "displayName": "Boba", "kind": "creature",
         "submittedBy": "railly",
         "sprit

### 核心类

- `ManifestEntry`: A single pet's row in the manifest.
- `ManifestError`: Raised when the manifest can't be fetched or parsed.

### 核心函数

- `clear_cache()`: Drop the cached manifest (forces the next fetch to hit the network).
- `prefetch()`: Warm the manifest cache in a daemon thread — idempotent, never blocks.

    The desktop picker calls
- `fetch_manifest()`: Return every approved pet from the public manifest.

    Cached in-process for ``_MANIFEST_TTL`` sec
- `find_entry()`: Return the manifest entry for *slug*, or ``None`` if not listed.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## render.py

**路径**: `agent\pet\render.py`
**行数**: 619

### 功能描述

Decode a pet spritesheet and encode frames for a terminal.

Shared by the base CLI (writes the escape bytes to its own stdout) and the
TUI (``tui_gateway`` ships the encoded bytes to Ink, which writes them) so the
decode + capability-detection + protocol-encoding logic exists exactly once.

Supporte

### 核心类

- `PetRenderer`: Holds a pet's spritesheet and yields encoded frames per (state, index).

    Construct once per pet,

### 核心函数

- `detect_terminal_graphics()`: Best-effort detection of the richest graphics protocol available.

    Env-based (non-blocking — we 
- `resolve_mode()`: Resolve the effective render mode from config + the environment.

    ``configured`` is ``display.pe
- `state_frame_counts()`: Map each driven :class:`PetState` → its real (padding-trimmed) frame count.

    The single source o
- `kitty_image_id()`: Stable per-pet image id in ``[1, 0x7FFF]``.

    The id is encoded in the placeholder's 24-bit foreg
- `kitty_color_hex()`: Hex foreground color (``#rrggbb``) that encodes *image_id* for kitty.
- `kitty_placeholder_rows()`: Build the placeholder text grid for an *rows*×*cols* image.

    Each line is one row of the grid: t
- `build_renderer()`: Convenience factory: resolve the mode from config+env, then construct.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## state.py

**路径**: `agent\pet\state.py`
**行数**: 82

### 功能描述

Map agent activity → a :class:`PetState`.

This is the one place the "what is the agent doing right now?" → "which
animation row?" decision lives.  Each surface feeds it the signals it already
tracks:

- CLI    — ``KawaiiSpinner`` waiting/thinking state + tool outcomes.
- TUI    — gateway ``tool.sta

### 核心函数

- `todos_all_done()`: True iff there's ≥1 todo and every one is completed/cancelled.

    The "celebrate" beat (``JUMP``) 
- `derive_pet_state()`: Resolve the animation state from coarse activity signals.

    Priority (highest first) — only one r

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## store.py

**路径**: `agent\pet\store.py`
**行数**: 504

### 功能描述

On-disk pet store — install / list / resolve pets.

Pets live under ``get_hermes_home()/pets/<slug>/`` so every profile gets its
own set (we deliberately do **not** reuse petdex's ``~/.codex/pets`` default —
that's owned by the petdex npm CLI and isn't profile-aware).  Each installed
pet directory h

### 核心类

- `PetStoreError`: Raised on install/IO failures.
- `InstalledPet`: A pet present on disk.

### 核心函数

- `pets_dir()`: Return the profile-scoped pets directory (created on demand).
- `load_pet()`: Return the :class:`InstalledPet` for *slug*, or ``None`` if absent.
- `installed_pets()`: Return every installed pet (dirs containing a usable spritesheet).
- `resolve_active_pet()`: Resolve which pet to display.

    Precedence: the configured slug (``display.pet.slug``) if it's in
- `install_pet()`: Download *slug* from the manifest into the pets directory.

    Idempotent: a fully-installed pet is
- `slugify()`: Lowercase, hyphenate, and strip a display name into a filesystem slug.
- `unique_slug()`: A :func:`slugify` result that doesn't collide with an existing pet dir.
- `register_local_pet()`: Write a locally-generated pet into the store and return it.

    *spritesheet* may be a PIL image, r
- `export_pet()`: Zip an installed pet's folder (pet.json + spritesheet) → (filename, bytes).

    Dotfiles (cached th
- `thumbnail_png()`: Return a small idle-frame PNG for *slug*, cached on disk.

    Crops the top-left (idle, frame 0) ce
- `remove_pet()`: Delete an installed pet directory.  Returns True if anything was removed.
- `rename_pet()`: Rename a pet's ``displayName`` AND realign its slug/dir to match.

    Generated pets are hatched un

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## plugin_llm.py

**路径**: `agent\plugin_llm.py`
**行数**: 1047

### 功能描述

Plugin LLM facade — host-owned LLM access for trusted plugins.
==============================================================

Plugins built on Hermes Agent often need to make their own LLM calls
out-of-band — a hook that rewrites a tool error before the user sees
it, a gateway adapter that translat

### 核心类

- `PluginLlmTextInput`: Text block in a structured input list.
- `PluginLlmImageInput`: Image block in a structured input list.

    Either ``data`` (raw bytes) or ``url`` (http(s) or data
- `PluginLlmUsage`: Token + cost usage for a completion. All fields optional — providers
    differ on what they return.
- `PluginLlmCompleteResult`: Result of :meth:`PluginLlm.complete`.
- `PluginLlmStructuredResult`: Result of :meth:`PluginLlm.complete_structured`.

    ``parsed`` is set only when ``json_mode=True``
- `_TrustPolicy`: Resolved trust gate for one plugin's LLM access.
- `PluginLlmTrustError`: Raised when a plugin attempts an LLM override without trust.
- `PluginLlm`: Host-owned LLM access for one trusted plugin.

    Instances are constructed by :class:`hermes_cli.p

### 核心函数

- `make_plugin_llm_for_test()`: Construct a :class:`PluginLlm` with an injected policy and caller.

    Used by unit tests that don'

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## portal_tags.py

**路径**: `agent\portal_tags.py`
**行数**: 65

### 功能描述

Centralized Nous Portal request tags.

Every Hermes request that hits the Nous Portal — main agent loop, auxiliary
client (compression / titles / vision / web_extract / session_search / etc.),
and any future code path — must carry the same product-attribution tags so
Nous can attribute usage to Herm

### 核心函数

- `hermes_client_tag()`: Return the ``client=...`` tag for Nous Portal requests.

    Format: ``client=hermes-client-v<MAJOR>
- `nous_portal_tags()`: Return the canonical list of Nous Portal product tags.

    Always returns a fresh list so callers c

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## process_bootstrap.py

**路径**: `agent\process_bootstrap.py`
**行数**: 168

### 功能描述

Process-level bootstrap helpers for ``run_agent``.

Three concerns, all tied to ``AIAgent`` boot-time / runtime IO setup:

1. **Lazy OpenAI SDK import** — ``_load_openai_cls`` + ``_OpenAIProxy``
   defer the 240ms-ish ``from openai import OpenAI`` cost until first use,
   while preserving ``isinstan

### 核心类

- `_OpenAIProxy`: Module-level proxy that looks like ``openai.OpenAI`` but imports lazily.
- `_SafeWriter`: Transparent stdio wrapper that catches OSError/ValueError from broken pipes.

    When hermes-agent 

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## prompt_builder.py

**路径**: `agent\prompt_builder.py`
**行数**: 1909

### 功能描述

System prompt assembly -- identity, platform hints, skills index, context files.

All functions are stateless. AIAgent._build_system_prompt() calls these to
assemble pieces, then combines them with memory and ephemeral prompts.

### 核心函数

- `computer_use_guidance()`: Return platform-aware computer-use guidance for the system prompt.

    ``platform_name`` is an ``sy
- `format_steer_marker()`: Wrap a mid-turn steer for appending to a tool result (see module note).
- `build_environment_hints()`: Return environment-specific guidance for the system prompt.

    Always emits a factual block descri
- `drain_truncation_warnings()`: Return and clear any truncation warnings accumulated in this context.
- `clear_skills_system_prompt_cache()`: Drop the in-process skills prompt cache (and optionally the disk snapshot).
- `build_skills_system_prompt()`: Build a compact skill index for the system prompt.

    Two-layer cache:
      1. In-process LRU dic
- `build_nous_subscription_prompt()`: Build a compact Nous subscription capability block for the system prompt.
- `load_soul_md()`: Load SOUL.md from HERMES_HOME and return its content, or None.

    Used as the agent identity (slot
- `build_context_files_prompt()`: Discover and load context files for the system prompt.

    Priority (first found wins — only ONE pr

### 依赖关系

**依赖组件**: cli, entry-points, gateway, security, state-management, tool-system
**跨组件调用**: 是

---

## prompt_caching.py

**路径**: `agent\prompt_caching.py`
**行数**: 80

### 功能描述

Anthropic prompt caching strategy.

Single layout: ``system_and_3``. 4 cache_control breakpoints — system
prompt + last 3 non-system messages, all at the same TTL (5m or 1h).
Reduces input token costs by ~75% on multi-turn conversations within a
single session.

Pure functions -- no class state, no 

### 核心函数

- `apply_anthropic_cache_control()`: Apply system_and_3 caching strategy to messages for Anthropic models.

    Places up to 4 cache_cont

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## rate_limit_tracker.py

**路径**: `agent\rate_limit_tracker.py`
**行数**: 247

### 功能描述

Rate limit tracking for inference API responses.

Captures x-ratelimit-* headers from provider responses and provides
formatted display for the /usage slash command.  Currently supports
the Nous Portal header format (also used by OpenRouter and OpenAI-compatible
APIs that follow the same convention)

### 核心类

- `RateLimitBucket`: One rate-limit window (e.g. requests per minute).
- `RateLimitState`: Full rate-limit state parsed from response headers.

### 核心函数

- `parse_rate_limit_headers()`: Parse x-ratelimit-* headers into a RateLimitState.

    Returns None if no rate limit headers are pr
- `format_rate_limit_display()`: Format rate limit state for terminal/chat display.
- `format_rate_limit_compact()`: One-line compact summary for status bars / gateway messages.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## reasoning_timeouts.py

**路径**: `agent\reasoning_timeouts.py`
**行数**: 217

### 功能描述

Per-reasoning-model stale-timeout floor for known reasoning models.

Reasoning models (those that emit extended thinking blocks before their
first content token) routinely exceed Hermes's default chat-model
stale detectors:

* Stream stale detector:   ``HERMES_STREAM_STALE_TIMEOUT``     default 180s

### 核心函数

- `get_reasoning_stale_timeout_floor()`: Return the stale-timeout floor (seconds) for a known reasoning model.

    Returns ``None`` when the

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## redact.py

**路径**: `agent\redact.py`
**行数**: 522

### 功能描述

Regex-based secret redaction for logs and tool output.

Applies pattern matching to mask API keys, tokens, and credentials
before they reach log files, verbose output, or gateway logs.

Short tokens (< 18 chars) are fully masked. Longer tokens preserve
the first 6 and last 4 characters for debuggabi

### 核心类

- `RedactingFormatter`: Log formatter that redacts secrets from all log messages.

### 核心函数

- `mask_secret()`: Mask a secret for display, preserving ``head`` and ``tail`` characters.

    Canonical helper for di
- `redact_sensitive_text()`: Apply all redaction patterns to a block of text.

    Safe to call on any string -- non-matching tex

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## retry_utils.py

**路径**: `agent\retry_utils.py`
**行数**: 130

### 功能描述

Retry utilities — jittered backoff for decorrelated retries.

Replaces fixed exponential backoff with jittered delays to prevent
thundering-herd retry spikes when multiple sessions hit the same
rate-limited provider concurrently.

### 核心函数

- `jittered_backoff()`: Compute a jittered exponential backoff delay.

    Args:
        attempt: 1-based retry attempt numb
- `is_zai_coding_overload_error()`: Return True for Z.AI Coding Plan transient overload 429s.

    The coding-plan endpoint reports over
- `adaptive_rate_limit_backoff()`: Provider-aware rate-limit backoff.

    For most providers this returns ``default_wait`` unchanged. 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## runtime_cwd.py

**路径**: `agent\runtime_cwd.py`
**行数**: 63

### 功能描述

Single source of truth for the agent working directory.

`TERMINAL_CWD` is the runtime carrier for the configured working directory
(design #19214/#19242: `terminal.cwd` is bridged once to `TERMINAL_CWD` at
gateway/cron startup). The local-CLI backend deliberately leaves it unset and
relies on the l

### 核心函数

- `set_session_cwd()`: Pin the logical cwd for the current context.
- `clear_session_cwd()`
- `resolve_agent_cwd()`
- `resolve_context_cwd()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## secret_scope.py

**路径**: `agent\secret_scope.py`
**行数**: 206

### 功能描述

Profile-scoped credential resolution for multi-profile gateway multiplexing.

The multiplexing gateway serves many profiles from one process. Each profile
has its own ``.env`` with its own provider keys and platform tokens, so we
**cannot** union them into the process-global ``os.environ`` (that wou

### 核心类

- `UnscopedSecretError`: Raised when a secret is read in multiplex mode with no scope installed.

    This is the fail-closed

### 核心函数

- `set_multiplex_active()`: Mark whether the process is running as a profile multiplexer.

    Called once at gateway startup. W
- `is_multiplex_active()`: Return whether the process is running as a profile multiplexer.
- `set_secret_scope()`: Install the active profile's secret mapping for the current context.

    Returns a token for ``rese
- `reset_secret_scope()`: Restore the previous secret scope.
- `current_secret_scope()`: Return the active secret mapping, or None when no scope is installed.
- `get_secret()`: Resolve a credential by env-var name, honoring the active profile scope.

    Resolution order:

   
- `load_env_file()`: Parse a ``.env`` file into a plain dict WITHOUT touching ``os.environ``.

    Used to load a profile
- `build_profile_secret_scope()`: Build a profile's secret mapping from its ``<home>/.env``.

    Returns a fresh dict (safe to instal

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `agent\secret_sources\__init__.py`
**行数**: 14

### 功能描述

External secret source integrations.

A secret source is anything that can supply environment-variable-shaped
credentials at process startup, _after_ ~/.hermes/.env has loaded.  By
default sources are non-destructive: they only set values for env vars
that aren't already present, so .env and shell e

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## bitwarden.py

**路径**: `agent\secret_sources\bitwarden.py`
**行数**: 693

### 功能描述

Bitwarden Secrets Manager (`bws` CLI) integration.

Hermes pulls API keys from Bitwarden Secrets Manager at process startup
so they don't have to live in plaintext in ``~/.hermes/.env``.

Design summary
--------------

* The ``bws`` binary is auto-installed into ``<hermes_home>/bin/bws`` on
  first 

### 核心类

- `_CachedFetch`
- `FetchResult`: Outcome of a single BSM pull.

### 核心函数

- `find_bws()`: Return a path to a usable ``bws`` binary, or None.

    Resolution order:
      1. ``<hermes_home>/b
- `install_bws()`: Download, verify, and install the pinned ``bws`` binary.

    Returns the path to the installed exec
- `fetch_bitwarden_secrets()`: Pull the secrets for ``project_id`` from Bitwarden Secrets Manager.

    Returns ``(secrets_dict, wa
- `apply_bitwarden_secrets()`: Pull secrets from BSM and set them on ``os.environ``.

    This is the function ``load_hermes_dotenv

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## shell_hooks.py

**路径**: `agent\shell_hooks.py`
**行数**: 900

### 功能描述

Shell-script hooks bridge.

Reads the ``hooks:`` block from ``cli-config.yaml``, prompts the user for
consent on first use of each ``(event, command)`` pair, and registers
callbacks on the existing plugin hook manager so every existing
``invoke_hook()`` site dispatches to the configured shell script

### 核心类

- `ShellHookSpec`: Parsed and validated representation of a single ``hooks:`` entry.

### 核心函数

- `register_from_config()`: Register every configured shell hook on the plugin manager.

    ``cfg`` is the full parsed config d
- `iter_configured_hooks()`: Return the parsed ``ShellHookSpec`` entries from config without
    registering anything.  Used by `
- `reset_for_tests()`: Clear the idempotence set.  Test-only helper.
- `allowlist_path()`: Path to the per-user shell-hook allowlist file.
- `load_allowlist()`: Return the parsed allowlist, or an empty skeleton if absent.
- `save_allowlist()`: Atomically persist the allowlist via per-process ``mkstemp`` +
    ``os.replace``.  Cross-process re
- `revoke()`: Remove every allowlist entry matching ``command``.

    Returns the number of entries removed.  Does
- `allowlist_entry_for()`: Return the allowlist record for this pair, if any.
- `script_mtime_iso()`: ISO-8601 mtime of the resolved script path, or ``None`` if the
    script is missing.
- `script_is_executable()`: Return ``True`` iff ``command`` is runnable as configured.

    For a bare invocation (``/path/hook.
- `run_once()`: Fire a single shell-hook invocation with a synthetic payload.
    Used by ``hermes hooks test`` and 

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## skill_bundles.py

**路径**: `agent\skill_bundles.py`
**行数**: 411

### 功能描述

Skill bundles — aliases that load multiple skills under one slash command.

A skill bundle is a small YAML file that names a set of skills to load
together. Invoking ``/<bundle-name>`` from the CLI or gateway loads every
referenced skill's full content into a single user message, the same way
``/<sk

### 核心函数

- `scan_bundles()`: Scan the bundles directory and rebuild the cache.

    Returns the same mapping as :func:`get_skill_
- `get_skill_bundles()`: Return the current bundle mapping, rescanning when disk changed.

    Cheap to call repeatedly: only
- `resolve_bundle_command_key()`: Resolve a user-typed command to its canonical bundle slash key.

    Hyphens and underscores are tre
- `reload_bundles()`: Re-scan the bundles directory and return a diff.

    Mirrors :func:`agent.skill_commands.reload_ski
- `list_bundles()`: Return a sorted list of bundle info dicts for display.
- `build_bundle_invocation_message()`: Build the user message content for a bundle slash command invocation.

    Returns ``(message, loade
- `bundle_path_for()`: Return the canonical filesystem path for a bundle name.
- `save_bundle()`: Write a bundle to disk and invalidate the cache.

    Raises ``FileExistsError`` if the target exist
- `delete_bundle()`: Delete a bundle by name. Returns the deleted path.

    Raises ``FileNotFoundError`` if the bundle d
- `get_bundle()`: Look up a bundle by name (slug-normalized).

### 依赖关系

**依赖组件**: state-management, tool-system
**跨组件调用**: 是

---

## skill_commands.py

**路径**: `agent\skill_commands.py`
**行数**: 613

### 功能描述

Shared slash command helpers for skills.

Shared between CLI (cli.py) and gateway (gateway/run.py) so both surfaces
can invoke skills via /skill-name commands.

### 核心函数

- `extract_user_instruction_from_skill_message()`: Recover the user's instruction from a slash-skill-expanded turn.

    Returns:
        - The origina
- `scan_skill_commands()`: Scan ~/.hermes/skills/ and return a mapping of /command -> skill info.

    Returns:
        Dict ma
- `get_skill_commands()`: Return the current skill commands mapping (scan first if empty).

    Rescans when the active platfo
- `reload_skills()`: Re-scan the skills directory and return a diff of what changed.

    Rescans ``~/.hermes/skills/`` a
- `resolve_skill_command_key()`: Resolve a user-typed /command to its canonical skill_cmds key.

    Skills are always stored with hy
- `build_skill_invocation_message()`: Build the user message content for a skill slash command invocation.

    Args:
        cmd_key: The
- `build_preloaded_skills_prompt()`: Load one or more skills for session-wide CLI preloading.

    Returns (prompt_text, loaded_skill_nam

### 依赖关系

**依赖组件**: gateway, state-management, tool-system
**跨组件调用**: 是

---

## skill_preprocessing.py

**路径**: `agent\skill_preprocessing.py`
**行数**: 141

### 功能描述

Shared SKILL.md preprocessing helpers.

### 核心函数

- `load_skills_config()`: Load the ``skills`` section of config.yaml (best-effort).
- `substitute_template_vars()`: Replace ${HERMES_SKILL_DIR} / ${HERMES_SESSION_ID} in skill content.

    Only substitutes tokens fo
- `run_inline_shell()`: Execute a single inline-shell snippet and return its stdout (trimmed).

    Failures return a short 
- `expand_inline_shell()`: Replace every !`cmd` snippet in ``content`` with its stdout.

    Runs each snippet with the skill d
- `preprocess_skill_content()`: Apply configured SKILL.md template and inline-shell preprocessing.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## skill_utils.py

**路径**: `agent\skill_utils.py`
**行数**: 768

### 功能描述

Lightweight skill metadata utilities shared by prompt_builder and skills_tool.

This module intentionally avoids importing the tool registry, CLI config, or any
heavy dependency chain.  It is safe to import at module level without triggering
tool registration or provider resolution.

### 核心函数

- `is_excluded_skill_path()`: True if *path* should be skipped by active skill scanners.

    Use this on every ``SKILL.md`` path 
- `is_skill_support_path()`: True if *path* is under a support dir of an actual skill root.

    ``references/``, ``templates/``,
- `yaml_load()`: Parse YAML with lazy import and CSafeLoader preference.
- `parse_frontmatter()`: Parse YAML frontmatter from a markdown string.

    Uses yaml with CSafeLoader for full YAML support
- `skill_matches_platform()`: Return True when the skill is compatible with the current OS.

    Skills declare platform requireme
- `skill_matches_environment()`: Return True when the skill is relevant to the current runtime environment.

    Skills may declare a
- `get_disabled_skill_names()`: Read disabled skill names from config.yaml.

    Args:
        platform: Explicit platform name (e.g
- `get_external_skills_dirs()`: Read ``skills.external_dirs`` from config.yaml and return validated paths.

    Each entry is expand
- `get_all_skills_dirs()`: Return all skill directories: local ``~/.hermes/skills/`` first, then external.

    The local dir i
- `is_external_skill_path()`: Return True when ``path`` lives under a configured external skills dir.

    ``skills.external_dirs`
- `extract_skill_conditions()`: Extract conditional activation fields from parsed frontmatter.
- `extract_skill_config_vars()`: Extract config variable declarations from parsed frontmatter.

    Skills declare config.yaml settin
- `discover_all_skill_config_vars()`: Scan all enabled skills and collect their config variable declarations.

    Walks every skills dire
- `resolve_skill_config_values()`: Resolve current values for skill config vars from config.yaml.

    Skill config is stored under ``s
- `extract_skill_description()`: Extract a truncated description from parsed frontmatter.
- ... 还有 3 个函数

### 依赖关系

**依赖组件**: gateway, state-management, tool-system
**跨组件调用**: 是

---

## ssl_guard.py

**路径**: `agent\ssl_guard.py`
**行数**: 95

### 功能描述

Preventive SSL CA certificate checks for Hermes Agent.

This module catches broken CA bundle paths before OpenAI/httpx turns them into
opaque ``FileNotFoundError: [Errno 2] No such file or directory`` failures.

### 核心函数

- `verify_ca_bundle()`: Verify configured and bundled CA certificates are present and loadable.

    Raises:
        SSLConf
- `verify_ca_bundle_with_fallback()`: Backward-compatible wrapper for older call sites.

    The old PR name mentioned a platform fallback

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## stream_diag.py

**路径**: `agent\stream_diag.py`
**行数**: 281

### 功能描述

Stream diagnostics — per-attempt counters, exception chains, retry logging.

When a streaming chat-completions request dies mid-response, we want to
know why: which Cloudflare edge served the request, which OpenRouter
downstream provider answered, how many bytes/chunks we got before the
drop, the HT

### 核心函数

- `stream_diag_init()`: Return a fresh per-attempt diagnostic dict.

    Mutated in-place by the streaming functions and rea
- `stream_diag_capture_response()`: Snapshot interesting headers + HTTP status from the live stream.

    Called once at stream open (be
- `flatten_exception_chain()`: Return a compact ``Outer(msg) <- Inner(msg) <- ...`` rendering.

    OpenAI SDK wraps httpx errors a
- `log_stream_retry()`: Record a transient stream-drop and retry to ``agent.log``.

    Always logs a structured WARNING so 
- `emit_stream_drop()`: Emit a single user-visible line for a stream drop+retry.

    Both top-level agents and subagents an

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## subdirectory_hints.py

**路径**: `agent\subdirectory_hints.py`
**行数**: 271

### 功能描述

Progressive subdirectory hint discovery.

As the agent navigates into subdirectories via tool calls (read_file, terminal,
search_files, etc.), this module discovers and loads project context files
(AGENTS.md, CLAUDE.md, .cursorrules) from those directories.  Discovered hints
are appended to the tool

### 核心类

- `SubdirectoryHintTracker`: Track which directories the agent visits and load hints on first access.

    Usage::

        track

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## system_prompt.py

**路径**: `agent\system_prompt.py`
**行数**: 537

### 功能描述

System-prompt assembly for :class:`AIAgent`.

The agent's system prompt is built once per session and reused across all
turns — only context compression triggers a rebuild.  This keeps the
upstream prefix cache warm.  See ``hermes-agent-dev``'s
``references/system-prompt-invariant.md`` for the invar

### 核心函数

- `build_system_prompt_parts()`: Assemble the system prompt as three ordered parts.

    Returns a dict with three keys:
      * ``st
- `build_system_prompt()`: Assemble the full system prompt from all layers.

    Called once per session (cached on ``agent._ca
- `invalidate_system_prompt()`: Invalidate the cached system prompt, forcing a rebuild on the next turn.

    Called after context c
- `format_tools_for_system_message()`: Format tool definitions for the system message in the trajectory format.

    Returns:
        str: 

### 依赖关系

**依赖组件**: entry-points, gateway, tool-system
**跨组件调用**: 是

---

## think_scrubber.py

**路径**: `agent\think_scrubber.py`
**行数**: 387

### 功能描述

Stateful scrubber for reasoning/thinking blocks in streamed assistant text.

``run_agent._strip_think_blocks`` is regex-based and correct for a complete
string, but when it runs *per-delta* in ``_fire_stream_delta`` it destroys
the state that downstream consumers (CLI ``_stream_delta``, gateway
``Ga

### 核心类

- `StreamingThinkScrubber`: Stateful scrubber for streaming reasoning/thinking blocks.

    State machine:
      - ``_in_block``

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## thinking_timeout_guidance.py

**路径**: `agent\thinking_timeout_guidance.py`
**行数**: 137

### 功能描述

Thinking-timeout detection and user-facing guidance for reasoning models.

When a known reasoning model (NVIDIA Nemotron 3 Ultra, OpenAI o1/o3,
Anthropic Opus 4.x thinking, DeepSeek R1, Qwen QwQ, xAI Grok reasoning)
hits a transport-layer error before the first content token arrives, the
upstream pr

### 核心函数

- `is_thinking_timeout()`: Return True when a reasoning model's thinking phase hit a transport kill.

    Args:
        classif
- `build_thinking_timeout_guidance()`: Return the user-facing guidance string appended to ``_final_response``.

    Args:
        provider:

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## title_generator.py

**路径**: `agent\title_generator.py`
**行数**: 197

### 功能描述

Auto-generate short session titles from the first user/assistant exchange.

Runs asynchronously after the first response is delivered so it never
adds latency to the user-facing reply.

### 核心函数

- `generate_title()`: Generate a session title from the first exchange.

    Uses the main runtime's model when available,
- `auto_title_session()`: Generate and set a session title if one doesn't already exist.

    Called in a background thread af
- `maybe_auto_title()`: Fire-and-forget title generation after the first exchange.

    Only generates a title when:
    - T

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## tool_dispatch_helpers.py

**路径**: `agent\tool_dispatch_helpers.py`
**行数**: 449

### 功能描述

Tool-dispatch helpers — parallelism gating, multimodal envelopes, mutation tracking.

Pure module-level utilities extracted from ``run_agent.py``:

* ``_is_destructive_command`` — terminal-command heuristic used to gate
  parallel batch dispatch.
* ``_should_parallelize_tool_batch`` / ``_extract_par

### 核心函数

- `make_tool_result_message()`: Build a tool-result message dict with both the OpenAI-format ``name``
    field (required by the wir

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## tool_executor.py

**路径**: `agent\tool_executor.py`
**行数**: 1539

### 功能描述

Tool-call execution — sequential and concurrent dispatch.

Both AIAgent methods (``_execute_tool_calls_sequential`` and
``_execute_tool_calls_concurrent``) live here as module-level
functions that take the parent ``AIAgent`` as their first argument.

``run_agent`` keeps thin wrappers so existing cal

### 核心函数

- `execute_tool_calls_concurrent()`: Execute multiple tool calls concurrently using a thread pool.

    Results are collected in the orig
- `execute_tool_calls_sequential()`: Execute tool calls sequentially (original behavior). Used for single calls or interactive tools.

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, llm-client, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## tool_guardrails.py

**路径**: `agent\tool_guardrails.py`
**行数**: 476

### 功能描述

Pure tool-call loop guardrail primitives.

The controller in this module is intentionally side-effect free: it tracks
per-turn tool-call observations and returns decisions. Runtime code owns whether
those decisions become warning guidance, synthetic tool results, or controlled
turn halts.

### 核心类

- `ToolCallGuardrailConfig`: Thresholds for per-turn tool-call loop detection.

    Warnings are enabled by default and never pre
- `ToolCallSignature`: Stable, non-reversible identity for a tool name plus canonical args.
- `ToolGuardrailDecision`: Decision returned by the tool-call guardrail controller.
- `ToolCallGuardrailController`: Per-turn controller for repeated failed/non-progressing tool calls.

### 核心函数

- `canonical_tool_args()`: Return sorted compact JSON for parsed tool arguments.
- `classify_tool_failure()`: Safety-fallback classifier used only when callers don't pass ``failed``.

    Mirrors ``agent.displa
- `toolguard_synthetic_result()`: Build a synthetic role=tool content string for a blocked tool call.
- `append_toolguard_guidance()`: Append runtime guidance to the current tool result content.

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## tool_result_classification.py

**路径**: `agent\tool_result_classification.py`
**行数**: 27

### 功能描述

Shared helpers for classifying tool result payloads.

### 核心函数

- `file_mutation_result_landed()`: Return True when a file mutation result proves the write landed.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## trajectory.py

**路径**: `agent\trajectory.py`
**行数**: 57

### 功能描述

Trajectory saving utilities and static helpers.

_convert_to_trajectory_format stays as an AIAgent method (batch_runner.py
calls agent._convert_to_trajectory_format). Only the static helpers and
the file-write logic live here.

### 核心函数

- `convert_scratchpad_to_think()`: Convert <REASONING_SCRATCHPAD> tags to <think> tags.
- `has_incomplete_scratchpad()`: Check if content has an opening <REASONING_SCRATCHPAD> without a closing tag.
- `save_trajectory()`: Append a trajectory entry to a JSONL file.

    Args:
        trajectory: The ShareGPT-format conver

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## transcription_provider.py

**路径**: `agent\transcription_provider.py`
**行数**: 194

### 功能描述

Transcription Provider ABC
==========================

Defines the pluggable-backend interface for speech-to-text. Providers
register instances via
:meth:`PluginContext.register_transcription_provider`; the active one
(selected via ``stt.provider`` in ``config.yaml``) services every
:func:`tools.tra

### 核心类

- `TranscriptionProvider`: Abstract base class for a speech-to-text backend.

    Subclasses must implement :attr:`name` and :m

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## transcription_registry.py

**路径**: `agent\transcription_registry.py`
**行数**: 123

### 功能描述

Transcription Provider Registry
================================

Central map of registered STT providers. Populated by plugins at
import-time via :meth:`PluginContext.register_transcription_provider`;
consumed by :mod:`tools.transcription_tools` to dispatch
:func:`transcribe_audio` calls to the act

### 核心函数

- `register_provider()`: Register a transcription provider.

    Rejects:

    - Non-:class:`TranscriptionProvider` instances
- `list_providers()`: Return all registered providers, sorted by name.
- `get_provider()`: Return the provider registered under *name*, or None.

    Name matching is case-insensitive and whi

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `agent\transports\__init__.py`
**行数**: 69

### 功能描述

Transport layer types and registry for provider response normalization.

Usage:
    from agent.transports import get_transport
    transport = get_transport("anthropic_messages")
    result = transport.normalize_response(raw_response)

### 核心函数

- `register_transport()`: Register a transport class for an api_mode string.
- `get_transport()`: Get a transport instance for the given api_mode.

    Returns None if no transport is registered for

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## anthropic.py

**路径**: `agent\transports\anthropic.py`
**行数**: 252

### 功能描述

Anthropic Messages API transport.

Delegates to the existing adapter functions in agent/anthropic_adapter.py.
This transport owns format conversion and normalization — NOT client lifecycle.

### 核心类

- `AnthropicTransport`: Transport for api_mode='anthropic_messages'.

    Wraps the existing functions in anthropic_adapter.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## base.py

**路径**: `agent\transports\base.py`
**行数**: 90

### 功能描述

Abstract base for provider transports.

A transport owns the data path for one api_mode:
  convert_messages → convert_tools → build_kwargs → normalize_response

It does NOT own: client construction, streaming, credential refresh,
prompt caching, interrupt handling, or retry logic.  Those stay on AIA

### 核心类

- `ProviderTransport`: Base class for provider-specific format conversion and normalization.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## bedrock.py

**路径**: `agent\transports\bedrock.py`
**行数**: 155

### 功能描述

AWS Bedrock Converse API transport.

Delegates to the existing adapter functions in agent/bedrock_adapter.py.
Bedrock uses its own boto3 client (not the OpenAI SDK), so the transport
owns format conversion and normalization, while client construction and
boto3 calls stay on AIAgent.

### 核心类

- `BedrockTransport`: Transport for api_mode='bedrock_converse'.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## chat_completions.py

**路径**: `agent\transports\chat_completions.py`
**行数**: 738

### 功能描述

OpenAI Chat Completions transport.

Handles the default api_mode ('chat_completions') used by ~16 OpenAI-compatible
providers (OpenRouter, Nous, NVIDIA, Qwen, Ollama, DeepSeek, xAI, Kimi, etc.).

Messages and tools are already in OpenAI format — convert_messages and
convert_tools are near-identity. 

### 核心类

- `ChatCompletionsTransport`: Transport for api_mode='chat_completions'.

    The default path for OpenAI-compatible providers.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## codex.py

**路径**: `agent\transports\codex.py`
**行数**: 470

### 功能描述

OpenAI Responses API (Codex) transport.

Delegates to the existing adapter functions in agent/codex_responses_adapter.py.
This transport owns format conversion and normalization — NOT client lifecycle,
streaming, or the _run_codex_stream() call path.

### 核心类

- `ResponsesApiTransport`: Transport for api_mode='codex_responses'.

    Wraps the functions extracted into codex_responses_ad

### 依赖关系

**依赖组件**: entry-points, llm-client
**跨组件调用**: 是

---

## codex_app_server.py

**路径**: `agent\transports\codex_app_server.py`
**行数**: 401

### 功能描述

Codex app-server JSON-RPC client.

Speaks the protocol documented in codex-rs/app-server/README.md (codex 0.125+).
Transport is newline-delimited JSON-RPC 2.0 over stdio: spawn `codex app-server`,
do an `initialize` handshake, then drive `thread/start` + `turn/start` and
consume streaming `item/*` n

### 核心类

- `CodexAppServerError`: Raised on JSON-RPC errors from the app-server.
- `_Pending`
- `CodexAppServerClient`: Minimal JSON-RPC 2.0 client for `codex app-server` over stdio.

    Threading model:
      - Spawnin

### 核心函数

- `parse_codex_version()`: Parse `codex --version` output. Returns (major, minor, patch) or None.
- `check_codex_binary()`: Verify codex CLI is installed and meets minimum version.

    Returns (ok, message). Used by setup w

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## codex_app_server_session.py

**路径**: `agent\transports\codex_app_server_session.py`
**行数**: 877

### 功能描述

Session adapter for codex app-server runtime.

Owns one Codex thread per Hermes session. Drives `turn/start`, consumes
streaming notifications via CodexEventProjector, handles server-initiated
approval requests (apply_patch, exec command), translates cancellation,
and returns a clean turn result tha

### 核心类

- `TurnResult`: Result of one user→assistant→tool turn through the codex app-server.
- `_ServerRequestRouting`: Default policies for codex-side approval requests when no interactive
    callback is wired in. Thes
- `CodexAppServerSession`: One Codex thread per Hermes session, lifetime owned by AIAgent.

    Not thread-safe — one caller dr

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## codex_event_projector.py

**路径**: `agent\transports\codex_event_projector.py`
**行数**: 313

### 功能描述

Projects codex app-server events into Hermes' messages list.

The translator that lets Hermes' memory/skill review keep working under the
Codex runtime: it converts Codex `item/*` notifications into the standard
OpenAI-shaped `{role, content, tool_calls, tool_call_id}` entries that
`agent/curator.py

### 核心类

- `ProjectionResult`: Output of projecting one Codex item.

    `messages` is a list because some Codex items produce two 
- `CodexEventProjector`: Stateful projector consuming Codex notifications in arrival order.

    Owns the in-progress reasoni

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## hermes_tools_mcp_server.py

**路径**: `agent\transports\hermes_tools_mcp_server.py`
**行数**: 234

### 功能描述

Hermes-tools-as-MCP server for the codex_app_server runtime.

When the user runs `openai/*` turns through the codex app-server, codex
owns the loop and builds its own tool list. By default, that means
Hermes' richer tool surface — web search, browser automation,
delegate_task subagents, vision analy

### 核心函数

- `main()`: Entry point for `python -m agent.transports.hermes_tools_mcp_server`.

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## types.py

**路径**: `agent\transports\types.py`
**行数**: 175

### 功能描述

Shared types for normalized provider responses.

These dataclasses define the canonical shape that all provider adapters
normalize responses to.  The shared surface is intentionally minimal —
only fields that every downstream consumer reads are top-level.
Protocol-specific state goes in ``provider_d

### 核心类

- `ToolCall`: A normalized tool call from any provider.

    ``id`` is the protocol's canonical identifier — what 
- `Usage`: Token usage from an API response.
- `NormalizedResponse`: Normalized API response from any provider.

    Shared fields are truly cross-provider — every calle

### 核心函数

- `build_tool_call()`: Build a ``ToolCall``, auto-serialising *arguments* if it's a dict.

    Any extra keyword arguments 
- `map_finish_reason()`: Translate a provider-specific stop reason to the normalised set.

    Falls back to ``"stop"`` for u

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tts_provider.py

**路径**: `agent\tts_provider.py`
**行数**: 275

### 功能描述

Text-to-Speech Provider ABC
============================

Defines the pluggable-backend interface for text-to-speech synthesis.
Providers register instances via
``PluginContext.register_tts_provider()``; the active one (selected via
``tts.provider`` in ``config.yaml``) services every ``text_to_speec

### 核心类

- `TTSProvider`: Abstract base class for a text-to-speech backend.

    Subclasses must implement :attr:`name` and :m

### 核心函数

- `resolve_output_format()`: Clamp an output_format value to the valid set.

    Invalid values are coerced to :data:`DEFAULT_OUT

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tts_registry.py

**路径**: `agent\tts_registry.py`
**行数**: 134

### 功能描述

TTS Provider Registry
=====================

Central map of registered TTS providers. Populated by plugins at
import-time via :meth:`PluginContext.register_tts_provider`; consumed
by :mod:`tools.tts_tool` to dispatch ``text_to_speech`` tool calls to
the active plugin backend **when** the configured 

### 核心函数

- `register_provider()`: Register a TTS provider.

    Rejects:

    - Non-:class:`TTSProvider` instances (raises :class:`Typ
- `list_providers()`: Return all registered providers, sorted by name.
- `get_provider()`: Return the provider registered under *name*, or None.

    Name matching is case-insensitive and whi

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## turn_context.py

**路径**: `agent\turn_context.py`
**行数**: 487

### 功能描述

Per-turn setup for ``run_conversation`` (the turn prologue).

``run_conversation`` opened with ~470 lines of straight-line setup before the
tool-calling loop ever started: stdio guarding, runtime-main wiring, retry-counter
resets, user-message sanitization, todo/nudge-counter hydration, system-promp

### 核心类

- `TurnContext`: Values produced by the turn prologue and consumed by the turn loop.

### 核心函数

- `build_turn_context()`: Run the once-per-turn setup and return the loop's input context.

    The callables/helpers the orig

### 依赖关系

**依赖组件**: cli, llm-client, tool-system
**跨组件调用**: 是

---

## turn_finalizer.py

**路径**: `agent\turn_finalizer.py`
**行数**: 482

### 功能描述

Post-loop turn finalization for ``run_conversation``.

Extracted from ``agent/conversation_loop.py`` as part of the god-file
decomposition campaign (``~/.hermes/plans/god-file-decomposition.md``, Phase 1
step 4 — the post-loop ``TurnFinalizer`` seam). ``run_conversation``'s tail
(everything after th

### 核心函数

- `finalize_turn()`: Run the post-loop finalization and return the turn ``result`` dict.

    Lifted verbatim from ``run_

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## turn_retry_state.py

**路径**: `agent\turn_retry_state.py`
**行数**: 75

### 功能描述

Per-attempt recovery bookkeeping for the conversation turn loop.

The inner retry loop in ``run_conversation`` (``while retry_count <
max_retries``) makes several distinct recovery attempts on a single model API
call: a credential-pool 429 retry, a per-provider OAuth refresh (codex,
anthropic, nous,

### 核心类

- `TurnRetryState`: One-shot recovery guards + restart signals for a single API-call attempt.

    A fresh instance is c

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## usage_pricing.py

**路径**: `agent\usage_pricing.py`
**行数**: 945

### 功能描述

Normalize a Bedrock model id to its bare foundation-model form.

    Bedrock cross-region inference profiles prefix the foundation model id
    with a region scope (``us.`` / ``global.`` / ``eu.`` / `

### 核心类

- `CanonicalUsage`
- `BillingRoute`
- `PricingEntry`
- `CostResult`

### 核心函数

- `resolve_billing_route()`
- `get_pricing_entry()`
- `normalize_usage()`: Normalize raw API response usage into canonical token buckets.

    Handles three API shapes:
    - 
- `estimate_usage_cost()`
- `has_known_pricing()`: Check whether we have pricing data for this model+route.

    Uses direct lookup instead of routing 
- `format_duration_compact()`
- `format_token_count_compact()`

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## verification_evidence.py

**路径**: `agent\verification_evidence.py`
**行数**: 619

### 功能描述

Coding verification evidence ledger.

This module records what the agent actually proved while working in a code
workspace. It is deliberately passive: it never decides to run a suite, never
blocks completion, and never upgrades targeted checks into "repo green".

### 核心类

- `VerificationEvidence`: A classified command result worth recording.

### 核心函数

- `classify_verification_command()`: Classify a terminal command as verification evidence, if applicable.
- `record_terminal_result()`: Record a foreground terminal result when it is verification evidence.
- `mark_workspace_edited()`: Mark verification evidence stale after a successful file edit.
- `verification_status()`: Return the best known verification state for a session/workspace.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## verification_stop.py

**路径**: `agent\verification_stop.py`
**行数**: 241

### 功能描述

Turn-end verification guard for coding edits.

This module is intentionally policy-only. It never runs checks itself; it turns
the passive verification ledger into a bounded follow-up when the model tries to
finish immediately after editing code without fresh evidence.

### 核心函数

- `verify_on_stop_enabled()`: Return whether edit -> verify-before-finish behavior is enabled.

    Precedence: an explicit ``HERM
- `build_verify_on_stop_nudge()`: Return a synthetic follow-up when edited code lacks fresh verification.

### 依赖关系

**依赖组件**: cli, gateway
**跨组件调用**: 是

---

## video_gen_provider.py

**路径**: `agent\video_gen_provider.py`
**行数**: 300

### 功能描述

Video Generation Provider ABC
=============================

Defines the pluggable-backend interface for video generation. Providers register
instances via ``PluginContext.register_video_gen_provider()``; the active one
(selected via ``video_gen.provider`` in ``config.yaml``) services every
``video_

### 核心类

- `VideoGenProvider`: Abstract base class for a video generation backend.

    Subclasses must implement :meth:`generate`.

### 核心函数

- `save_b64_video()`: Decode base64 video data and write under ``$HERMES_HOME/cache/videos/``.

    Returns the absolute :
- `save_bytes_video()`: Write raw video bytes (e.g. an HTTP download body) to the cache.
- `success_response()`: Build a uniform success response dict.

    ``video`` may be an HTTP URL or an absolute filesystem p
- `error_response()`: Build a uniform error response dict.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## video_gen_registry.py

**路径**: `agent\video_gen_registry.py`
**行数**: 118

### 功能描述

Video Generation Provider Registry
==================================

Central map of registered providers. Populated by plugins at import-time via
``PluginContext.register_video_gen_provider()``; consumed by the
``video_generate`` tool to dispatch each call to the active backend.

Active selection


### 核心函数

- `register_provider()`: Register a video generation provider.

    Re-registration (same ``name``) overwrites the previous e
- `list_providers()`: Return all registered providers, sorted by name.
- `get_provider()`: Return the provider registered under *name*, or None.
- `get_active_provider()`: Resolve the currently-active provider.

    Reads ``video_gen.provider`` from config.yaml; falls bac

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## web_search_provider.py

**路径**: `agent\web_search_provider.py`
**行数**: 186

### 功能描述

Web Search Provider ABC
=======================

Defines the pluggable-backend interface for web search and content extraction.
Providers register instances via ``PluginContext.register_web_search_provider()``;
the active one (selected via ``web.search_backend`` / ``web.extract_backend`` /
``web.bac

### 核心类

- `WebSearchProvider`: Abstract base class for a web search/extract backend.

    Subclasses must implement :meth:`is_avail

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## web_search_registry.py

**路径**: `agent\web_search_registry.py`
**行数**: 246

### 功能描述

Web Search Provider Registry
============================

Central map of registered web providers. Populated by plugins at import-time
via :meth:`PluginContext.register_web_search_provider`; consumed by the
``web_search`` and ``web_extract`` tool wrappers in :mod:`tools.web_tools` to
dispatch each 

### 核心函数

- `register_provider()`: Register a web search/extract provider.

    Re-registration (same ``name``) overwrites the previous
- `list_providers()`: Return all registered providers, sorted by name.
- `get_provider()`: Return the provider registered under *name*, or None.
- `get_active_search_provider()`: Resolve the currently-active web search provider.

    Reads ``web.search_backend`` (preferred) or `
- `get_active_extract_provider()`: Resolve the currently-active web extract provider.

    Reads ``web.extract_backend`` (preferred) or

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

