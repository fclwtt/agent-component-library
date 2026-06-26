# tool-system 模块详细说明

本组件包含 106 个模块。

---

## __init__.py

**路径**: `tools\__init__.py`
**行数**: 26

### 功能描述

Tools package namespace.

Keep package import side effects minimal. Importing ``tools`` should not
eagerly import the full tool stack, because several subsystems load tools while
``hermes_cli.config`` is still initializing.

Callers should import concrete submodules directly, for example:

    impor

### 核心函数

- `check_file_requirements()`: File tools only require terminal backend availability.

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## ansi_strip.py

**路径**: `tools\ansi_strip.py`
**行数**: 45

### 功能描述

Strip ANSI escape sequences from subprocess output.

Used by terminal_tool, code_execution_tool, and process_registry to clean
command output before returning it to the model.  This prevents ANSI codes
from entering the model's context — which is the root cause of models
copying escape sequences int

### 核心函数

- `strip_ansi()`: Remove ANSI escape sequences from text.

    Returns the input unchanged (fast path) when no ESC or 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## approval.py

**路径**: `tools\approval.py`
**行数**: 2089

### 功能描述

Dangerous command approval -- detection, prompting, and per-session state.

This module is the single source of truth for the dangerous command system:
- Pattern detection (DANGEROUS_PATTERNS, detect_dangerous_command)
- Per-session approval state (thread-safe, keyed by session_key)
- Approval promp

### 核心类

- `_ApprovalEntry`: One pending dangerous-command approval inside a gateway session.

### 核心函数

- `set_current_session_key()`: Bind the active approval session key to the current context.
- `reset_current_session_key()`: Restore the prior approval session key context.
- `set_current_observability_context()`: Bind active tool correlation IDs to approval hooks.
- `reset_current_observability_context()`: Restore prior approval hook correlation IDs.
- `get_current_session_key()`: Return the active session key, preferring context-local state.

    Resolution order:
    1. approva
- `detect_hardline_command()`: Check if a command matches the unconditional hardline blocklist.

    Returns:
        (is_hardline,
- `detect_dangerous_command()`: Check if a command matches any dangerous patterns.

    Returns:
        (is_dangerous, pattern_key,
- `register_gateway_notify()`: Register a per-session callback for sending approval requests to the user.

    The callback signatu
- `unregister_gateway_notify()`: Unregister the per-session gateway approval callback.

    Signals ALL blocked threads for this sess
- `resolve_gateway_approval()`: Called by the gateway's /approve or /deny handler to unblock
    waiting agent thread(s).

    When 
- `has_blocking_approval()`: Check if a session has one or more blocking gateway approvals waiting.
- `submit_pending()`: Store a pending approval request for a session.
- `approve_session()`: Approve a pattern for this session only.
- `enable_session_yolo()`: Enable YOLO bypass for a single session key.
- `disable_session_yolo()`: Disable YOLO bypass for a single session key.
- ... 还有 13 个函数

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, gateway, llm-client, security, state-management
**跨组件调用**: 是

---

## async_delegation.py

**路径**: `tools\async_delegation.py`
**行数**: 557

### 功能描述

Async (background) delegation registry.

Backs ``delegate_task(background=true)``: the parent agent dispatches a
subagent that runs on a module-level daemon executor and returns a handle
immediately, so the user and the model can keep working while the child runs.

When the child finishes, a complet

### 核心类

- `_DaemonThreadPoolExecutor`: ThreadPoolExecutor variant whose workers do not block process exit.

    Stdlib ``ThreadPoolExecutor

### 核心函数

- `active_count()`: Number of async delegations currently running.
- `dispatch_async_delegation()`: Spawn ``runner`` on the daemon executor and return a handle immediately.

    Parameters
    -------
- `dispatch_async_delegation_batch()`: Dispatch a WHOLE fan-out batch as ONE background unit.

    Unlike ``dispatch_async_delegation`` (wh
- `list_async_delegations()`: Snapshot of async delegations (running + recently completed).

    Safe to call from any thread. Exc
- `interrupt_all()`: Signal every running async delegation to stop. Returns how many.

    Used on ``/stop`` and gateway 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## binary_extensions.py

**路径**: `tools\binary_extensions.py`
**行数**: 43

### 功能描述

Binary file extensions to skip for text-based operations.

These files can't be meaningfully compared as text and are often large.
Ported from free-code src/constants/files.ts.

### 核心函数

- `has_binary_extension()`: Check if a file path has a binary extension. Pure string check, no I/O.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## blueprints.py

**路径**: `tools\blueprints.py`
**行数**: 326

### 功能描述

Blueprints: shareable plain-language automations layered on skills + cron.

A "blueprint" is NOT a new object type. It is an ordinary skill (a SKILL.md the
agent loads) that additionally declares an automation schedule in its
frontmatter:

    metadata:
      hermes:
        blueprint:
          sch

### 核心类

- `BlueprintError`: Raised when a blueprint block is present but malformed.
- `BlueprintSpec`: Parsed ``metadata.hermes.blueprint`` automation spec for a skill.

### 核心函数

- `parse_blueprint()`: Extract a BlueprintSpec from a SKILL.md string, or None if not a blueprint.

    A skill is a bluepr
- `blueprint_spec_for_installed()`: Locate an installed skill's SKILL.md and parse its blueprint block.

    Searches the standard skill
- `blueprint_to_job_spec()`: Build the ``cron.jobs.create_job`` kwargs dict for a BlueprintSpec.

    This is the single source o
- `create_blueprint_job()`: Create the cron job described by a BlueprintSpec via the existing cron API.

    The blueprint's ski
- `register_blueprint_suggestion()`: Turn an installed blueprint into a pending Suggested Cron Job.

    Blueprints are source ``blueprin
- `export_blueprint()`: Render a shareable blueprint SKILL.md from an existing cron job dict.

    The inverse of ``create_b

### 依赖关系

**依赖组件**: cli, cron
**跨组件调用**: 是

---

## browser_camofox.py

**路径**: `tools\browser_camofox.py`
**行数**: 810

### 功能描述

Camofox browser backend — local anti-detection browser via REST API.

Camofox-browser is a self-hosted Node.js server wrapping Camoufox (Firefox
fork with C++ fingerprint spoofing).  It exposes a REST API that maps 1:1
to our browser tool interface: accessibility snapshots with element refs,
click/t

### 核心函数

- `get_camofox_url()`: Return the configured Camofox server URL, or empty string.
- `is_camofox_mode()`: True when Camofox backend is configured and no CDP override is active.

    When the user has explic
- `check_camofox_available()`: Verify the Camofox server is reachable.
- `get_vnc_url()`: Return the VNC URL if the Camofox server exposes one, or None.
- `camofox_soft_cleanup()`: Release the in-memory session without destroying the server-side context.

    When managed persiste
- `camofox_navigate()`: Navigate to a URL via Camofox.
- `camofox_snapshot()`: Get accessibility tree snapshot from Camofox.
- `camofox_click()`: Click an element by ref via Camofox.
- `camofox_type()`: Type text into an element by ref via Camofox.
- `camofox_scroll()`: Scroll the page via Camofox.
- `camofox_back()`: Navigate back via Camofox.
- `camofox_press()`: Press a keyboard key via Camofox.
- `camofox_close()`: Close the browser session via Camofox.
- `camofox_get_images()`: Get images on the current page via Camofox.

    Extracts image information from the accessibility t
- `camofox_vision()`: Take a screenshot and analyze it with vision AI via Camofox.
- ... 还有 1 个函数

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client, state-management
**跨组件调用**: 是

---

## browser_camofox_state.py

**路径**: `tools\browser_camofox_state.py`
**行数**: 48

### 功能描述

Hermes-managed Camofox state helpers.

Provides profile-scoped identity and state directory paths for Camofox
persistent browser profiles.  When managed persistence is enabled, Hermes
sends a deterministic userId derived from the active profile so that
Camofox can map it to the same persistent brows

### 核心函数

- `get_camofox_state_dir()`: Return the profile-scoped root directory for Camofox persistence.
- `get_camofox_identity()`: Return the stable Hermes-managed Camofox identity for this profile.

    The user identity is profil

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## browser_cdp_tool.py

**路径**: `tools\browser_cdp_tool.py`
**行数**: 570

### 功能描述

Raw Chrome DevTools Protocol (CDP) passthrough tool.

Exposes a single tool, ``browser_cdp``, that sends arbitrary CDP commands to
the browser's DevTools WebSocket endpoint.  Works when a CDP URL is
configured — either via ``/browser connect`` (sets ``BROWSER_CDP_URL``) or
``browser.cdp_url`` in ``c

### 核心函数

- `browser_cdp()`: Send a raw CDP command.  See ``CDP_DOCS_URL`` for method documentation.

    Args:
        method: C

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## browser_dialog_tool.py

**路径**: `tools\browser_dialog_tool.py`
**行数**: 149

### 功能描述

Agent-facing tool: respond to a native JS dialog captured by the CDP supervisor.

This tool is response-only — the agent first reads ``pending_dialogs`` from
``browser_snapshot`` output, then calls ``browser_dialog(action=...)`` to
accept or dismiss.

Gated on the same ``_browser_cdp_check`` as ``br

### 核心函数

- `browser_dialog()`: Respond to a pending dialog on the active task's CDP supervisor.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## browser_supervisor.py

**路径**: `tools\browser_supervisor.py`
**行数**: 1476

### 功能描述

Persistent CDP supervisor for browser dialog + frame detection.

One ``CDPSupervisor`` runs per Hermes ``task_id`` that has a reachable CDP
endpoint. It holds a single persistent WebSocket to the backend, subscribes
to ``Page`` / ``Runtime`` / ``Target`` events on every attached session
(top-level p

### 核心类

- `PendingDialog`: A JS dialog currently open on some frame's session.
- `DialogRecord`: A historical record of a dialog that was opened and then handled.

    Retained in ``recent_dialogs`
- `FrameInfo`: One frame in the page's frame tree.

    ``is_oopif`` means the frame has its own CDP target (separa
- `ConsoleEvent`: Ring buffer entry for console + exception traffic.
- `SupervisorSnapshot`: Read-only snapshot of supervisor state.

    Frozen dataclass so tool handlers can freely dereferenc
- `CDPSupervisor`: One supervisor per (task_id, cdp_url) pair.

    Lifecycle:
      * ``start()`` — kicked off by ``Su
- `_SupervisorRegistry`: Process-global (task_id → supervisor) map with idempotent start/stop.

    One instance, exposed as 

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## browser_tool.py

**路径**: `tools\browser_tool.py`
**行数**: 4020

### 功能描述

Browser Tool Module

This module provides browser automation tools using agent-browser CLI.  It
supports multiple backends — **Browser Use** (cloud, default for Nous
subscribers), **Browserbase** (cloud, direct credentials), and **local
Chromium** — with identical agent-facing behaviour.  The backen

### 核心函数

- `browser_navigate()`: Navigate to a URL in the browser.

    Args:
        url: The URL to navigate to
        task_id: Ta
- `browser_snapshot()`: Get a text-based snapshot of the current page's accessibility tree.

    Args:
        full: If True
- `browser_click()`: Click on an element.

    Args:
        ref: Element reference (e.g., "@e5")
        task_id: Task i
- `browser_type()`: Type text into an input field.

    Args:
        ref: Element reference (e.g., "@e3")
        text:
- `browser_scroll()`: Scroll the page.

    Args:
        direction: "up" or "down"
        task_id: Task identifier for s
- `browser_back()`: Navigate back in browser history.

    Args:
        task_id: Task identifier for session isolation

- `browser_press()`: Press a keyboard key.

    Args:
        key: Key to press (e.g., "Enter", "Tab")
        task_id: T
- `browser_console()`: Get browser console messages and JavaScript errors, or evaluate JS in the page.

    When ``expressi
- `browser_get_images()`: Get all images on the current page.

    Args:
        task_id: Task identifier for session isolatio
- `browser_vision()`: Take a screenshot of the current page for visual inspection.

    Captures what's visually displayed
- `cleanup_browser()`: Clean up browser session(s) for a task.

    Called automatically when a task completes or when inac
- `cleanup_all_browsers()`: Clean up all active browser sessions.

    Useful for cleanup on shutdown.
- `check_browser_requirements()`: Check if browser tool requirements are met.

    In **local mode** (no cloud provider configured): t
- `check_browser_vision_requirements()`: Whether ``browser_vision`` should be advertised to the model.

    Requires BOTH a working browser (

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, llm-client, plugin-system, state-management
**跨组件调用**: 是

---

## budget_config.py

**路径**: `tools\budget_config.py`
**行数**: 115

### 功能描述

Configurable budget constants for tool result persistence.

Per-tool resolution: pinned > config overrides > registry > default.

### 核心类

- `BudgetConfig`: Immutable budget constants for the 3-layer tool result persistence system.

    Layer 2 (per-result)

### 核心函数

- `budget_for_context_window()`: Return a BudgetConfig scaled to the active model's context window.

    The fixed defaults (100K res

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## checkpoint_manager.py

**路径**: `tools\checkpoint_manager.py`
**行数**: 1669

### 功能描述

Checkpoint Manager — Transparent filesystem snapshots via a single shared
shadow git store.

Creates automatic snapshots of working directories before file-mutating
operations (``write_file``, ``patch``, ``terminal`` with destructive flags),
triggered once per conversation turn.  Provides rollback t

### 核心类

- `CheckpointManager`: Manages automatic filesystem checkpoints.

    Designed to be owned by AIAgent.  Call ``new_turn()``

### 核心函数

- `format_checkpoint_list()`: Format checkpoint list for display to user.
- `prune_checkpoints()`: Delete stale/orphan checkpoints and reclaim store space.

    A project entry is deleted when either
- `maybe_auto_prune_checkpoints()`: Idempotent wrapper around ``prune_checkpoints`` for startup hooks.

    Writes ``CHECKPOINT_BASE/.la
- `store_status()`: Return a summary of the shadow store.

    ``{"base": path, "store_size_bytes": N, "legacy_size_byte
- `clear_all()`: Nuke the entire checkpoint base (store + legacy).  Irreversible.

    Returns ``{"bytes_freed": N, "
- `clear_legacy()`: Delete all ``legacy-*`` archive directories.

    Returns ``{"bytes_freed": N, "deleted": count}``.

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## clarify_gateway.py

**路径**: `tools\clarify_gateway.py`
**行数**: 279

### 功能描述

Gateway-side clarify primitive (blocking event-based queue).

The ``clarify`` tool needs to ask the user a question and block the agent
thread until they respond.  In CLI mode this is trivial — ``input()`` is
synchronous.  In gateway mode the agent runs on a worker thread while the
event loop handle

### 核心类

- `_ClarifyEntry`: One pending clarify request inside a gateway session.

### 核心函数

- `register()`: Register a pending clarify request and return the entry.

    The caller (gateway clarify_callback) 
- `wait_for_response()`: Block on the entry's event until resolved or timeout fires.

    Polls in 1-second slices so the age
- `resolve_gateway_clarify()`: Unblock the agent thread waiting on ``clarify_id``.

    Returns True if an entry was found and reso
- `get_pending_for_session()`: Return the OLDEST pending clarify entry for a session, or None.

    Used by the text-fallback inter
- `mark_awaiting_text()`: Flip an entry into text-capture mode (user picked the 'Other' button).

    Returns True if the entr
- `has_pending()`: Return True when this session has at least one pending clarify entry.
- `clear_session()`: Resolve and drop every pending clarify for a session.

    Used by session-boundary cleanup (e.g. ``
- `get_clarify_timeout()`: Read the clarify response timeout (seconds) from config.

    Defaults to 600 (10 minutes) — long en
- `register_notify()`: Register a per-session notify callback used by ``clarify_callback``.
- `unregister_notify()`: Drop the per-session notify callback and cancel any pending clarify entries.
- `get_notify()`

### 依赖关系

**依赖组件**: cli, llm-client
**跨组件调用**: 是

---

## clarify_tool.py

**路径**: `tools\clarify_tool.py`
**行数**: 192

### 功能描述

Clarify Tool Module - Interactive Clarifying Questions

Allows the agent to present structured multiple-choice questions or open-ended
prompts to the user. In CLI mode, choices are navigable with arrow keys. On
messaging platforms, choices are rendered as a numbered list.

The actual user-interactio

### 核心函数

- `clarify_tool()`: Ask the user a question, optionally with multiple-choice options.

    Args:
        question: The q
- `check_clarify_requirements()`: Clarify tool has no external requirements -- always available.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## code_execution_tool.py

**路径**: `tools\code_execution_tool.py`
**行数**: 1849

### 功能描述

Code Execution Tool -- Programmatic Tool Calling (PTC)

Lets the LLM write a Python script that calls Hermes tools via RPC,
collapsing multi-step tool chains into a single inference turn.

Architecture (two transports):

  **Local backend (UDS):**
  1. Parent generates a `hermes_tools.py` stub modul

### 核心函数

- `check_sandbox_requirements()`: Code execution sandbox requires a POSIX OS for Unix domain sockets.
- `generate_hermes_tools_module()`: Build the source code for the hermes_tools.py stub module.

    Only tools in both SANDBOX_ALLOWED_T
- `json_parse()`
- `shell_quote()`
- `retry()`
- `execute_code()`: Run a Python script in a sandboxed child process with RPC access
    to a subset of Hermes tools.

 
- `build_execute_code_schema()`: Build the execute_code schema with description listing only enabled tools.

    When tools are disab

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, llm-client, state-management
**跨组件调用**: 是

---

## __init__.py

**路径**: `tools\computer_use\__init__.py`
**行数**: 44

### 功能描述

Computer use toolset — universal (any-model) macOS desktop control.

Architecture
------------
This toolset drives macOS apps through cua-driver's background computer-use
primitive (SkyLight private SPIs for focus-without-raise + pid-scoped event
posting). Unlike #4562's pyautogui backend, it does N

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## backend.py

**路径**: `tools\computer_use\backend.py`
**行数**: 172

### 功能描述

Abstract backend interface for computer use.

Any implementation (cua-driver over MCP, pyautogui, noop, future Linux/Windows)
must return the shape described below. All methods synchronous; async is
handled inside the backend implementation if needed.

### 核心类

- `UIElement`: One interactable element on the current screen.
- `CaptureResult`: Result of a screen capture call.

    At least one of png_b64 / elements is populated depending on c
- `ActionResult`: Result of any action (click / type / scroll / drag / key / wait).
- `ComputerUseBackend`: Lifecycle: `start()` before first use, `stop()` at shutdown.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## cua_backend.py

**路径**: `tools\computer_use\cua_backend.py`
**行数**: 1791

### 功能描述

Cua-driver backend (macOS, Windows, Linux).

Speaks MCP over stdio to `cua-driver`. The Python `mcp` SDK is async, so we
run a dedicated asyncio event loop on a background thread and marshal sync
calls through it.

The same `cua-driver call <tool>` surface (click, type_text, hotkey, drag,
scroll, sc

### 核心类

- `_AsyncBridge`: Runs one asyncio loop on a daemon thread; marshals coroutines from the caller.
- `_CuaDriverSession`: Holds the mcp ClientSession. Spawned lazily; re-entered on drop.

    Lifecycle ownership: a single 
- `CuaDriverBackend`: Default computer-use backend. Cross-platform via cua-driver MCP.

### 核心函数

- `cua_driver_child_env()`: Return the environment dict for spawning cua-driver.

    Starts from ``base_env`` (defaults to ``os
- `cua_driver_binary_available()`: True if `cua-driver` is on $PATH or HERMES_CUA_DRIVER_CMD resolves.
- `cua_driver_update_check()`: Run ``cua-driver check-update --json`` and return its parsed state.

    The payload mirrors the ``c
- `cua_driver_update_nudge()`: One-line "an update is available" message, or ``None`` when up to date,
    indeterminate, or the dr
- `cua_driver_install_hint()`

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## doctor.py

**路径**: `tools\computer_use\doctor.py`
**行数**: 272

### 功能描述

`hermes computer-use doctor` — thin client for cua-driver's `health_report` MCP tool.

cua-driver owns the health model (#1908 / be761fac on `main`). This module
just drives the stdio JSON-RPC handshake, calls `health_report`, and
renders the structured response. When the driver gets new checks, the

### 核心函数

- `run_doctor()`: Resolve the cua-driver binary, call `health_report`, render the result.

    Honors `HERMES_CUA_DRIV

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## permissions.py

**路径**: `tools\computer_use\permissions.py`
**行数**: 190

### 功能描述

Cross-platform Computer Use readiness + macOS permission helpers.

cua-driver runs on macOS, Windows, and Linux, but "ready to drive" means
something different on each:

  * macOS — explicit TCC grants (Accessibility + Screen Recording). cua-driver
    reports/requests them via ``permissions status`

### 核心函数

- `computer_use_status()`: Unified, OS-aware Computer Use readiness for the desktop card.

    ``ready`` is the single signal t
- `request_permissions_grant()`: Run ``cua-driver permissions grant`` (macOS); stream its output.

    Launches CuaDriver via LaunchS

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## schema.py

**路径**: `tools\computer_use\schema.py`
**行数**: 223

### 功能描述

Schema for the generic `computer_use` tool.

Model-agnostic. Any tool-calling model can drive this. Vision-capable models
should prefer `capture(mode='som')` then `click(element=N)` — much more
reliable than pixel coordinates. Pixel coordinates remain supported for
models that were trained on them (

### 核心函数

- `get_computer_use_schema()`: Return the generic OpenAI function-calling schema.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tool.py

**路径**: `tools\computer_use\tool.py`
**行数**: 918

### 功能描述

Entry point for the `computer_use` tool.

Universal (any-model) desktop control across macOS, Windows, and Linux via
cua-driver's background computer-use primitive. Replaces #4562's
Anthropic-native `computer_20251124` approach — the schema here is standard
OpenAI function-calling so every tool-capa

### 核心类

- `_NoopBackend`: Test/CI stub. Records calls; returns trivial results.

### 核心函数

- `set_approval_callback()`: Register a callback for computer_use approval prompts (used by CLI).

    Matches the terminal_tool.
- `reset_backend_for_tests()`: Test helper — tear down the cached backend.
- `handle_computer_use()`: Main entry point — dispatched by tools.registry.

    Returns either a JSON string (text-only) or a 
- `check_computer_use_requirements()`: Return True iff computer_use can run on this host.

    Conditions: macOS, Windows, or Linux + cua-d
- `get_computer_use_schema()`

### 依赖关系

**依赖组件**: cli, entry-points, llm-client, state-management
**跨组件调用**: 是

---

## vision_routing.py

**路径**: `tools\computer_use\vision_routing.py`
**行数**: 205

### 功能描述

Vision-routing decisions for ``computer_use`` capture results.

Background
----------
``computer_use(action='capture', mode='som'|'vision')`` returns a
``_multimodal`` envelope containing the captured screenshot. That envelope
is delivered back to the **active session model** as the tool result. Whe

### 核心函数

- `should_route_capture_to_aux_vision()`: Return True iff the captured screenshot should be pre-analysed via aux vision.

    Args:
      prov

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## computer_use_tool.py

**路径**: `tools\computer_use_tool.py`
**行数**: 40

### 功能描述

Shim for tool discovery. Registers `computer_use` with tools.registry.

The real implementation lives in the `tools/computer_use/` package to keep
the file structure clean. This shim exists because tools.registry auto-imports
`tools/*.py` — we need a top-level module to trigger the registration.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## credential_files.py

**路径**: `tools\credential_files.py`
**行数**: 456

### 功能描述

File passthrough registry for remote terminal backends.

Remote backends (Docker, Modal, SSH) create sandboxes with no host files.
This module ensures that credential files, skill directories, and host-side
cache directories (documents, images, audio, screenshots) are mounted or
synced into those sa

### 核心函数

- `register_credential_file()`: Register a credential file for mounting into remote sandboxes.

    *relative_path* is relative to `
- `register_credential_files()`: Register multiple credential files from skill frontmatter entries.

    Each entry is either a strin
- `get_credential_file_mounts()`: Return all credential files that should be mounted into remote sandboxes.

    Each item has ``host_
- `get_skills_directory_mount()`: Return mount info for all skill directories (local + external).

    Skills may include ``scripts/``
- `iter_skills_files()`: Yield individual (host_path, container_path) entries for skills files.

    Includes both the local 
- `get_cache_directory_mounts()`: Return mount entries for each cache directory that exists on disk.

    Used by Docker to create bin
- `map_cache_path_to_container()`: Map a host cache path to its mounted path under *container_base*.

    Returns the POSIX container p
- `to_agent_visible_cache_path()`: Translate a host cache path to its mounted path inside the sandbox.

    Returns the input unchanged
- `iter_cache_files()`: Return individual (host_path, container_path) entries for cache files.

    Used by Modal to upload 
- `clear_credential_files()`: Reset the skill-scoped registry (e.g. on session reset).

### 依赖关系

**依赖组件**: agent-engine, cli, security, state-management
**跨组件调用**: 是

---

## cronjob_tools.py

**路径**: `tools\cronjob_tools.py`
**行数**: 1033

### 功能描述

Cron job management tools for Hermes Agent.

Expose a single compressed action-oriented tool to avoid schema/context bloat.
Compatibility wrappers remain for direct Python callers and legacy tests.

### 核心函数

- `cronjob()`: Unified cron job management tool.
- `check_cronjob_requirements()`: Check if cronjob tools can be used.

    Available in interactive CLI mode and gateway/messaging pla

### 依赖关系

**依赖组件**: cli, cron, entry-points, gateway, security, state-management
**跨组件调用**: 是

---

## debug_helpers.py

**路径**: `tools\debug_helpers.py`
**行数**: 106

### 功能描述

Shared debug session infrastructure for Hermes tools.

Replaces the identical DEBUG_MODE / _log_debug_call / _save_debug_log /
get_debug_session_info boilerplate previously duplicated across web_tools,
vision_tools, and image_generation_tool.

Usage in a tool module:

    from tools.debug_helpers im

### 核心类

- `DebugSession`: Per-tool debug session that records tool calls to a JSON log file.

    Activated by a tool-specific

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## delegate_tool.py

**路径**: `tools\delegate_tool.py`
**行数**: 3199

### 功能描述

Delegate Tool -- Subagent Architecture

Spawns child AIAgent instances with isolated context, restricted toolsets,
and their own terminal sessions. Supports single-task and batch (parallel)
modes. The parent blocks until all children complete.

Each child gets:
  - A fresh conversation (no parent hi

### 核心类

- `DelegateEvent`: Formal event types emitted during delegation progress.

    _build_child_progress_callback normalise

### 核心函数

- `set_spawn_paused()`: Globally block/unblock new delegate_task spawns.

    Active children keep running; only NEW calls t
- `is_spawn_paused()`
- `interrupt_subagent()`: Request that a single running subagent stop at its next iteration boundary.

    Does not hard-kill 
- `list_active_subagents()`: Snapshot of the currently running subagent tree.

    Each record: {subagent_id, parent_id, depth, g
- `check_delegate_requirements()`: Delegation has no external requirements -- always available.
- `delegate_task()`: Spawn one or more child agents to handle delegated tasks.

    Supports two modes:
      - Single: p

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, gateway, state-management
**跨组件调用**: 是

---

## discord_tool.py

**路径**: `tools\discord_tool.py`
**行数**: 960

### 功能描述

Discord server introspection and management tool.

Provides the agent with the ability to interact with Discord servers
when running on the Discord gateway. Uses Discord REST API directly
with the bot token — no dependency on the gateway adapter's client.

Only included in the hermes-discord toolset

### 核心类

- `DiscordAPIError`: Raised when a Discord API call fails.

### 核心函数

- `get_dynamic_schema_core()`
- `get_dynamic_schema_admin()`
- `get_dynamic_schema()`: Backward-compat wrapper — returns core schema.
- `check_discord_tool_requirements()`: Tool is available only when a Discord bot token is configured.
- `discord_core()`: Execute a core Discord action (fetch_messages, search_members, create_thread).
- `discord_admin_handler()`: Execute a Discord admin action (server management).

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## env_passthrough.py

**路径**: `tools\env_passthrough.py`
**行数**: 164

### 功能描述

Environment variable passthrough registry.

Skills that declare ``required_environment_variables`` in their frontmatter
need those vars available in sandboxed execution environments (execute_code,
terminal).  By default both sandboxes strip secrets from the child process
environment for security.  T

### 核心函数

- `register_env_passthrough()`: Register environment variable names as allowed in sandboxed environments.

    Typically called when
- `is_env_passthrough()`: Check whether *var_name* is allowed to pass through to sandboxes.

    Returns ``True`` if the varia
- `get_all_passthrough()`: Return the union of skill-registered and config-based passthrough vars.
- `clear_env_passthrough()`: Reset the skill-scoped allowlist (e.g. on session reset).

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## env_probe.py

**路径**: `tools\env_probe.py`
**行数**: 249

### 功能描述

Local-environment toolchain probe for the system prompt.

When the terminal backend is local (the agent's tools run on the same
machine as Hermes itself), we surface a single deterministic line about
Python tooling state so models don't have to discover it by hitting
walls.  Common failure modes thi

### 核心函数

- `get_environment_probe_line()`: Return the cached probe line (building it on first call).

    Returns "" when the environment is cl

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `tools\environments\__init__.py`
**行数**: 15

### 功能描述

Hermes execution environment backends.

Each backend provides the same interface (BaseEnvironment ABC) for running
shell commands in a specific execution context: local, Docker, SSH,
Singularity, Modal, or Daytona. (Modal additionally has direct and
Nous-managed modes, selected via terminal.modal_mo

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## base.py

**路径**: `tools\environments\base.py`
**行数**: 898

### 功能描述

Base class for all Hermes execution environment backends.

Unified spawn-per-call model: every command spawns a fresh ``bash -c`` process.
A session snapshot (env vars, functions, aliases) is captured once at init and
re-sourced before each command. CWD persists via in-band stdout markers (remote)
o

### 核心类

- `ProcessHandle`: Duck type that every backend's _run_bash() must return.

    subprocess.Popen satisfies this nativel
- `_ThreadedProcessHandle`: Adapter for SDK backends (Modal, Daytona) that have no real subprocess.

    Wraps a blocking ``exec
- `BaseEnvironment`: Common interface and unified execution flow for all Hermes backends.

    Subclasses implement ``_ru

### 核心函数

- `set_activity_callback()`: Register a callback that _wait_for_process fires periodically.
- `touch_activity_if_due()`: Fire the activity callback at most once every ``state['interval']`` seconds.

    *state* must conta
- `get_sandbox_dir()`: Return the host-side root for all sandbox storage (Docker workspaces,
    Singularity overlays/SIF c

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## daytona.py

**路径**: `tools\environments\daytona.py`
**行数**: 271

### 功能描述

Daytona cloud execution environment.

Uses the Daytona Python SDK to run commands in cloud sandboxes.
Supports persistent sandboxes: when enabled, sandboxes are stopped on cleanup
and resumed on next creation, preserving the filesystem across sessions.

### 核心类

- `DaytonaEnvironment`: Daytona cloud sandbox execution backend.

    Spawn-per-call via _ThreadedProcessHandle wrapping blo

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## docker.py

**路径**: `tools\environments\docker.py`
**行数**: 1313

### 功能描述

Docker execution environment for sandboxed command execution.

Security hardened (cap-drop ALL, no-new-privileges, PID limits),
configurable resource limits (CPU, memory, disk), and optional filesystem
persistence via bind mounts.

### 核心类

- `DockerEnvironment`: Hardened Docker container execution with resource limits and persistence.

    Security: all capabil

### 核心函数

- `reap_orphan_containers()`: Remove stale hermes-tagged containers left behind by prior processes.

    Targets containers that m
- `find_docker()`: Locate the docker (or podman) CLI binary.

    Resolution order:
    1. ``HERMES_DOCKER_BINARY`` env

### 依赖关系

**依赖组件**: cli, llm-client, state-management
**跨组件调用**: 是

---

## file_sync.py

**路径**: `tools\environments\file_sync.py`
**行数**: 404

### 功能描述

Shared file sync manager for remote execution backends.

Tracks local file changes via mtime+size, detects deletions, and
syncs to remote environments transactionally.  Used by SSH, Modal,
and Daytona.  Docker and Singularity use bind mounts (live host FS
view) and don't need this.

### 核心类

- `FileSyncManager`: Tracks local file changes and syncs to a remote environment.

    Backends instantiate this with tra

### 核心函数

- `iter_sync_files()`: Enumerate all files that should be synced to a remote environment.

    Combines credentials, skills
- `quoted_rm_command()`: Build a shell ``rm -f`` command for a batch of remote paths.
- `quoted_mkdir_command()`: Build a shell ``mkdir -p`` command for a batch of directories.
- `unique_parent_dirs()`: Extract sorted unique parent directories from (host, remote) pairs.

### 依赖关系

**依赖组件**: gateway, llm-client, state-management
**跨组件调用**: 是

---

## local.py

**路径**: `tools\environments\local.py`
**行数**: 878

### 功能描述

Local execution environment — spawn-per-call with session snapshot.

### 核心类

- `LocalEnvironment`: Run commands directly on the host machine.

    Spawn-per-call: every execute() spawns a fresh bash 

### 依赖关系

**依赖组件**: acp-adapter, cli, gateway, llm-client, state-management
**跨组件调用**: 是

---

## managed_modal.py

**路径**: `tools\environments\managed_modal.py`
**行数**: 283

### 功能描述

Managed Modal environment backed by tool-gateway.

### 核心类

- `_ManagedModalExecHandle`
- `ManagedModalEnvironment`: Gateway-owned Modal sandbox with Hermes-compatible execute/cleanup.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## modal.py

**路径**: `tools\environments\modal.py`
**行数**: 479

### 功能描述

Modal cloud execution environment using the native Modal SDK directly.

Uses ``Sandbox.create()`` + ``Sandbox.exec()`` instead of the older runtime
wrapper, while preserving Hermes' persistent snapshot behavior across sessions.

### 核心类

- `_AsyncWorker`: Background thread with its own event loop for async-safe Modal calls.
- `ModalEnvironment`: Modal cloud execution via native Modal sandboxes.

    Spawn-per-call via _ThreadedProcessHandle wra

### 依赖关系

**依赖组件**: agent-engine, llm-client, state-management
**跨组件调用**: 是

---

## modal_utils.py

**路径**: `tools\environments\modal_utils.py`
**行数**: 205

### 功能描述

Shared Hermes-side execution flow for Modal transports.

This module deliberately stops at the Hermes boundary:
- command preparation
- cwd/timeout normalization
- stdin/sudo shell wrapping
- common result shape
- interrupt/cancel polling

Direct Modal and managed Modal keep separate transport logic

### 核心类

- `PreparedModalExec`: Normalized command data passed to a transport-specific exec runner.
- `ModalExecStart`: Transport response after starting an exec.
- `BaseModalExecutionEnvironment`: Execution flow for the *managed* Modal transport (gateway-owned sandbox).

    This deliberately ove

### 核心函数

- `wrap_modal_stdin_heredoc()`: Append stdin as a shell heredoc for transports without stdin piping.
- `wrap_modal_sudo_pipe()`: Feed sudo via a shell pipe for transports without direct stdin piping.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## singularity.py

**路径**: `tools\environments\singularity.py`
**行数**: 266

### 功能描述

Singularity/Apptainer persistent container environment.

Security-hardened with --containall, --no-home, capability dropping.
Supports configurable resource limits and optional filesystem persistence
via writable overlay directories that survive across sessions.

### 核心类

- `SingularityEnvironment`: Hardened Singularity/Apptainer container with resource limits and persistence.

    Spawn-per-call: 

### 依赖关系

**依赖组件**: llm-client, state-management
**跨组件调用**: 是

---

## ssh.py

**路径**: `tools\environments\ssh.py`
**行数**: 376

### 功能描述

SSH remote execution environment with ControlMaster connection persistence.

### 核心类

- `SSHEnvironment`: Run commands on a remote machine over SSH.

    Spawn-per-call: every execute() spawns a fresh ``ssh

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## fal_common.py

**路径**: `tools\fal_common.py`
**行数**: 164

### 功能描述

Shared FAL.ai SDK plumbing.

Holds the stateless atoms that every FAL-backed tool needs:

* :func:`import_fal_client` — lazy import + ``lazy_deps`` integration so
  ``fal_client`` isn't pulled at cold start (it added ~64 ms per CLI
  invocation when imported eagerly).
* :class:`_ManagedFalSyncClient

### 核心类

- `_ManagedFalSyncClient`: Small per-instance wrapper around ``fal_client.SyncClient`` for
    managed queue hosts.

    The wr

### 核心函数

- `import_fal_client()`: Import ``fal_client`` (via ``lazy_deps`` when available) and return
    the module reference.

    C

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## feishu_doc_tool.py

**路径**: `tools\feishu_doc_tool.py`
**行数**: 139

### 功能描述

Feishu Document Tool -- read document content via Feishu/Lark API.

Provides ``feishu_doc_read`` for reading document content as plain text.
Uses the same lazy-import + BaseRequest pattern as feishu_comment.py.

### 核心函数

- `set_client()`: Store a lark client for the current thread (called by feishu_comment).
- `get_client()`: Return the lark client for the current thread, or None.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## feishu_drive_tool.py

**路径**: `tools\feishu_drive_tool.py`
**行数**: 432

### 功能描述

Feishu Drive Tools -- document comment operations via Feishu/Lark API.

Provides tools for listing, replying to, and adding document comments.
Uses the same lazy-import + BaseRequest pattern as feishu_comment.py.
The lark client is injected per-thread by the comment event handler.

### 核心函数

- `set_client()`: Store a lark client for the current thread (called by feishu_comment).
- `get_client()`: Return the lark client for the current thread, or None.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## file_operations.py

**路径**: `tools\file_operations.py`
**行数**: 2424

### 功能描述

File Operations Module

Provides file manipulation capabilities (read, write, patch, search) that work
across all terminal backends (local, docker, ssh, singularity, modal, daytona).

The key insight is that all file operations can be expressed as shell commands,
so we wrap the terminal backend's ex

### 核心类

- `ReadResult`: Result from reading a file.
- `WriteResult`: Result from writing a file.
- `PatchResult`: Result from patching a file.
- `SearchMatch`: A single search match.
- `SearchResult`: Result from searching.
- `LintResult`: Result from linting a file.
- `ExecuteResult`: Result from executing a shell command.
- `FileOperations`: Abstract interface for file operations across terminal backends.
- `ShellFileOperations`: File operations implemented via shell commands.
    
    Works with ANY terminal backend that has ex

### 核心函数

- `normalize_read_pagination()`: Return safe read_file pagination bounds.

    Tool schemas declare minimum/maximum values, but not e
- `normalize_search_pagination()`: Return safe search pagination bounds for shell head/tail pipelines.

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## file_state.py

**路径**: `tools\file_state.py`
**行数**: 333

### 功能描述

Cross-agent file state coordination.

Prevents mangled edits when concurrent subagents (same process, same
filesystem) touch the same file. Complements the single-agent path-overlap
check in ``run_agent._should_parallelize_tool_batch`` — this module catches
the case where subagent B writes a file th

### 核心类

- `FileStateRegistry`: Process-wide coordinator for cross-agent file edits.

### 核心函数

- `get_registry()`
- `record_read()`
- `note_write()`: Record a successful write.

        Updates the global last-writer map AND this agent's own read sta
- `check_stale()`: Return a model-facing warning if this write would be stale.

        Three staleness classes, in ord
- `lock_path()`: Acquire the per-path lock for a read→modify→write section.

        Same process, same filesystem — 
- `writes_since()`: Return ``{writer_task_id: [paths]}`` for writes done after
        ``since_ts`` by agents OTHER than
- `known_reads()`: Return the list of resolved paths this agent has read.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## file_tools.py

**路径**: `tools\file_tools.py`
**行数**: 1829

### 功能描述

File Tools Module - LLM agent file manipulation tools.

### 核心函数

- `clear_file_ops_cache()`: Clear the file operations cache.
- `read_file_tool()`: Read a file with pagination and line numbers.
- `reset_file_dedup()`: Clear the deduplication cache for file reads.

    Called after context compression — the original r
- `notify_other_tool_call()`: Reset consecutive read/search counter for a task.

    Called by the tool dispatcher (model_tools.py
- `write_file_tool()`: Write content to a file.

    ``cross_profile`` opts out of the soft cross-Hermes-profile guard. The
- `patch_tool()`: Patch a file using replace mode or V4A patch format.

    ``cross_profile`` opts out of the soft cro
- `search_tool()`: Search for content or files.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, security, state-management
**跨组件调用**: 是

---

## fuzzy_match.py

**路径**: `tools\fuzzy_match.py`
**行数**: 866

### 功能描述

Fuzzy Matching Module for File Operations

Implements a multi-strategy matching chain to robustly find and replace text,
accommodating variations in whitespace, indentation, and escaping common
in LLM-generated code.

The 9-strategy chain (inspired by OpenCode), tried in order:
1. Exact match - Dire

### 核心函数

- `fuzzy_find_and_replace()`: Find and replace text using a chain of increasingly fuzzy matching strategies.

    Args:
        co
- `find_closest_lines()`: Find lines in content most similar to old_string for "did you mean?" feedback.

    Returns a format
- `format_no_match_hint()`: Return a '\n\nDid you mean...' snippet for plain no-match errors.

    Gated so the hint only fires 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## homeassistant_tool.py

**路径**: `tools\homeassistant_tool.py`
**行数**: 514

### 功能描述

Home Assistant tool for controlling smart home devices via REST API.

Registers four LLM-callable tools:
- ``ha_list_entities`` -- list/filter entities by domain or area
- ``ha_get_state`` -- get detailed state of a single entity
- ``ha_list_services`` -- list available services (actions) per domain

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## image_generation_tool.py

**路径**: `tools\image_generation_tool.py`
**行数**: 1681

### 功能描述

Image Generation Tools Module

Provides image generation via FAL.ai. Multiple FAL models are supported and
selectable via ``hermes tools`` → Image Generation; the active model is
persisted to ``image_gen.model`` in ``config.yaml``.

Architecture:
- ``FAL_MODELS`` is a catalog of supported models wit

### 核心函数

- `image_generate_tool()`: Generate an image from a text prompt, or edit a source image, via FAL.

    Routing: when ``image_ur
- `check_fal_api_key()`: True if the FAL.ai API key (direct or managed gateway) is available.
- `check_image_generation_requirements()`: True if any image gen backend is available.

    Providers are considered in this order:

    1. The
- `is_krea_model()`: True when ``model_id`` is a native Krea plugin id (``krea-2-*``).

### 依赖关系

**依赖组件**: agent-engine, cli, state-management
**跨组件调用**: 是

---

## interrupt.py

**路径**: `tools\interrupt.py`
**行数**: 99

### 功能描述

Per-thread interrupt signaling for all tools.

Provides thread-scoped interrupt tracking so that interrupting one agent
session does not kill tools running in other sessions.  This is critical
in the gateway where multiple agents run concurrently in the same process.

The agent stores its execution 

### 核心类

- `_ThreadAwareEventProxy`: Drop-in proxy that maps threading.Event methods to per-thread state.

### 核心函数

- `set_interrupt()`: Set or clear interrupt for a specific thread.

    Args:
        active: True to signal interrupt, F
- `is_interrupted()`: Check if an interrupt has been requested for the current thread.

    Safe to call from any thread —

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## kanban_tools.py

**路径**: `tools\kanban_tools.py`
**行数**: 1590

### 功能描述

Kanban tools — structured tool-call surface for worker + orchestrator agents.

These tools are registered into the model's schema when the agent is
running under the dispatcher (env var ``HERMES_KANBAN_TASK`` set) or when
the active profile explicitly enables the ``kanban`` toolset for
orchestrator 

### 核心函数

- `heartbeat_current_worker_from_env()`: Best-effort: extend the kanban claim + bump board heartbeat for the
    current dispatcher-spawned w

### 依赖关系

**依赖组件**: agent-engine, cli, gateway
**跨组件调用**: 是

---

## lazy_deps.py

**路径**: `tools\lazy_deps.py`
**行数**: 911

### 功能描述

Lazy dependency installer for opt-in Hermes Agent backends.

Many Hermes features (Mistral TTS, ElevenLabs TTS, Honcho memory, Bedrock,
Slack, Matrix, etc.) require Python packages that not every user needs. The
historical approach was to bundle them all under ``pyproject.toml`` extras
(``hermes-age

### 核心类

- `FeatureUnavailable`: A lazily-installable feature is missing and cannot be made available.

    Either the deps were neve
- `_InstallResult`

### 核心函数

- `activate_durable_lazy_target()`: Public: wire the durable lazy-install target onto ``sys.path``.

    Safe no-op when :data:`_LAZY_TA
- `feature_specs()`: Return the registered specs for a feature, or raise KeyError.
- `feature_missing()`: Return the subset of specs for ``feature`` not currently installed.
- `ensure()`: Make sure all packages for ``feature`` are importable.

    If they're missing, attempts to install 
- `is_available()`: Return True if the feature's deps are already satisfied.
- `feature_install_command()`: Return the ``pip install`` command a user could run manually, or None.
- `active_features()`: Return the list of features the user has ever lazy-installed.

    A feature counts as "active" if a
- `refresh_active_features()`: Re-run ``ensure`` for every feature the user has previously activated.

    Returns a ``{feature: st
- `ensure_and_bind()`: Ensure a feature is installed, then rebind names into the caller's globals.

    Combines :func:`ens

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## managed_tool_gateway.py

**路径**: `tools\managed_tool_gateway.py`
**行数**: 193

### 功能描述

Generic managed-tool gateway helpers for Nous-hosted vendor passthroughs.

### 核心类

- `ManagedToolGatewayConfig`

### 核心函数

- `auth_json_path()`: Return the Hermes auth store path, respecting HERMES_HOME overrides.
- `peek_nous_access_token()`: Cheap probe for a Nous gateway token without triggering refresh.

    Availability scans (`hermes to
- `read_nous_access_token()`: Read a Nous Subscriber OAuth access token from auth store or env override.
- `get_tool_gateway_scheme()`: Return configured shared gateway URL scheme.
- `build_vendor_gateway_url()`: Return the gateway origin for a specific vendor.
- `resolve_managed_tool_gateway()`: Resolve shared managed-tool gateway config for a vendor.
- `is_managed_tool_gateway_ready()`: Return True when gateway URL and a likely-usable Nous token are present.

    Defaults to :func:`pee

### 依赖关系

**依赖组件**: acp-adapter, state-management
**跨组件调用**: 是

---

## mcp_oauth.py

**路径**: `tools\mcp_oauth.py`
**行数**: 812

### 功能描述

MCP OAuth 2.1 Client Support

Implements the browser-based OAuth 2.1 authorization code flow with PKCE
for MCP servers that require OAuth authentication instead of static bearer
tokens.

Uses the MCP Python SDK's ``OAuthClientProvider`` (an ``httpx.Auth`` subclass)
which handles discovery, dynamic c

### 核心类

- `OAuthNonInteractiveError`: Raised when OAuth requires browser interaction in a non-interactive env.
- `HermesTokenStorage`: Persist OAuth tokens and client registration to JSON files.

    File layout::

        HERMES_HOME/

### 核心函数

- `remove_oauth_tokens()`: Delete stored OAuth tokens and client info for a server.
- `build_oauth_auth()`: Build an ``httpx.Auth``-compatible OAuth handler for an MCP server.

    Public API preserved for ba

### 依赖关系

**依赖组件**: acp-adapter, state-management
**跨组件调用**: 是

---

## mcp_oauth_manager.py

**路径**: `tools\mcp_oauth_manager.py`
**行数**: 715

### 功能描述

Central manager for per-server MCP OAuth state.

One instance shared across the process. Holds per-server OAuth provider
instances and coordinates:

- **Cross-process token reload** via mtime-based disk watch. When an external
  process (e.g. a user cron job) refreshes tokens on disk, the next auth 

### 核心类

- `_ProviderEntry`: Per-server OAuth state tracked by the manager.

    Fields:
        server_url: The MCP server URL u
- `MCPOAuthManager`: Single source of truth for per-server MCP OAuth state.

    Thread-safe: the ``_entries`` dict is gu

### 核心函数

- `get_manager()`: Return the process-wide :class:`MCPOAuthManager` singleton.
- `reset_manager_for_tests()`: Test-only helper: drop the singleton so fixtures start clean.

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## mcp_tool.py

**路径**: `tools\mcp_tool.py`
**行数**: 4771

### 功能描述

MCP (Model Context Protocol) Client Support

Connects to external MCP servers via stdio, HTTP/StreamableHTTP, or SSE
transport, discovers their tools, and registers them into the hermes-agent
tool registry so the agent can call them like any built-in tool.

Configuration is read from ~/.hermes/confi

### 核心类

- `InvalidMcpUrlError`: Raised when a remote MCP server's ``url`` cannot be parsed as http(s)://.

    Validated once at sta
- `NonMcpEndpointError`: Raised when an HTTP MCP URL serves a non-MCP response.

    A genuine MCP Streamable-HTTP endpoint a
- `SamplingHandler`: Handles sampling/createMessage requests for a single MCP server.

    Each MCPServerTask that has sa
- `ElicitationHandler`: Handles ``elicitation/create`` requests for a single MCP server.

    Each ``MCPServerTask`` that ha
- `MCPServerTask`: Manages a single MCP server connection in a dedicated asyncio Task.

    The entire connection lifec

### 核心函数

- `sanitize_mcp_name_component()`: Return an MCP name component safe for tool and prefix generation.

    Preserves Hermes's historical
- `register_mcp_servers()`: Connect to explicit MCP servers and register their tools.

    Idempotent for already-connected serv
- `discover_mcp_tools()`: Entry point: load config, connect to MCP servers, register tools.

    Called from ``model_tools`` a
- `is_mcp_tool_parallel_safe()`: Check if an MCP tool belongs to a server that supports parallel tool calls.

    MCP tool names foll
- `get_mcp_status()`: Return status of all configured MCP servers for banner display.

    Returns a list of dicts with ke
- `probe_mcp_server_tools()`: Temporarily connect to configured MCP servers and list their tools.

    Designed for ``hermes tools
- `has_registered_mcp_tools()`: True if any MCP server has actually registered tools into the registry.

    Cheap — checks the glob
- `refresh_agent_mcp_tools()`: Re-derive an already-built agent's tool snapshot from the live registry.

    The agent snapshots ``
- `shutdown_mcp_servers()`: Close all MCP server connections and stop the background loop.

    Each server Task is signalled to

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, gateway, llm-client, memory-system, state-management
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

## microsoft_graph_auth.py

**路径**: `tools\microsoft_graph_auth.py`
**行数**: 246

### 功能描述

Microsoft Graph app-only authentication helpers.

### 核心类

- `MicrosoftGraphAuthError`: Base class for Microsoft Graph auth failures.
- `MicrosoftGraphConfigError`: Raised when Graph credentials are missing or invalid.
- `MicrosoftGraphTokenError`: Raised when token acquisition fails.
- `GraphCredentials`: Normalized Microsoft Graph app-only credentials.
- `CachedAccessToken`: Cached app-only Graph access token.
- `MicrosoftGraphTokenProvider`: Acquire and cache Microsoft Graph app-only access tokens.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## microsoft_graph_client.py

**路径**: `tools\microsoft_graph_client.py`
**行数**: 409

### 功能描述

Reusable Microsoft Graph REST client helpers.

### 核心类

- `MicrosoftGraphClientError`: Base class for Graph client failures.
- `MicrosoftGraphAPIError`: Raised when a Graph API request fails.
- `MicrosoftGraphClient`: Minimal async Microsoft Graph client with retries and pagination.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## neutts_synth.py

**路径**: `tools\neutts_synth.py`
**行数**: 105

### 功能描述

Standalone NeuTTS synthesis helper.

Called by tts_tool.py via subprocess to keep the TTS model (~500MB)
in a separate process that exits after synthesis — no lingering memory.

Usage:
    python -m tools.neutts_synth --text "Hello" --out output.wav         --ref-audio samples/jo.wav --ref-text samp

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## openrouter_client.py

**路径**: `tools\openrouter_client.py`
**行数**: 34

### 功能描述

Shared OpenRouter API client for Hermes tools.

Provides a single lazy-initialized AsyncOpenAI client that all tool modules
can share.  Routes through the centralized provider router in
agent/auxiliary_client.py so auth, headers, and API format are handled
consistently.

### 核心函数

- `get_async_client()`: Return a shared async OpenAI-compatible client for OpenRouter.

    The client is created lazily on 
- `check_api_key()`: Check whether the OpenRouter API key is present.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## osv_check.py

**路径**: `tools\osv_check.py`
**行数**: 170

### 功能描述

OSV malware check for MCP extension packages.

Before launching an MCP server via npx/uvx, queries the OSV (Open Source
Vulnerabilities) API to check if the package has any known malware advisories
(MAL-* IDs).  Regular CVEs are ignored — only confirmed malware is blocked.

The API is free, public, 

### 核心函数

- `check_package_for_malware()`: Check if an MCP server package has known malware advisories.

    Inspects the *command* (e.g. ``npx

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## patch_parser.py

**路径**: `tools\patch_parser.py`
**行数**: 623

### 功能描述

V4A Patch Format Parser

Parses the V4A patch format used by codex, cline, and other coding agents.

V4A Format:
    *** Begin Patch
    *** Update File: path/to/file.py
    @@ optional context hint @@
     context line (space prefix)
    -removed line (minus prefix)
    +added line (plus prefix)
  

### 核心类

- `OperationType`
- `HunkLine`: A single line in a patch hunk.
- `Hunk`: A group of changes within a file.
- `PatchOperation`: A single operation in a V4A patch.

### 核心函数

- `parse_v4a_patch()`: Parse a V4A format patch.
    
    Args:
        patch_content: The patch text in V4A format
    
  
- `apply_v4a_operations()`: Apply V4A patch operations using a file operations interface.

    Uses a two-phase validate-then-ap

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## path_security.py

**路径**: `tools\path_security.py`
**行数**: 44

### 功能描述

Shared path validation helpers for tool implementations.

Extracts the ``resolve() + relative_to()`` and ``..`` traversal check
patterns previously duplicated across skill_manager_tool, skills_tool,
skills_hub, cronjob_tools, and credential_files.

### 核心函数

- `validate_within_dir()`: Ensure *path* resolves to a location within *root*.

    Returns an error message string if validati
- `has_traversal_component()`: Return True if *path_str* contains ``..`` traversal components.

    Quick check for obvious travers

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## process_registry.py

**路径**: `tools\process_registry.py`
**行数**: 2083

### 功能描述

Process Registry -- In-memory registry for managed background processes.

Tracks processes spawned via terminal(background=true), providing:
  - Output buffering (rolling 200KB window)
  - Status polling and log retrieval
  - Blocking wait with interrupt support
  - Process killing
  - Crash recover

### 核心类

- `ProcessSession`: A tracked background process with output buffering.
- `ProcessRegistry`: In-memory registry of running and finished background processes.

    Thread-safe. Accessed from:
  

### 核心函数

- `format_uptime_short()`
- `format_process_notification()`: Format a process notification event into a [IMPORTANT: ...] message.

    Handles completion events 

### 依赖关系

**依赖组件**: cli, entry-points, gateway
**跨组件调用**: 是

---

## project_tools.py

**路径**: `tools\project_tools.py`
**行数**: 190

### 功能描述

Project tools — the agent's INTENTIONAL handle on first-class Projects.

Projects (per-profile ``projects.db``) are the named workspaces the desktop
sidebar groups sessions into. Creating / switching a project is a deliberate act
expressed as explicit tools — never a side effect of a terminal ``cd``

### 核心函数

- `set_project_workspace_callback()`
- `project_list()`
- `project_create()`
- `project_switch()`

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## read_extract.py

**路径**: `tools\read_extract.py`
**行数**: 249

### 功能描述

Stdlib document-to-text extraction for ``read_file``.

Supports Jupyter notebooks, DOCX, and XLSX without adding hard dependencies.
Malformed documents raise :class:`ExtractionError`; callers can then fall back to
normal text/binary handling.

### 核心类

- `ExtractionError`: Raised when a supported-looking document cannot be rendered as text.

### 核心函数

- `is_extractable_document()`
- `extract_document_text()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## read_terminal_tool.py

**路径**: `tools\read_terminal_tool.py`
**行数**: 94

### 功能描述

Read the in-app terminal pane in the Hermes desktop GUI.

The embedded terminal's buffer lives in the desktop renderer (xterm.js), so this
tool round-trips through the gateway's blocking-prompt bridge — the same one
`clarify` uses: tui_gateway emits ``terminal.read.request``, the renderer answers
wi

### 核心函数

- `read_terminal_tool()`: Return the in-app terminal's contents (+ line metadata) as a JSON string.
- `check_read_terminal_requirements()`: Desktop GUI only — HERMES_DESKTOP is set on the gateway the app spawns.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## registry.py

**路径**: `tools\registry.py`
**行数**: 590

### 功能描述

Central registry for all hermes-agent tools.

Each tool file calls ``registry.register()`` at module level to declare its
schema, handler, toolset membership, and availability check.  ``model_tools.py``
queries the registry instead of maintaining its own parallel data structures.

Import chain (circ

### 核心类

- `ToolEntry`: Metadata for a single registered tool.
- `ToolRegistry`: Singleton registry that collects tool schemas + handlers from tool files.

### 核心函数

- `discover_builtin_tools()`: Import built-in self-registering tool modules and return their module names.
- `invalidate_check_fn_cache()`: Drop all cached ``check_fn`` results. Call after config changes that
    affect tool availability (e
- `tool_error()`: Return a JSON error string for tool handlers.

    >>> tool_error("file not found")
    '{"error": "
- `tool_result()`: Return a JSON result string for tool handlers.

    Accepts a dict positional arg *or* keyword argum

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## schema_sanitizer.py

**路径**: `tools\schema_sanitizer.py`
**行数**: 484

### 功能描述

Sanitize tool JSON schemas for broad LLM-backend compatibility.

Some local inference backends (notably llama.cpp's ``json-schema-to-grammar``
converter used to build GBNF tool-call parsers) are strict about what JSON
Schema shapes they accept. Schemas that OpenAI / Anthropic / most cloud
providers 

### 核心函数

- `sanitize_tool_schemas()`: Return a copy of ``tools`` with each tool's parameter schema sanitized.

    Input is an OpenAI-form
- `strip_nullable_unions()`: Collapse ``anyOf`` / ``oneOf`` nullable unions to the non-null branch.

    MCP / Pydantic optional 
- `strip_pattern_and_format()`: Strip ``pattern`` and ``format`` JSON Schema keywords from tool schemas.

    This is a *reactive* s
- `strip_slash_enum()`: Strip ``enum`` keywords whose string values contain a forward slash.

    xAI's ``/v1/responses`` an

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## send_message_tool.py

**路径**: `tools\send_message_tool.py`
**行数**: 1692

### 功能描述

Send Message Tool -- cross-channel messaging via platform APIs.

Sends a message to a user or channel on any connected messaging platform
(Telegram, Discord, Slack). Supports listing available targets and resolving
human-friendly channel names to IDs. Works in both CLI and gateway contexts.

### 核心函数

- `send_message_tool()`: Handle cross-channel send_message tool calls.

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, gateway, llm-client
**跨组件调用**: 是

---

## session_search_tool.py

**路径**: `tools\session_search_tool.py`
**行数**: 881

### 功能描述

Session Search Tool - Long-Term Conversation Recall

Single-shape tool with three calling modes (inferred from args, no explicit
mode parameter):

  1. DISCOVERY — pass ``query``. Runs FTS5, dedupes hits by session lineage,
     returns top N sessions each with: snippet, ±5 message window around the

### 核心函数

- `session_search()`: Single-shape tool. Mode inferred from which args are set.

    Discovery: pass ``query``.
    Scroll
- `check_session_search_requirements()`: Requires the SQLite state database.

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## skill_manager_tool.py

**路径**: `tools\skill_manager_tool.py`
**行数**: 1326

### 功能描述

Skill Manager Tool -- Agent-Managed Skill Creation & Editing

Allows the agent to create, update, and delete skills, turning successful
approaches into reusable procedural knowledge. New skills are created in
~/.hermes/skills/. Existing skills (bundled, hub-installed, or user-created)
can be modifie

### 核心函数

- `apply_skill_pending()`: Replay a staged skill write, bypassing the gate. Returns the tool result
    JSON string. Called by 
- `skill_manage()`: Manage user-created skills. Dispatches to the appropriate action handler.

    Returns JSON string w

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, security, state-management
**跨组件调用**: 是

---

## skill_provenance.py

**路径**: `tools\skill_provenance.py`
**行数**: 79

### 功能描述

Skill write-origin provenance — ContextVar for distinguishing agent-sediment skill writes from foreground user-directed writes.

The curator only consolidates/prunes skills it autonomously created via the
background self-improvement review fork. Skills a user asks a foreground
agent to write belong 

### 核心函数

- `set_current_write_origin()`: Bind the active write origin to the current context.

    Returns a Token the caller must pass to re
- `reset_current_write_origin()`: Restore the prior write origin context.
- `get_current_write_origin()`: Return the active write origin.

    Default: "foreground" — any tool call made by a regular (non-re
- `is_background_review()`: Convenience: True iff the current write origin is the background
    review fork.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## skill_usage.py

**路径**: `tools\skill_usage.py`
**行数**: 948

### 功能描述

Skill usage telemetry + provenance tracking for the Curator feature.

Tracks per-skill usage metadata in a sidecar JSON file (~/.hermes/skills/.usage.json)
keyed by skill name. Counters are bumped by the existing skill tools (skill_view,
skill_manage); the curator orchestrator reads the derived acti

### 核心函数

- `is_protected_builtin()`: Whether *skill_name* is a load-bearing built-in the curator never touches.

    Protected built-ins 
- `latest_activity_at()`: Return the newest actual activity timestamp for a usage record.

    "Activity" means a skill was us
- `activity_count()`: Return the total observed activity count across use/view/patch events.
- `read_suppressed_names()`: Built-in skills the curator pruned — the re-seeder must leave archived.

    One skill name per line
- `add_suppressed_name()`: Record that a built-in skill was pruned, so sync won't restore it.
- `remove_suppressed_name()`: Clear a built-in's suppression entry (e.g. on restore).
- `list_agent_created_skill_names()`: Enumerate skills the curator may manage.

    Always includes agent-authored skills (those marked in
- `list_archived_skill_names()`: Enumerate skills in ``~/.hermes/skills/.archive/``.

    Archive layout is flat (``.archive/<skill>/
- `is_agent_created()`: Whether *skill_name* is neither bundled nor hub-installed.
- `is_hub_installed()`: Whether *skill_name* was installed via the Skills Hub.
- `is_bundled()`: Whether *skill_name* was seeded from the bundled repo skills.
- `is_curation_eligible()`: Whether the curator may track/archive *skill_name*.

    Agent-created skills are always eligible. B
- `load_usage()`: Read the entire .usage.json map. Returns empty dict on missing/corrupt.
- `save_usage()`: Write the usage map atomically. Best-effort — errors are logged, not raised.
- `get_record()`: Return the record for *skill_name*, creating a fresh one if missing.
- ... 还有 13 个函数

### 依赖关系

**依赖组件**: agent-engine, cli, state-management
**跨组件调用**: 是

---

## skills_ast_audit.py

**路径**: `tools\skills_ast_audit.py`
**行数**: 134

### 功能描述

AST-level deep audit for skill Python files — opt-in diagnostic, not a security gate.

Per SECURITY.md §2.4, Skills Guard is in-process heuristics ("useful — not
boundaries"). This module is a separate opt-in diagnostic that flags dynamic
import / dynamic attribute access patterns operators may want

### 核心函数

- `ast_scan_path()`: Scan a single .py file or recursively scan all .py under a directory.

    Returns a list of (file, 
- `format_ast_report()`: Plain-text report (Rich-markup-free) grouped by file.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## skills_guard.py

**路径**: `tools\skills_guard.py`
**行数**: 1087

### 功能描述

Skills Guard — Security scanner for externally-sourced skills.

Every skill downloaded from a registry passes through this scanner before
installation. It uses regex-based static analysis to detect known-bad patterns
(data exfiltration, prompt injection, destructive commands, persistence, etc.)
and 

### 核心类

- `Finding`
- `ScanResult`

### 核心函数

- `scan_file()`: Scan a single file for threat patterns and invisible unicode characters.

    Args:
        file_pat
- `scan_skill()`: Scan all files in a skill directory for security threats.

    Performs:
    1. Structural checks (f
- `should_allow_install()`: Determine whether a skill should be installed based on scan result and trust.

    Args:
        res
- `format_scan_report()`: Format a scan result as a human-readable report string.

    Returns a compact multi-line report sui
- `content_hash()`: Compute a SHA-256 hash of all files in a skill directory for integrity tracking.

    File paths (re

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## skills_hub.py

**路径**: `tools\skills_hub.py`
**行数**: 3889

### 功能描述

Skills Hub — Source adapters and hub state management for the Hermes Skills Hub.

This is a library module (not an agent tool). It provides:
  - GitHubAuth: Shared GitHub API authentication (PAT, gh CLI, GitHub App)
  - SkillSource ABC: Interface for all skill registry adapters
  - OptionalSkillSour

### 核心类

- `SkillMeta`: Minimal metadata returned by search results.
- `SkillBundle`: A downloaded skill ready for quarantine/scanning/installation.
- `GitHubAuth`: GitHub API authentication. Tries methods in priority order:
      1. GITHUB_TOKEN / GH_TOKEN env var
- `SkillSource`: Abstract base for all skill registry adapters.
- `GitHubSource`: Fetch skills from GitHub repos via the Contents API.
- `WellKnownSkillSource`: Read skills from a domain exposing /.well-known/skills/index.json.
- `UrlSource`: Fetch a single-file SKILL.md skill directly from an HTTP(S) URL.

    The identifier IS the URL (e.g
- `SkillsShSource`: Discover skills via skills.sh and fetch content from the underlying GitHub repo.
- `ClawHubSource`: Fetch skills from ClawHub (clawhub.ai) via their HTTP API.
    All skills are treated as community t
- `ClaudeMarketplaceSource`: Discover skills from Claude Code marketplace repos.
    Marketplace repos contain .claude-plugin/mar
- ... 还有 6 个类

### 核心函数

- `append_audit_log()`: Append a line to the audit log.
- `ensure_hub_dirs()`: Create the .hub directory structure if it doesn't exist.
- `quarantine_bundle()`: Write a skill bundle to the quarantine directory for scanning.
- `install_from_quarantine()`: Move a scanned skill from quarantine into the skills directory.
- `uninstall_skill()`: Remove a hub-installed skill. Refuses to remove builtins.
- `bundle_content_hash()`: Compute a deterministic hash for an in-memory skill bundle.
- `check_for_skill_updates()`: Check installed hub skills for upstream changes.
- `create_source_router()`: Create all configured source adapters.
    Returns a list of active sources for search/fetch operati
- `parallel_search_sources()`: Search all sources in parallel with per-source timeout.

    Returns ``(all_results, source_counts, 
- `unified_search()`: Search all sources (in parallel) and merge results.

### 依赖关系

**依赖组件**: agent-engine, state-management
**跨组件调用**: 是

---

## skills_sync.py

**路径**: `tools\skills_sync.py`
**行数**: 1125

### 功能描述

Skills Sync -- Manifest-based seeding and updating of bundled skills.

Copies bundled skills from the repo's skills/ directory into ~/.hermes/skills/
and uses a manifest to track which skills have been synced and their origin hash.

Manifest format (v2): each line is "skill_name:origin_hash" where o

### 核心函数

- `restore_official_optional_skill()`: Restore one or all official optional skills from repo source.

    ``restore=False`` only performs e
- `sync_skills()`: Sync bundled skills into ~/.hermes/skills/ using the manifest.

    Returns:
        dict with keys:
- `reset_bundled_skill()`: Reset a bundled skill's manifest tracking so future syncs work normally.

    When a user edits a bu
- `list_user_modified_bundled_skills()`: Return the bundled skills that ``hermes update`` keeps because the user
    edited them locally.

  
- `diff_bundled_skill()`: Diff a user's copy of a bundled skill against the current stock version.

    Lets a user see exactl
- `set_bundled_skills_opt_out()`: Toggle the .no-bundled-skills opt-out marker for the active profile.

    When ``enabled`` is True, 
- `is_bundled_skills_opt_out()`: Return True if the active profile carries the opt-out marker.
- `remove_pristine_bundled_skills()`: Delete bundled skills that are present, manifest-tracked, AND unmodified.

    Safety is the whole p

### 依赖关系

**依赖组件**: agent-engine, entry-points, state-management
**跨组件调用**: 是

---

## skills_tool.py

**路径**: `tools\skills_tool.py`
**行数**: 1639

### 功能描述

Skills Tool Module

This module provides tools for listing and viewing skill documents.
Skills are organized as directories containing a SKILL.md file (the main instructions)
and optional supporting files like references, templates, and examples.

Inspired by Anthropic's Claude Skills system with pr

### 核心类

- `SkillReadinessStatus`

### 核心函数

- `load_env()`: Load profile-scoped environment variables from HERMES_HOME/.env.
- `set_secret_capture_callback()`
- `skill_matches_platform()`: Check if a skill is compatible with the current OS platform.

    Delegates to ``agent.skill_utils.s
- `skill_matches_environment()`: Check if a skill is relevant to the current runtime environment.

    Delegates to ``agent.skill_uti
- `check_skills_requirements()`: Skills are always available -- the directory is created on first use if needed.
- `skills_list()`: List all available skills (progressive disclosure tier 1 - minimal metadata).

    Returns only name
- `skill_view()`: View the content of a skill or a specific file within a skill directory.

    Args:
        name: Na

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, gateway, llm-client, security, state-management
**跨组件调用**: 是

---

## slash_confirm.py

**路径**: `tools\slash_confirm.py`
**行数**: 168

### 功能描述

Generic slash-command confirmation primitive (gateway-side).

Slash commands that have a non-destructive but expensive side effect worth
surfacing to the user (currently only ``/reload-mcp``, which invalidates
the provider prompt cache) route through this module.

Two delivery paths:

  1. Button UI

### 核心函数

- `register()`: Register a pending slash-command confirmation.

    Overwrites any prior pending confirm for the sam
- `get_pending()`: Return the pending confirm dict for a session, or None.
- `clear()`: Drop the pending confirm for ``session_key`` without running it.
- `clear_if_stale()`: Drop the pending confirm if older than ``timeout`` seconds.

    Returns True if an entry was droppe
- `resolve_sync_compat()`: Synchronous helper: schedule resolve() on a loop and wait for the result.

    Used by platform call

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## terminal_tool.py

**路径**: `tools\terminal_tool.py`
**行数**: 2945

### 功能描述

Terminal Tool Module

A terminal tool that executes commands in local, Docker, Modal, SSH,
Singularity, and Daytona environments. Supports local execution,
containerized backends, and cloud sandboxes, including managed Modal mode.

Supported environments:
- "local": Execute directly on the host mach

### 核心函数

- `set_sudo_password_callback()`: Register a callback for sudo password prompts (used by CLI).

    Per-thread scope — ACP sessions th
- `set_approval_callback()`: Register a callback for dangerous command approval prompts.

    Per-thread scope — ACP sessions tha
- `register_task_env_overrides()`: Register environment overrides for a specific task/rollout.

    Called by Atropos environments befo
- `clear_task_env_overrides()`: Clear environment overrides for a task after rollout completes.

    Called during cleanup to avoid 
- `resolve_task_overrides()`: Return the env overrides for *task_id*, raw key first then collapsed.

    ``register_task_env_overr
- `get_active_env()`: Return the active BaseEnvironment for *task_id*, or None.
- `is_persistent_env()`: Return True if the active environment for task_id is configured for
    cross-turn persistence (``pe
- `cleanup_all_environments()`: Clean up ALL active environments. Use with caution.
- `cleanup_vm()`: Manually clean up a specific environment by task_id.

    *force_remove* (default False) is forwarde
- `terminal_tool()`: Execute a command in the configured terminal environment.

    Args:
        command: The command to
- `check_terminal_requirements()`: Check if all requirements for the terminal tool are met.

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, gateway, state-management
**跨组件调用**: 是

---

## thread_context.py

**路径**: `tools\thread_context.py`
**行数**: 121

### 功能描述

Propagate agent-turn context into worker threads that dispatch Hermes tools.

A bare ``threading.Thread`` / ``ThreadPoolExecutor`` worker starts with an
empty ``contextvars.Context`` and no thread-local approval/sudo callbacks.
Tool dispatch inside such a thread therefore silently loses:

  * the ap

### 核心函数

- `propagate_context_to_thread()`: Wrap *target* for execution on a worker thread with the *current*
    thread's ContextVars and appro

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## threat_patterns.py

**路径**: `tools\threat_patterns.py`
**行数**: 259

### 功能描述

Shared threat-pattern library for context window security scanning.

This module is the single source of truth for prompt-injection / promptware /
exfiltration patterns used across the context-assembly scanners
(``agent/prompt_builder.py``, ``tools/memory_tool.py``) and the tool-result
delimiter sys

### 核心函数

- `scan_for_threats()`: Return a list of matched pattern IDs in ``content`` at the given scope.

    ``scope`` selects which
- `first_threat_message()`: Return a human-readable error string for the first threat found, or None.

    Convenience wrapper u

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tirith_security.py

**路径**: `tools\tirith_security.py`
**行数**: 872

### 功能描述

Tirith pre-exec security scanning wrapper.

Runs the tirith binary as a subprocess to scan commands for content-level
threats (homograph URLs, pipe-to-interpreter, terminal injection, etc.).

Exit code is the verdict source of truth:
  0 = allow, 1 = block, 2 = warn

JSON stdout enriches findings/su

### 核心函数

- `is_platform_supported()`: True when tirith ships a prebuilt binary for this OS+arch.

    Used by callers (CLI banner, etc.) t
- `ensure_installed()`: Ensure tirith is available, downloading in background if needed.

    Quick PATH/local checks are sy
- `check_command_security()`: Run tirith security scan on a command.

    Exit code determines action (0=allow, 1=block, 2=warn). 

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## todo_tool.py

**路径**: `tools\todo_tool.py`
**行数**: 326

### 功能描述

Todo Tool Module - Planning & Task Management

Provides an in-memory task list the agent uses to decompose complex tasks,
track progress, and maintain focus across long conversations. The state
lives on the AIAgent instance (one per session) and is re-injected into
the conversation after context com

### 核心类

- `TodoStore`: In-memory todo list. One instance per AIAgent (one per session).

    Items are ordered -- list posi

### 核心函数

- `todo_tool()`: Single entry point for the todo tool. Reads or writes depending on params.

    Args:
        todos:
- `check_todo_requirements()`: Todo tool has no external requirements -- always available.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## tool_backend_helpers.py

**路径**: `tools\tool_backend_helpers.py`
**行数**: 183

### 功能描述

Shared helpers for tool backend selection.

### 核心函数

- `managed_nous_tools_enabled()`: Return True when the user is entitled to the Nous Tool Gateway.

    Entitlement is paid Nous Portal
- `nous_tool_gateway_unavailable_message()`: Return account-aware guidance for an unavailable Nous Tool Gateway path.
- `normalize_browser_cloud_provider()`: Return a normalized browser provider key.
- `coerce_modal_mode()`: Return the requested modal mode when valid, else the default.
- `normalize_modal_mode()`: Return a normalized modal execution mode.
- `has_direct_modal_credentials()`: Return True when direct Modal credentials/config are available.
- `resolve_modal_backend_state()`: Resolve direct vs managed Modal backend selection.

    Semantics:
    - ``direct`` means direct-onl
- `resolve_openai_audio_api_key()`: Prefer the voice-tools key, but fall back to the normal OpenAI key.
- `prefers_gateway()`: Return True when the user opted into the Tool Gateway for this tool.

    Reads ``<section>.use_gate
- `fal_key_is_configured()`: Return True when FAL_KEY is set to a non-whitespace value.

    Consults both ``os.environ`` and ``~

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## tool_output_limits.py

**路径**: `tools\tool_output_limits.py`
**行数**: 111

### 功能描述

Configurable tool-output truncation limits.

Ported from anomalyco/opencode PR #23770 (``feat(truncate): allow
configuring tool output truncation limits``).

OpenCode hardcoded ``MAX_LINES = 2000`` and ``MAX_BYTES = 50 * 1024``
as tool-output truncation thresholds. Hermes-agent had the same
hardcode

### 核心函数

- `get_tool_output_limits()`: Return resolved tool-output limits, reading ``tool_output`` from config.

    Keys: ``max_bytes``, `
- `get_max_bytes()`: Shortcut for terminal-tool callers that only need the byte cap.
- `get_max_lines()`: Shortcut for file-ops callers that only need the line cap.
- `get_max_line_length()`: Shortcut for file-ops callers that only need the per-line cap.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## tool_result_storage.py

**路径**: `tools\tool_result_storage.py`
**行数**: 233

### 功能描述

Tool result persistence -- preserves large outputs instead of truncating.

Defense against context-window overflow operates at three levels:

1. **Per-tool output cap** (inside each tool): Tools like search_files
   pre-truncate their own output before returning. This is the first line
   of defense

### 核心函数

- `generate_preview()`: Truncate at last newline within max_chars. Returns (preview, has_more).
- `maybe_persist_tool_result()`: Layer 2: persist oversized result into the sandbox, return preview + path.

    Writes via env.execu
- `enforce_turn_budget()`: Layer 3: enforce aggregate budget across all tool results in a turn.

    If total chars exceed budg

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tool_search.py

**路径**: `tools\tool_search.py`
**行数**: 736

### 功能描述

Progressive tool disclosure ("tool search") for Hermes Agent.

When enabled, MCP and non-core plugin tools are replaced in the model-visible
tools array by three bridge tools — ``tool_search``, ``tool_describe``,
``tool_call`` — and surfaced on demand. Core Hermes tools never defer.

Design constrai

### 核心类

- `ToolSearchConfig`: Resolved, validated tool-search configuration for a single assembly.
- `CatalogEntry`: One deferrable tool, in a form the bridge tools can search and serve.
- `AssemblyResult`: Outcome of one assembly. Useful for tests and observability.

### 核心函数

- `load_config()`: Load tool-search config from the user config file.
- `is_deferrable_tool_name()`: Return True if a tool with this name is *eligible* for deferral.

    A tool is deferrable iff it is
- `classify_tools()`: Split a tool-defs list into (visible, deferrable).

    ``visible`` retains every tool that must sta
- `estimate_tokens_from_schemas()`: Estimate the token cost of a tool-defs list via the chars/4 rule.

    Cheap and stable across provi
- `should_activate()`: Decide whether tool search should activate for the current assembly.

    ``"off"`` skips unconditio
- `build_catalog()`: Build the deferred-tool catalog from a tool-defs list.

    Caller is expected to pass only the defe
- `search_catalog()`: Return the top-``limit`` catalog entries for ``query`` by BM25.

    Falls back to a stable name-sub
- `bridge_tool_schemas()`: Build the bridge tool schemas to inject in place of deferred tools.

    The schemas are intentional
- `assemble_tool_defs()`: Return the tool-defs list the model should actually see.

    When tool search is inactive (off, no 
- `is_bridge_tool()`
- `dispatch_tool_search()`: Execute the ``tool_search`` bridge tool. Returns a JSON string.
- `dispatch_tool_describe()`: Execute the ``tool_describe`` bridge tool. Returns a JSON string.
- `scoped_deferrable_names()`: Return the set of deferrable tool names present in ``tool_defs``.

    ``tool_defs`` is expected to 
- `resolve_underlying_call()`: Parse a ``tool_call`` invocation into (underlying_name, args, error_msg).

    Used by:
    * the di

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## transcription_tools.py

**路径**: `tools\transcription_tools.py`
**行数**: 1799

### 功能描述

Transcription Tools Module

Provides speech-to-text transcription with six providers:

  - **local** (default, free) — faster-whisper running locally, no API key needed.
    Auto-downloads the model (~150 MB for ``base``) on first use.
  - **groq** (free tier) — Groq Whisper API, requires ``GROQ_API

### 核心函数

- `get_env_value()`: Read env values through the live config module.

    Tests may monkeypatch and later restore ``herme
- `is_stt_enabled()`: Return whether STT is enabled in config.
- `transcribe_audio()`: Transcribe an audio file using the configured STT provider.

    Provider priority:
      1. User co

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points
**跨组件调用**: 是

---

## tts_tool.py

**路径**: `tools\tts_tool.py`
**行数**: 2845

### 功能描述

Text-to-Speech Tool Module

Built-in TTS providers:
- Edge TTS (default, free, no API key): Microsoft Edge neural voices
- ElevenLabs (premium): High-quality voices, needs ELEVENLABS_API_KEY
- OpenAI TTS: Good quality, needs OPENAI_API_KEY
- MiniMax TTS: High-quality with voice cloning, needs MINIMA

### 核心函数

- `get_env_value()`: Read env values through the live config module.

    Tests may monkeypatch and later restore ``herme
- `text_to_speech_tool()`: Convert text to speech audio.

    Reads provider/voice config from ~/.hermes/config.yaml (tts: sect
- `check_tts_requirements()`: Check if at least one TTS provider is available.

    Edge TTS needs no API key and is the default, 
- `stream_tts_to_speaker()`: Consume text deltas from *text_queue*, buffer them into sentences,
    and stream each sentence thro

### 依赖关系

**依赖组件**: agent-engine, cli, gateway, llm-client, security, state-management
**跨组件调用**: 是

---

## url_safety.py

**路径**: `tools\url_safety.py`
**行数**: 410

### 功能描述

URL safety checks — blocks requests to private/internal network addresses.

Prevents SSRF (Server-Side Request Forgery) where a malicious prompt or
skill could trick the agent into fetching internal resources like cloud
metadata endpoints (169.254.169.254), localhost services, or private
network hos

### 核心函数

- `normalize_url_for_request()`: Return an ASCII-safe HTTP URL for Hermes-owned URL tools.

    Browsers and HTTP clients expect URIs
- `is_always_blocked_url()`: Return True when the URL targets an always-blocked endpoint.

    This is the security floor — cloud
- `is_safe_url()`: Return True if the URL target is not a private/internal address.

    Resolves the hostname to an IP

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## video_generation_tool.py

**路径**: `tools\video_generation_tool.py`
**行数**: 565

### 功能描述

Video Generation Tool
=====================

Single ``video_generate`` tool that dispatches to a plugin-registered
video generation provider. Mirrors the ``image_generate`` design:

- ``agent/video_gen_provider.py`` defines the :class:`VideoGenProvider` ABC.
- ``agent/video_gen_registry.py`` holds t

### 核心函数

- `check_video_generation_requirements()`: Return True when at least one registered provider reports available.

    Triggers plugin discovery 

### 依赖关系

**依赖组件**: agent-engine, cli
**跨组件调用**: 是

---

## vision_tools.py

**路径**: `tools\vision_tools.py`
**行数**: 1592

### 功能描述

Vision Tools Module

This module provides vision analysis tools that work with image URLs.
Uses the centralized auxiliary vision router, which can select OpenRouter,
Nous, Codex, native Anthropic, or a custom OpenAI-compatible endpoint.

Available tools:
- vision_analyze_tool: Analyze images from UR

### 核心函数

- `check_vision_requirements()`: Check if the configured runtime vision path can resolve a client.

    Mirrors the fallback chain th

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client, state-management
**跨组件调用**: 是

---

## voice_mode.py

**路径**: `tools\voice_mode.py`
**行数**: 1219

### 功能描述

Voice Mode -- Push-to-talk audio recording and playback for the CLI.

Provides audio capture via sounddevice, WAV encoding via stdlib wave,
STT dispatch via tools.transcription_tools, and TTS playback via
sounddevice or system audio players.

Dependencies (optional):
    pip install sounddevice nump

### 核心类

- `TermuxAudioRecorder`: Recorder backend that uses Termux:API microphone capture commands.
- `AudioRecorder`: Thread-safe audio recorder using sounddevice.InputStream.

    Usage::

        recorder = AudioReco

### 核心函数

- `detect_audio_environment()`: Detect if the current environment supports audio I/O.

    Returns dict with 'available' (bool), 'wa
- `play_beep()`: Play a short beep tone using numpy + sounddevice.

    Args:
        frequency: Tone frequency in Hz
- `create_audio_recorder()`: Return the best recorder backend for the current environment.
- `is_whisper_hallucination()`: Check if a transcript is a known Whisper hallucination on silence.
- `transcribe_recording()`: Transcribe a WAV recording using the existing Whisper pipeline.

    Delegates to ``tools.transcript
- `stop_playback()`: Interrupt the currently playing audio (if any).
- `play_audio_file()`: Play an audio file through the default output device.

    Strategy:
    1. WAV files via ``sounddev
- `check_voice_requirements()`: Check if all voice mode requirements are met.

    Returns:
        Dict with ``available``, ``audio
- `cleanup_temp_recordings()`: Remove old temporary voice recording files.

    Args:
        max_age_seconds: Delete files older t

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## web_tools.py

**路径**: `tools\web_tools.py`
**行数**: 1378

### 功能描述

Standalone Web Tools Module

This module provides generic web tools that work with multiple backend providers.
Backend is selected during ``hermes tools`` setup (web.backend in config.yaml).
When available, Hermes can route Firecrawl calls through a Nous-hosted tool-gateway
for Nous Subscribers only

### 核心函数

- `clean_base64_images()`: Remove base64 encoded images from text to reduce token count and clutter.
    
    This function fin
- `web_search_tool()`: Search the web for information using available search API backend.

    This function provides a gen
- `check_web_api_key()`: Check whether the configured web backend is available.
- `check_auxiliary_model()`: Check if an auxiliary text model is available for LLM content processing.

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client, plugin-system
**跨组件调用**: 是

---

## website_policy.py

**路径**: `tools\website_policy.py`
**行数**: 283

### 功能描述

Website access policy helpers for URL-capable tools.

This module loads a user-managed website blocklist from ~/.hermes/config.yaml
and optional shared list files. It is intentionally lightweight so web/browser
tools can enforce URL policy without pulling in the heavier CLI config stack.

Policy is 

### 核心类

- `WebsitePolicyError`: Raised when a website policy file is malformed.

### 核心函数

- `load_website_blocklist()`: Load and return the parsed website blocklist policy.

    Results are cached for ``_CACHE_TTL_SECOND
- `invalidate_cache()`: Force the next ``check_website_access`` call to re-read config.
- `check_website_access()`: Check whether a URL is allowed by the website blocklist policy.

    Returns ``None`` if access is a

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## write_approval.py

**路径**: `tools\write_approval.py`
**行数**: 494

### 功能描述

Write-approval gate + pending store for memory and skill writes.

Background
----------
The agent writes to two persistent stores that survive across sessions:

  * **memory** — MEMORY.md / USER.md, small (~200 char) declarative entries
  * **skills** — SKILL.md + supporting files, potentially huge 

### 核心类

- `GateDecision`: Result of evaluating the write gate for a single write attempt.

    Exactly one of the boolean flag

### 核心函数

- `write_approval_enabled()`: Return whether the approval gate is enabled for ``subsystem``.

    Reads ``<subsystem>.write_approv
- `stage_write()`: Persist a pending write and return a short record describing it.

    Args:
        subsystem: ``mem
- `list_pending()`: Return all pending records for ``subsystem``, oldest first.
- `get_pending()`: Return a single pending record by id, or None.
- `discard_pending()`: Delete a pending record. Returns True if it existed.
- `pending_count()`: Cheap count of pending records (for notification badges).
- `current_origin()`: Return the active write origin: ``foreground`` or ``background_review``.

    Reuses the skill-prove
- `is_background()`
- `evaluate_gate()`: Decide what to do with a pending write for ``subsystem``.

    Args:
        subsystem: ``memory`` o
- `skill_gist()`: Build a one-line human gist for a pending skill write.

    Heuristic, no model call — the gist surf
- `skill_pending_diff()`: Build a full unified diff (or full content) for a staged skill write.

    Used by /skills diff <id>

### 依赖关系

**依赖组件**: cli, state-management
**跨组件调用**: 是

---

## x_search_tool.py

**路径**: `tools\x_search_tool.py`
**行数**: 526

### 功能描述

X Search tool backed by xAI's built-in ``x_search`` Responses API tool.

Authentication
--------------
The tool registers when **either** xAI credential path is available:

* ``XAI_API_KEY`` is set in ``~/.hermes/.env`` or the process environment
  (paid xAI API key), OR
* The user is signed in via 

### 核心函数

- `check_x_search_requirements()`: Return True when xAI credentials are available AND valid.

    ``resolve_xai_http_credentials`` call
- `x_search_tool()`

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## xai_http.py

**路径**: `tools\xai_http.py`
**行数**: 129

### 功能描述

Shared helpers for direct xAI HTTP integrations.

### 核心函数

- `has_xai_credentials()`: Cheap probe — return True when xAI credentials are *likely* usable.

    Deliberately avoids :func:`
- `get_env_value()`: Read ``name`` from ``~/.hermes/.env`` first, then ``os.environ``.

    Wraps :func:`hermes_cli.confi
- `hermes_xai_user_agent()`: Return a stable Hermes-specific User-Agent for xAI HTTP calls.
- `resolve_xai_http_credentials()`: Resolve bearer credentials for direct xAI HTTP endpoints.

    Prefers Hermes-managed xAI OAuth cred

### 依赖关系

**依赖组件**: acp-adapter, cli, state-management
**跨组件调用**: 是

---

## yuanbao_tools.py

**路径**: `tools\yuanbao_tools.py`
**行数**: 738

### 功能描述

yuanbao_tools.py - 元宝平台工具集

提供以下工具函数，供 hermes-agent 的 "hermes-yuanbao" toolset 使用：
  - get_group_info        : 查询群基本信息（群名、群主、成员数）
  - query_group_members   : 查询群成员（按名搜索、列举 bot、列举全部）
  - search_sticker        : 按关键词搜索内置贴纸（返回候选列表，含 sticker_id/name/description）
  - send_sticker          : 向当前会话或指定 chat

### 依赖关系

**依赖组件**: cli, gateway, llm-client
**跨组件调用**: 是

---

