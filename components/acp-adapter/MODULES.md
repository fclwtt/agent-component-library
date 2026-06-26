# acp-adapter 模块详细说明

本组件包含 11 个模块。

---

## __init__.py

**路径**: `acp_adapter\__init__.py`
**行数**: 2

### 功能描述

ACP (Agent Communication Protocol) adapter for hermes-agent.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __main__.py

**路径**: `acp_adapter\__main__.py`
**行数**: 6

### 功能描述

Allow running the ACP adapter as ``python -m acp_adapter``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## auth.py

**路径**: `acp_adapter\auth.py`
**行数**: 80

### 功能描述

ACP auth helpers — detect and advertise Hermes authentication methods.

### 核心函数

- `detect_provider()`: Resolve the active Hermes runtime provider, or None if unavailable.

    Treats a ``Callable`` ``api
- `has_provider()`: Return True if Hermes can resolve any runtime provider credentials.
- `build_auth_methods()`: Return registry-compatible ACP auth methods for Hermes.

    The official ACP registry validates tha

### 依赖关系

**依赖组件**: cli, tool-system
**跨组件调用**: 是

---

## edit_approval.py

**路径**: `acp_adapter\edit_approval.py`
**行数**: 287

### 功能描述

Pre-execution ACP edit approval helpers.

This module is intentionally isolated from the generic tool registry.  ACP binds
an edit approval requester in a ContextVar for the duration of one ACP agent run;
CLI, gateway, and other sessions leave it unset and therefore bypass this guard.

### 核心类

- `EditProposal`: A proposed single-file edit that can be shown to an ACP client.

### 核心函数

- `set_edit_approval_requester()`: Bind an ACP edit approval requester for the current context.
- `reset_edit_approval_requester()`: Restore a previous edit approval requester binding.
- `clear_edit_approval_requester()`: Clear the current requester; primarily used by tests.
- `get_edit_approval_requester()`
- `build_edit_proposal()`: Return an edit proposal for supported file mutation calls.
- `should_auto_approve_edit()`: Return whether an ACP edit proposal may bypass the prompt for this session.

    This is intentional
- `maybe_require_edit_approval()`: Run ACP edit approval if bound.

    Returns a JSON tool-error string when the edit must be blocked,
- `build_acp_edit_tool_call()`: Build the ToolCallUpdate payload for ACP request_permission.
- `make_acp_edit_approval_requester()`: Return a sync requester that bridges edit proposals to ACP permissions.

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## entry.py

**路径**: `acp_adapter\entry.py`
**行数**: 272

### 功能描述

CLI entry point for the hermes-agent ACP adapter.

Loads environment variables from ``~/.hermes/.env``, configures logging
to write to stderr (so stdout is reserved for ACP JSON-RPC transport),
and starts the ACP agent server.

Usage::

    python -m acp_adapter.entry
    # or
    hermes acp
    # o

### 核心类

- `_BenignProbeMethodFilter`: Suppress acp 'Background task failed' tracebacks caused by unknown
    liveness-probe methods (e.g. 

### 核心函数

- `main()`: Entry point: load env, configure logging, run the ACP agent.

### 依赖关系

**依赖组件**: cli, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## events.py

**路径**: `acp_adapter\events.py`
**行数**: 280

### 功能描述

Callback factories for bridging AIAgent events to ACP notifications.

Each factory returns a callable with the signature that AIAgent expects
for its callbacks. Internally, the callbacks push ACP session updates
to the client via ``conn.session_update()`` using
``asyncio.run_coroutine_threadsafe()``

### 核心函数

- `make_tool_progress_cb()`: Create a ``tool_progress_callback`` for AIAgent.

    Signature expected by AIAgent::

        tool_
- `make_thinking_cb()`: Create a ``thinking_callback`` for AIAgent.
- `make_step_cb()`: Create a ``step_callback`` for AIAgent.

    Signature expected by AIAgent::

        step_callback(
- `make_message_cb()`: Create a callback that streams agent response text to the editor.

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## permissions.py

**路径**: `acp_adapter\permissions.py`
**行数**: 169

### 功能描述

ACP permission bridging for Hermes dangerous-command approvals.

### 核心函数

- `make_approval_callback()`: Return a Hermes-compatible approval callback that bridges to ACP.

    The callback accepts ``comman

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

## provenance.py

**路径**: `acp_adapter\provenance.py`
**行数**: 128

### 功能描述

Derive ACP session-provenance metadata from the existing compression chain.

This is an additive Hermes extension surfaced under ACP ``_meta.hermes`` so
existing ACP clients ignore it. It carries no new persisted state: everything
is derived on demand from the ``sessions`` table (``parent_session_id

### 核心函数

- `build_session_provenance()`: Build ``_meta.hermes.sessionProvenance`` for an ACP session.

    Args:
        db: A ``SessionDB`` 
- `session_provenance_meta()`: Return a ready ``_meta`` payload: ``{"hermes": {"sessionProvenance": ...}}``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## server.py

**路径**: `acp_adapter\server.py`
**行数**: 2060

### 功能描述

ACP agent server — exposes Hermes Agent via the Agent Client Protocol.

### 核心类

- `HermesACPAgent`: ACP Agent implementation wrapping Hermes AIAgent.

### 依赖关系

**依赖组件**: agent-engine, cli, entry-points, gateway, memory-system, tool-system
**跨组件调用**: 是

---

## session.py

**路径**: `acp_adapter\session.py`
**行数**: 628

### 功能描述

ACP session manager — maps ACP sessions to Hermes AIAgent instances.

Sessions are persisted to the shared SessionDB (``~/.hermes/state.db``) so they
survive process restarts and appear in ``session_search``.  When the editor
reconnects after idle/restart, the ``load_session`` / ``resume_session`` c

### 核心类

- `SessionState`: Tracks per-session state for an ACP-managed Hermes agent.
- `SessionManager`: Thread-safe manager for ACP sessions backed by Hermes AIAgent instances.

    Sessions are held in-m

### 依赖关系

**依赖组件**: cli, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## tools.py

**路径**: `acp_adapter\tools.py`
**行数**: 1292

### 功能描述

ACP tool-call helpers for mapping hermes tools to ACP ToolKind and building content.

### 核心函数

- `get_tool_kind()`: Return the ACP ToolKind for a hermes tool, defaulting to 'other'.
- `make_tool_call_id()`: Generate a unique tool call ID.
- `build_tool_title()`: Build a human-readable title for a tool call.
- `build_tool_start()`: Create a ToolCallStart event for the given hermes tool invocation.
- `build_tool_complete()`: Create a ToolCallUpdate (progress) event for a completed tool call.
- `extract_locations()`: Extract file-system locations from tool arguments.

### 依赖关系

**依赖组件**: agent-engine, cli, tool-system
**跨组件调用**: 是

---

