# plugin-system 模块详细说明

本组件包含 173 个模块。

---

## __init__.py

**路径**: `plugins\__init__.py`
**行数**: 2

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\browser\browser_use\__init__.py`
**行数**: 15

### 功能描述

Browser Use cloud browser plugin — bundled, auto-loaded.

Mirrors the ``plugins/web/<vendor>/`` layout: ``provider.py`` holds the
provider class; ``__init__.py::register`` instantiates and registers it.

### 核心函数

- `register()`: Register the Browser Use provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\browser\browser_use\provider.py`
**行数**: 318

### 功能描述

Browser Use cloud browser provider — plugin form.

Subclasses :class:`agent.browser_provider.BrowserProvider` (the plugin-facing
ABC introduced in PR #25214). The legacy in-tree module
``tools.browser_providers.browser_use`` was removed in the same PR; this file
is now the canonical implementation.


### 核心类

- `BrowserUseBrowserProvider`: Browser Use (https://browser-use.com) cloud browser backend.

    Dual auth: prefers a direct BROWSE

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\browser\browserbase\__init__.py`
**行数**: 16

### 功能描述

Browserbase cloud browser plugin — bundled, auto-loaded.

Mirrors the ``plugins/web/<vendor>/`` and ``plugins/image_gen/openai/``
layout: ``provider.py`` holds the provider class; ``__init__.py::register``
instantiates and registers it via the plugin context.

### 核心函数

- `register()`: Register the Browserbase provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\browser\browserbase\provider.py`
**行数**: 298

### 功能描述

Browserbase cloud browser provider — plugin form.

Subclasses :class:`agent.browser_provider.BrowserProvider` (the plugin-facing
ABC introduced in PR #25214). The legacy in-tree module
``tools.browser_providers.browserbase`` was removed in the same PR; this file
is now the canonical implementation.


### 核心类

- `BrowserbaseBrowserProvider`: Browserbase (https://browserbase.com) cloud browser backend.

    Direct credentials only — managed-

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\browser\firecrawl\__init__.py`
**行数**: 17

### 功能描述

Firecrawl cloud browser plugin — bundled, auto-loaded.

Distinct from ``plugins/web/firecrawl/`` (the web search/extract/crawl
plugin); both share the FIRECRAWL_API_KEY but speak to different endpoints
(``/v2/browser`` here vs ``/v2/search`` / ``/v2/scrape`` / ``/v2/crawl``
over there).

### 核心函数

- `register()`: Register the Firecrawl cloud-browser provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\browser\firecrawl\provider.py`
**行数**: 172

### 功能描述

Firecrawl cloud browser provider — plugin form.

Subclasses :class:`agent.browser_provider.BrowserProvider` (the plugin-facing
ABC introduced in PR #25214). The legacy in-tree module
``tools.browser_providers.firecrawl`` was removed in the same PR; this file
is now the canonical implementation.

Thi

### 核心类

- `FirecrawlBrowserProvider`: Firecrawl (https://firecrawl.dev) cloud browser backend.

    Cloud-browser path only — search/extra

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\context_engine\__init__.py`
**行数**: 286

### 功能描述

Context engine plugin discovery.

Scans ``plugins/context_engine/<name>/`` directories for context engine
plugins.  Each subdirectory must contain ``__init__.py`` with a class
implementing the ContextEngine ABC.

Context engines are separate from the general plugin system — they live
in the repo and

### 核心类

- `_EngineCollector`: Fake plugin context that captures register_context_engine calls.

    Plugin context engines using t

### 核心函数

- `discover_context_engines()`: Scan plugins/context_engine/ for available engines.

    Returns list of (name, description, is_avai
- `load_context_engine()`: Load and return a ContextEngine instance by name.

    Returns None if the engine is not found or fa

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\cron_providers\__init__.py`
**行数**: 357

### 功能描述

Cron scheduler provider plugin discovery.

Scans two directories for cron scheduler provider plugins:

1. Bundled providers: ``plugins/cron_providers/<name>/`` (shipped with hermes-agent)
2. User-installed providers: ``$HERMES_HOME/plugins/<name>/``

Each subdirectory must contain ``__init__.py`` wi

### 核心类

- `_ProviderCollector`: Fake plugin context that captures register_cron_scheduler calls.

### 核心函数

- `find_provider_dir()`: Resolve a provider name to its directory.

    Checks bundled first, then user-installed.
- `discover_cron_schedulers()`: Scan bundled and user-installed directories for available providers.

    Returns list of (name, des
- `load_cron_scheduler()`: Load and return a CronScheduler instance by name.

    Checks both bundled (``plugins/cron_providers

### 依赖关系

**依赖组件**: cron, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\cron_providers\chronos\__init__.py`
**行数**: 242

### 功能描述

Chronos — NAS-mediated managed cron provider (scale-to-zero).

Chronos (the Greek god of time, alongside Hermes) is the first non-default
``CronScheduler``. It lets a hosted gateway scale to zero while idle and still
fire cron jobs: instead of a 60s in-process ticker, it asks NAS to arm exactly
one 

### 核心类

- `ChronosCronScheduler`: NAS-mediated external cron provider.

### 核心函数

- `register()`: Plugin entrypoint — register the Chronos provider with the loader.

    Mirrors the memory-plugin sh

### 依赖关系

**依赖组件**: acp-adapter, cli, cron
**跨组件调用**: 是

---

## _nas_client.py

**路径**: `plugins\cron_providers\chronos\_nas_client.py`
**行数**: 124

### 功能描述

Thin HTTP client for the agent → NAS ``agent-cron`` endpoints (Chronos).

The Chronos provider speaks ONLY to NAS — it names no scheduler vendor and
holds no scheduler credentials. NAS owns the external scheduler (an internal
implementation detail) and that scheduler's account; the agent just asks N

### 核心类

- `NasCronClientError`: Raised when a NAS agent-cron call fails (non-2xx or transport error).
- `NasCronClient`: Minimal client for the agent→NAS provision/cancel/list endpoints.

    Uses the agent's refresh-awar

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## verify.py

**路径**: `plugins\cron_providers\chronos\verify.py`
**行数**: 104

### 功能描述

Inbound cron-fire token verification for Chronos (Phase 4E.1).

When NAS relays an external scheduler fire to the agent, it POSTs
``/api/cron/fire`` with a short-lived NAS-minted JWT. This module verifies that
JWT before any job runs — the security boundary for remotely-triggered job
execution.

We 

### 核心函数

- `verify_nas_fire_token()`: Verify a NAS-minted cron-fire JWT. Return decoded claims, or None.

    Checks (all must pass):
    
- `get_fire_verifier()`: Return the active inbound-fire verifier.

    Default = the NAS-JWT verifier. The DQ-4 escape hatch 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\dashboard_auth\basic\__init__.py`
**行数**: 492

### 功能描述

BasicAuthProvider — username/password dashboard auth (no OAuth IDP).

A self-hosted "just put a password on my dashboard" provider. It plugs
into the same ``DashboardAuthProvider`` framework as the Nous OAuth
provider, but authenticates with a username + password instead of an
OAuth redirect: it set

### 核心类

- `BasicAuthProvider`: Username/password provider with stateless HMAC-signed sessions.

### 核心函数

- `hash_password()`: Return a ``scrypt$n$r$p$<salt_b64>$<dk_b64>`` hash string.

    Use this to precompute ``password_ha
- `register()`: Plugin entry — registers BasicAuthProvider when credentials exist.

    Loopback / ``--insecure`` op

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\dashboard_auth\drain\__init__.py`
**行数**: 291

### 功能描述

DrainSecretProvider — shared-bearer-secret auth for the drain-control endpoint.

Task 2.0b of the safe-shutdown plan, and the FIRST consumer of the generic
non-interactive token-auth capability added in Task 2.0a
(``supports_token`` / ``verify_token`` on the ``DashboardAuthProvider`` ABC +
the route

### 核心类

- `DrainSecretProvider`: Non-interactive shared-bearer-secret provider for drain control.

### 核心函数

- `assess_secret_strength()`: Return a rejection reason if ``secret`` is too weak, else ``None``.

    Fail-closed entropy gate (d
- `register()`: Plugin entry — registers DrainSecretProvider when a strong secret is set.

    No-op (records a skip

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\dashboard_auth\nous\__init__.py`
**行数**: 668

### 功能描述

NousDashboardAuthProvider — Nous Portal OAuth (authorization-code + PKCE).

Implements ``nous-account-service/docs/agent-dashboard-oauth-contract.md``
(PR #180). The plugin auto-loads (bundled, kind=backend) but only registers
its provider when a client_id is configured — either via ``config.yaml`` 

### 核心类

- `NousDashboardAuthProvider`: Nous Portal OAuth via authorization-code + PKCE (S256).

### 核心函数

- `register()`: Plugin entry — called by the plugin loader at startup.

    Registers ``NousDashboardAuthProvider`` 

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\dashboard_auth\self_hosted\__init__.py`
**行数**: 737

### 功能描述

SelfHostedOIDCProvider — generic self-hosted OpenID Connect dashboard auth.

A standards-compliant OpenID Connect Relying Party for the ``hermes dashboard``
OAuth gate. Unlike the bundled ``nous`` provider (which encodes Nous Portal's
bespoke contract — ``agent:{instance_id}`` client ids, a custom a

### 核心类

- `SelfHostedOIDCProvider`: Generic self-hosted OpenID Connect provider (authorization-code + PKCE).

### 核心函数

- `register()`: Plugin entry — called by the plugin loader at startup.

    Registers :class:`SelfHostedOIDCProvider

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\disk-cleanup\__init__.py`
**行数**: 317

### 功能描述

disk-cleanup plugin — auto-cleanup of ephemeral Hermes session files.

Wires three behaviours:

1. ``post_tool_call`` hook — inspects ``write_file`` and ``terminal``
   tool results for newly-created paths matching test/temp patterns
   under ``HERMES_HOME`` and tracks them silently.  Zero agent
   

### 核心函数

- `register()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## disk_cleanup.py

**路径**: `plugins\disk-cleanup\disk_cleanup.py`
**行数**: 584

### 功能描述

disk_cleanup — ephemeral file cleanup for Hermes Agent.

Library module wrapping the deterministic cleanup rules written by
@LVT382009 in PR #12212. The plugin ``__init__.py`` wires these
functions into ``post_tool_call`` and ``on_session_end`` hooks so
tracking and cleanup happen automatically — th

### 核心函数

- `get_state_dir()`: State dir — separate from ``$HERMES_HOME/logs/``.
- `get_tracked_file()`
- `get_log_file()`: Audit log — intentionally NOT under ``$HERMES_HOME/logs/``.
- `is_safe_path()`: Accept only paths under HERMES_HOME or ``/tmp/hermes-*``.

    Rejects Windows mounts (``/mnt/c`` et
- `load_tracked()`: Load tracked.json.  Restores from ``.bak`` on corruption.
- `save_tracked()`: Atomic write: ``.tmp`` → backup old → rename.
- `fmt_size()`
- `track()`: Register a file for tracking. Returns True if newly tracked.
- `forget()`: Remove a path from tracking without deleting the file.
- `dry_run()`: Return (auto_delete_list, needs_prompt_list) without touching files.
- `quick()`: Safe deterministic cleanup — no prompts.

    Returns: ``{"deleted": N, "empty_dirs": N, "freed": by
- `deep()`: Deep cleanup.

    Runs :func:`quick` first, then asks the *confirm* callable for each
    risky ite
- `status()`: Return per-category breakdown and top 10 largest tracked files.
- `format_status()`: Human-readable status string (for slash command output).
- `guess_category()`: Return a category label for *path*, or None if we shouldn't track it.

    Used by the ``post_tool_c

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\google_meet\__init__.py`
**行数**: 104

### 功能描述

google_meet plugin — let the agent join a Meet call, transcribe it, follow up.

v1: transcribe-only. Spawns a headless Chromium via Playwright, joins the Meet
URL, enables live captions, scrapes them into a transcript file. The agent then
has the transcript in its workspace and can do whatever follo

### 核心函数

- `register()`: Register tools, CLI, and lifecycle hooks.

    Called once by the plugin loader when the plugin is e

### 依赖关系

**依赖组件**: acp-adapter, entry-points
**跨组件调用**: 是

---

## audio_bridge.py

**路径**: `plugins\google_meet\audio_bridge.py`
**行数**: 249

### 功能描述

Virtual audio bridge for feeding generated speech into Chrome's mic.

v2 module. Provisions a platform-specific virtual audio device so the
Meet bot's Chromium instance can be pointed at an input source we
control. The OpenAI Realtime client writes PCM bytes into this device;
Chrome reads them as if

### 核心类

- `AudioBridge`: Manages a virtual audio device for Chrome fake-mic input.

    Call ``setup()`` once before launchin

### 核心函数

- `chrome_fake_audio_flags()`: Return Chrome flags for using the fake audio input.

    The PulseAudio source is selected via the `

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## cli.py

**路径**: `plugins\google_meet\cli.py`
**行数**: 478

### 功能描述

CLI commands for the google_meet plugin.

Wires ``hermes meet <subcommand>``:
  setup       — preflight playwright, chromium, auth file, print fixes
  auth        — open a browser to sign into Google, save storage state
  join <url>  — join a Meet URL synchronously (also callable from the agent)
  s

### 核心函数

- `register_cli()`: Build the ``hermes meet`` argparse tree.

    Called by :func:`_register_cli_commands` at plugin loa
- `meet_command()`

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, state-management
**跨组件调用**: 是

---

## meet_bot.py

**路径**: `plugins\google_meet\meet_bot.py`
**行数**: 859

### 功能描述

Headless Google Meet bot — Playwright + live-caption scraping.

Runs as a standalone subprocess spawned by ``process_manager.py``. Reads config
from env vars, writes status + transcript to files under
``$HERMES_HOME/workspace/meetings/<meeting-id>/``. The main hermes process
reads those files via th

### 核心类

- `_BotState`: Single-process mutable state, flushed to ``status.json`` on each change.

### 核心函数

- `run_bot()`

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\google_meet\node\__init__.py`
**行数**: 55

### 功能描述

Remote 'node host' primitive for the google_meet plugin.

Lets the Meet bot (Playwright + Chrome) run on a different machine than
the hermes-agent gateway. The gateway speaks a small JSON-over-WebSocket
RPC protocol to the remote node; the node wraps the existing
``plugins.google_meet.process_manage

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli
**跨组件调用**: 是

---

## cli.py

**路径**: `plugins\google_meet\node\cli.py`
**行数**: 126

### 功能描述

`hermes meet node ...` subcommand tree.

Wired into the existing ``hermes meet`` parser by the plugin's top-level
CLI. This module only defines the subparsers and their dispatch — it
does not mutate the existing cli.py.

### 核心函数

- `register_cli()`: Add ``run / list / approve / remove / status / ping`` subparsers.

    *subparser* is the ``hermes m
- `node_command()`: Dispatch for ``hermes meet node ...``.

    Returns a process exit code. Side-effects print to stdou

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli
**跨组件调用**: 是

---

## client.py

**路径**: `plugins\google_meet\node\client.py`
**行数**: 108

### 功能描述

Gateway-side RPC client for a remote meet node.

Each call opens a short-lived synchronous WebSocket to the node, sends
exactly one request, reads exactly one response, and closes. This keeps
the client trivial to use from non-async tool handlers and avoids
maintaining persistent connection state ac

### 核心类

- `NodeClient`: Thin synchronous WS client matching the server's request surface.

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## protocol.py

**路径**: `plugins\google_meet\node\protocol.py`
**行数**: 125

### 功能描述

Wire protocol for gateway ↔ node RPC.

Everything is a JSON object with the same envelope shape:

    Request:   {"type": <str>, "id": <str>, "token": <str>, "payload": <dict>}
    Response:  {"type": "<req-type>_res", "id": <req-id>, "payload": <dict>}
    Error:     {"type": "error", "id": <req-id

### 核心函数

- `make_request()`: Construct a request envelope.

    ``req_id`` is auto-generated (uuid4 hex) when not supplied so cal
- `make_response()`: Build a success response. The caller supplies the *request* type;
    we suffix it with ``_res`` so 
- `make_error()`
- `encode()`: Serialize a message envelope to a JSON string.
- `decode()`: Parse a JSON envelope, raising ValueError on anything malformed.

    Minimal type validation: must 
- `validate_request()`: Check a decoded request against the server's shared token.

    Returns ``(True, "")`` when the enve

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## registry.py

**路径**: `plugins\google_meet\node\registry.py`
**行数**: 113

### 功能描述

Local JSON registry of approved remote meet nodes.

Lives at ``$HERMES_HOME/workspace/meetings/nodes.json``. The gateway
consults it to resolve a ``chrome_node`` name to a ``(url, token)`` pair
before opening a WebSocket to the remote bot host.

Schema
------
    {
      "nodes": {
        "<name>":

### 核心类

- `NodeRegistry`: Simple file-backed registry. Not concurrent-safe across processes
    — single writer assumed (the g

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## server.py

**路径**: `plugins\google_meet\node\server.py`
**行数**: 201

### 功能描述

Remote node server.

Runs on the machine that will host the Meet bot (typically the user's
Mac laptop with a signed-in Chrome). Exposes a WebSocket endpoint that
accepts signed RPC requests and dispatches them to the existing
``plugins.google_meet.process_manager`` module.

Launched by ``hermes meet

### 核心类

- `NodeServer`: WebSocket server that executes meet bot RPCs locally.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## process_manager.py

**路径**: `plugins\google_meet\process_manager.py`
**行数**: 324

### 功能描述

Subprocess lifecycle manager for the google_meet bot.

Single active meeting at a time. Stores the running pid + out_dir in a
session-scoped state file under ``$HERMES_HOME/workspace/meetings/.active.json``
so tool calls across turns can find the bot, and ``on_session_end`` can clean
it up.

The bot

### 核心函数

- `start()`: Spawn the meet_bot subprocess for *url*.

    If a bot is already running for this hermes install, l
- `status()`: Return the current meeting state, or ``{"ok": False, "reason": ...}``.
- `transcript()`: Read the current transcript file. Returns ok=False if none exists.
- `enqueue_say()`: Append a ``say`` request to the active bot's JSONL queue.

    Returns ``{"ok": False, "reason": ...
- `stop()`: Signal the active bot to leave cleanly, then clear the active pointer.

    Sends SIGTERM and waits 

### 依赖关系

**依赖组件**: cli, gateway, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\google_meet\realtime\__init__.py`
**行数**: 11

### 功能描述

Realtime speech subpackage for the google_meet plugin (v2).

Provides a thin OpenAI Realtime API client and a file-queue speaker
wrapper so the Meet bot can play synthesized speech through the
virtual audio bridge.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## openai_client.py

**路径**: `plugins\google_meet\realtime\openai_client.py`
**行数**: 333

### 功能描述

OpenAI Realtime API WebSocket client + file-queue speaker.

This module is the "output" side of the v2 voice bridge: it takes text,
sends it to the OpenAI Realtime API, receives audio deltas back, and
appends the PCM bytes to a file. A separate consumer (the audio
bridge) streams that file into Chro

### 核心类

- `RealtimeSession`: Minimal sync client for the OpenAI Realtime WebSocket API.

    Usage:
        sess = RealtimeSessio
- `RealtimeSpeaker`: File-based JSONL queue wrapper around :class:`RealtimeSession`.

    Each line in ``queue_path`` is 

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## tools.py

**路径**: `plugins\google_meet\tools.py`
**行数**: 349

### 功能描述

Agent-facing tools for the google_meet plugin.

Tools:
  meet_join        — join a Google Meet URL (spawns Playwright bot locally
                     OR on a remote node host via node=<name>)
  meet_status      — report bot liveness + transcript progress
  meet_transcript  — read the current transc

### 核心函数

- `check_meet_requirements()`: Return True when the plugin can actually run LOCALLY.

    Gates on:
      * Python ``playwright`` p
- `handle_meet_join()`
- `handle_meet_status()`
- `handle_meet_transcript()`
- `handle_meet_leave()`
- `handle_meet_say()`

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## plugin_api.py

**路径**: `plugins\hermes-achievements\dashboard\plugin_api.py`
**行数**: 1062

### 功能描述

Hermes Achievements dashboard plugin backend.

Mounted at /api/plugins/hermes-achievements/ by Hermes dashboard.

### 核心函数

- `tiers()`
- `req()`
- `state_path()`
- `snapshot_path()`
- `checkpoint_path()`
- `load_state()`
- `save_state()`
- `load_snapshot()`
- `save_snapshot()`
- `load_checkpoint()`
- `save_checkpoint()`
- `session_fingerprint()`
- `model_provider()`
- `is_local_model_name()`
- `analyze_messages()`
- ... 还有 12 个函数

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\image_gen\fal\__init__.py`
**行数**: 212

### 功能描述

FAL.ai image generation backend.

Wraps the 18-model FAL catalog (FLUX 2, Z-Image, Nano Banana, GPT
Image 1.5, Recraft, Imagen 4, Qwen, Ideogram, …) as an
:class:`ImageGenProvider` implementation.

The heavy lifting — model catalog, payload construction, request
submission, managed-Nous-gateway sele

### 核心类

- `FalImageGenProvider`: FAL.ai image generation backend.

    Delegates to ``tools.image_generation_tool.image_generate_tool

### 核心函数

- `register()`: Plugin entry point — wire ``FalImageGenProvider`` into the registry.

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\image_gen\krea\__init__.py`
**行数**: 744

### 功能描述

Krea image generation backend.

Exposes Krea's `Krea 2` foundation image model family — Krea 2 Medium and
Krea 2 Large — as an :class:`ImageGenProvider` implementation.

Krea's API is asynchronous: the generate endpoint returns a ``job_id``
that you poll at ``GET /jobs/{job_id}``. This provider hide

### 核心类

- `KreaImageGenProvider`: Krea ``Krea 2`` foundation image model backend (Medium + Large).

### 核心函数

- `register()`: Plugin entry point — wire ``KreaImageGenProvider`` into the registry.

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\image_gen\openai-codex\__init__.py`
**行数**: 469

### 功能描述

OpenAI image generation backend — ChatGPT/Codex OAuth variant.

Identical model catalog and tier semantics to the ``openai`` image-gen plugin
(``gpt-image-2`` at low/medium/high quality), but routes the request through
the Codex Responses API ``image_generation`` tool instead of the
``images.generat

### 核心类

- `OpenAICodexImageGenProvider`: gpt-image-2 routed through ChatGPT/Codex OAuth instead of an API key.

### 核心函数

- `register()`: Plugin entry point — register the Codex-backed image-gen provider.

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\image_gen\openai\__init__.py`
**行数**: 415

### 功能描述

OpenAI image generation backend.

Exposes OpenAI's ``gpt-image-2`` model at three quality tiers as an
:class:`ImageGenProvider` implementation. The tiers are implemented as
three virtual model IDs so the ``hermes tools`` model picker and the
``image_gen.model`` config key behave like any other multi

### 核心类

- `OpenAIImageGenProvider`: OpenAI ``images.generate`` / ``images.edit`` backend — gpt-image-2.

### 核心函数

- `register()`: Plugin entry point — wire ``OpenAIImageGenProvider`` into the registry.

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\image_gen\openrouter\__init__.py`
**行数**: 512

### 功能描述

OpenRouter-compatible image generation backend (OpenRouter + Nous Portal).

Both OpenRouter and the Nous Portal inference endpoint speak the same
OpenAI-style ``/chat/completions`` image-generation protocol: send
``modalities: ["image", "text"]`` with an image-output model (e.g.
``google/gemini-3-pr

### 核心类

- `OpenRouterCompatImageProvider`: Image generation over an OpenRouter-compatible chat-completions endpoint.

    Instantiated once per

### 核心函数

- `register()`: Register the OpenRouter + Nous Portal image gen providers.

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\image_gen\xai\__init__.py`
**行数**: 415

### 功能描述

xAI image generation backend.

Exposes xAI's ``grok-imagine-image`` model as an
:class:`ImageGenProvider` implementation.

Features:
- Text-to-image generation
- Multiple aspect ratios (1:1, 16:9, 9:16, etc.)
- Multiple resolutions (1K, 2K)
- Base64 output saved to cache

Selection precedence (first

### 核心类

- `XAIImageGenProvider`: xAI ``grok-imagine-image`` backend.

### 核心函数

- `register()`: Register this provider with the image gen registry.

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## plugin_api.py

**路径**: `plugins\kanban\dashboard\plugin_api.py`
**行数**: 2455

### 功能描述

Kanban dashboard plugin — backend API routes.

Mounted at /api/plugins/kanban/ by the dashboard plugin system.

This layer is intentionally thin: every handler is a small wrapper around
``hermes_cli.kanban_db`` or a direct SQL query. Writes use the same code
paths the CLI and gateway ``/kanban`` com

### 核心类

- `CreateTaskBody`
- `UpdateTaskBody`
- `CommentBody`
- `LinkBody`
- `BulkTaskBody`
- `TerminateRunBody`
- `ReclaimBody`
- `SpecifyBody`: Optional author override. Nothing else is configurable from the
    dashboard — model + prompt come 
- `ReassignBody`
- `CreateBoardBody`
- ... 还有 5 个类

### 核心函数

- `get_board()`: Return the full board grouped by status column.

    ``_conn()`` auto-initializes ``kanban.db`` on f
- `get_task()`
- `create_task()`
- `list_task_attachments()`
- `download_attachment()`
- `remove_attachment()`
- `update_task()`
- `delete_task()`
- `add_comment()`
- `add_link()`
- `delete_link()`
- `bulk_update()`: Apply the same patch to every id in ``payload.ids``.

    This is an *independent* iteration — per-t
- `list_diagnostics()`: Return ``[{task_id, task_title, task_status, task_assignee,
    diagnostics: [...]}, ...]`` for ever
- `list_active_workers()`: Return every currently-running worker on the board.

    A worker is a ``task_runs`` row whose ``end
- `get_run_endpoint()`: Direct lookup of a ``task_runs`` row by its integer id.

    Returns ``{run: {...}}`` using the same
- ... 还有 24 个函数

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

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

**依赖组件**: cli, memory-system, state-management
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

**依赖组件**: cli, memory-system, state-management
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

**依赖组件**: agent-engine, cli, entry-points, memory-system, state-management, tool-system
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

**依赖组件**: agent-engine, cli, memory-system, state-management
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

**依赖组件**: agent-engine, memory-system
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

**依赖组件**: memory-system, state-management
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

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, memory-system, state-management
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

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, memory-system, state-management
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

**依赖组件**: cli, state-management, tool-system
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

**依赖组件**: cli, entry-points, memory-system, state-management
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

**依赖组件**: memory-system
**跨组件调用**: 是

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

**依赖组件**: cli, memory-system, state-management
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

**依赖组件**: agent-engine, cli, entry-points, memory-system, state-management
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

**依赖组件**: cli, memory-system, state-management
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

**依赖组件**: cli, entry-points, memory-system, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\alibaba-coding-plan\__init__.py`
**行数**: 22

### 功能描述

Alibaba Cloud Coding Plan provider profile.

Separate from the standard `alibaba` profile because it hits a different
endpoint (coding-intl.dashscope.aliyuncs.com) with a dedicated API key tier.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\alibaba\__init__.py`
**行数**: 14

### 功能描述

Alibaba Cloud DashScope provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\anthropic\__init__.py`
**行数**: 54

### 功能描述

Native Anthropic provider profile.

### 核心类

- `AnthropicProfile`: Native Anthropic — uses x-api-key header, not Bearer.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\arcee\__init__.py`
**行数**: 14

### 功能描述

Arcee AI provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\azure-foundry\__init__.py`
**行数**: 22

### 功能描述

Microsoft Foundry provider profile.

Azure Foundry exposes an OpenAI-compatible endpoint; users supply their own
base URL at setup since endpoints are per-resource.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\bedrock\__init__.py`
**行数**: 31

### 功能描述

AWS Bedrock provider profile.

### 核心类

- `BedrockProfile`: AWS Bedrock — no REST /v1/models endpoint; uses AWS SDK.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\copilot-acp\__init__.py`
**行数**: 36

### 功能描述

GitHub Copilot ACP provider profile.

copilot-acp uses an external ACP subprocess — NOT the standard
transport. api_mode="copilot_acp" is handled separately in run_agent.py.
The profile captures auth + endpoint metadata for registry migration.

### 核心类

- `CopilotACPProfile`: GitHub Copilot ACP — external process, no REST models endpoint.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\copilot\__init__.py`
**行数**: 59

### 功能描述

Copilot / GitHub Models provider profile.

Copilot uses per-model api_mode routing:
  - GPT-5+ / Codex models → codex_responses
  - Claude models → anthropic_messages
  - Everything else → chat_completions (this profile covers that subset)

Key quirks for the chat_completions subset:
  - Editor attr

### 核心类

- `CopilotProfile`: GitHub Copilot / GitHub Models — editor headers + reasoning.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\custom\__init__.py`
**行数**: 75

### 功能描述

Custom / Ollama (local) provider profile.

Covers any endpoint registered as provider="custom", including local
Ollama instances. Key quirks:
  - ollama_num_ctx → extra_body.options.num_ctx (local context window)
  - reasoning_config disabled → extra_body.think = False

### 核心类

- `CustomProfile`: Custom/Ollama local provider — think=false and num_ctx support.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\deepseek\__init__.py`
**行数**: 101

### 功能描述

DeepSeek provider profile.

DeepSeek's V4 family (and the legacy ``deepseek-reasoner``) defaults to
thinking-mode ON when ``extra_body.thinking`` is unset.  The API then returns
``reasoning_content`` and starts enforcing the contract that subsequent turns
echo it back; combined with how Hermes repla

### 核心类

- `DeepSeekProfile`: DeepSeek — extra_body.thinking + top-level reasoning_effort.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\gemini\__init__.py`
**行数**: 62

### 功能描述

Google Gemini provider profiles.

gemini:            Google AI Studio (API key) — uses GeminiNativeClient

Reports api_mode="chat_completions" but uses a custom native client
that bypasses the standard OpenAI transport. The profile captures auth
and endpoint metadata for auth.py / runtime_provider.p

### 核心类

- `GeminiProfile`: Gemini — translate reasoning_config to thinking_config in extra_body.

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\gmi\__init__.py`
**行数**: 32

### 功能描述

GMI Cloud provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\huggingface\__init__.py`
**行数**: 21

### 功能描述

Hugging Face provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\kilocode\__init__.py`
**行数**: 15

### 功能描述

Kilo Code provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\kimi-coding\__init__.py`
**行数**: 81

### 功能描述

Kimi / Moonshot provider profiles.

Kimi has dual endpoints:
  - sk-kimi-* keys → api.kimi.com/coding (Anthropic Messages API)
  - legacy keys → api.moonshot.ai/v1 (OpenAI chat completions)

This module covers the chat_completions path (/v1 endpoint).

### 核心类

- `KimiProfile`: Kimi/Moonshot — temperature omitted, thinking xor reasoning_effort.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\minimax\__init__.py`
**行数**: 98

### 功能描述

MiniMax provider profiles (international + China).

The default API-key routes use anthropic_messages because their base URLs end
with /anthropic. Users can opt MiniMax-M3 into the OpenAI-compatible endpoint
with base_url=https://api.minimax.io/v1; that route needs MiniMax-specific
reasoning control

### 核心类

- `MiniMaxProfile`: MiniMax — M3 OpenAI-compatible reasoning controls.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\nous\__init__.py`
**行数**: 55

### 功能描述

Nous Portal provider profile.

### 核心类

- `NousProfile`: Nous Portal — product tags, reasoning with Nous-specific omission.

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\novita\__init__.py`
**行数**: 28

### 功能描述

NovitaAI provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\nvidia\__init__.py`
**行数**: 22

### 功能描述

NVIDIA NIM provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\ollama-cloud\__init__.py`
**行数**: 74

### 功能描述

Ollama Cloud provider profile.

Ollama Cloud's OpenAI-compatible ``/v1/chat/completions`` endpoint
supports top-level ``reasoning_effort`` with values ``none``, ``low``,
``medium``, ``high``, and ``max`` (the last being undocumented but
empirically confirmed for DeepSeek V4 — ``max`` produces ~2.5× 

### 核心类

- `OllamaCloudProfile`: Ollama Cloud — maps xhigh→max via top-level reasoning_effort.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\openai-codex\__init__.py`
**行数**: 16

### 功能描述

OpenAI Codex (Responses API) provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\opencode-zen\__init__.py`
**行数**: 127

### 功能描述

OpenCode provider profiles (Zen + Go).

Both use per-model api_mode routing:
  - OpenCode Zen: Claude → anthropic_messages, GPT-5/Codex → codex_responses,
    everything else → chat_completions (this profile)
  - OpenCode Go: MiniMax → anthropic_messages, GLM/Kimi → chat_completions
    (this profil

### 核心类

- `OpenCodeGoProfile`: OpenCode Go - model-specific reasoning controls.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\openrouter\__init__.py`
**行数**: 189

### 功能描述

OpenRouter provider profile.

### 核心类

- `OpenRouterProfile`: OpenRouter aggregator — provider preferences, reasoning config passthrough.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\qwen-oauth\__init__.py`
**行数**: 83

### 功能描述

Qwen Portal provider profile.

### 核心类

- `QwenProfile`: Qwen Portal — message normalization, vl_high_resolution, metadata top-level.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\stepfun\__init__.py`
**行数**: 15

### 功能描述

StepFun provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\xai\__init__.py`
**行数**: 16

### 功能描述

xAI (Grok) provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\xiaomi\__init__.py`
**行数**: 17

### 功能描述

Xiaomi MiMo provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\model-providers\zai\__init__.py`
**行数**: 23

### 功能描述

ZAI / GLM provider profile.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\observability\langfuse\__init__.py`
**行数**: 1138

### 功能描述

langfuse — Hermes plugin for Langfuse observability.

Traces Hermes conversations, LLM calls, and tool usage to Langfuse.

Activation is handled by the Hermes plugin system — standalone plugins only
load when listed in ``plugins.enabled`` (via ``hermes plugins enable
observability/langfuse`` or ``he

### 核心类

- `TraceState`

### 核心函数

- `on_pre_llm_call()`
- `on_pre_llm_request()`
- `on_post_llm_call()`
- `on_pre_tool_call()`
- `on_post_tool_call()`
- `register()`

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\observability\nemo_relay\__init__.py`
**行数**: 963

### 功能描述

nemo_relay — optional Hermes plugin for NeMo Relay observability.

### 核心类

- `_SessionState`
- `_SubagentParent`
- `_Settings`
- `_Runtime`

### 核心函数

- `register()`
- `on_session_start()`
- `on_session_end()`
- `on_session_finalize()`
- `on_session_reset()`
- `on_pre_llm_call()`
- `on_post_llm_call()`
- `on_pre_api_request()`
- `on_post_api_request()`
- `on_api_request_error()`
- `on_pre_tool_call()`
- `on_post_tool_call()`
- `on_pre_approval_request()`
- `on_post_approval_response()`
- `on_subagent_start()`
- ... 还有 4 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\platforms\dingtalk\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\dingtalk\adapter.py`
**行数**: 1708

### 功能描述

DingTalk platform adapter using Stream Mode.

Uses dingtalk-stream SDK (>=0.20) for real-time message reception without webhooks.
Responses are sent via DingTalk's session webhook (markdown format).
Supports: text, images, audio, video, rich text, files, and group @mentions.

Requires:
    pip insta

### 核心类

- `DingTalkAdapter`: DingTalk chatbot adapter using Stream Mode.

    The dingtalk-stream SDK maintains a long-lived WebS
- `_IncomingHandler`: dingtalk-stream ChatbotHandler that forwards messages to the adapter.

    SDK >= 0.20 changed proce

### 核心函数

- `check_dingtalk_requirements()`: Check if DingTalk dependencies are available and configured.

    Lazy-installs dingtalk-stream via 
- `interactive_setup()`: Configure DingTalk — QR scan (recommended) or manual credential entry.

    Replaces hermes_cli/setu
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: cli, entry-points, gateway, llm-client, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\discord\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\discord\adapter.py`
**行数**: 7177

### 功能描述

Minimal object exposing ``.id`` — satisfies discord.py's Snowflake
    protocol for ``channel.history(before=...)`` without constructing a
    ``discord.Object`` (which test doubles that stub the disc

### 核心类

- `_Snowflake`: Minimal object exposing ``.id`` — satisfies discord.py's Snowflake
    protocol for ``channel.histor
- `_DiscordNonConversationalMessageTracker`: Persistent bounded set of Discord message IDs that are status noise.
- `VoiceReceiver`: Captures and decodes voice audio from a Discord voice channel.

    Attaches to a VoiceClient's sock
- `DiscordAdapter`: Discord bot adapter.

    Handles:
    - Receiving messages from servers and DMs
    - Sending respo

### 核心函数

- `check_discord_requirements()`: Check if Discord dependencies are available.

    Lazy-installs discord.py via ``tools.lazy_deps.ens
- `interactive_setup()`: Guide the user through Discord bot setup.

    Mirrors Teams' ``interactive_setup`` shape: lazy-impo
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## voice_mixer.py

**路径**: `plugins\platforms\discord\voice_mixer.py`
**行数**: 380

### 功能描述

A single audio stream feeding into :class:`VoiceMixer`.

    Wraps raw 48 kHz / stereo / s16le PCM bytes.  ``read_frame`` hands back one
    20 ms frame at a time, optionally looping, with a per-child

### 核心类

- `MixerChild`: A single audio stream feeding into :class:`VoiceMixer`.

    Wraps raw 48 kHz / stereo / s16le PCM b
- `VoiceMixer`: A continuous ``discord.AudioSource`` that mixes N child streams.

    Use :meth:`set_ambient` to ins

### 核心函数

- `decode_to_pcm()`: Decode any audio file to 48 kHz / stereo / s16le PCM via ffmpeg.

    Returns the raw PCM bytes, or 
- `synth_ambient_pcm()`: Synthesise a subtle looping ambient bed (no asset file required).

    A soft, slowly-pulsing low pa

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\platforms\email\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\email\adapter.py`
**行数**: 1236

### 功能描述

Email platform adapter for the Hermes gateway.

Allows users to interact with Hermes by sending emails.
Uses IMAP to receive and SMTP to send messages.

Environment variables:
    EMAIL_IMAP_HOST     — IMAP server host (e.g., imap.gmail.com)
    EMAIL_IMAP_PORT     — IMAP server port (default: 993)


### 核心类

- `_IPv4SMTP`
- `_IPv4SMTP_SSL`
- `EmailAdapter`: Email gateway adapter using IMAP (receive) and SMTP (send).

### 核心函数

- `check_email_requirements()`: Check if email platform settings are available and non-blank.

    Treats blank/whitespace-only valu
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: cli, entry-points, llm-client, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\feishu\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\feishu\adapter.py`
**行数**: 5513

### 功能描述

Feishu/Lark platform adapter.

Supports:
- WebSocket long connection and Webhook transport
- Direct-message and group @mention-gated text receive/send
- Inbound image/file/audio/media caching
- Gateway allowlist integration via FEISHU_ALLOWED_USERS
- Persistent dedup state across restarts
- Per-chat

### 核心类

- `FeishuPostMediaRef`
- `FeishuMentionRef`
- `_FeishuBotIdentity`
- `FeishuPostParseResult`
- `FeishuNormalizedMessage`
- `FeishuAdapterSettings`
- `FeishuGroupRule`: Per-group policy rule for controlling which users may interact with the bot.
- `FeishuBatchState`
- `FeishuAdapter`: Feishu/Lark bot adapter.

### 核心函数

- `parse_feishu_post_payload()`
- `normalize_feishu_message()`
- `check_feishu_requirements()`: Check if Feishu/Lark dependencies are available.

    Lazy-installs lark-oapi via ``tools.lazy_deps.
- `probe_bot()`: Verify bot connectivity via /open-apis/bot/v3/info.

    Uses lark_oapi SDK when available, falls ba
- `qr_register()`: Run the Feishu / Lark scan-to-create QR registration flow.

    Returns on success::

        {
    
- `interactive_setup()`: Interactive setup for Feishu / Lark — scan-to-create or manual creds.

    Replaces the central _set
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, gateway, llm-client, state-management, tool-system, tui
**跨组件调用**: 是

---

## feishu_comment.py

**路径**: `plugins\platforms\feishu\feishu_comment.py`
**行数**: 1383

### 功能描述

Feishu/Lark drive document comment handling.

Processes ``drive.notice.comment_add_v1`` events and interacts with the
Drive v2 comment reaction API.  Kept in a separate module so that the
main ``feishu.py`` adapter does not grow further and comment-related
logic can evolve independently.

Flow:
  1.

### 核心函数

- `parse_drive_comment_event()`: Extract structured fields from a ``drive.notice.comment_add_v1`` payload.

    *data* may be a ``Cus
- `build_local_comment_prompt()`: Build the prompt for a local (quoted-text) comment.
- `build_whole_comment_prompt()`: Build the prompt for a whole-document comment.

### 依赖关系

**依赖组件**: cli, entry-points, gateway, tool-system
**跨组件调用**: 是

---

## feishu_comment_rules.py

**路径**: `plugins\platforms\feishu\feishu_comment_rules.py`
**行数**: 430

### 功能描述

Feishu document comment access-control rules.

3-tier rule resolution: exact doc > wildcard "*" > top-level > code defaults.
Each field (enabled/policy/allow_from) falls back independently.
Config: ~/.hermes/feishu_comment_rules.json (mtime-cached, hot-reload).
Pairing store: ~/.hermes/feishu_commen

### 核心类

- `CommentDocumentRule`: Per-document rule.  ``None`` means 'inherit from lower tier'.
- `CommentsConfig`: Top-level comment access config.
- `ResolvedCommentRule`: Fully resolved rule after field-by-field fallback.
- `_MtimeCache`: Generic mtime-based file cache.  ``stat()`` per access, re-read only on change.

### 核心函数

- `load_config()`: Load comment rules from disk (mtime-cached).
- `has_wiki_keys()`: Check if any document rule key starts with 'wiki:'.
- `resolve_rule()`: Resolve effective rule: exact doc → wiki key → wildcard → top-level → defaults.
- `pairing_add()`: Add a user to the pairing-approved list. Returns True if newly added.
- `pairing_remove()`: Remove a user from the pairing-approved list. Returns True if removed.
- `pairing_list()`: Return the approved dict  {user_open_id: {approved_at: ...}}.
- `is_user_allowed()`: Check if user passes the resolved rule's policy gate.

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## feishu_meeting_invite.py

**路径**: `plugins\platforms\feishu\feishu_meeting_invite.py`
**行数**: 213

### 功能描述

Feishu/Lark meeting-invitation event handling.

Processes ``vc.bot.meeting_invited_v1`` events by converting them into a
synthetic gateway ``MessageEvent``.  Unlike document comments, the response
should go back to the inviter through the normal Hermes gateway pipeline, so
this module does not insta

### 核心类

- `MeetingInviteUser`
- `MeetingInviteMeeting`
- `MeetingInvitedPayload`

### 核心函数

- `parse_meeting_invited_event()`
- `build_meeting_invite_prompt()`

### 依赖关系

**依赖组件**: agent-engine, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\google_chat\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\google_chat\adapter.py`
**行数**: 3349

### 功能描述

Google Chat platform adapter.

Uses Google Cloud Pub/Sub (pull subscription) for inbound events and the
Google Chat REST API for outbound messages. Pattern parallels Slack Socket
Mode and Telegram long-polling: no public endpoint required.

Concurrency model
-----------------
The Pub/Sub SubscriberC

### 核心类

- `_ThreadCountStore`: Per-(chat_id, thread_name) inbound message counter, persisted to disk.

    Drives the DM main-flow 
- `GoogleChatAdapter`: Google Chat bot adapter using Pub/Sub pull + Chat REST API.

    Required environment (see gateway/c

### 核心函数

- `check_google_chat_requirements()`: Check if Google Chat optional dependencies are installed.

    Triggers the lazy import of the googl
- `interactive_setup()`: Walk the user through Google Chat configuration via ``hermes setup``.

    The setup wizard at ``her
- `register()`: Plugin entry point — called by the Hermes plugin system at startup.

    Registers the Google Chat a

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, gateway, llm-client, memory-system, state-management
**跨组件调用**: 是

---

## oauth.py

**路径**: `plugins\platforms\google_chat\oauth.py`
**行数**: 668

### 功能描述

User OAuth helper for the Google Chat gateway adapter.

Google Chat's ``media.upload`` REST endpoint hard-rejects service-account
authentication:

    "This method doesn't support app authentication with a service
     account. Authenticate with a user account."

(See https://developers.google.com/w

### 核心函数

- `load_user_credentials()`: Load + validate persisted user OAuth credentials.

    ``email`` selects the per-user token file; ``
- `refresh_or_none()`: Refresh ``creds`` if expired. Returns the credentials or ``None``.

    Used by the adapter just bef
- `build_user_chat_service()`: Build a Google Chat API client authenticated as the user.

    Used for media.upload + the subsequen
- `list_authorized_emails()`: Return the set of user emails that have stored per-user tokens.

    Lists files in the per-user tok
- `install_deps()`
- `check_auth()`: Print status; return True if creds are usable.

    Per-user when ``email`` given, legacy single-use
- `store_client_secret()`: Validate and copy the user's OAuth client_secret.json into HERMES_HOME.
- `get_auth_url()`: Print the OAuth URL for the user to visit. Persists PKCE state.

    ``email`` namespaces the pendin
- `exchange_auth_code()`: Exchange an auth code (or pasted redirect URL) for a refresh token.

    ``email`` selects the desti
- `revoke()`: Revoke the stored token with Google and delete it locally.

    Per-user when ``email`` given, legac
- `main()`

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\homeassistant\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\homeassistant\adapter.py`
**行数**: 578

### 功能描述

Home Assistant platform adapter.

Connects to the HA WebSocket API for real-time event monitoring.
State-change events are converted to MessageEvent objects and forwarded
to the agent for processing.  Outbound messages are delivered as HA
persistent notifications.

Requires:
- aiohttp (already in me

### 核心类

- `HomeAssistantAdapter`: Home Assistant WebSocket adapter.

    Subscribes to ``state_changed`` events and forwards them as
 

### 核心函数

- `check_ha_requirements()`: Check if Home Assistant dependencies are available and configured.
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\irc\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\irc\adapter.py`
**行数**: 972

### 功能描述

IRC Platform Adapter for Hermes Agent.

A plugin-based gateway adapter that connects to an IRC server and relays
messages to/from the Hermes agent.  Zero external dependencies — uses
Python's stdlib asyncio for the IRC protocol.

Configuration in config.yaml::

    gateway:
      platforms:
        

### 核心类

- `IRCAdapter`: Async IRC adapter implementing the BasePlatformAdapter interface.

    This class is instantiated by

### 核心函数

- `check_requirements()`: Check if IRC is configured.

    Only requires the server and channel — no external pip packages nee
- `validate_config()`: Validate that the platform config has enough info to connect.
- `interactive_setup()`: Interactive `hermes gateway setup` flow for the IRC platform.

    Lazy-imports ``hermes_cli.setup``
- `is_connected()`: Check whether IRC is configured (env or config.yaml).
- `register()`: Plugin entry point: called by the Hermes plugin system.

### 依赖关系

**依赖组件**: cli, entry-points, gateway, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\line\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\line\adapter.py`
**行数**: 1653

### 功能描述

LINE Messaging API platform adapter for Hermes Agent.

A bundled platform plugin that runs an aiohttp webhook server, accepts LINE
webhook events (signature-verified), and relays messages to/from the agent
via the standard ``BasePlatformAdapter`` interface.

Design highlights
-----------------

**Re

### 核心类

- `State`
- `_CacheEntry`
- `RequestCache`: In-memory cache for slow-LLM postback retrieval.

    PRs #18153 originally combined two TTLs — one 
- `_MessageDeduplicator`: Bounded LRU of LINE webhook event IDs to ignore at-least-once retries.
- `_LineClient`: Thin async wrapper around the LINE Messaging API.

    We use ``aiohttp`` directly to avoid a ``line
- `LineAdapter`: LINE Messaging API gateway adapter.

### 核心函数

- `strip_markdown_preserving_urls()`: Strip Markdown that LINE can't render, but keep URLs usable.

    LINE's text bubble has zero Markdo
- `split_for_line()`: Split ``text`` into LINE-sized bubbles, preferring paragraph/line breaks.

    Returns at most ``LIN
- `verify_line_signature()`: Verify a LINE webhook's ``X-Line-Signature`` header.

    LINE signs the *raw* request body with HMA
- `build_postback_button_message()`: Template Buttons message — the slow-LLM postback bubble.

    From PR #18153 (leepoweii). Template B
- `check_requirements()`: Plugin gate: require credentials AND aiohttp at runtime.
- `validate_config()`
- `is_connected()`: Surface in ``hermes status`` even before the adapter is instantiated.
- `interactive_setup()`: Minimal stdin wizard for ``hermes setup line``.

    Mirrors the irc/teams style: prompts for the tw
- `register()`: Plugin entry point — called by the Hermes plugin system at startup.

### 依赖关系

**依赖组件**: cli, llm-client, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\matrix\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\matrix\adapter.py`
**行数**: 4398

### 功能描述

Matrix gateway adapter.

Connects to any Matrix homeserver (self-hosted or matrix.org) via the
mautrix Python SDK.  Supports optional end-to-end encryption (E2EE)
when installed with ``pip install "mautrix[encryption]"``.

Environment variables:
    MATRIX_HOMESERVER           Homeserver URL (e.g. h

### 核心类

- `_MatrixHtmlSanitizer`: Allowlist sanitizer for Matrix-compatible formatted HTML.
- `MatrixRoomIdentity`: Resolved Matrix room identity for routing and prompt context.
- `_MatrixApprovalPrompt`: Tracks a pending Matrix reaction-based exec approval prompt.
- `_MatrixModelPickerPrompt`: Tracks a pending Matrix reaction-based model picker prompt.
- `_CryptoStateStore`: Adapter that satisfies the mautrix crypto StateStore interface.

    OlmMachine requires a StateStor
- `MatrixAdapter`: Gateway adapter for Matrix (any homeserver).

### 核心函数

- `get_matrix_capabilities()`: Return Matrix gateway capabilities for docs and release checks.
- `check_matrix_requirements()`: Return True if the Matrix adapter can be used.

    Lazy-installs the full ``platform.matrix`` featu
- `interactive_setup()`: Configure Matrix credentials. Replaces hermes_cli/setup.py::_setup_matrix
    and the static _PLATFO
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\mattermost\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\mattermost\adapter.py`
**行数**: 1271

### 功能描述

Mattermost gateway adapter.

Connects to a self-hosted (or cloud) Mattermost instance via its REST API
(v4) and WebSocket for real-time events.  No external Mattermost library
required — uses aiohttp which is already a Hermes dependency.

Environment variables:
    MATTERMOST_URL              Server

### 核心类

- `MattermostAdapter`: Gateway adapter for Mattermost (self-hosted or cloud).

### 核心函数

- `check_mattermost_requirements()`: Return True if the Mattermost adapter can be used.
- `interactive_setup()`: Guide the user through Mattermost bot setup.

    Mirrors Discord/Teams' ``interactive_setup`` shape
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: cli, gateway, llm-client, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\ntfy\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\ntfy\adapter.py`
**行数**: 594

### 功能描述

ntfy platform adapter (Hermes plugin).

Subscribes to a topic on ntfy.sh or any self-hosted ntfy server via
HTTP streaming (``/json`` endpoint with ``poll=false``) and publishes
replies via HTTP POST. No external SDK — only httpx, which is already
a Hermes dependency.

This adapter ships as a Hermes

### 核心类

- `_FatalStreamError`: Raised when a stream error is unrecoverable (e.g. 401, 404).
- `NtfyAdapter`: ntfy adapter.

    Subscribes to a topic via HTTP streaming (``/json`` endpoint) and
    publishes r

### 核心函数

- `check_requirements()`: Check whether the ntfy adapter is installable and minimally configured.

    Reads ``NTFY_TOPIC`` di
- `validate_config()`: Validate that the configured ntfy platform has a topic set.
- `is_connected()`: Check whether ntfy is configured (env or config.yaml).
- `register()`: Plugin entry point — called by the Hermes plugin system at startup.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\photon\__init__.py`
**行数**: 5

### 功能描述

Photon Spectrum (iMessage) platform plugin entry point.

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\photon\adapter.py`
**行数**: 1695

### 功能描述

Photon Spectrum (iMessage) platform adapter for Hermes Agent.

Both directions of traffic flow through a small supervised Node sidecar
(see ``sidecar/index.mjs``) that runs the ``spectrum-ts`` SDK — the SDK is
TypeScript-only and there is no public HTTP message API, so a sidecar is
unavoidable.

Inb

### 核心类

- `PhotonAdapter`: Bidirectional bridge to Photon Spectrum via the Node spectrum-ts sidecar.

    Inbound: consume the 

### 核心函数

- `check_requirements()`: Return True when both Python deps and the Node sidecar are available.
- `validate_config()`
- `is_connected()`
- `register()`: Called by the Hermes plugin loader at startup.

### 依赖关系

**依赖组件**: acp-adapter, cli, gateway, llm-client
**跨组件调用**: 是

---

## auth.py

**路径**: `plugins\platforms\photon\auth.py`
**行数**: 1047

### 功能描述

Photon Dashboard API client + device-code login flow.

This module is pure Python — it intentionally does not depend on
``spectrum-ts``.  Every management-plane operation (login, find/create
project, rotate the project secret, register a user, list the assigned
iMessage line) talks to Photon's **Das

### 核心类

- `PhotonDashboardAuthError`: Raised when Photon rejects a device-flow token for the dashboard API.
- `DeviceCode`
- `_DeviceTokenCandidate`: A token-like value extracted from the device-token response.

### 核心函数

- `load_photon_token()`: Return the device-flow bearer token stored by ``login()`` or ``None``.
- `store_photon_token()`: Persist a dashboard bearer token under ``credential_pool.photon``.
- `load_project_credentials()`: Return the runtime SDK creds ``(spectrum_project_id, project_secret)``.

    Precedence: process env
- `load_dashboard_project_id()`: Return the project id used for management API calls.

    Post-unification the dashboard id and the 
- `store_project_credentials()`: Persist project credentials to both .env (runtime) and auth.json (mgmt).

    The runtime SDK creds 
- `store_user_numbers()`: Persist non-secret Photon user numbers for offline ``status`` output.
- `request_device_code()`: POST ``/api/auth/device/code`` and return the device + user codes.
- `poll_for_token()`: Poll ``/api/auth/device/token`` until the user approves.

    Mirrors the official CLI's polling loo
- `validate_photon_token()`: Verify a device-flow token is usable for dashboard project APIs.

    The device flow can return a t
- `login_device_flow()`: Run the full device-code login flow and persist the token.

    Returns the bearer token.  ``on_user
- `get_session()`: GET ``/api/auth/get-session`` — confirm the token + fetch the user.
- `list_projects()`: GET ``/api/projects`` — return the caller's projects.
- `find_project_by_name()`: Return the first project whose name matches (case-insensitive).
- `create_project()`: POST ``/api/projects`` and return ``{success, id}``.

    Spectrum is always provisioned at create-t
- `regenerate_project_secret()`: POST ``/api/projects/{id}/regenerate-secret`` → the new project secret.

    This is the only way to
- ... 还有 12 个函数

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## cli.py

**路径**: `plugins\platforms\photon\cli.py`
**行数**: 440

### 功能描述

``hermes photon ...`` CLI subcommands — registered by the plugin via
``ctx.register_cli_command()``.

Subcommands:

    setup              full first-time setup (device login + project + user + sidecar)
    status             show login + project + sidecar dep state
    install-sidecar    npm instal

### 核心函数

- `register_cli()`: Wire up `hermes photon ...` subcommands.
- `dispatch()`
- `gateway_setup()`: Run Photon first-time setup from the `hermes gateway setup` wizard.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\raft\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\raft\adapter.py`
**行数**: 783

### 功能描述

Raft channel platform adapter.

Starts a local wake endpoint, spawns ``raft agent bridge`` as a child process,
and injects content-free wake hints into Hermes' normal gateway session pipeline.
Token and port are auto-generated when not provided via env/config.
The bridge remains responsible for Raft

### 核心类

- `ActivityQueue`: Bounded at-most-once queue for Raft external activity telemetry.
- `RaftAdapter`: Local HTTP endpoint for Raft channel bridge delivery.

### 核心函数

- `check_raft_requirements()`: Check if Raft channel dependencies are available.

    Intentionally silent on failure — this is a p
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, cli, llm-client, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\simplex\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\simplex\adapter.py`
**行数**: 1314

### 功能描述

SimpleX Chat platform adapter (Hermes plugin).

Connects to a simplex-chat daemon running in WebSocket mode.
Inbound messages arrive via a persistent WebSocket connection.
Outbound messages use the same WebSocket with JSON commands.

This adapter ships as a Hermes platform plugin under
``plugins/pla

### 核心类

- `SimplexAdapter`: SimpleX Chat adapter using the simplex-chat daemon WebSocket API.

    Instantiated by the ``adapter

### 核心函数

- `check_requirements()`: Plugin gate: require SIMPLEX_WS_URL AND the websockets package.

    Returning False keeps the platf
- `validate_config()`: Validate that the platform config has enough info to connect.
- `is_connected()`: Check whether SimpleX is configured (env or config.yaml).
- `interactive_setup()`: Minimal stdin wizard for ``hermes setup gateway`` → SimpleX.

    Prompts for the WebSocket URL and 
- `register()`: Plugin entry point — called by the Hermes plugin system at startup.

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\slack\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\slack\adapter.py`
**行数**: 4294

### 功能描述

Slack platform adapter.

Uses slack-bolt (Python) with Socket Mode for:
- Receiving messages from channels and DMs
- Sending responses back
- Handling slash commands
- Thread support

### 核心类

- `_ThreadContextCache`: Cache entry for fetched thread context.
- `SlackAdapter`: Slack bot adapter using Socket Mode.

    Requires two tokens:
      - SLACK_BOT_TOKEN (xoxb-...) fo

### 核心函数

- `check_slack_requirements()`: Check if Slack dependencies are available.

    Lazy-installs slack-bolt/slack-sdk via ``tools.lazy_
- `interactive_setup()`: Guide the user through Slack bot setup.

    Mirrors Discord's ``interactive_setup`` shape: lazy-imp
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, cli, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\sms\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\sms\adapter.py`
**行数**: 494

### 功能描述

SMS (Twilio) platform adapter.

Connects to the Twilio REST API for outbound SMS and runs an aiohttp
webhook server to receive inbound messages.

Shares credentials with the optional telephony skill — same env vars:
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
  - TWILIO_PHONE_NUMBER  (E.164 from-nu

### 核心类

- `SmsAdapter`: Twilio SMS <-> Hermes gateway adapter.

    Each inbound phone number gets its own Hermes session (m

### 核心函数

- `check_sms_requirements()`: Check if SMS adapter dependencies are available.
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: cli, gateway, llm-client, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\teams\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\teams\adapter.py`
**行数**: 1445

### 功能描述

Microsoft Teams platform adapter for Hermes Agent.

Uses the microsoft-teams-apps SDK for authentication and activity processing.
Runs an aiohttp webhook server to receive messages from Teams.
Proactive messaging (send, typing) uses the SDK's App.send() method.

Requires:
    pip install microsoft-t

### 核心类

- `_StaticAccessTokenProvider`: Minimal token-provider shim so outbound Graph delivery can reuse the shared client.
- `TeamsSummaryWriter`: Pipeline-facing Teams outbound delivery surface.

    This stays inside the existing Teams platform 
- `_AiohttpBridgeAdapter`: HttpServerAdapter that bridges the Teams SDK into an aiohttp server.

    Without a custom adapter, 
- `TeamsAdapter`: Microsoft Teams adapter using the microsoft-teams-apps SDK.

### 核心函数

- `check_requirements()`: Return True when all Teams dependencies and credentials are present.
- `validate_config()`: Return True when the config has the minimum required credentials.
- `is_connected()`: Check whether Teams is configured (env or config.yaml).
- `check_teams_requirements()`: Ensure the Teams SDK is importable, lazy-installing it on first use.

    Lazy-installs ``microsoft-
- `interactive_setup()`: Guide the user through Teams setup using the Teams CLI.
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: agent-engine, cli, gateway, llm-client, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\telegram\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\telegram\adapter.py`
**行数**: 7594

### 功能描述

Telegram platform adapter.

Uses python-telegram-bot library for:
- Receiving messages from users/groups
- Sending responses back
- Handling media and commands

### 核心类

- `TelegramAdapter`: Telegram bot adapter.

    Handles:
    - Receiving messages from users and groups
    - Sending res

### 核心函数

- `check_telegram_requirements()`: Check if Telegram dependencies are available.

    If python-telegram-bot is missing, attempts to la
- `interactive_setup()`: Configure Telegram bot credentials and allowlist.

    Delegates to the existing CLI setup helpers (
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## telegram_network.py

**路径**: `plugins\platforms\telegram\telegram_network.py`
**行数**: 260

### 功能描述

Telegram-specific network helpers.

Provides a hostname-preserving fallback transport for networks where
api.telegram.org resolves to an endpoint that is unreachable from the current
host. The transport keeps the logical request host and TLS SNI as
api.telegram.org while retrying the TCP connection 

### 核心类

- `TelegramFallbackTransport`: Retry Telegram Bot API requests via fallback IPs while preserving TLS/SNI.

    Requests continue to

### 核心函数

- `parse_fallback_ip_env()`

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\platforms\wecom\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\wecom\adapter.py`
**行数**: 1866

### 功能描述

WeCom (Enterprise WeChat) platform adapter.

Uses the WeCom AI Bot WebSocket gateway for inbound and outbound messages.
The adapter focuses on the core gateway path:

- authenticate via ``aibot_subscribe``
- receive inbound ``aibot_msg_callback`` events
- send outbound markdown messages via ``aibot_

### 核心类

- `WeComAdapter`: WeCom AI Bot adapter backed by a persistent WebSocket connection.

### 核心函数

- `check_wecom_requirements()`: Check if WeCom runtime dependencies are available.
- `qr_scan_for_bot_info()`: Run the WeCom QR scan flow to obtain bot_id and secret.

    Fetches a QR code from WeCom, renders i
- `interactive_setup()`: Interactive setup for WeCom — QR scan or manual credential input.

    Replaces hermes_cli/gateway.p
- `register()`: Plugin entry point — registers both WeCom platforms.

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, gateway, llm-client, tool-system
**跨组件调用**: 是

---

## callback_adapter.py

**路径**: `plugins\platforms\wecom\callback_adapter.py`
**行数**: 426

### 功能描述

WeCom callback-mode adapter for self-built enterprise applications.

Unlike the bot/websocket adapter in ``wecom.py``, this handles the standard
WeCom callback flow: WeCom POSTs encrypted XML to an HTTP endpoint, the
adapter decrypts it, queues the message for the agent, and immediately
acknowledges

### 核心类

- `WecomCallbackAdapter`

### 核心函数

- `check_wecom_callback_requirements()`

### 依赖关系

**依赖组件**: cli, gateway, llm-client
**跨组件调用**: 是

---

## wecom_crypto.py

**路径**: `plugins\platforms\wecom\wecom_crypto.py`
**行数**: 143

### 功能描述

WeCom BizMsgCrypt-compatible AES-CBC encryption for callback mode.

Implements the same wire format as Tencent's official ``WXBizMsgCrypt``
SDK so that WeCom can verify, encrypt, and decrypt callback payloads.

### 核心类

- `WeComCryptoError`
- `SignatureError`
- `DecryptError`
- `EncryptError`
- `PKCS7Encoder`
- `WXBizMsgCrypt`: Minimal WeCom callback crypto helper compatible with BizMsgCrypt semantics.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\platforms\whatsapp\__init__.py`
**行数**: 4

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## adapter.py

**路径**: `plugins\platforms\whatsapp\adapter.py`
**行数**: 1467

### 功能描述

WhatsApp platform adapter.

WhatsApp integration is more complex than Telegram/Discord because:
- No official bot API for personal accounts
- Business API requires Meta Business verification
- Most solutions use web-based automation

This adapter supports multiple backends:
1. WhatsApp Business API 

### 核心类

- `WhatsAppAdapter`: WhatsApp adapter.
    
    This implementation uses a simple HTTP bridge pattern where:
    1. A Nod

### 核心函数

- `check_whatsapp_requirements()`: Check if WhatsApp dependencies are available.
    
    WhatsApp requires a Node.js bridge for most i
- `interactive_setup()`: Guide the user through WhatsApp setup.

    Replaces the central _setup_whatsapp in hermes_cli/gatew
- `register()`: Plugin entry point — called by the Hermes plugin system.

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, gateway, llm-client, state-management
**跨组件调用**: 是

---

## plugin_utils.py

**路径**: `plugins\plugin_utils.py`
**行数**: 136

### 功能描述

Shared concurrency helpers for plugin authors.

The most common plugin footgun is the lazy process-wide singleton:

    _client = None

    def get_client():
        global _client
        if _client is not None:
            return _client
        _client = ExpensiveClient(...)   # <-- TOCTOU: two t

### 核心类

- `SingletonSlot`: Thread-safe lazy slot for accessors that take a build argument.

    Use this when the cached instan

### 核心函数

- `lazy_singleton()`: Wrap a zero-argument factory into a thread-safe lazy singleton accessor.

    The wrapped callable r

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\security-guidance\__init__.py`
**行数**: 260

### 功能描述

security-guidance plugin — fast pattern-matched security warnings on file writes.

Wires one behaviour:

* ``transform_tool_result`` hook — scans the *content being written* by
  ``write_file`` / ``patch`` / ``skill_manage`` (write/patch modes) for known
  dangerous code patterns (eval(, pickle.load

### 核心函数

- `register()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## patterns.py

**路径**: `plugins\security-guidance\patterns.py`
**行数**: 369

### 功能描述

Regex-based security pattern definitions for the security-guidance plugin.

Pure data + one pure helper. No env-var reads, no I/O — kept side-effect-free
so it can be imported in isolation.

Forked verbatim from Anthropic's claude-plugins-official repository
(plugins/security-guidance/hooks/patterns

### 核心类

- `RuleId`: Stable numeric IDs for SECURITY_PATTERNS rules, emitted via the PostToolUse
    metrics field so tel

### 核心函数

- `rule_names_to_mask()`: Pack a set of rule names into a bitmask. Bit N set means RuleId(N) matched.
    User-defined pattern

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\spotify\__init__.py`
**行数**: 67

### 功能描述

Spotify integration plugin — bundled, auto-loaded.

Registers 7 tools (playback, devices, queue, search, playlists, albums,
library) into the ``spotify`` toolset. Each tool's handler is gated by
``_check_spotify_available()`` — when the user has not run ``hermes auth
spotify``, the tools remain regi

### 核心函数

- `register()`: Register all Spotify tools. Called once by the plugin loader.

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## client.py

**路径**: `plugins\spotify\client.py`
**行数**: 436

### 功能描述

Thin Spotify Web API helper used by Hermes native tools.

### 核心类

- `SpotifyError`: Base Spotify tool error.
- `SpotifyAuthRequiredError`: Raised when the user needs to authenticate with Spotify first.
- `SpotifyAPIError`: Structured Spotify API failure.
- `SpotifyClient`

### 核心函数

- `normalize_spotify_id()`
- `normalize_spotify_uri()`
- `normalize_spotify_uris()`
- `compact_json()`

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## tools.py

**路径**: `plugins\spotify\tools.py`
**行数**: 455

### 功能描述

Native Spotify tools for Hermes (registered via plugins/spotify).

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\teams_pipeline\__init__.py`
**行数**: 24

### 功能描述

Teams meeting pipeline plugin.

Registers only operator-facing CLI surfaces. The agent should invoke these via
the terminal tool; no model tools are added by this plugin.

### 核心函数

- `register()`

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## cli.py

**路径**: `plugins\teams_pipeline\cli.py`
**行数**: 462

### 功能描述

CLI commands for the Teams meeting pipeline plugin.

### 核心函数

- `register_cli()`
- `teams_pipeline_command()`

### 依赖关系

**依赖组件**: agent-engine, cli, state-management, tool-system
**跨组件调用**: 是

---

## meetings.py

**路径**: `plugins\teams_pipeline\meetings.py`
**行数**: 334

### 功能描述

Graph-backed Teams meeting helpers for the plugin runtime.

### 核心类

- `TeamsMeetingError`: Base class for Teams meeting pipeline failures.
- `TeamsMeetingNotFoundError`: Raised when the meeting cannot be resolved from Graph.
- `TeamsMeetingArtifactNotFoundError`: Raised when a transcript or recording cannot be found.
- `TeamsMeetingPermissionError`: Raised when Graph access is denied for the requested resource.

### 核心函数

- `select_preferred_transcript()`

### 依赖关系

**依赖组件**: cli, tool-system
**跨组件调用**: 是

---

## models.py

**路径**: `plugins\teams_pipeline\models.py`
**行数**: 351

### 功能描述

Normalized models for the Teams meeting pipeline plugin.

### 核心类

- `GraphSubscription`
- `TeamsMeetingRef`
- `MeetingArtifact`
- `TeamsMeetingSummaryPayload`
- `TeamsMeetingPipelineJob`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pipeline.py

**路径**: `plugins\teams_pipeline\pipeline.py`
**行数**: 690

### 功能描述

Pipeline orchestration for Microsoft Teams meeting summaries.

### 核心类

- `TeamsPipelineError`: Base class for Teams meeting pipeline failures.
- `TeamsPipelineRetryableError`: Raised when the pipeline should be retried later.
- `TeamsPipelineSinkError`: Raised when an output sink fails.
- `TeamsPipelineArtifactNotFoundError`: Raised when meeting artifacts are not yet available.
- `TeamsPipelineConfig`
- `NotionWriter`
- `LinearWriter`
- `TeamsMeetingPipeline`: Transcript-first Teams meeting pipeline with durable lifecycle state.

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## runtime.py

**路径**: `plugins\teams_pipeline\runtime.py`
**行数**: 136

### 功能描述

Gateway runtime wiring for the Teams meeting pipeline plugin.

### 核心函数

- `build_pipeline_runtime_config()`: Build pipeline config from gateway platform config.

    Pipeline-specific knobs live under ``teams.
- `build_pipeline_runtime()`
- `bind_gateway_runtime()`: Attach the Teams pipeline runtime to the msgraph webhook adapter.

### 依赖关系

**依赖组件**: agent-engine, cli, gateway
**跨组件调用**: 是

---

## store.py

**路径**: `plugins\teams_pipeline\store.py`
**行数**: 194

### 功能描述

Durable local state for the Teams pipeline plugin.

### 核心类

- `TeamsPipelineStore`: JSON-backed durable store for Teams pipeline state.

### 核心函数

- `resolve_teams_pipeline_store_path()`

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## subscriptions.py

**路径**: `plugins\teams_pipeline\subscriptions.py`
**行数**: 250

### 功能描述

Microsoft Graph subscription helpers for the Teams pipeline plugin.

### 核心函数

- `build_graph_client()`
- `resolve_store_path()`
- `build_store()`
- `sync_graph_subscription_record()`
- `expected_client_state()`
- `is_managed_subscription()`

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\video_gen\fal\__init__.py`
**行数**: 621

### 功能描述

FAL.ai video generation backend.

User-facing surface: pick a **model family** (e.g. "Pixverse v6",
"Veo 3.1", "Seedance 2.0", "Kling v3 4K", "LTX 2.3", "Happy Horse").
The plugin auto-routes to the family's text-to-video endpoint when
called without ``image_url``, and to its image-to-video endpoint

### 核心类

- `FALVideoGenProvider`: FAL.ai multi-family video generation backend.

    Routes between text-to-video and image-to-video e

### 核心函数

- `register()`: Plugin entry point — wire ``FALVideoGenProvider`` into the registry.

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\video_gen\xai\__init__.py`
**行数**: 505

### 功能描述

xAI Grok-Imagine video generation backend.

Surface: text-to-video and image-to-video (animate an input image)
through xAI's ``/videos/generations`` endpoint. Edit and extend are not
exposed in this unified surface — xAI is the only backend that supports
them and the inconsistency would force per-ba

### 核心类

- `XAIVideoGenProvider`: xAI Grok Imagine video backend (text-to-video + image-to-video).

### 核心函数

- `register()`: Plugin entry point — wire ``XAIVideoGenProvider`` into the registry.

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\__init__.py`
**行数**: 8

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `plugins\web\brave_free\__init__.py`
**行数**: 15

### 功能描述

Brave Search (free tier) plugin — bundled, auto-loaded.

Mirrors the ``plugins/image_gen/openai/`` layout: ``provider.py`` holds the
provider class, ``__init__.py::register(ctx)`` registers an instance.

### 核心函数

- `register()`: Register the Brave-free provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\brave_free\provider.py`
**行数**: 138

### 功能描述

Brave Search (free tier) — plugin form.

Subclasses :class:`agent.web_search_provider.WebSearchProvider` (the
plugin-facing ABC). The legacy in-tree module
``tools.web_providers.brave_free`` was removed in the same commit that
moved this code under ``plugins/``; this file is now the canonical
implem

### 核心类

- `BraveFreeWebSearchProvider`: Search-only Brave provider using the free-tier Data-for-Search API.

    Free tier is 2,000 queries/

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\ddgs\__init__.py`
**行数**: 16

### 功能描述

DuckDuckGo search plugin — bundled, auto-loaded.

Backed by the community ``ddgs`` Python package which scrapes DDG's HTML
results page. No API key required, but the package itself must be installed
(it's an optional dep — gated via :meth:`is_available`).

### 核心函数

- `register()`: Register the DDGS provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\ddgs\provider.py`
**行数**: 159

### 功能描述

DuckDuckGo search — plugin form (via the ``ddgs`` package).

Subclasses the plugin-facing :class:`agent.web_search_provider.WebSearchProvider`.
The legacy in-tree module ``tools.web_providers.ddgs`` was removed in the
same commit that moved this code under ``plugins/``; this file is now the
canonica

### 核心类

- `DDGSWebSearchProvider`: DuckDuckGo HTML-scrape search provider.

    No API key needed. Rate limits are enforced server-side

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\exa\__init__.py`
**行数**: 16

### 功能描述

Exa web search + extract plugin — bundled, auto-loaded.

Backed by the official Exa SDK (``exa-py``). Both search and extract are
sync; the dispatcher in :mod:`tools.web_tools` handles the wrap when the
caller is async.

### 核心函数

- `register()`: Register the Exa provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\exa\provider.py`
**行数**: 213

### 功能描述

Exa web search + content extraction — plugin form.

Subclasses :class:`agent.web_search_provider.WebSearchProvider`. Uses the
official Exa SDK (``exa-py``) which is lazy-loaded via
:func:`tools.lazy_deps.ensure` so that cold-start CLI users don't pay the
SDK import cost when Exa isn't configured.

C

### 核心类

- `ExaWebSearchProvider`: Exa search + extract provider.

    Both methods are sync — Exa's SDK is sync-only. The web_extract_

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\firecrawl\__init__.py`
**行数**: 29

### 功能描述

Firecrawl web search + extract plugin — bundled, auto-loaded.

Largest single plugin in this PR. Captures everything the previous
inline implementation in tools/web_tools.py did:

  - Lazy import of the firecrawl SDK (~200ms cold-start cost) via a
    callable proxy that defers the actual import to 

### 核心函数

- `register()`: Register the Firecrawl provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\firecrawl\provider.py`
**行数**: 595

### 功能描述

Firecrawl web search + extract — plugin form.

Subclasses :class:`agent.web_search_provider.WebSearchProvider`. This is
the largest provider migrated in this PR; it captures the full inline
firecrawl implementation that previously lived in tools/web_tools.py:

  - :data:`Firecrawl` lazy proxy that d

### 核心类

- `_FirecrawlProxy`: Callable proxy that looks like ``firecrawl.Firecrawl`` but imports lazily.
- `FirecrawlWebSearchProvider`: Firecrawl search + extract provider with dual auth paths.

### 核心函数

- `check_firecrawl_api_key()`: Return True when Firecrawl backend (direct or gateway) is usable.

    Re-exported by :mod:`tools.we

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\parallel\__init__.py`
**行数**: 17

### 功能描述

Parallel.ai web search + extract plugin — bundled, auto-loaded.

First plugin in this repo to expose an async :meth:`extract` — Parallel's
SDK is async-native (``AsyncParallel.beta.extract``). The web_extract_tool
dispatcher detects coroutines via :func:`inspect.iscoroutinefunction` and
awaits.

### 核心函数

- `register()`: Register the Parallel provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\parallel\provider.py`
**行数**: 292

### 功能描述

Parallel.ai web search + content extraction — plugin form.

Subclasses :class:`agent.web_search_provider.WebSearchProvider`. Uses two
distinct Parallel SDK clients:

- ``Parallel`` (sync)        — for :meth:`search`
- ``AsyncParallel`` (async)  — for :meth:`extract`

This is the first plugin to exer

### 核心类

- `ParallelWebSearchProvider`: Parallel.ai search + async extract provider.

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\searxng\__init__.py`
**行数**: 16

### 功能描述

SearXNG search plugin — bundled, auto-loaded.

Backed by a user-hosted SearXNG instance (URL configured via ``SEARXNG_URL``).
Search-only — pair with an extract provider (firecrawl/tavily/exa) for
``web_extract`` calls.

### 核心函数

- `register()`: Register the SearXNG provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\searxng\provider.py`
**行数**: 154

### 功能描述

SearXNG search — plugin form.

Subclasses :class:`agent.web_search_provider.WebSearchProvider`. Same JSON
API call (``/search?format=json``), same result normalization. The legacy
in-tree module ``tools.web_providers.searxng`` was removed in the same
commit that moved this code under ``plugins/``; t

### 核心类

- `SearXNGWebSearchProvider`: Search via a user-hosted SearXNG instance.

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\tavily\__init__.py`
**行数**: 11

### 功能描述

Tavily web search + extract plugin — bundled, auto-loaded.

### 核心函数

- `register()`: Register the Tavily provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\tavily\provider.py`
**行数**: 221

### 功能描述

Tavily web search + content extraction — plugin form.

Subclasses :class:`agent.web_search_provider.WebSearchProvider`. Two
capabilities advertised:

- ``supports_search()``  -> True (Tavily ``/search``)
- ``supports_extract()`` -> True (Tavily ``/extract``)

Both are sync — the underlying call is `

### 核心类

- `TavilyWebSearchProvider`: Tavily search + extract provider.

### 依赖关系

**依赖组件**: agent-engine, tool-system
**跨组件调用**: 是

---

## __init__.py

**路径**: `plugins\web\xai\__init__.py`
**行数**: 15

### 功能描述

xAI web search plugin — bundled, auto-loaded.

Mirrors the ``plugins/web/brave_free/`` layout: ``provider.py`` holds the
provider class, ``__init__.py::register(ctx)`` registers an instance.

### 核心函数

- `register()`: Register the xAI Web Search provider with the plugin context.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## provider.py

**路径**: `plugins\web\xai\provider.py`
**行数**: 558

### 功能描述

xAI Web Search — plugin form.

Routes ``web_search`` tool calls through xAI's agentic Web Search tool
(server-side ``web_search`` on the Responses API). Grok runs the actual
searching and page-browsing server-side; we ask it to return the top
results as structured JSON so we can hand back the same
`

### 核心类

- `XAIWebSearchProvider`: Search-only provider backed by xAI's agentic Web Search tool.

    Sends a structured prompt to Grok

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

