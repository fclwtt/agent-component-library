# tui 模块详细说明

本组件包含 10 个模块。

---

## __init__.py

**路径**: `tui_gateway\__init__.py`
**行数**: 1

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## entry.py

**路径**: `tui_gateway\entry.py`
**行数**: 348

### 功能描述

Mirror every dispatcher emit to the dashboard sidebar via WS.

    Activated by `HERMES_TUI_SIDECAR_URL`, set by the dashboard's
    ``/api/pty`` endpoint when a chat tab passes a ``channel`` query pa

### 核心函数

- `wait_for_mcp_discovery()`: Block until background MCP discovery finishes, up to the resolved bound.

    MCP discovery runs in 
- `mcp_discovery_in_flight()`: Return True if the background MCP discovery thread is still running.

    Used by the agent-build pa
- `join_mcp_discovery()`: Block until background MCP discovery finishes, up to ``timeout`` seconds.

    Returns True if disco
- `main()`

### 依赖关系

**依赖组件**: acp-adapter, cli, entry-points, gateway, tool-system
**跨组件调用**: 是

---

## event_publisher.py

**路径**: `tui_gateway\event_publisher.py`
**行数**: 127

### 功能描述

Best-effort WebSocket publisher transport for the PTY-side gateway.

The dashboard's `/api/pty` spawns `hermes --tui` as a child process, which
spawns its own ``tui_gateway.entry``.  Tool/reasoning/status events fire on
*that* gateway's transport — three processes removed from the dashboard
server i

### 核心类

- `WsPublisherTransport`

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## git_probe.py

**路径**: `tui_gateway\git_probe.py`
**行数**: 188

### 功能描述

Git working-tree probing for the gateway: run git, resolve repo roots, fold
linked worktrees under their common root.

Probing runs where the gateway runs, so it resolves repos for both local and
remote backends (unlike the desktop's electron probe, which only sees the local
fs). Resolved roots are 

### 核心类

- `_RootCache`: Thread-safe, single-flight cache of git-root probes. Positive results are
    cached for the process

### 核心函数

- `run_git()`: ``git -C <cwd> <args>`` → stripped stdout, or ``""`` on any failure.
- `branch()`
- `invalidate()`: Drop cached roots after a known mutation (e.g. a worktree was added).
- `repo_root()`: Top-level git repo root for ``cwd`` (``""`` when not a repo).
- `common_repo_root()`: The MAIN (common) repo root for ``cwd``, folding linked worktrees.

    ``--show-toplevel`` returns 
- `resolve()`: Inject-able resolver for ``project_tree.build_tree``.

    Returns ``{"repo_root": <common root>, "w
- `warm_roots()`: Pre-resolve many cwds' roots in parallel (bounded) so a cold first paint
    doesn't serialize one g

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## project_tree.py

**路径**: `tui_gateway\project_tree.py`
**行数**: 559

### 功能描述

Authoritative project -> repo -> lane -> session tree builder.

This is the single source of truth for how the desktop sidebar groups sessions
into projects, repos, and lanes. It is pure (all git resolution is injected via
``resolve``) so it can be unit-tested with fixtures and reused by the gateway

### 核心类

- `_FolderIndex`: Maps a normalized folder path → (owning project, depth), so a session is
    matched to its project 

### 核心函数

- `base_name()`
- `kanban_worktree_dir()`: The ``<repo>/.worktrees`` dir for a ``.../.worktrees/<task>`` path, else None.
- `build_tree()`: Build the authoritative project tree.

    ``projects`` are ``projects_db.Project.to_dict()`` shapes

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## render.py

**路径**: `tui_gateway\render.py`
**行数**: 50

### 功能描述

Rendering bridge — routes TUI content through Python-side renderers.

When agent.rich_output exists, its functions are used. When it doesn't,
everything returns None and the TUI falls back to its own markdown.tsx.

### 核心函数

- `render_message()`
- `render_diff()`
- `make_stream_renderer()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## server.py

**路径**: `tui_gateway\server.py`
**行数**: 13470

### 功能描述

Detached WS sink: keep sessions resumable without writing stale frames.

### 核心类

- `_DropTransport`: Detached WS sink: keep sessions resumable without writing stale frames.
- `_SlashWorker`: Persistent HermesCLI subprocess for slash commands.
- `_NoProject`: Raised inside a projects handler when ``params['id']`` resolves to None.

### 核心函数

- `write_json()`: Emit one JSON frame. Routes via the most-specific transport available.

    Precedence:

    1. Even
- `method()`
- `handle_request()`
- `dispatch()`: Route inbound RPCs — long handlers to the pool, everything else inline.

    Returns a response dict
- `resolve_skin()`

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## slash_worker.py

**路径**: `tui_gateway\slash_worker.py`
**行数**: 138

### 功能描述

Persistent slash-command worker — one HermesCLI per TUI session.

Protocol: reads JSON lines from stdin {id, command}, writes {id, ok, output|error} to stdout.

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## transport.py

**路径**: `tui_gateway\transport.py`
**行数**: 220

### 功能描述

Transport abstraction for the tui_gateway JSON-RPC server.

Historically the gateway wrote every JSON frame directly to real stdout.  This
module decouples the I/O sink from the handler logic so the same dispatcher
can be driven over stdio (``tui_gateway.entry``) or WebSocket
(``tui_gateway.ws``) wi

### 核心类

- `Transport`: Minimal interface every transport implements.
- `StdioTransport`: Writes JSON frames to a stream (usually ``sys.stdout``).

    The stream is resolved via a callable 
- `TeeTransport`: Mirrors writes to one primary plus N best-effort secondaries.

    The primary's return value (and e

### 核心函数

- `current_transport()`: Return the transport bound for the current request, if any.
- `bind_transport()`: Bind *transport* for the current context. Returns a token for :func:`reset_transport`.
- `reset_transport()`: Restore the transport binding captured by :func:`bind_transport`.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## ws.py

**路径**: `tui_gateway\ws.py`
**行数**: 341

### 功能描述

WebSocket transport for the tui_gateway JSON-RPC server.

Reuses :func:`tui_gateway.server.dispatch` verbatim so every RPC method, every
slash command, every approval/clarify/sudo flow, and every agent event flows
through the same handlers whether the client is Ink over stdio or an iOS /
web client 

### 核心类

- `WSTransport`: Per-connection WS transport.

    ``write`` is safe to call from any thread *other than* the event l

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

