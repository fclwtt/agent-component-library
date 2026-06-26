# entry-points 模块详细说明

本组件包含 16 个模块。

---

## batch_runner.py

**路径**: `batch_runner.py`
**行数**: 1322

### 功能描述

Batch Agent Runner

This module provides parallel batch processing capabilities for running the agent
across multiple prompts from a dataset. It includes:
- Dataset loading and batching
- Parallel batch processing with multiprocessing
- Checkpointing for fault tolerance and resumption
- Trajectory s

### 核心类

- `BatchRunner`: Manages batch processing of agent prompts with checkpointing and statistics.

### 核心函数

- `main()`: Run batch processing of agent prompts from a dataset.

    Args:
        dataset_file (str): Path to

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## cli.py

**路径**: `cli.py`
**行数**: 15531

### 功能描述

Hermes Agent CLI - Interactive Terminal Interface

A beautiful command-line interface for the Hermes Agent, inspired by Claude Code.
Features ASCII art branding, interactive REPL, toolset selection, and rich formatting.

Usage:
    python cli.py                          # Start interactive mode with

### 核心类

- `_SkinAwareAnsi`: Lazy ANSI escape that resolves from the skin engine on first use.

    Acts as a string in f-strings
- `ChatConsole`: Rich Console adapter for prompt_toolkit's patch_stdout context.

    Captures Rich's rendered ANSI o
- `HermesCLI`: Interactive CLI for the Hermes Agent.
    
    Provides a REPL interface with rich formatting, comma

### 核心函数

- `CanonicalUsage()`
- `estimate_usage_cost()`
- `format_duration_compact()`
- `format_token_count_compact()`
- `is_table_divider()`
- `looks_like_table_row()`
- `realign_markdown_tables()`
- `load_cli_config()`: Load CLI configuration from config files.
    
    Config lookup order:
    1. ~/.hermes/config.yaml
- `AIAgent()`
- `get_tool_definitions()`
- `get_toolset_for_tool()`
- `get_all_toolsets()`
- `get_toolset_info()`
- `validate_toolset()`
- `get_job()`
- ... 还有 10 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, gateway, llm-client, security, state-management, tool-system
**跨组件调用**: 是

---

## hermes_bootstrap.py

**路径**: `hermes_bootstrap.py`
**行数**: 196

### 功能描述

Windows UTF-8 bootstrap for Hermes entry points.

Python on Windows has two long-standing text-encoding footguns:

1. ``sys.stdout`` / ``sys.stderr`` are bound to the console code page
   (``cp1252`` on US-locale installs), so ``print("café")`` crashes with
   ``UnicodeEncodeError: 'charmap' codec c

### 核心函数

- `apply_windows_utf8_bootstrap()`: Apply the Windows UTF-8 bootstrap if we're on Windows.

    Returns True if bootstrap was applied (i
- `harden_import_path()`: Stop a package in the current directory from shadowing Hermes modules.

    Hermes ships top-level m
- `activate_durable_lazy_target()`: Put the durable lazy-install dir on ``sys.path`` if one is configured.

    On immutable Docker imag

### 依赖关系

**依赖组件**: acp-adapter
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

## hermes_logging.py

**路径**: `hermes_logging.py`
**行数**: 577

### 功能描述

Centralized logging setup for Hermes Agent.

Provides a single ``setup_logging()`` entry point that both the CLI and
gateway call early in their startup path.  All log files live under
``~/.hermes/logs/`` (profile-aware via ``get_hermes_home()``).

Log files produced:
    agent.log   — INFO+, all ag

### 核心类

- `_ComponentFilter`: Only pass records whose logger name starts with one of *prefixes*.

    Used to route gateway-specif
- `_ManagedRotatingFileHandler`: RotatingFileHandler that ensures group-writable perms in managed mode
    AND survives external rota

### 核心函数

- `set_session_context()`: Set the session ID for the current thread.

    All subsequent log records on this thread will inclu
- `clear_session_context()`: Clear the session ID for the current thread.
- `setup_logging()`: Configure the Hermes logging subsystem.

    Safe to call multiple times — the second call is a no-o
- `setup_verbose_logging()`: Enable DEBUG-level console logging for ``--verbose`` / ``-v`` mode.

    Called by ``AIAgent.__init_

### 依赖关系

**依赖组件**: agent-engine, cli, state-management
**跨组件调用**: 是

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

**依赖组件**: memory-system, state-management
**跨组件调用**: 是

---

## hermes_time.py

**路径**: `hermes_time.py`
**行数**: 125

### 功能描述

Timezone-aware clock for Hermes.

Provides a single ``now()`` helper that returns a timezone-aware datetime
based on the user's configured IANA timezone (e.g. ``Asia/Kolkata``).

Resolution order:
  1. ``HERMES_TIMEZONE`` environment variable
  2. ``timezone`` key in ``~/.hermes/config.yaml``
  3. F

### 核心函数

- `get_timezone()`: Return the user's configured ZoneInfo, or None (meaning server-local).

    Resolved once and cached
- `reset_cache()`: Clear the cached timezone so the next call re-resolves it.

    Call this after the configured timez
- `now()`: Return the current time as a timezone-aware datetime.

    If a valid timezone is configured, return

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## mcp_serve.py

**路径**: `mcp_serve.py`
**行数**: 905

### 功能描述

Hermes MCP Server — expose messaging conversations as MCP tools.

Starts a stdio MCP server that lets any MCP client (Claude Code, Cursor, Codex,
etc.) list conversations, read message history, send messages, poll for live
events, and manage approval requests across all connected platforms.

Matches

### 核心类

- `QueueEvent`: An event in the bridge's in-memory queue.
- `EventBridge`: Background poller that watches SessionDB for new messages and
    maintains an in-memory event queue

### 核心函数

- `create_mcp_server()`: Create and return the Hermes MCP server with all tools registered.
- `run_mcp_server()`: Start the Hermes MCP server on stdio.

### 依赖关系

**依赖组件**: state-management, tool-system
**跨组件调用**: 是

---

## mini_swe_runner.py

**路径**: `mini_swe_runner.py`
**行数**: 733

### 功能描述

SWE Runner with Hermes Trajectory Format

A runner that uses Hermes-Agent's built-in execution environments
(local, docker, modal) and outputs trajectories in the Hermes-Agent format
compatible with batch_runner.py and trajectory_compressor.py.

Features:
- Uses Hermes-Agent's Docker, Modal, or Loca

### 核心类

- `MiniSWERunner`: Agent runner that uses Hermes-Agent's built-in execution environments
    and outputs trajectories i

### 核心函数

- `create_environment()`: Create an execution environment using Hermes-Agent's built-in backends.
    
    Args:
        env_t
- `main()`: Run SWE tasks with Hermes trajectory format output.
    
    Args:
        task: Single task to run 

### 依赖关系

**依赖组件**: agent-engine, llm-client, tool-system
**跨组件调用**: 是

---

## model_tools.py

**路径**: `model_tools.py`
**行数**: 1256

### 功能描述

Model Tools Module

Thin orchestration layer over the tool registry. Each tool file in tools/
self-registers its schema, handler, and metadata via tools.registry.register().
This module triggers discovery (by importing all tool modules), then provides
the public API that run_agent.py, cli.py, batch_

### 核心函数

- `get_tool_definitions()`: Get tool definitions for model API calls with toolset-based filtering.

    All tools must be part o
- `coerce_tool_args()`: Coerce tool call arguments to match their JSON Schema types.

    LLMs frequently return numbers as 
- `handle_function_call()`: Main function call dispatcher that routes calls to the tool registry.

    Args:
        function_na
- `get_all_tool_names()`: Return all registered tool names.
- `get_toolset_for_tool()`: Return the toolset a tool belongs to.
- `get_available_toolsets()`: Return toolset availability info for UI display.
- `check_toolset_requirements()`: Return {toolset: available_bool} for every registered toolset.
- `check_tool_availability()`: Return (available_toolsets, unavailable_info).

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, tool-system
**跨组件调用**: 是

---

## run_agent.py

**路径**: `run_agent.py`
**行数**: 5591

### 功能描述

AI Agent Runner with Tool Calling

This module provides a clean, standalone agent that can execute AI models
with tool calling capabilities. It handles the conversation loop, tool execution,
and response management.

Features:
- Automatic tool calling loop until completion
- Configurable model param

### 核心类

- `_StreamErrorEvent`: Synthesized provider error surfaced from a Responses ``error`` SSE frame.

    Some Codex-style Resp
- `AIAgent`: AI Agent with tool calling capabilities.

    This class manages the conversation flow, tool executi

### 核心函数

- `main()`: Main function for running the agent directly.

    Args:
        query (str): Natural language query

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, gateway, llm-client, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## setup.py

**路径**: `setup.py`
**行数**: 88

### 功能描述

（需从代码逻辑分析）

### 核心类

- `ReadOnlySourceBuild`
- `ReadOnlySourceEggInfo`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## toolset_distributions.py

**路径**: `toolset_distributions.py`
**行数**: 359

### 功能描述

Toolset Distributions Module

This module defines distributions of toolsets for data generation runs.
Each distribution specifies which toolsets should be used and their probability
of being selected for any given prompt during the batch processing.

A distribution is a dictionary mapping toolset na

### 核心函数

- `get_distribution()`: Get a toolset distribution by name.
    
    Args:
        name (str): Name of the distribution
    
- `list_distributions()`: List all available distributions.
    
    Returns:
        Dict: All distribution definitions
- `sample_toolsets_from_distribution()`: Sample toolsets based on a distribution's probabilities.
    
    Each toolset in the distribution h
- `validate_distribution()`: Check if a distribution name is valid.
    
    Args:
        distribution_name (str): Distribution 
- `print_distribution_info()`: Print detailed information about a distribution.
    
    Args:
        distribution_name (str): Dis

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## toolsets.py

**路径**: `toolsets.py`
**行数**: 940

### 功能描述

Toolsets Module

This module provides a flexible system for defining and managing tool aliases/toolsets.
Toolsets allow you to group tools together for specific scenarios and can be composed
from individual tools or other toolsets.

Features:
- Define custom toolsets with specific tools
- Compose to

### 核心函数

- `get_toolset()`: Get a toolset definition by name.
    
    Args:
        name (str): Name of the toolset
        
  
- `bundle_non_core_tools()`: Return a ``hermes-*`` bundle's platform-specific tools, excluding core.

    Platform bundles are de
- `resolve_toolset()`: Recursively resolve a toolset to get all tool names.
    
    This function handles toolset composit
- `resolve_multiple_toolsets()`: Resolve multiple toolsets and combine their tools.
    
    Args:
        toolset_names (List[str]):
- `get_all_toolsets()`: Get all available toolsets with their definitions.

    Includes both statically-defined toolsets an
- `get_toolset_names()`: Get names of all available toolsets (excluding aliases).

    Includes plugin-registered toolset nam
- `validate_toolset()`: Check if a toolset name is valid.
    
    Args:
        name (str): Toolset name to validate
      
- `create_custom_toolset()`: Create a custom toolset at runtime.
    
    Args:
        name (str): Name for the new toolset
    
- `get_toolset_info()`: Get detailed information about a toolset including resolved tools.
    
    Args:
        name (str)

### 依赖关系

**依赖组件**: cli, gateway
**跨组件调用**: 是

---

## trajectory_compressor.py

**路径**: `trajectory_compressor.py`
**行数**: 1575

### 功能描述

Trajectory Compressor

Post-processes completed agent trajectories to compress them within a target
token budget while preserving training signal quality.

Compression Strategy:
1. Protect first turns (system, human, first gpt, first tool)
2. Protect last N turns (final actions and conclusions)
3. C

### 核心类

- `CompressionConfig`: Configuration for trajectory compression.
- `TrajectoryMetrics`: Metrics for a single trajectory compression.
- `AggregateMetrics`: Aggregate metrics across all trajectories.
- `TrajectoryCompressor`: Compresses agent trajectories to fit within a target token budget.
    
    Compression strategy:
  

### 核心函数

- `main()`: Compress agent trajectories to fit within a target token budget.
    
    Supports both single JSONL

### 依赖关系

**依赖组件**: agent-engine, cli, llm-client, state-management
**跨组件调用**: 是

---

## utils.py

**路径**: `utils.py`
**行数**: 482

### 功能描述

Shared utility functions for hermes-agent.

### 核心类

- `IndentDumper`: PyYAML dumper that indents list items under mapping keys (2-space).

    Default PyYAML emits "inden

### 核心函数

- `is_truthy_value()`: Coerce bool-ish values using the project's shared truthy string set.
- `env_var_enabled()`: Return True when an environment variable is set to a truthy value.
- `atomic_replace()`: Atomically move *tmp_path* onto *target*, preserving symlinks.

    ``os.replace(tmp, target)`` atom
- `atomic_json_write()`: Write JSON data to a file atomically.

    Uses temp file + fsync + os.replace to ensure the target 
- `atomic_yaml_write()`: Write YAML data to a file atomically.

    Uses temp file + fsync + os.replace to ensure the target 
- `atomic_roundtrip_yaml_update()`: Update one dotted YAML key while preserving comments and readable text.

    This is intentionally n
- `safe_json_loads()`: Parse JSON, returning *default* on any parse error.

    Replaces the ``try: json.loads(x) except (J
- `env_int()`: Read an environment variable as an integer, with fallback.
- `env_float()`: Read an environment variable as a float, with fallback.
- `env_bool()`: Read an environment variable as a boolean.
- `normalize_proxy_url()`: Normalize proxy URLs for httpx/aiohttp compatibility.

    WSL/Clash-style environments often export
- `normalize_proxy_env_vars()`: Rewrite supported proxy env vars to canonical URL forms in-place.
- `base_url_hostname()`: Return the lowercased hostname for a base URL, or ``""`` if absent.

    Use exact-hostname comparis
- `model_forces_max_completion_tokens()`: Return True for model families that require ``max_completion_tokens``.

    OpenAI's newer families 
- `base_url_host_matches()`: Return True when the base URL's hostname is ``domain`` or a subdomain.

    Safer counterpart to ``d

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

