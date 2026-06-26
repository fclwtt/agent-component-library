# llm-client 模块详细说明

本组件包含 15 个模块。

---

## __init__.py

**路径**: `__init__.py`
**行数**: 192

### 功能描述

Provider module registry.

Provider profiles can live in two places:

1. Bundled plugins: ``plugins/model-providers/<name>/`` (shipped with hermes-agent)
2. User plugins: ``$HERMES_HOME/plugins/model-providers/<name>/``

Each plugin directory contains:
  - ``__init__.py`` — calls ``register_provider

### 核心函数

- `register_provider()`: Register a provider profile by name and aliases.

    Later registrations with the same name replace
- `get_provider_profile()`: Look up a provider profile by name or alias.

    Returns None if the provider has no profile (falls
- `list_providers()`: Return all registered provider profiles (one per canonical name).

### 依赖关系

**依赖组件**: cli, state-management
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

**依赖组件**: acp-adapter, agent-engine, entry-points, state-management, tool-system
**跨组件调用**: 是

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

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, state-management, tool-system
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

**依赖组件**: acp-adapter, agent-engine, tool-system
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

**依赖组件**: agent-engine, tool-system
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

**依赖组件**: agent-engine
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

**依赖组件**: agent-engine, cli, entry-points, state-management
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

**依赖组件**: cli
**跨组件调用**: 是

---

## anthropic_adapter.py

**路径**: `anthropic_adapter.py`
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

**依赖组件**: acp-adapter, agent-engine, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## auxiliary_client.py

**路径**: `auxiliary_client.py`
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

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## base.py

**路径**: `base.py`
**行数**: 218

### 功能描述

Provider profile base class.

A ProviderProfile declares everything about an inference provider in one place:
auth, endpoints, client quirks, request-time quirks. The transport reads this
instead of receiving 20+ boolean flags.

Provider profiles are DECLARATIVE — they describe the provider's behavi

### 核心类

- `ProviderProfile`: Base provider profile — subclass or instantiate with overrides.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `providers\__init__.py`
**行数**: 192

### 功能描述

Provider module registry.

Provider profiles can live in two places:

1. Bundled plugins: ``plugins/model-providers/<name>/`` (shipped with hermes-agent)
2. User plugins: ``$HERMES_HOME/plugins/model-providers/<name>/``

Each plugin directory contains:
  - ``__init__.py`` — calls ``register_provider

### 核心函数

- `register_provider()`: Register a provider profile by name and aliases.

    Later registrations with the same name replace
- `get_provider_profile()`: Look up a provider profile by name or alias.

    Returns None if the provider has no profile (falls
- `list_providers()`: Return all registered provider profiles (one per canonical name).

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## base.py

**路径**: `providers\base.py`
**行数**: 218

### 功能描述

Provider profile base class.

A ProviderProfile declares everything about an inference provider in one place:
auth, endpoints, client quirks, request-time quirks. The transport reads this
instead of receiving 20+ boolean flags.

Provider profiles are DECLARATIVE — they describe the provider's behavi

### 核心类

- `ProviderProfile`: Base provider profile — subclass or instantiate with overrides.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

