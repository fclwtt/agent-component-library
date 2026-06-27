# memory-system 模块详细说明

本组件包含 30 个模块。

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

**依赖组件**: agent-engine, cli, entry-points, state-management
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

## memory_oauth.py

**路径**: `hermes_cli\memory_oauth.py`
**行数**: 84

### 功能描述

HTTP routes for memory-provider OAuth connect, mounted by ``web_server``.

Kept out of ``web_server.py`` so the memory feature's surface stays in the
memory layer. Dispatch is by convention: a provider's flow lives at
``plugins.memory.<provider>.oauth_flow`` exposing ``start_loopback_flow_background

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## memory_providers.py

**路径**: `hermes_cli\memory_providers.py`
**行数**: 150

### 功能描述

Declarative configuration schema for desktop memory providers.

Each memory provider *declares* its configurable surface here — the fields, their
types, which values are secrets, and (for selects) the allowed options. A single
generic renderer in the desktop UI and a single generic ``GET/PUT
/api/me

### 核心类

- `ProviderFieldOption`: A single choice for a ``select`` field.
- `ProviderField`: One configurable field on a memory provider.

    A field is stored in exactly one place, decided by
- `MemoryProvider`: A declared memory provider and its configurable fields.

### 核心函数

- `get_memory_provider()`: Return the declared provider for ``name``, or ``None`` if undeclared.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## memory_setup.py

**路径**: `hermes_cli\memory_setup.py`
**行数**: 519

### 功能描述

hermes memory setup|status — configure memory provider plugins.

Auto-detects installed memory providers via the plugin system.
Interactive curses-based UI for provider selection, then walks through
the provider's config schema. Writes config to config.yaml + .env.

### 核心函数

- `cmd_setup_provider()`: Run memory setup for a specific provider, skipping the picker.
- `cmd_setup()`: Interactive memory provider setup wizard.
- `cmd_status()`: Show current memory provider config.
- `memory_command()`: Route memory subcommands.

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## memory.py

**路径**: `hermes_cli\subcommands\memory.py`
**行数**: 54

### 功能描述

``hermes memory`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_memory_parser()`: Attach the ``memory`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## memory_manager.py

**路径**: `memory_manager.py`
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

**依赖组件**: agent-engine, cli, entry-points, state-management
**跨组件调用**: 是

---

## memory_provider.py

**路径**: `memory_provider.py`
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

## __init__.py

**路径**: `plugins\memory\__init__.py`
**行数**: 451

### 功能描述

Memory provider plugin discovery.

Scans two directories for memory provider plugins:

1. Bundled providers: ``plugins/memory/<name>/`` (shipped with hermes-agent)
2. User-installed providers: ``$HERMES_HOME/plugins/<name>/``

Each subdirectory must contain ``__init__.py`` with a class implementing


### 核心类

- `_ProviderCollector`: Fake plugin context that captures register_memory_provider calls.

### 核心函数

- `find_provider_dir()`: Resolve a provider name to its directory.

    Checks bundled first, then user-installed.
- `discover_memory_providers()`: Scan bundled and user-installed directories for available providers.

    Returns list of (name, des
- `load_memory_provider()`: Load and return a MemoryProvider instance by name.

    Checks both bundled (``plugins/memory/<name>
- `discover_plugin_cli_commands()`: Return CLI commands for the **active** memory plugin only.

    Only one memory provider can be acti

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\byterover\__init__.py`
**行数**: 385

### 功能描述

ByteRover memory plugin — MemoryProvider interface.

Persistent memory via the ByteRover CLI (``brv``). Organizes knowledge into
a hierarchical context tree with tiered retrieval (fuzzy text → LLM-driven
search). Local-first with optional cloud sync.

Original PR #3499 by hieuntg81, adapted to Memor

### 核心类

- `ByteRoverMemoryProvider`: ByteRover persistent memory via the brv CLI.

### 核心函数

- `register()`: Register ByteRover as a memory provider plugin.

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\hindsight\__init__.py`
**行数**: 1969

### 功能描述

Hindsight memory plugin — MemoryProvider interface.

Long-term memory with knowledge graph, entity resolution, and multi-strategy
retrieval. Supports cloud (API key) and local modes.

Configurable request timeout via HINDSIGHT_TIMEOUT env var or config.json.
Configurable embedded daemon idle timeout

### 核心类

- `HindsightMemoryProvider`: Hindsight long-term memory with knowledge graph and multi-strategy retrieval.

### 核心函数

- `register()`: Register Hindsight as a memory provider plugin.

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\holographic\__init__.py`
**行数**: 409

### 功能描述

hermes-memory-store — holographic memory plugin using MemoryProvider interface.

Registers as a MemoryProvider plugin, giving the agent structured fact storage
with entity resolution, trust scoring, and HRR-based compositional retrieval.

Original plugin by dusterbloom (PR #2351), adapted to the Mem

### 核心类

- `HolographicMemoryProvider`: Holographic memory with structured facts, entity resolution, and HRR retrieval.

### 核心函数

- `register()`: Register the holographic memory provider with the plugin system.

### 依赖关系

**依赖组件**: agent-engine, cli, state-management
**跨组件调用**: 是

---

## holographic.py

**路径**: `plugins\memory\holographic\holographic.py`
**行数**: 204

### 功能描述

Holographic Reduced Representations (HRR) with phase encoding.

HRRs are a vector symbolic architecture for encoding compositional structure
into fixed-width distributed representations. This module uses *phase vectors*:
each concept is a vector of angles in [0, 2π). The algebraic operations are:

 

### 核心函数

- `encode_atom()`: Deterministic phase vector via SHA-256 counter blocks.

    Uses hashlib (not numpy RNG) for cross-p
- `bind()`: Circular convolution = element-wise phase addition.

    Binding associates two concepts into a sing
- `unbind()`: Circular correlation = element-wise phase subtraction.

    Unbinding retrieves the value associated
- `bundle()`: Superposition via circular mean of complex exponentials.

    Bundling merges multiple vectors into 
- `similarity()`: Phase cosine similarity. Range [-1, 1].

    Returns 1.0 for identical vectors, near 0.0 for random 
- `encode_text()`: Bag-of-words: bundle of atom vectors for each token.

    Tokenizes by lowercasing, splitting on whi
- `encode_fact()`: Structured encoding: content bound to ROLE_CONTENT, each entity bound to ROLE_ENTITY, all bundled.


- `phases_to_bytes()`: Serialize phase vector to bytes. float64 tobytes — 8 KB at dim=1024.
- `bytes_to_phases()`: Deserialize bytes back to phase vector. Inverse of phases_to_bytes.

    The .copy() call is require
- `snr_estimate()`: Signal-to-noise ratio estimate for holographic storage.

    SNR = sqrt(dim / n_items) when n_items 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## retrieval.py

**路径**: `plugins\memory\holographic\retrieval.py`
**行数**: 594

### 功能描述

Hybrid keyword/BM25 retrieval for the memory store.

Ported from KIK memory_agent.py — combines FTS5 full-text search with
Jaccard similarity reranking and trust-weighted scoring.

### 核心类

- `FactRetriever`: Multi-strategy fact retrieval with trust-weighted scoring.

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## store.py

**路径**: `plugins\memory\holographic\store.py`
**行数**: 579

### 功能描述

SQLite-backed fact store with entity resolution and trust scoring.
Single-user Hermes memory store plugin.

### 核心类

- `MemoryStore`: SQLite-backed fact store with entity resolution and trust scoring.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\honcho\__init__.py`
**行数**: 1433

### 功能描述

Honcho memory plugin — MemoryProvider for Honcho AI-native memory.

Provides cross-session user modeling with dialectic Q&A, semantic search,
peer cards, and persistent conclusions via the Honcho SDK. Honcho provides AI-native cross-session user
modeling with dialectic Q&A, semantic search, peer car

### 核心类

- `HonchoMemoryProvider`: Honcho AI-native memory with dialectic Q&A and persistent user modeling.

### 核心函数

- `register()`: Register Honcho as a memory provider plugin.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, state-management
**跨组件调用**: 是

---

## cli.py

**路径**: `plugins\memory\honcho\cli.py`
**行数**: 1869

### 功能描述

CLI commands for Honcho integration management.

Handles: hermes honcho setup | status | sessions | map | peer

### 核心函数

- `clone_honcho_for_profile()`: Auto-clone Honcho config for a new profile from the default host block.

    Called during profile c
- `cmd_enable()`: Enable Honcho for the active profile.
- `cmd_disable()`: Disable Honcho for the active profile.
- `cmd_sync()`: Sync Honcho config to all existing profiles.

    Scans all Hermes profiles and creates host blocks 
- `sync_honcho_profiles_quiet()`: Sync Honcho host blocks for all profiles. Returns count of newly created blocks.

    Called from `h
- `cmd_setup()`: Interactive Honcho setup wizard.
- `cmd_status()`: Show current Honcho config and connection status.
- `cmd_peers()`: Show peer identities across all profiles.
- `cmd_sessions()`: List known directory → session name mappings.
- `cmd_map()`: Map current directory to a Honcho session name.
- `cmd_peer()`: Show or update peer names and dialectic reasoning level.
- `cmd_mode()`: Show or set the recall mode.
- `cmd_strategy()`: Show or set the session strategy.
- `cmd_tokens()`: Show or set token budget settings.
- `cmd_identity()`: Seed AI peer identity or show both peer representations.
- ... 还有 3 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, state-management
**跨组件调用**: 是

---

## client.py

**路径**: `plugins\memory\honcho\client.py`
**行数**: 921

### 功能描述

Honcho client initialization and configuration.

Resolution order for config file:
  1. $HERMES_HOME/honcho.json  (instance-local, enables isolated Hermes instances)
  2. ~/.honcho/config.json     (global, shared across all Honcho-enabled apps)
  3. Environment variables     (HONCHO_API_KEY, HONCHO_

### 核心类

- `HonchoClientConfig`: Configuration for Honcho client, resolved for a specific host.

### 核心函数

- `profile_host_key()`: Return the safe Honcho host key for a Hermes profile.
- `resolve_active_host()`: Derive the Honcho host key from the active Hermes profile.

    Resolution order:
      1. HERMES_HO
- `resolve_global_config_path()`: Return the shared Honcho config path for the current HOME.
- `resolve_config_path()`: Return the active Honcho config path.

    Resolution order:
      1. $HERMES_HOME/honcho.json      
- `get_honcho_client()`: Get or create the Honcho client singleton.

    When no config is provided, attempts to load ~/.honc
- `reset_honcho_client()`: Reset the Honcho client singleton (useful for testing).

### 依赖关系

**依赖组件**: cli, plugin-system, state-management, tool-system
**跨组件调用**: 是

---

## oauth.py

**路径**: `plugins\memory\honcho\oauth.py`
**行数**: 372

### 功能描述

OAuth credential storage and refresh for the Honcho memory provider.

An access token authenticates exactly like a scoped API key, so it is stored
as the host's ``apiKey``; this module exchanges the refresh token before
expiry to keep it live.

Refresh tokens rotate with single-use reuse detection: 

### 核心类

- `OAuthCredential`: An OAuth grant as stored in a honcho.json host block.

    ``access_token`` mirrors the host's ``api

### 核心函数

- `is_oauth_access_token()`: True when ``value`` is an OAuth access token (vs a static API key).
- `ensure_fresh_token()`: Return ``(access_token, refreshed)`` for ``host``, refreshing if near expiry.

    Returns ``(None, 
- `install_grant()`: Apply a fresh OAuth grant to ``path`` for ``host``.

    Deep-merges the grant's ``config`` (the man
- `apply_token_to_client()`: Rotate the live Honcho client's Bearer in place. Returns success.

    The SDK builds its auth heade

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## oauth_flow.py

**路径**: `plugins\memory\honcho\oauth_flow.py`
**行数**: 432

### 功能描述

Browser sign-in flow for the Honcho memory provider — no CLI step.

``begin_authorization`` / ``complete_authorization`` are the transport-agnostic
core: the code can arrive via the loopback listener here or a future
``hermes://`` handler. Endpoints are env-overridable with local-dev defaults
becaus

### 核心类

- `OAuthEndpoints`: Resolved authorization-server URLs and client identity.
- `_Pending`
- `FlowStatus`

### 核心函数

- `resolve_endpoints()`: Resolve OAuth endpoints, zero-config by default.

    Keys off the host's honcho ``environment`` (pr
- `begin_authorization()`: Start an authorization: return ``(authorize_url, state)`` and stash PKCE.

    ``source`` tags the a
- `complete_authorization()`: Exchange ``code`` for a grant and persist it. Raises on bad state/exchange.

    ``apply_config=Fals
- `capture_loopback_code()`: Serve a single ``/callback`` GET on ``server`` and return ``(code, state)``.

    Replies with a clo
- `authorize_via_loopback()`: Drive the full loopback flow: open browser → capture code → exchange → persist.

    ``open_url`` de
- `get_flow_status()`
- `start_loopback_flow_background()`: Launch the loopback flow in a daemon thread; returns the initial status.

    Idempotent while a flo

### 依赖关系

**依赖组件**: acp-adapter, agent-engine
**跨组件调用**: 是

---

## session.py

**路径**: `plugins\memory\honcho\session.py`
**行数**: 1345

### 功能描述

Honcho-based session management for conversation history.

### 核心类

- `HonchoSession`: A conversation session backed by Honcho.

    Provides a local message cache that syncs to Honcho's

- `HonchoSessionManager`: Manages conversation sessions using Honcho.

    Runs alongside hermes' existing SQLite state and fi

### 依赖关系

**依赖组件**: acp-adapter, agent-engine
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\mem0\__init__.py`
**行数**: 563

### 功能描述

Mem0 memory plugin — MemoryProvider interface.

Server-side LLM fact extraction, semantic search, and automatic deduplication
via the Mem0 Platform API (cloud) or OSS (self-hosted) via Memory.

Original PR #2933 by kartik-mem0, adapted to MemoryProvider ABC.

Configuration
-------------
Secret (live

### 核心类

- `Mem0MemoryProvider`: Mem0 memory with server-side extraction and semantic search.

    Supports Platform API (cloud) and 

### 核心函数

- `register()`: Register Mem0 as a memory provider plugin.

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## _backend.py

**路径**: `plugins\memory\mem0\_backend.py`
**行数**: 244

### 功能描述

Backend abstraction for Mem0 Platform and OSS modes.

### 核心类

- `Mem0Backend`: Unified interface over Platform (MemoryClient) and OSS (Memory) backends.
- `PlatformBackend`: Wraps mem0.MemoryClient for Mem0 Platform (cloud API).
- `OSSBackend`: Wraps mem0.Memory for self-hosted (OSS) mode.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _oss_providers.py

**路径**: `plugins\memory\mem0\_oss_providers.py`
**行数**: 85

### 功能描述

OSS provider definitions for LLM, embedder, and vector store.

### 核心函数

- `validate_oss_config()`: Validate an OSS config dict. Returns list of error strings (empty = valid).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _setup.py

**路径**: `plugins\memory\mem0\_setup.py`
**行数**: 859

### 功能描述

Setup wizard for Mem0 plugin — interactive and flag-based modes.

### 核心函数

- `has_oss_flags()`: Check if OSS-related flags are present in sys.argv.
- `parse_flags()`: Parse CLI flags from argv. Returns dict of flag values.
- `build_oss_config()`: Build OSS config dict + env_writes from parsed flags.

    Returns (oss_config, env_writes) where os
- `post_setup()`: Entry point called by hermes memory setup framework.

    Only intercepts when OSS mode is requested

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\openviking\__init__.py`
**行数**: 3713

### 功能描述

OpenViking memory plugin — full bidirectional MemoryProvider interface.

Context database by Volcengine (ByteDance) that organizes agent knowledge
into a filesystem hierarchy (viking:// URIs) with tiered context loading,
automatic memory extraction, and session management.

Original PR #3369 by Miba

### 核心类

- `_OvcliProfile`
- `_OpenVikingHTTPError`
- `_VikingClient`: Thin HTTP client for the OpenViking REST API.
- `OpenVikingMemoryProvider`: Full bidirectional memory via OpenViking context database.

### 核心函数

- `register()`: Register OpenViking as a memory provider plugin.

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\retaindb\__init__.py`
**行数**: 767

### 功能描述

RetainDB memory plugin — MemoryProvider interface.

Cross-session memory via RetainDB cloud API.

Features:
- Correct API routes for all operations
- Durable SQLite write-behind queue (crash-safe, async ingest)
- Semantic search + user profile retrieval
- Context query with deduplication overlay
- D

### 核心类

- `_Client`
- `_WriteQueue`: SQLite-backed async write queue. Survives crashes — pending rows replay on startup.
- `RetainDBMemoryProvider`: RetainDB cloud memory — durable queue, semantic search, dialectic synthesis, shared files.

### 核心函数

- `register()`: Register RetainDB as a memory provider plugin.

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\memory\supermemory\__init__.py`
**行数**: 898

### 功能描述

Supermemory memory plugin using the MemoryProvider interface.

Provides semantic long-term memory with profile recall, semantic search,
explicit memory tools, cleaned turn capture, and session-end conversation ingest.

### 核心类

- `_SupermemoryClient`
- `SupermemoryMemoryProvider`

### 核心函数

- `register()`

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## memory_tool.py

**路径**: `tools\memory_tool.py`
**行数**: 1094

### 功能描述

Memory Tool Module - Persistent Curated Memory

Provides bounded, file-backed memory that persists across sessions. Two stores:
  - MEMORY.md: agent's personal notes and observations (environment facts, project
    conventions, tool quirks, things learned)
  - USER.md: what the agent knows about the

### 核心类

- `MemoryStore`: Bounded curated memory with file persistence. One instance per AIAgent.

    Maintains two parallel 

### 核心函数

- `get_memory_dir()`: Return the profile-scoped memories directory.
- `load_on_disk_store()`: Build a fresh on-disk :class:`MemoryStore`, honoring configured char limits.

    Use this from any 
- `memory_tool()`: Single entry point for the memory tool. Dispatches to MemoryStore methods.

    Two shapes:
      - 
- `check_memory_requirements()`: Memory tool has no external requirements -- always available.
- `apply_memory_pending()`: Replay a staged memory write directly against the store, bypassing the
    write gate. Called by the

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, security, state-management
**跨组件调用**: 是

---

