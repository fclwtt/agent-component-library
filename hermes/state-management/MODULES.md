# state-management 模块详细说明

本组件包含 11 个模块。

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

**依赖组件**: acp-adapter, agent-engine, cli, llm-client
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

**依赖组件**: acp-adapter, cli
**跨组件调用**: 是

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

**依赖组件**: agent-engine
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

## credential_pool.py

**路径**: `credential_pool.py`
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

**依赖组件**: acp-adapter, agent-engine, cli, llm-client
**跨组件调用**: 是

---

## hermes_constants.py

**路径**: `hermes_constants.py`
**行数**: 916

### 功能描述

Shared constants for Hermes Agent.

Import-safe module with no dependencies — can be imported from anywhere
without risk of circular imports.

### 核心函数

- `set_hermes_home_override()`: Set a context-local Hermes home override and return its reset token.

    This is for in-process, pe
- `reset_hermes_home_override()`: Restore the previous context-local Hermes home override.
- `get_hermes_home_override()`: Return the active context-local Hermes home override, if any.
- `get_hermes_home()`: Return the Hermes home directory (default: platform-native path).

    Reads HERMES_HOME env var, fa
- `get_default_hermes_root()`: Return the root Hermes directory for profile-level operations.

    In standard deployments this is 
- `get_optional_skills_dir()`: Return the optional-skills directory, honoring package-manager wrappers.

    Packaged installs may 
- `get_optional_mcps_dir()`: Return the optional-mcps directory, honoring package-manager wrappers.

    Mirrors :func:`get_optio
- `get_bundled_skills_dir()`: Return the bundled skills directory for source and packaged installs.

    Resolution order:
       
- `get_hermes_dir()`: Resolve a Hermes subdirectory with backward compatibility.

    New installs get the consolidated la
- `iter_hermes_node_dirs()`: Return Hermes-managed Node.js directories in preferred lookup order.

    Windows installs from ``sc
- `node_tool_runnable()`: Return True only when *path* is a Node/npm/npx binary that actually runs.

    Hermes-managed Node t
- `hermes_managed_node_tree_present()`: Return True when any Hermes-managed node/npm/npx shim exists on disk.
- `heal_hermes_managed_node()`: Redownload Hermes-managed Node when the tree exists but is broken.

    Runs at most once per proces
- `find_hermes_node_executable()`: Return a Hermes-managed Node/npm executable path, healing broken trees.
- `find_node_executable_on_path()`: Return a Node/npm executable from PATH with Windows shim ordering.

    ``shutil.which("npm")`` can 
- ... 还有 16 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## hermes_state.py

**路径**: `hermes_state.py`
**行数**: 5352

### 功能描述

SQLite State Store for Hermes Agent.

Provides persistent session storage with FTS5 full-text search, replacing
the per-session JSONL file approach. Stores session metadata, full message
history, and model configuration for CLI and gateway sessions.

Key design decisions:
- WAL mode for concurrent r

### 核心类

- `SessionDB`: SQLite-backed session storage with FTS5 search.

    Thread-safe for the common gateway pattern (mul

### 核心函数

- `get_last_init_error()`: Return the most recent state.db init failure, if any.

    Slash-command handlers (``/resume``, ``/t
- `format_session_db_unavailable()`: Format a user-facing 'session DB unavailable' message with cause.

    When ``SessionDB()`` init fai
- `apply_wal_with_fallback()`: Set ``journal_mode=WAL`` on ``conn``, falling back to DELETE on failure.

    Returns the journal mo
- `is_malformed_db_error()`: True if *exc* is a SQLite 'malformed schema / disk image' error.

    These are the corruption class
- `repair_state_db_schema()`: Repair a state.db whose ``sqlite_master`` schema is malformed or whose
    FTS indexes reject writes

### 依赖关系

**依赖组件**: memory-system
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

**依赖组件**: agent-engine, cli, security
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

