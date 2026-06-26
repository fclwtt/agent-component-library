# cli 模块详细说明

本组件包含 192 个模块。

---

## __init__.py

**路径**: `hermes_cli\__init__.py`
**行数**: 93

### 功能描述

Hermes CLI - Unified command-line interface for Hermes Agent.

Provides subcommands for:
- hermes chat          - Interactive chat (same as ./hermes)
- hermes gateway       - Run gateway in foreground
- hermes gateway start - Start gateway service
- hermes gateway stop  - Stop gateway service
- herm

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _parser.py

**路径**: `hermes_cli\_parser.py`
**行数**: 412

### 功能描述

Top-level argparse construction for the hermes CLI.

Lives in its own module so other modules (e.g. ``relaunch.py``) can
introspect the parser to discover which flags exist without running the
``main`` fn.

Only the top-level parser and the ``chat`` subparser live here. Every other
subparser (model,

### 核心函数

- `build_top_level_parser()`: Build the top-level parser, the subparsers action, and the ``chat`` subparser.

    Returns ``(parse

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _subprocess_compat.py

**路径**: `hermes_cli\_subprocess_compat.py`
**行数**: 235

### 功能描述

Windows subprocess compatibility helpers.

Hermes is developed on Linux / macOS and tested natively on Windows too.
Several common subprocess patterns break silently-or-loudly on Windows:

* ``["npm", "install", ...]`` — on Windows ``npm`` is ``npm.cmd``, a batch
  shim.  ``subprocess.Popen(["npm", 

### 核心函数

- `resolve_node_command()`: Resolve a Node-ecosystem command name to an absolute-path argv.

    On Windows, commands like ``npm
- `windows_detach_flags()`: Return Win32 creationflags that detach a child from the parent
    console and process group.  0 on 
- `windows_detach_flags_without_breakaway()`: Same as :func:`windows_detach_flags` minus ``CREATE_BREAKAWAY_FROM_JOB``.

    The docstring on :fun
- `windows_hide_flags()`: Return Win32 creationflags that merely hide the child's console
    window without detaching the chi
- `windows_detach_popen_kwargs()`: Return a dict of Popen kwargs that detach a child on Windows and
    fall back to the POSIX equivale

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## active_sessions.py

**路径**: `hermes_cli\active_sessions.py`
**行数**: 358

### 功能描述

Cross-process active chat session leases.

The session database records persisted conversations.  This module records
currently open chat surfaces, including idle CLI/TUI sessions that have not
written a transcript row yet.

### 核心类

- `_FileLock`
- `ActiveSessionLease`

### 核心函数

- `coerce_max_concurrent_sessions()`: Return a positive integer cap, or None when disabled/invalid.
- `resolve_max_concurrent_sessions()`: Resolve top-level max_concurrent_sessions with gateway.* fallback.
- `active_session_limit_message()`
- `try_acquire_active_session()`: Acquire an active-session slot.

    Returns ``(lease, None)`` on success.  When the cap is disabled
- `release_active_session()`
- `transfer_active_session()`: Move an existing lease to a new session id without dropping the slot.
- `active_session_registry_snapshot()`: Return the pruned active-session registry for diagnostics/tests.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## auth.py

**路径**: `hermes_cli\auth.py`
**行数**: 8277

### 功能描述

Multi-provider authentication system for Hermes Agent.

Supports OAuth device code flows (Nous Portal, future: OpenAI Codex) and
traditional API key providers (OpenRouter, custom endpoints). Auth state
is persisted in ~/.hermes/auth.json with cross-process file locking.

Architecture:
- ProviderConf

### 核心类

- `ProviderConfig`: Describes a known inference provider.
- `AuthError`: Structured auth error with UX mapping hints.

### 核心函数

- `get_anthropic_key()`: Return the first usable Anthropic credential, or ``""``.

    Checks both the ``.env`` file (via ``g
- `has_usable_secret()`: Return True when a configured secret looks usable, not empty/placeholder.
- `detect_zai_endpoint()`: Probe z.ai endpoints to find one that accepts this API key.

    Returns {"id": ..., "base_url": ...
- `is_rate_limited_auth_error()`: True when an :class:`AuthError` represents upstream rate-limiting / quota
    exhaustion rather than
- `format_auth_error()`: Map auth failures to concise user-facing guidance.
- `mark_provider_active_if_unset()`: Set ``active_provider`` to *provider_id* only when none is set yet.

    Used by ``hermes auth add``
- `is_known_auth_provider()`
- `get_auth_provider_display_name()`
- `read_credential_pool()`: Return the persisted credential pool, or one provider slice.

    In profile mode, the profile's cre
- `write_credential_pool()`: Persist one provider's credential pool under auth.json.

    This is the final disk-boundary guard f
- `suppress_credential_source()`: Mark a credential source as suppressed so it won't be re-seeded.
- `is_source_suppressed()`: Check if a credential source has been suppressed by the user.
- `unsuppress_credential_source()`: Clear a suppression marker so the source will be re-seeded on the next load.

    Returns True if a 
- `get_provider_auth_state()`: Return persisted auth state for a provider, or None.

    In profile mode, ``_load_provider_state`` 
- `get_active_provider()`: Return the currently active provider ID from auth store.
- ... 还有 35 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, state-management
**跨组件调用**: 是

---

## auth_commands.py

**路径**: `hermes_cli\auth_commands.py`
**行数**: 781

### 功能描述

Credential-pool auth subcommands.

### 核心函数

- `auth_add_command()`
- `auth_list_command()`
- `auth_remove_command()`
- `auth_reset_command()`
- `auth_status_command()`
- `auth_logout_command()`
- `auth_spotify_command()`
- `auth_command()`

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, state-management
**跨组件调用**: 是

---

## azure_detect.py

**路径**: `hermes_cli\azure_detect.py`
**行数**: 407

### 功能描述

Azure Foundry endpoint auto-detection.

Inspect a Microsoft Foundry / Azure OpenAI endpoint to determine:
  - API transport (OpenAI-style ``chat_completions`` vs
    Anthropic-style ``anthropic_messages``)
  - Available models (best effort — Azure does not expose a deployment
    listing via the inf

### 核心类

- `DetectionResult`: Everything auto-detection could gather from a base URL + API key.

### 核心函数

- `detect()`: Inspect an Azure endpoint and describe its transport + models.

    Call this from the wizard before
- `lookup_context_length()`: Thin wrapper around :func:`agent.model_metadata.get_model_context_length`
    that returns ``None`` 

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## backup.py

**路径**: `hermes_cli\backup.py`
**行数**: 1377

### 功能描述

Backup and import commands for hermes CLI.

`hermes backup` creates a zip archive of the entire ~/.hermes/ directory
(excluding the hermes-agent repo and transient files).

`hermes import` restores from a backup zip, overlaying onto the current
HERMES_HOME root.

### 核心函数

- `run_backup()`: Create a zip backup of the Hermes home directory.
- `run_import()`: Restore a Hermes backup from a zip file.
- `create_quick_snapshot()`: Create a quick state snapshot of critical files.

    Copies STATE_FILES to a timestamped directory 
- `list_quick_snapshots()`: List existing quick state snapshots, most recent first.
- `restore_quick_snapshot()`: Restore state from a quick snapshot.

    Overwrites current state files with the snapshot's copies.
- `restore_cron_jobs_if_emptied()`: Safety net for silent cron-job loss across ``hermes update``.

    Config-version migrations have be
- `prune_quick_snapshots()`: Manually prune quick snapshots. Returns count deleted.
- `run_quick_backup()`: CLI entry point for hermes backup --quick.
- `create_pre_update_backup()`: Create a full zip backup of HERMES_HOME under ``backups/``.

    Mirrors :func:`run_backup` (same ex
- `create_pre_migration_backup()`: Create a full zip backup of HERMES_HOME under ``backups/`` before a
    ``hermes claw migrate`` appl

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## banner.py

**路径**: `hermes_cli\banner.py`
**行数**: 887

### 功能描述

Welcome banner, ASCII art, skills summary, and update check for the CLI.

Pure display functions with no HermesCLI state dependency.

### 核心函数

- `cprint()`: Print ANSI-colored text through prompt_toolkit's renderer.
- `get_available_skills()`: Return skills grouped by category, filtered by platform and disabled state.

    Delegates to ``_fin
- `check_via_pypi()`: Compare installed version against PyPI latest.

    Returns 0 if up-to-date, 1 if behind, None on fa
- `check_for_updates()`: Check whether a Hermes update is available.

    Two paths: if ``HERMES_REVISION`` is set (nix build
- `get_git_banner_state()`: Return upstream/local git hashes for the startup banner.

    For source installs and dev images thi
- `get_latest_release_tag()`: Return ``(tag, release_url)`` for the latest git tag, or None.

    Local-only — runs ``git describe
- `format_banner_version_label()`: Return the version label shown in the startup banner title.
- `prefetch_update_check()`: Kick off update check in a background daemon thread.
- `get_update_result()`: Get result of prefetched check. Returns None if not ready.
- `build_welcome_banner()`: Build and print a welcome banner with caduceus on left and info on right.

    Args:
        console

### 依赖关系

**依赖组件**: entry-points, state-management, tool-system
**跨组件调用**: 是

---

## blueprint_cmd.py

**路径**: `hermes_cli\blueprint_cmd.py`
**行数**: 319

### 功能描述

Shared ``/blueprint`` command logic for CLI, TUI, and gateway.

The conversational counterpart to the dashboard's Automation Blueprints form. Where a
surface has a screen, the user fills a form (dashboard / GUI app) and the API
calls ``fill_blueprint`` -> ``create_job`` directly. Where a surface is 

### 核心类

- `BlueprintCommandResult`: Outcome of a ``/blueprint`` invocation.

    ``text`` is always shown to the user. When ``agent_seed

### 核心函数

- `match_blueprint()`: Resolve a free-typed blueprint name to a blueprint.

    Returns ``(blueprint, candidates)``:
      
- `build_blueprint_seed()`: Build the natural-language fill-request the agent will act on.

    The agent reads this as a normal
- `handle_blueprint_command()`: Dispatch a ``/blueprint`` invocation.

    Returns a :class:`BlueprintCommandResult`. When ``agent_s

### 依赖关系

**依赖组件**: cron, gateway
**跨组件调用**: 是

---

## browser_connect.py

**路径**: `hermes_cli\browser_connect.py`
**行数**: 218

### 功能描述

Shared helpers for attaching Hermes to a local Chromium-family CDP port.

### 核心函数

- `get_chrome_debug_candidates()`
- `chrome_debug_data_dir()`
- `is_browser_debug_ready()`: Return True when ``url`` exposes a reachable Chrome DevTools endpoint.
- `manual_chrome_debug_command()`
- `try_launch_chrome_debug()`

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## build_info.py

**路径**: `hermes_cli\build_info.py`
**行数**: 52

### 功能描述

Baked-in build metadata for Hermes Agent.

Source installs report their git revision live via ``git rev-parse`` (see
``hermes_cli/dump.py`` and ``hermes_cli/banner.py``).  That doesn't work inside
the published Docker image because ``.dockerignore`` excludes ``.git``, so
those callsites fall back to

### 核心函数

- `get_build_sha()`: Return the baked-in build SHA, truncated to ``short`` chars, or None.

    Reads ``<project_root>/.h

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## bundles.py

**路径**: `hermes_cli\bundles.py`
**行数**: 230

### 功能描述

Implementation of the ``hermes bundles`` CLI subcommand.

Mirrors the structure of ``hermes_cli/skills_hub.py`` but for skill
bundles. Bundles are tiny YAML files that name a set of skills to load
together via a single ``/<bundle>`` slash command.

Subcommands:
- list: show all bundles
- show: dump 

### 核心函数

- `register_cli()`: Build the ``hermes bundles`` argparse tree.

    Called from ``hermes_cli/main.py`` where it owns th
- `bundles_command()`: Dispatch ``hermes bundles <subcommand>`` to the right handler.

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## callbacks.py

**路径**: `hermes_cli\callbacks.py`
**行数**: 243

### 功能描述

Interactive prompt callbacks for terminal_tool integration.

These bridge terminal_tool's interactive prompts (clarify, sudo, approval)
into prompt_toolkit's event loop. Each function takes the HermesCLI instance
as its first argument and uses its state (queues, app reference) to coordinate
with the

### 核心函数

- `clarify_callback()`: Prompt for clarifying question through the TUI.

    Sets up the interactive selection UI, then bloc
- `prompt_for_secret()`: Prompt for a secret value through the TUI (e.g. API keys for skills).

    Returns a dict with keys:
- `approval_callback()`: Prompt for dangerous command approval through the TUI.

    Shows a selection UI with choices: once 

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## checkpoints.py

**路径**: `hermes_cli\checkpoints.py`
**行数**: 245

### 功能描述

`hermes checkpoints` CLI subcommand.

Gives users direct visibility and control over the filesystem checkpoint
store at ``~/.hermes/checkpoints/``.  Actions:

    hermes checkpoints               # same as `status`
    hermes checkpoints status        # total size, project count, breakdown
    herme

### 核心函数

- `cmd_status()`
- `cmd_list()`
- `cmd_prune()`
- `cmd_clear()`
- `cmd_clear_legacy()`
- `register_cli()`: Wire subcommands onto the ``hermes checkpoints`` parser.

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## claw.py

**路径**: `hermes_cli\claw.py`
**行数**: 810

### 功能描述

hermes claw — OpenClaw migration commands.

Usage:
    hermes claw migrate              # Preview then migrate (always shows preview first)
    hermes claw migrate --dry-run    # Preview only, no changes
    hermes claw migrate --yes        # Skip confirmation prompt
    hermes claw migrate --preset

### 核心函数

- `claw_command()`: Route hermes claw subcommands.

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## cli_agent_setup_mixin.py

**路径**: `hermes_cli\cli_agent_setup_mixin.py`
**行数**: 690

### 功能描述

Agent-construction and session-resume display methods for ``HermesCLI``.

Extracted from ``cli.py`` as part of the god-file decomposition campaign
(``~/.hermes/plans/god-file-decomposition.md``, Phase 4 step 2). This mixin holds
the agent lifecycle/setup cluster: runtime-credential resolution, per-t

### 核心类

- `CLIAgentSetupMixin`: Agent construction + session-resume display methods for ``HermesCLI``.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, state-management
**跨组件调用**: 是

---

## cli_commands_mixin.py

**路径**: `hermes_cli\cli_commands_mixin.py`
**行数**: 2661

### 功能描述

Slash-command handlers for the interactive CLI (god-file decomposition Phase 4).

This module hosts the ``_handle_*_command`` slash-command handlers lifted out of
``cli.py``'s ``HermesCLI`` class. ``HermesCLI`` inherits ``CLICommandsMixin`` so
every ``self.<handler>`` call resolves unchanged via the

### 核心类

- `CLICommandsMixin`: Mixin holding the interactive-CLI slash-command handlers.

    All methods use only ``self`` state p

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, memory-system, state-management, tool-system
**跨组件调用**: 是

---

## cli_output.py

**路径**: `hermes_cli\cli_output.py`
**行数**: 78

### 功能描述

Shared CLI output helpers for Hermes CLI modules.

Extracts the identical ``print_info/success/warning/error`` and ``prompt()``
functions previously duplicated across setup.py, tools_config.py,
mcp_config.py, and memory_setup.py.

### 核心函数

- `print_info()`: Print a dim informational message.
- `print_success()`: Print a green success message with ✓ prefix.
- `print_warning()`: Print a yellow warning message with ⚠ prefix.
- `print_error()`: Print a red error message with ✗ prefix.
- `print_header()`: Print a bold yellow header.
- `prompt()`: Prompt the user for input with optional default and password masking.

    Replaces the four indepen
- `prompt_yes_no()`: Prompt for a yes/no answer. Returns bool.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## clipboard.py

**路径**: `hermes_cli\clipboard.py`
**行数**: 495

### 功能描述

Clipboard image extraction for macOS, Windows, Linux, and WSL2.

Provides a single function `save_clipboard_image(dest)` that checks the
system clipboard for image data, saves it to *dest* as PNG, and returns
True on success.  No external Python dependencies — uses only OS-level
CLI tools that ship 

### 核心函数

- `save_clipboard_image()`: Extract an image from the system clipboard and save it as PNG.

    Returns True if an image was fou
- `has_clipboard_image()`: Quick check: does the clipboard currently contain an image?

    Lighter than save_clipboard_image —

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## codex_models.py

**路径**: `hermes_cli\codex_models.py`
**行数**: 207

### 功能描述

Codex model discovery from API, local cache, and config.

### 核心函数

- `get_codex_model_ids()`: Return available Codex model IDs, trying API first, then local sources.
    
    Resolution order: A

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## codex_runtime_plugin_migration.py

**路径**: `hermes_cli\codex_runtime_plugin_migration.py`
**行数**: 758

### 功能描述

Migrate Hermes' MCP server config and Codex's installed curated plugins
to the format Codex expects in ~/.codex/config.toml.

When the user enables the codex_app_server runtime, the codex subprocess
runs its own MCP client and its own plugin runtime (Linear, Atlassian,
Asana, plus per-account ChatGP

### 核心类

- `MigrationReport`: Outcome of a migration pass.

### 核心函数

- `render_codex_toml_section()`: Render the managed [mcp_servers.<n>] / [plugins.<id>] / [permissions]
    block for ~/.codex/config.
- `migrate()`: Translate Hermes mcp_servers config + Codex curated plugins into
    ~/.codex/config.toml.

    Args

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## codex_runtime_switch.py

**路径**: `hermes_cli\codex_runtime_switch.py`
**行数**: 267

### 功能描述

Shared logic for the /codex-runtime slash command.

Toggles `model.openai_runtime` between "auto" (= chat_completions, Hermes'
default) and "codex_app_server" (= hand turns to a codex subprocess).

Both CLI (cli.py) and gateway (gateway/run.py) call into this module so the
behavior stays identical a

### 核心类

- `CodexRuntimeStatus`: Result of a /codex-runtime invocation. Callers render this however
    suits their surface (CLI uses

### 核心函数

- `parse_args()`: Parse the slash-command argument string. Returns (value, errors).

    No args         → return curr
- `get_current_runtime()`: Read the current `model.openai_runtime` value from a config dict.
    Returns 'auto' for unset / emp
- `set_runtime()`: Mutate the config dict in place to persist the new runtime value.
    Returns the previous value for
- `check_codex_binary_ok()`: Best-effort verification that codex CLI is installed at acceptable
    version. Returns (ok, version
- `apply()`: Top-level entry point used by both CLI and gateway handlers.

    Args:
        config: in-memory co

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## colors.py

**路径**: `hermes_cli\colors.py`
**行数**: 39

### 功能描述

Shared ANSI color utilities for Hermes CLI modules.

### 核心类

- `Colors`

### 核心函数

- `should_use_color()`: Return True when colored output is appropriate.

    Respects the NO_COLOR environment variable (htt
- `color()`: Apply color codes to text (only when color output is appropriate).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## commands.py

**路径**: `hermes_cli\commands.py`
**行数**: 2049

### 功能描述

Slash command definitions and autocomplete for the Hermes CLI.

Central registry for all slash commands. Every consumer -- CLI help, gateway
dispatch, Telegram BotCommands, Slack subcommand mapping, autocomplete --
derives its data from ``COMMAND_REGISTRY``.

To add a command: add a ``CommandDef`` e

### 核心类

- `CommandDef`: Definition of a single slash command.
- `SlashCommandCompleter`: Autocomplete for built-in slash commands, subcommands, and skill commands.
- `SlashCommandAutoSuggest`: Inline ghost-text suggestions for slash commands and their subcommands.

    Shows the rest of a com

### 核心函数

- `resolve_command()`: Resolve a command name or alias to its CommandDef.

    Accepts names with or without the leading sl
- `is_gateway_known_command()`: Return True if ``name`` resolves to a gateway-dispatchable slash command.

    This covers both buil
- `should_bypass_active_session()`: Return True for any resolvable slash command.

    Rationale: every gateway-registered slash command
- `gateway_help_lines()`: Generate gateway help text lines from the registry.
- `telegram_bot_commands()`: Return (command_name, description) pairs for Telegram setMyCommands.

    Telegram command names can
- `telegram_menu_max_commands()`: Return configured Telegram BotCommand menu cap with safe bounds.
- `telegram_menu_commands()`: Return Telegram menu commands capped to the Bot API limit.

    Priority order (higher priority = ne
- `discord_skill_commands()`: Return skill entries for Discord slash command registration.

    Same priority and filtering logic 
- `discord_skill_commands_by_category()`: Return skill entries organized by category for Discord ``/skill`` autocomplete.

    Skills whose di
- `slack_native_slashes()`: Return (slash_name, description, usage_hint) triples for Slack.

    Every gateway-available command
- `slack_app_manifest()`: Generate a Slack app manifest with all gateway commands as slashes.

    ``request_url`` is required
- `slack_subcommand_map()`: Return subcommand -> /command mapping for Slack /hermes handler.

    Maps both canonical names and 

### 依赖关系

**依赖组件**: agent-engine, entry-points, tool-system
**跨组件调用**: 是

---

## completion.py

**路径**: `hermes_cli\completion.py`
**行数**: 320

### 功能描述

Shell completion script generation for hermes CLI.

Walks the live argparse parser tree to generate accurate, always-up-to-date
completion scripts — no hardcoded subcommand lists, no extra dependencies.

Supports bash, zsh, and fish.

### 核心函数

- `generate_bash()`
- `generate_zsh()`
- `generate_fish()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## config.py

**路径**: `hermes_cli\config.py`
**行数**: 7365

### 功能描述

Configuration management for Hermes Agent.

Config files are stored in ~/.hermes/ for easy access:
- ~/.hermes/config.yaml  - All settings (model, toolsets, terminal, etc.)
- ~/.hermes/.env         - API keys and secrets

This module provides:
- hermes config          - Show current configuration
- 

### 核心类

- `ConfigIssue`: A detected config structure problem.

### 核心函数

- `get_managed_system()`: Return the package manager owning this install, if any.
- `is_managed()`: Check if Hermes is running in package-manager-managed mode.

    Two signals: the HERMES_MANAGED env
- `get_managed_update_command()`: Return the preferred upgrade command for a managed install.
- `detect_install_method()`: Detect how Hermes was installed: 'docker', 'nixos', 'homebrew', 'git', or 'pip'.

    Resolution ord
- `stamp_install_method()`: Write the install method next to the running code (code-scoped stamp).

    The stamp lives in the i
- `is_uv_tool_install()`: Return True when the *running* Hermes lives in a ``uv tool`` layout.

    ``uv tool install hermes-a
- `recommended_update_command_for_method()`: Return the update command or guidance for a given install method.
- `recommended_update_command()`: Return the best update command for the current installation.
- `format_docker_update_message()`: Return the user-facing message for ``hermes update`` inside Docker.

    Centralised so ``cmd_update
- `format_managed_message()`: Build a user-facing error for managed installs.
- `managed_error()`: Print user-friendly error for managed mode.
- `get_container_exec_info()`: Read container mode metadata from HERMES_HOME/.container-mode.

    Returns a dict with keys: backen
- `get_config_path()`: Get the main config file path.
- `get_env_path()`: Get the .env file path (for API keys).
- `get_project_root()`: Get the project installation directory.
- ... 还有 38 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, state-management
**跨组件调用**: 是

---

## container_boot.py

**路径**: `hermes_cli\container_boot.py`
**行数**: 526

### 功能描述

Container-boot reconciliation of per-profile gateway s6 services.

Service directories under /run/service/ live on **tmpfs** and are wiped
on every container restart. Profile directories under
``$HERMES_HOME/profiles/<name>/`` live on the persistent VOLUME, and
each one records its gateway's last st

### 核心类

- `ReconcileAction`: One profile's outcome from a single reconciliation pass.

### 核心函数

- `reconcile_profile_gateways()`: Recreate s6 service registrations for every persistent profile.

    Always registers a ``gateway-de
- `main()`: Entry point invoked from /etc/cont-init.d/02-reconcile-profiles.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## context_switch_guard.py

**路径**: `hermes_cli\context_switch_guard.py`
**行数**: 170

### 功能描述

Warn when an in-session model switch will trigger preflight compression on the next turn.

Addresses part of #23767 ("user-facing guardrail when switching from a
high-context provider to a substantially lower-context provider"). The other
proposed fixes from that issue (hard preflight token guard, m

### 核心函数

- `merge_preflight_compression_warning()`: If the next user message will likely preflight-compress, append a warning.
- `enrich_model_switch_warnings_for_gateway()`: Gateway helper: cached agent + session DB messages.

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## copilot_auth.py

**路径**: `hermes_cli\copilot_auth.py`
**行数**: 393

### 功能描述

GitHub Copilot authentication utilities.

Implements the OAuth device code flow used by the Copilot CLI and handles
token validation/exchange for the Copilot API.

Token type support (per GitHub docs):
  gho_          OAuth token           ✓  (default via copilot login)
  github_pat_   Fine-grained 

### 核心函数

- `validate_copilot_token()`: Validate that a token is usable with the Copilot API.

    Returns (valid, message).
- `resolve_copilot_token()`: Resolve a GitHub token suitable for Copilot API use.

    Returns (token, source) where source descr
- `copilot_device_code_login()`: Run the GitHub OAuth device code flow for Copilot.

    Prints instructions for the user, polls for 
- `exchange_copilot_token()`: Exchange a raw GitHub token for a short-lived Copilot API token.

    Calls ``GET https://api.github
- `get_copilot_api_token()`: Exchange a raw GitHub token for a Copilot API token, with fallback.

    Convenience wrapper: return
- `copilot_request_headers()`: Build the standard headers for Copilot API requests.

    Replicates the header set used by opencode

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## cron.py

**路径**: `hermes_cli\cron.py`
**行数**: 425

### 功能描述

Cron subcommand for hermes CLI.

Handles standalone cron management commands like list, create, edit,
pause/resume/run/remove, status, and tick.

### 核心函数

- `cron_list()`: List all scheduled jobs.
- `cron_tick()`: Run due jobs once and exit.
- `cron_status()`: Show cron execution status.
- `cron_create()`
- `cron_edit()`
- `cron_command()`: Handle cron subcommands.

### 依赖关系

**依赖组件**: cron, tool-system
**跨组件调用**: 是

---

## curator.py

**路径**: `hermes_cli\curator.py`
**行数**: 620

### 功能描述

CLI subcommand: `hermes curator <subcommand>`.

Thin shell around agent/curator.py and tools/skill_usage.py. Renders a status
table, triggers a run, pauses/resumes, and pins/unpins skills.

This module intentionally has no side effects at import time — main.py wires
the argparse subparsers on demand

### 核心函数

- `register_cli()`: Attach `curator` subcommands to *parent*.

    main.py calls this with the ArgumentParser returned b
- `cli_main()`: Standalone entry (also usable by hermes_cli.main fallthrough).

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## curses_ui.py

**路径**: `hermes_cli\curses_ui.py`
**行数**: 873

### 功能描述

Shared curses-based UI components for Hermes CLI.

Used by `hermes tools` and `hermes skills` for interactive checklists.
Provides a curses multi-select with keyboard navigation, plus a
text-based numbered fallback for terminals without curses support.

### 核心类

- `_SearchState`: Mutable search state shared by curses picker loops.

### 核心函数

- `flush_stdin()`: Flush any stray bytes from the stdin input buffer.

    Must be called after ``curses.wrapper()`` (o
- `read_menu_key()`: Read one keypress and normalize it to a menu action.

    Decodes raw arrow-key escape sequences in 
- `curses_checklist()`: Curses multi-select checklist. Returns set of selected indices.

    Args:
        title: Header lin
- `curses_radiolist()`: Curses single-select radio list. Returns the selected index.

    Args:
        title: Header line d
- `curses_single_select()`: Curses single-select menu. Returns selected index or None on cancel.

    Works inside prompt_toolki

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `hermes_cli\dashboard_auth\__init__.py`
**行数**: 47

### 功能描述

Dashboard authentication provider framework.

The dashboard auth gate engages only when the dashboard binds to a
non-loopback host without ``--insecure``. In that mode, every request must
carry a verified session from one of the registered ``DashboardAuthProvider``
plugins.

The Nous provider lives 

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## audit.py

**路径**: `hermes_cli\dashboard_auth\audit.py`
**行数**: 90

### 功能描述

Audit log for dashboard-auth events.

Profile-aware location: ``$HERMES_HOME/logs/dashboard-auth.log``.
Format: one JSON object per line. Token-like fields are stripped before
serialisation to avoid leaking refresh tokens or JWTs to disk.

This module deliberately keeps a minimal dependency surface 

### 核心类

- `AuditEvent`: Event types written to dashboard-auth.log.

    Values are the literal ``event`` field on the JSON l

### 核心函数

- `audit_log()`: Append one event to the audit log.

    Token-like fields are dropped. Missing log directory is crea

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## base.py

**路径**: `hermes_cli\dashboard_auth\base.py`
**行数**: 294

### 功能描述

Abstract base + dataclasses + exceptions for dashboard auth providers.

### 核心类

- `Session`: A verified identity. Returned by ``complete_login`` and ``verify_session``.

    All fields are mand
- `TokenPrincipal`: A verified non-interactive (service-to-service) caller.

    The token analog of :class:`Session`. W
- `LoginStart`: First leg of the OAuth round trip.

    ``redirect_url`` is the URL the browser must navigate to (e.
- `ProviderError`: IDP unreachable, network error, or other transient failure.

    Middleware translates this to HTTP 
- `InvalidCodeError`: The OAuth callback ``code`` / ``state`` failed validation.

    Middleware translates this to HTTP 4
- `InvalidCredentialsError`: A username/password pair was rejected by a password provider.

    Raised by :meth:`DashboardAuthPro
- `RefreshExpiredError`: The refresh token is dead.

    Middleware clears cookies and forces re-login (302 → ``/login``).
- `DashboardAuthProvider`: Protocol every dashboard-auth provider plugin implements.

    Lifecycle:
      1. ``start_login`` —

### 核心函数

- `assert_protocol_compliance()`: Raise ``TypeError`` if ``cls`` doesn't fully implement the provider protocol.

    Call this in ever

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## cookies.py

**路径**: `hermes_cli\dashboard_auth\cookies.py`
**行数**: 248

### 功能描述

Cookie helpers for dashboard auth.

Three cookies in play:
  - hermes_session_at:   the OAuth access token
                         (HttpOnly, lifetime = token TTL, ~15 min)
  - hermes_session_rt:   the OAuth refresh token
                         (HttpOnly, lifetime = 24h, ROTATING + reuse-detected

### 核心函数

- `set_session_cookies()`: Set the session cookies on the response.

    ``access_token_expires_in`` is in seconds. Use the pro
- `clear_session_cookies()`: Emit Max-Age=0 deletions for both session cookies.

    To delete a cookie reliably the deletion's `
- `set_pkce_cookie()`
- `clear_pkce_cookie()`
- `read_session_cookies()`: Returns (access_token, refresh_token), either may be None.
- `read_pkce_cookie()`
- `detect_https()`: Decide whether to set the ``Secure`` cookie flag.

    Reads ``request.url.scheme`` — under uvicorn'

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## login_page.py

**路径**: `hermes_cli\dashboard_auth\login_page.py`
**行数**: 535

### 功能描述

Server-rendered /login page.

No React, no JavaScript dependency. Listed providers come from the
registry; clicking a provider sends a GET to
``/auth/login?provider=<name>``.

Visual styling mirrors the Nous Research design system (the
``@nous-research/ui`` package the React dashboard uses): the sam

### 核心类

- `name`

### 核心函数

- `render_login_html()`: Return the full HTML for ``GET /login``.

    ``next_path`` — when set, the post-login landing path 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## middleware.py

**路径**: `hermes_cli\dashboard_auth\middleware.py`
**行数**: 376

### 功能描述

Auth-gate middleware for the dashboard.

Engaged when ``app.state.auth_required is True``. The gate's job:

  1. Allow a small set of routes through unauthenticated (login page,
     ``/auth/*`` OAuth round trip, ``/api/auth/providers``, static
     assets).
  2. For everything else, demand a valid 

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## prefix.py

**路径**: `hermes_cli\dashboard_auth\prefix.py`
**行数**: 202

### 功能描述

Helpers for X-Forwarded-Prefix support.

Mission-control style deploys reverse-proxy the dashboard at a path
prefix (e.g. ``mission-control.tilos.com/hermes/*`` -> dashboard on
:9119), injecting ``X-Forwarded-Prefix: /hermes`` so the backend can
reconstruct prefixed URLs (Location: headers, OAuth re

### 核心函数

- `normalise_prefix()`: Normalise an X-Forwarded-Prefix header value.

    Returns a string like ``"/hermes"`` (no trailing 
- `prefix_from_request()`: Convenience wrapper that reads the header off a Starlette/FastAPI
    Request and normalises it. Ret
- `resolve_public_url()`: Resolve the operator-declared dashboard public URL.

    Precedence (mirrors ``dashboard.oauth.clien

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## public_paths.py

**路径**: `hermes_cli\dashboard_auth\public_paths.py`
**行数**: 56

### 功能描述

Shared allowlist of ``/api/*`` paths that bypass dashboard auth.

Two middlewares enforce dashboard auth and previously kept independent
copies of this list:

* ``hermes_cli.web_server.auth_middleware`` — loopback / ``--insecure``
  mode, gates on the ephemeral ``_SESSION_TOKEN``.
* ``hermes_cli.das

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## registry.py

**路径**: `hermes_cli\dashboard_auth\registry.py`
**行数**: 73

### 功能描述

Module-level registry for DashboardAuthProvider instances.

Plugins call ``register_provider`` via the plugin context hook at startup.
The auth gate middleware iterates ``list_providers()`` and uses
``get_provider`` to dispatch on the session's ``provider`` field.

### 核心函数

- `register_provider()`: Register a provider.

    Raises:
        TypeError: on protocol violation.
        ValueError: if a
- `get_provider()`: Return the registered provider for ``name``, or None if unknown.
- `list_providers()`: All registered providers, in registration order.
- `list_token_providers()`: Registered providers that support non-interactive token auth.

    The subset of ``list_providers()`
- `clear_providers()`: Test-only: drop all registrations.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## routes.py

**路径**: `hermes_cli\dashboard_auth\routes.py`
**行数**: 622

### 功能描述

HTTP routes for the dashboard-auth OAuth round trip.

Mounted at root (no prefix) by ``web_server.py``. The router does not
auto-gate; gating is performed by ``gated_auth_middleware``, which
allowlists everything under ``/auth/*`` and ``/api/auth/providers``.

The routes:

  GET  /login             

### 核心类

- `_PasswordLoginBody`

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## token_auth.py

**路径**: `hermes_cli\dashboard_auth\token_auth.py`
**行数**: 195

### 功能描述

Route-agnostic non-interactive (bearer-token) auth seam for the dashboard.

This is the generic API-token capability (decisions.md Q-C): a reusable seam
that ANY service-to-service / machine-credential provider plugs into, NOT a
drain-specific hook. The drain bearer-secret plugin is merely the first

### 核心函数

- `register_token_route()`: Mark ``path`` (exact match) as token-authable.

    Idempotent. Call at module import / app setup so
- `is_token_route()`: True if ``path`` was registered as token-authable (exact match).
- `clear_token_routes()`: Test-only: drop all registered token routes.
- `extract_bearer_token()`: Return the bearer token from the ``Authorization`` header, or "".

    Accepts ``<scheme> <token>`` 
- `authenticate_token()`: Try every token provider against the request's bearer token.

    Returns ``(principal, unreachable_

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## ws_tickets.py

**路径**: `hermes_cli\dashboard_auth\ws_tickets.py`
**行数**: 162

### 功能描述

WS-upgrade auth credentials for gated mode.

Browsers cannot set ``Authorization`` on a WebSocket upgrade. In loopback
mode the legacy ``?token=<_SESSION_TOKEN>`` query param works because the
token is injected into the SPA bundle. In gated mode there is no injected
token — so this module provides t

### 核心类

- `TicketInvalid`: Ticket missing, expired, or already consumed.

### 核心函数

- `mint_ticket()`: Generate a one-shot ticket bound to this user identity.

    The returned token is base64url, 43 byt
- `consume_ticket()`: Validate and consume. Raises :class:`TicketInvalid` on missing/expired/used.

    Single-use semanti
- `internal_ws_credential()`: Return the process-lifetime internal WS credential, minting it once.

    Used by the server to auth
- `consume_internal_credential()`: Validate an internal credential. Raises :class:`TicketInvalid` on mismatch.

    Unlike :func:`consu

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## dashboard_register.py

**路径**: `hermes_cli\dashboard_register.py`
**行数**: 428

### 功能描述

``hermes dashboard register`` — register a self-hosted dashboard OAuth client.

Automates what a user otherwise does by hand: open the Nous Portal
``/local-dashboards`` page in a browser, click "register", copy the
resulting ``agent:{id}`` OAuth client ID, and paste it into ``~/.hermes/.env``
as ``H

### 核心函数

- `cmd_dashboard_register()`: Register a self-hosted dashboard OAuth client with Nous Portal.

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## debug.py

**路径**: `hermes_cli\debug.py`
**行数**: 849

### 功能描述

``hermes debug`` debug tools for Hermes Agent.

Currently supports:
    hermes debug share    Upload debug report (system info + logs) to a
                          paste service and print a shareable URL.
                          By default, log content is run through
                          ``

### 核心类

- `LogSnapshot`: Single-read snapshot of a log file used by debug-share.
- `DebugShareResult`: Structured outcome of a ``debug share`` upload.

    Returned by :func:`build_debug_share` so non-CL

### 核心函数

- `delete_paste()`: Delete a paste from paste.rs.  Returns True on success.

    Only paste.rs supports unauthenticated 
- `upload_to_pastebin()`: Upload *content* to a paste service, trying paste.rs then dpaste.com.

    Returns the paste URL on 
- `collect_debug_report()`: Build the summary debug report: system dump + log tails.

    Parameters
    ----------
    log_line
- `build_debug_share()`: Collect the debug report + full logs, upload each, return the URLs.

    This is the shared core beh
- `run_debug_share()`: Collect debug report + full logs, upload each, print URLs.
- `run_debug_delete()`: Delete one or more paste URLs uploaded by /debug.
- `run_debug()`: Route debug subcommands.

### 依赖关系

**依赖组件**: agent-engine, entry-points, state-management
**跨组件调用**: 是

---

## default_soul.py

**路径**: `hermes_cli\default_soul.py`
**行数**: 77

### 功能描述

Default SOUL.md template seeded into HERMES_HOME on first run.

### 核心函数

- `is_legacy_template_soul()`: True if ``text`` is an old empty-template SOUL.md (no user persona).

    Older installers seeded a 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## dep_ensure.py

**路径**: `hermes_cli\dep_ensure.py`
**行数**: 162

### 功能描述

Lazy dependency bootstrapper for non-Python runtime deps.

Detection and prompting live here in Python — not in install.sh — because:
  1. shutil.which() works on every platform; install.sh needs bash.
  2. Detection is instant; spawning bash for a "is node installed?" check is waste.
  3. Python co

### 核心函数

- `ensure_dependency()`: Ensure a non-Python dependency is available. Returns True if available.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## dingtalk_auth.py

**路径**: `hermes_cli\dingtalk_auth.py`
**行数**: 294

### 功能描述

DingTalk Device Flow authorization.

Implements the same 3-step registration flow as dingtalk-openclaw-connector:
  1. POST /app/registration/init   → get nonce
  2. POST /app/registration/begin  → get device_code + verification_uri_complete
  3. POST /app/registration/poll   → poll until SUCCESS → 

### 核心类

- `RegistrationError`: Raised when a DingTalk registration API call fails.

### 核心函数

- `begin_registration()`: Start a device-flow registration.

    Returns a dict with keys:
        device_code, verification_u
- `poll_registration()`: Poll the registration status once.

    Returns a dict with keys:  status, client_id?, client_secret
- `wait_for_registration_success()`: Block until the registration succeeds or times out.

    Returns (client_id, client_secret).
- `render_qr_to_terminal()`: Render *url* as a compact QR code in the terminal.

    Returns True if the QR code was printed, Fal
- `dingtalk_qr_auth()`: Run the interactive QR-code device-flow authorization.

    Returns (client_id, client_secret) on su

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## doctor.py

**路径**: `hermes_cli\doctor.py`
**行数**: 2385

### 功能描述

Doctor command for hermes CLI.

Diagnoses issues with Hermes Agent setup.

### 核心函数

- `check_ok()`
- `check_warn()`
- `check_fail()`
- `check_info()`
- `check_certificates()`: Verify the certifi CA bundle is loadable.

    Surfaces the SSLConfigurationError user-friendly path
- `managed_scope_check()`: Report the active managed scope (resolved dir + pinned key counts).

    Silent when no managed scop
- `run_doctor()`: Run diagnostic checks.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## dump.py

**路径**: `hermes_cli\dump.py`
**行数**: 404

### 功能描述

Dump command for hermes CLI.

Outputs a compact, plain-text summary of the user's Hermes setup
that can be copy-pasted into Discord/GitHub/Telegram for support context.
No ANSI colors, no checkmarks — just data.

### 核心函数

- `run_dump()`: Output a compact, copy-pasteable setup summary.

### 依赖关系

**依赖组件**: agent-engine, state-management
**跨组件调用**: 是

---

## env_loader.py

**路径**: `hermes_cli\env_loader.py`
**行数**: 378

### 功能描述

Helpers for loading Hermes .env files consistently across entrypoints.

### 核心函数

- `get_secret_source()`: Return the label of the secret source that supplied ``env_var``, if any.

    Returns ``"bitwarden"`
- `reset_secret_source_cache()`: Forget which HERMES_HOME paths have already had external secrets applied.

    The first call to ``_
- `format_secret_source_suffix()`: Return a human-readable suffix like ``" (from Bitwarden)"`` or ``""``.

    Use this when printing a
- `load_hermes_dotenv()`: Load Hermes environment files with user config taking precedence.

    Behavior:
    - `~/.hermes/.e

### 依赖关系

**依赖组件**: agent-engine, entry-points
**跨组件调用**: 是

---

## fallback_cmd.py

**路径**: `hermes_cli\fallback_cmd.py`
**行数**: 355

### 功能描述

hermes fallback — manage the fallback provider chain.

Fallback providers are tried in order when the primary model fails with
rate-limit, overload, or connection errors. See:
https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers

Subcommands:
  hermes fallback [list]   S

### 核心函数

- `cmd_fallback_list()`: Print the current fallback chain.
- `cmd_fallback_add()`: Launch the same picker as `hermes model`, then append the selection to the chain.
- `cmd_fallback_remove()`: Pick an entry from the chain and remove it.
- `cmd_fallback_clear()`: Remove all fallback entries (with confirmation).
- `cmd_fallback()`: Top-level dispatcher for ``hermes fallback [subcommand]``.

### 依赖关系

**依赖组件**: acp-adapter, entry-points
**跨组件调用**: 是

---

## fallback_config.py

**路径**: `hermes_cli\fallback_config.py`
**行数**: 73

### 功能描述

Helpers for reading the effective fallback provider chain from config.

### 核心函数

- `get_fallback_chain()`: Return the effective fallback chain merged across old and new config keys.

    ``fallback_providers

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## gateway.py

**路径**: `hermes_cli\gateway.py`
**行数**: 6743

### 功能描述

Gateway subcommand for hermes CLI.

Handles: hermes gateway [run|start|stop|restart|status|install|uninstall|setup]

### 核心类

- `GatewayRuntimeSnapshot`
- `ProfileGatewayProcess`
- `UserSystemdUnavailableError`: Raised when ``systemctl --user`` cannot reach the user D-Bus session.

    Typically hit on fresh RH
- `SystemScopeRequiresRootError`: Raised when a system-scope gateway operation is attempted as non-root.

    System-scope units live 

### 核心函数

- `find_gateway_pids()`: Find PIDs of running gateway processes.

    Args:
        exclude_pids: PIDs to exclude from the re
- `find_profile_gateway_processes()`: Return running gateway PIDs mapped to Hermes profiles via PID files.
- `launch_detached_gateway_restart_by_cmdline()`: Relaunch a gateway by replaying its captured command line after exit.

    Companion to ``launch_det
- `launch_detached_profile_gateway_restart()`: Relaunch a manually-run profile gateway after its current PID exits.
- `get_gateway_runtime_snapshot()`: Return a unified view of gateway liveness for the current profile.
- `kill_gateway_processes()`: Kill any running gateway processes. Returns count killed.

    Args:
        force: Use the platform
- `stop_profile_gateway()`: Stop only the gateway for the current profile (HERMES_HOME-scoped).

    Uses the PID file written b
- `is_linux()`
- `supports_systemd_services()`
- `is_macos()`
- `is_windows()`
- `get_service_name()`: Derive a systemd service name scoped to this HERMES_HOME.

    Default ``~/.hermes`` returns ``herme
- `get_systemd_unit_path()`
- `get_installed_systemd_scopes()`
- `has_conflicting_systemd_units()`
- ... 还有 32 个函数

### 依赖关系

**依赖组件**: entry-points, gateway, state-management
**跨组件调用**: 是

---

## gateway_enroll.py

**路径**: `hermes_cli\gateway_enroll.py`
**行数**: 261

### 功能描述

``hermes gateway enroll`` — enroll a self-hosted gateway with a relay connector.

The connector⇄gateway channel is authenticated (the gateway may be
customer-managed and internet-exposed). This command is the gateway half of the
zero-touch enrollment in the connector repo's
``docs/connector-gateway-

### 核心函数

- `cmd_gateway_enroll()`: Enroll this gateway with a relay connector; persist the auth creds to .env.

### 依赖关系

**依赖组件**: acp-adapter, gateway
**跨组件调用**: 是

---

## gateway_windows.py

**路径**: `hermes_cli\gateway_windows.py`
**行数**: 1612

### 功能描述

Windows gateway service backend (Scheduled Task + Startup-folder fallback).

This mirrors the contract exposed by ``launchd_install`` / ``launchd_start`` /
``launchd_status`` etc. on macOS and ``systemd_install`` / ``systemd_start`` on
Linux. It uses ``schtasks`` under the hood with ``/SC ONLOGON`` 

### 核心函数

- `get_task_name()`: Scheduled Task name, scoped per profile.

    Default profile: ``Hermes_Gateway``
    Named profile 
- `get_task_script_path()`: The generated ``gateway.cmd`` wrapper kept beside the VBS launcher.

    Lives under ``%LOCALAPPDATA
- `get_startup_entry_path()`
- `install()`: Install the gateway as a Windows Scheduled Task (with Startup fallback).

    Idempotent: re-running
- `uninstall()`: Remove both the Scheduled Task and the Startup-folder fallback, if present.
- `is_task_registered()`
- `is_startup_entry_installed()`
- `is_installed()`: True when either the schtasks entry or the Startup fallback is present.
- `query_task_status()`: Parse ``schtasks /Query /V /FO LIST`` and pull the interesting keys.
- `status()`: Print a status report for the Windows gateway service.
- `start()`: Start the gateway using the canonical detached Windows launch path.
- `stop()`: Stop the gateway.

    Writes the planned-stop marker first so the gateway can drain
    in-flight a
- `restart()`: Stop the gateway then start it again.

    Waits for the old gateway to be authoritatively gone befo

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## goals.py

**路径**: `hermes_cli\goals.py`
**行数**: 1766

### 功能描述

Persistent session goals — the Ralph loop for Hermes.

A goal is a free-form user objective that stays active across turns. After
each turn completes, a small judge call asks an auxiliary model "is this
goal satisfied by the assistant's last response?". If not, Hermes feeds a
continuation prompt bac

### 核心类

- `GoalContract`: Optional structured completion contract for a goal.

    Each field is free-form prose the user (or 
- `GoalState`: Serializable goal state stored per session.
- `GoalManager`: Per-session goal state + continuation decisions.

    The CLI and gateway each hold one ``GoalManage

### 核心函数

- `parse_contract()`: Split user-typed goal text into a headline + structured contract.

    Supports inline ``field: valu
- `load_goal()`: Load the goal for a session, or None if none exists.
- `save_goal()`: Persist a goal to SessionDB. No-op if DB unavailable.
- `clear_goal()`: Mark a goal cleared in the DB (preserved for audit, status=cleared).
- `migrate_goal_to_session()`: Carry a persistent /goal from a parent session to its continuation.

    Context compression rotates
- `judge_goal()`: Ask the auxiliary model whether the goal is satisfied.

    Returns ``(verdict, reason, parse_failed
- `gather_background_processes()`: Return the live background-process snapshot for the goal judge.

    Thin, fail-safe wrapper over ``
- `draft_contract()`: Expand a plain-language objective into a structured completion contract.

    Uses the ``goal_judge`
- `run_kanban_goal_loop()`: Drive a kanban worker through a Ralph-style goal loop.

    The dispatcher spawns a goal-mode worker

### 依赖关系

**依赖组件**: llm-client, state-management, tool-system
**跨组件调用**: 是

---

## gui_uninstall.py

**路径**: `hermes_cli\gui_uninstall.py`
**行数**: 286

### 功能描述

Hermes Desktop (Chat GUI) uninstaller.

The desktop GUI ships in two shapes and this module knows how to find and
remove the artifacts of both, on Linux, macOS, and Windows, WITHOUT touching
the Python agent or the user's config/data:

  1. Source-built GUI (``hermes desktop`` / ``hermes gui``)
    

### 核心函数

- `log_info()`
- `log_success()`
- `log_warn()`
- `desktop_userdata_dir()`: Return the Electron ``userData`` directory for the desktop app.

    Mirrors Electron's ``app.getPat
- `source_built_gui_artifacts()`: GUI build artifacts produced by ``hermes desktop`` inside the checkout.

    These are removable on 
- `packaged_gui_app_paths()`: Standard install locations of the packaged desktop distributable.

    Returns every candidate for t
- `agent_is_installed()`: Return True when a usable Python agent install exists under HERMES_HOME.

    Used by the desktop UI
- `gui_is_installed()`: Return True when any desktop GUI artifact exists (built or packaged).
- `gui_install_summary()`: Structured snapshot of what's installed, for the desktop UI to render.

    Returns JSON-serializabl
- `uninstall_gui()`: Remove the desktop GUI's artifacts, leaving the agent + user data intact.

    Removes:
      - sour

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## hooks.py

**路径**: `hermes_cli\hooks.py`
**行数**: 386

### 功能描述

hermes hooks — inspect and manage shell-script hooks.

Usage::

    hermes hooks list
    hermes hooks test <event> [--for-tool X] [--payload-file F]
    hermes hooks revoke <command>
    hermes hooks doctor

Consent records live under ``~/.hermes/shell-hooks-allowlist.json`` and
hook definitions co

### 核心函数

- `hooks_command()`: Entry point for ``hermes hooks`` — dispatches to the requested action.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## inventory.py

**路径**: `hermes_cli\inventory.py`
**行数**: 468

### 功能描述

Provider/model inventory context — shared substrate for the dashboard
``/api/model/options``, the TUI ``model.options``/``model.save_key``
JSON-RPC handlers, and the interactive picker.

Before this module the three call-sites each duplicated:

1. The 17-LOC config-slice that pulls ``model.{default,

### 核心类

- `ConfigContext`: Snapshot of the model + provider config every inventory caller
    needs. Built once via ``load_pick

### 核心函数

- `load_picker_context()`: Load the disk-config snapshot every consumer needs.

    Replaces the inline 17-LOC config-slice tha
- `build_models_payload()`: Build the ``{providers, model, provider}`` shape every consumer
    needs from a single substrate ca

### 依赖关系

**依赖组件**: acp-adapter, agent-engine
**跨组件调用**: 是

---

## kanban.py

**路径**: `hermes_cli\kanban.py`
**行数**: 2846

### 功能描述

CLI for the Hermes Kanban board — ``hermes kanban …`` subcommand.

Exposes the full Kanban command surface documented in the design spec
(``docs/hermes-kanban-v1-spec.pdf``).  All DB work is delegated to
``kanban_db``.  This module adds:

  * Argparse subcommand construction (``build_parser``).
  * 

### 核心函数

- `build_parser()`: Attach the ``kanban`` subcommand tree under an existing subparsers.

    Returns the top-level ``kan
- `kanban_command()`: Entry point from ``hermes kanban …`` argparse dispatch.

    Returns a shell-style exit code (0 on s
- `run_slash()`: Execute a ``/kanban …`` string and return captured stdout/stderr.

    ``rest`` is everything after 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## kanban_db.py

**路径**: `hermes_cli\kanban_db.py`
**行数**: 8618

### 功能描述

SQLite-backed Kanban board for multi-profile, multi-project collaboration.

In a fresh install the board lives at ``<root>/kanban.db`` where
``<root>`` is the **shared Hermes root** (the parent of any active
profile). Profiles intentionally collapse onto a shared board: it IS
the cross-profile coord

### 核心类

- `Task`: In-memory view of a row from the ``tasks`` table.
- `Run`: In-memory view of a ``task_runs`` row.

    A run is one attempt to execute a task — created on clai
- `Comment`
- `Attachment`: In-memory view of a row from the ``task_attachments`` table.
- `Event`
- `KanbanDbCorruptError`: Raised when an existing kanban DB file fails integrity checks.

    Fail-closed guard against silent
- `HallucinatedCardsError`: Raised by ``complete_task`` when ``created_cards`` contains ids
    that don't exist or weren't crea
- `DispatchResult`: Outcome of a single ``dispatch`` pass.

### 核心函数

- `scoped_current_board()`: Temporarily pin the active board for the current context only.
- `kanban_home()`: Return the shared Hermes root that anchors the kanban board.

    Resolution order:

    1. ``HERMES
- `boards_root()`: Return ``<root>/kanban/boards`` — the parent of non-default board dirs.

    ``default`` is intentio
- `current_board_path()`: Return the path to ``<root>/kanban/current``.

    One-line text file written by ``hermes kanban boa
- `get_current_board()`: Return the active board slug, honouring the resolution chain.

    Order (highest precedence first):
- `set_current_board()`: Persist ``slug`` as the active board. Returns the file written.

    Writes ``<root>/kanban/current`
- `clear_current_board()`: Remove ``<root>/kanban/current`` so the active board reverts to ``default``.
- `board_dir()`: Return the on-disk directory for ``board``.

    ``default`` is ``<root>/kanban/boards/default/`` **
- `board_exists()`: Return True if the board has persisted metadata or a DB on disk.

    ``default`` is considered to a
- `kanban_db_path()`: Return the path to the ``kanban.db`` for ``board``.

    Resolution (highest precedence first):

   
- `workspaces_root()`: Return the directory under which ``scratch`` workspaces are created.

    Anchored per-board so work
- `attachments_root()`: Return the directory under which task file attachments are stored.

    Mirrors :func:`worker_logs_d
- `task_attachments_dir()`: Return the per-task attachment directory ``<root>/<task_id>/``.
- `worker_logs_dir()`: Return the directory under which per-task worker logs are written.

    ``default`` keeps the legacy
- `board_metadata_path()`: Return the path to ``board.json`` for ``board``.

    Stores display metadata (display name, descrip
- ... 还有 78 个函数

### 依赖关系

**依赖组件**: entry-points, gateway, state-management
**跨组件调用**: 是

---

## kanban_decompose.py

**路径**: `hermes_cli\kanban_decompose.py`
**行数**: 478

### 功能描述

Kanban decomposer — fan a triage task out into a graph of child tasks.

Invoked by ``hermes kanban decompose [task_id | --all]`` and the
auto-decompose path in the gateway dispatcher loop. Reads the user's
profile roster (with descriptions) and asks the auxiliary LLM to
return a task graph in JSON. 

### 核心类

- `DecomposeOutcome`: Result of decomposing a single triage task.

### 核心函数

- `decompose_task()`: Decompose a triage task into a graph of child tasks.

    Returns an outcome describing what happene
- `list_triage_ids()`: Return task ids currently in the triage column.

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## kanban_diagnostics.py

**路径**: `hermes_cli\kanban_diagnostics.py`
**行数**: 1108

### 功能描述

Kanban diagnostics — structured, actionable distress signals for tasks.

A ``Diagnostic`` is a machine-readable description of something that's wrong
with a kanban task: a hallucinated card id, a spawn crash-loop, a task
stuck blocked for too long, etc. Each one carries:

* A **kind** (canonical cod

### 核心类

- `DiagnosticAction`: A single recovery action attached to a diagnostic.

    The ``kind`` determines how both the UI and 
- `Diagnostic`: One active distress signal on a task.

### 核心函数

- `severity_at_or_above()`: Return True when ``severity`` meets or exceeds ``threshold``.
- `triage_aux_status()`: Inspect raw config and report whether triage paths look configured.

    Returns ``None`` when confi
- `config_from_kanban_config()`: Build diagnostics config from the runtime ``kanban`` config section.

    ``kanban.diagnostics.failu
- `config_from_runtime_config()`: Build diagnostics config from the full Hermes runtime config.

    Carries through ``kanban``, ``aux
- `compute_task_diagnostics()`: Run every rule against a single task's state and return a
    severity-sorted list of active diagnos

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## kanban_specify.py

**路径**: `hermes_cli\kanban_specify.py`
**行数**: 274

### 功能描述

Kanban triage specifier — flesh out a one-liner into a real spec.

Used by ``hermes kanban specify [task_id | --all]``. Takes a task that
lives in the Triage column (a rough idea, typically only a title), calls
the auxiliary LLM to produce:

  * A tightened title (optional — only replaces if the mod

### 核心类

- `SpecifyOutcome`: Result of specifying a single triage task.

### 核心函数

- `specify_task()`: Specify a single triage task and promote it to ``todo``.

    Returns an outcome describing what hap
- `list_triage_ids()`: Return task ids currently in the triage column.

    ``tenant`` narrows the sweep; ``None`` returns 

### 依赖关系

**依赖组件**: entry-points, llm-client
**跨组件调用**: 是

---

## kanban_swarm.py

**路径**: `hermes_cli\kanban_swarm.py`
**行数**: 279

### 功能描述

Kanban Swarm v1: thin swarm topology helpers on top of Kanban.

This module intentionally does not introduce a second scheduler. It writes a
small task graph into the existing Kanban kernel:

    planning root (completed immediately)
        ├─ parallel specialist workers (ready)
        └─ verifier

### 核心类

- `SwarmWorkerSpec`: A single parallel worker card in a swarm.
- `SwarmCreated`: IDs produced by :func:`create_swarm`.

### 核心函数

- `create_swarm()`: Create a durable Kanban swarm graph.

    The returned graph is immediately dispatchable: the planni
- `post_blackboard_update()`: Append one structured update to the swarm root blackboard.
- `latest_blackboard()`: Merge structured blackboard comments on a root card.

    Later comments replace earlier values for 
- `parse_worker_arg()`: Parse CLI ``--worker profile:title[:skill,skill]`` values.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## logs.py

**路径**: `hermes_cli\logs.py`
**行数**: 395

### 功能描述

``hermes logs`` — view and filter Hermes log files.

Supports tailing, following, session filtering, level filtering,
component filtering, and relative time ranges.  All log files live
under ``~/.hermes/logs/``.

Usage examples::

    hermes logs                    # last 50 lines of agent.log
    h

### 核心函数

- `tail_log()`: Read and display log lines, optionally following in real time.

    Parameters
    ----------
    lo
- `list_logs()`: Print available log files with sizes.

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## main.py

**路径**: `hermes_cli\main.py`
**行数**: 13296

### 功能描述

Hermes CLI - Main entry point.

Usage:
    hermes                     # Interactive chat (default)
    hermes chat                # Interactive chat
    hermes gateway             # Run gateway in foreground
    hermes gateway start       # Start gateway as service
    hermes gateway stop        # S

### 核心类

- `_UpdateOutputStream`: Stream wrapper used during ``hermes update`` to survive terminal loss.

    Wraps the process's orig

### 核心函数

- `cmd_chat()`: Run interactive chat CLI.
- `cmd_gateway()`: Gateway management commands.
- `cmd_proxy()`: Local OpenAI-compatible proxy to OAuth providers.
- `cmd_whatsapp()`: Set up WhatsApp: choose mode, configure, install bridge, pair via QR.
- `cmd_whatsapp_cloud()`: Set up WhatsApp Business Cloud API (official Meta integration).

    Walks the user through the Meta
- `cmd_setup()`: Interactive setup wizard.
- `cmd_postinstall()`: One-shot bootstrap for pip users: install non-Python deps + run setup.
- `cmd_model()`: Select default model — starts with provider selection, then model picker.
- `select_provider_and_model()`: Core provider selection + model picking logic.

    Shared by ``cmd_model`` (``hermes model``) and t
- `cmd_login()`: Authenticate Hermes CLI with a provider.
- `cmd_logout()`: Clear provider authentication.
- `cmd_auth()`: Manage pooled credentials.
- `cmd_status()`: Show status of all components.
- `cmd_cron()`: Cron job management.
- `cmd_webhook()`: Webhook subscription management.
- ... 还有 32 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## managed_scope.py

**路径**: `hermes_cli\managed_scope.py`
**行数**: 215

### 功能描述

Managed scope — IT-pushed, user-immutable config & env layer.

A system-level directory (default ``/etc/hermes``, root-owned and not
user-writable) supplies ``config.yaml`` and ``.env`` values that WIN over the
user's ``~/.hermes/config.yaml`` and ``~/.hermes/.env`` on a per-leaf-key basis.

This is

### 核心函数

- `get_managed_dir()`: Resolve the managed-scope directory, or None when no scope is present.

    Resolution (highest prio
- `invalidate_managed_cache()`: Drop cached managed config/env. For tests and post-edit reloads.
- `load_managed_config()`: Parsed managed config.yaml, or {} when absent/malformed (fail-open).
- `load_managed_env()`: Parsed managed .env (KEY=VALUE), or {} when absent (fail-open).
- `apply_managed_overlay()`: Overlay administrator-pinned config values on top of an already-built dict.

    The single, shared 
- `managed_config_keys()`: Dotted leaf keys pinned by the managed config (e.g. {'model.default'}).
- `is_key_managed()`: True if the exact dotted config key is pinned by the managed layer.
- `is_env_managed()`: True if the env var name is pinned by the managed .env layer.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## managed_uv.py

**路径**: `hermes_cli\managed_uv.py`
**行数**: 254

### 功能描述

Managed uv — one path, no guessing.

Hermes owns its own uv binary at ``$HERMES_HOME/bin/uv`` (or ``uv.exe`` on
Windows).  Every code path that needs uv resolves it from that single location.
If the binary is missing, ``ensure_uv()`` bootstraps it via the official
standalone installer with ``UV_UNMA

### 核心类

- `_UvResult`: ``ensure_uv()`` return value that survives an update boundary.

    ``ensure_uv()``'s arity has flip

### 核心函数

- `managed_uv_path()`: Return the path where Hermes keeps *its* uv binary.

    ``$HERMES_HOME/bin/uv`` on POSIX, ``$HERMES
- `resolve_uv()`: Return the managed uv path if it exists, else ``None``.

    No side effects — pure lookup.
- `ensure_uv()`: Return the managed uv path, installing it first if necessary.

    On **POSIX** the result is a :cla
- `update_managed_uv()`: Run ``uv self update`` on the managed uv binary.

    Call this during ``hermes update`` so the mana
- `rebuild_venv()`: True

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## mcp_catalog.py

**路径**: `hermes_cli\mcp_catalog.py`
**行数**: 779

### 功能描述

MCP catalog — curated, Nous-approved MCP servers shipped with the repo.

Mirrors the optional-skills/ pattern: each catalog entry lives under
``optional-mcps/<name>/manifest.yaml`` and ships disabled. Users discover
entries via ``hermes mcp catalog`` or the interactive ``hermes mcp picker``,
and ins

### 核心类

- `EnvVarSpec`
- `AuthSpec`
- `TransportSpec`
- `InstallSpec`: Optional bootstrap step (git clone + dep install).

    Omit for one-shot launchable servers (npx, u
- `ToolsSpec`: Manifest-side tool-selection hints.

    Drives the pre-checked state of the install-time tool check
- `CatalogEntry`
- `CatalogError`: Manifest parse/validation failure or install error.

### 核心函数

- `list_catalog()`: Return all valid catalog entries, sorted by name.

    Invalid manifests are skipped silently (CI te
- `catalog_diagnostics()`: Diagnostics from the most recent :func:`list_catalog` call.

    Returns a list of ``(entry_name, ki
- `get_entry()`: Look up a single entry by name. ``official/<name>`` prefix accepted.
- `installed_servers()`: Return current ``mcp_servers`` block from config.yaml.
- `is_installed()`
- `is_enabled()`
- `install_entry()`: Install a catalog entry end-to-end.

    Steps:
        1. If ``install.type == git``, clone + run b
- `uninstall_entry()`: Remove a catalog-installed MCP from config and (optionally) wipe its
    clone directory. Returns Tr

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## mcp_config.py

**路径**: `hermes_cli\mcp_config.py`
**行数**: 978

### 功能描述

MCP Server Management CLI — ``hermes mcp`` subcommand.

Implements ``hermes mcp add/remove/list/test/configure`` for interactive
MCP server lifecycle management (issue #690 Phase 2).

Relies on tools/mcp_tool.py for connection/discovery and keeps
configuration in ~/.hermes/config.yaml under the ``mc

### 核心函数

- `cmd_mcp_add()`: Add a new MCP server with discovery-first tool selection.
- `cmd_mcp_remove()`: Remove an MCP server from config.
- `cmd_mcp_list()`: List all configured MCP servers.
- `cmd_mcp_test()`: Test connection to an MCP server.
- `cmd_mcp_login()`: Force re-authentication for an OAuth-based MCP server.

    Deletes cached tokens (both on disk and 
- `cmd_mcp_reauth()`: Re-authenticate one OAuth MCP server, or all of them sequentially.

    ``hermes mcp reauth <name>``
- `cmd_mcp_configure()`: Reconfigure which tools are enabled for an existing MCP server.
- `mcp_command()`: Main dispatcher for ``hermes mcp`` subcommands.

### 依赖关系

**依赖组件**: entry-points, state-management, tool-system
**跨组件调用**: 是

---

## mcp_picker.py

**路径**: `hermes_cli\mcp_picker.py`
**行数**: 323

### 功能描述

MCP picker — interactive `hermes mcp picker` (also the default `hermes mcp`).

Lists every catalog entry plus any custom MCP servers the user has added via
``hermes mcp add``, lets them pick one, and routes to install / enable /
disable / uninstall / configure-tools flows.

Mirrors the `hermes plugi

### 核心类

- `_Row`: A row in the picker. ``entry`` is set for catalog rows; for custom
    user-added MCPs only ``name``

### 核心函数

- `show_catalog()`: `hermes mcp catalog` — print the curated list + custom servers, no interaction.
- `run_picker()`: `hermes mcp picker` (and default `hermes mcp`) — interactive selector.

    Loops until the user hit
- `install_by_name()`: `hermes mcp install <name>` — non-interactive entry-point.

    Returns 0 on success, non-zero on fa

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## mcp_security.py

**路径**: `hermes_cli\mcp_security.py`
**行数**: 182

### 功能描述

Security checks for user-configured MCP server entries.

MCP stdio transports intentionally support arbitrary local commands so users can
run custom servers. This module does not try to sandbox that capability. It
blocks two high-signal abuse shapes seen in the wild:

1. The exfiltration shape from 

### 核心函数

- `validate_mcp_server_entry()`: Return security warnings for an MCP server entry.

    Empty return means the entry is not suspiciou
- `is_mcp_server_entry_suspicious()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## mcp_startup.py

**路径**: `hermes_cli\mcp_startup.py`
**行数**: 89

### 功能描述

Shared CLI/TUI-safe helpers for background MCP discovery.

### 核心函数

- `start_background_mcp_discovery()`: Spawn one shared background MCP discovery thread for this process.
- `wait_for_mcp_discovery()`: Wait for background MCP discovery before the first tool snapshot.

    ``thread.join(timeout)`` retu

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

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

**依赖组件**: state-management
**跨组件调用**: 是

---

## middleware.py

**路径**: `hermes_cli\middleware.py`
**行数**: 314

### 功能描述

Hermes middleware contract helpers.

Observer hooks report what happened. Middleware can change what happens by
rewriting a request or wrapping the actual execution callback. Keep the small
contract helpers here so agent-loop call sites and plugins share one vocabulary.

### 核心类

- `RequestMiddlewareResult`: Result of applying request middleware to a mutable payload.

### 核心函数

- `observer_payload()`
- `middleware_payload()`
- `apply_llm_request_middleware()`: Apply registered LLM request middleware.

    Middleware may return ``{"request": {...}}`` to replac
- `apply_tool_request_middleware()`: Apply registered tool request middleware.

    Middleware may return ``{"args": {...}}`` to replace 
- `apply_api_request_middleware()`: Compatibility wrapper for older ``api_request`` naming.
- `run_llm_execution_middleware()`: Run provider execution through registered LLM execution middleware.
- `run_tool_execution_middleware()`: Run tool execution through registered tool execution middleware.
- `run_api_execution_middleware()`: Compatibility wrapper for older ``api_execution`` naming.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## migrate.py

**路径**: `hermes_cli\migrate.py`
**行数**: 116

### 功能描述

CLI handlers for ``hermes migrate ...``.

Currently exposes only ``hermes migrate xai`` — diagnoses and (with --apply)
rewrites references to xAI models retired on May 15, 2026.

### 核心函数

- `cmd_migrate()`: Dispatcher for ``hermes migrate <subtype>``.
- `cmd_migrate_xai()`: Run xAI May-15 model migration in dry-run or apply mode.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## moa_cmd.py

**路径**: `hermes_cli\moa_cmd.py`
**行数**: 136

### 功能描述

CLI helpers for configuring Mixture of Agents.

### 核心函数

- `cmd_moa()`: Manage Mixture of Agents model presets.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## moa_config.py

**路径**: `hermes_cli\moa_config.py`
**行数**: 175

### 功能描述

Mixture-of-Agents configuration and slash-command helpers.

### 核心函数

- `normalize_moa_config()`: Return validated MoA config with named presets.

    Backward compatible with the first PR shape whe
- `list_moa_presets()`
- `resolve_moa_preset()`
- `exact_moa_preset_name()`
- `set_active_moa_preset()`
- `encode_moa_turn()`: Encode a /moa one-shot turn for frontends that can only send text.
- `decode_moa_turn()`: Decode a hidden /moa one-shot marker.
- `build_moa_turn_prompt()`: Build the hidden one-shot payload used by TUI/gateway routing.
- `moa_usage()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## model_catalog.py

**路径**: `hermes_cli\model_catalog.py`
**行数**: 395

### 功能描述

Remote model catalog fetcher.

The Hermes docs site hosts a JSON manifest of curated models for providers
we want to update without shipping a release (currently OpenRouter and
Nous Portal). This module fetches, validates, and caches that manifest,
falling back to the in-repo hardcoded lists when th

### 核心函数

- `get_catalog()`: Return the parsed model catalog manifest, or an empty dict on failure.

    Callers should treat a m
- `get_curated_openrouter_models()`: Return OpenRouter's curated ``[(id, description), ...]`` from the manifest.

    Returns ``None`` wh
- `get_curated_nous_models()`: Return Nous Portal's curated list of model ids from the manifest.

    Returns ``None`` when the man
- `seed_cache_from_checkout()`: Overwrite the disk cache with the catalog shipped in a local checkout.

    ``hermes update`` pulls 
- `reset_cache()`: Clear the in-process cache. Used by tests and ``hermes model --refresh``.

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## model_cost_guard.py

**路径**: `hermes_cli\model_cost_guard.py`
**行数**: 135

### 功能描述

Expensive-model confirmation helpers for model selection surfaces.

### 核心类

- `ExpensiveModelWarning`: Confirmation payload for models above Hermes' cost guardrail.

### 核心函数

- `expensive_model_warning()`: Return a warning payload when known pricing exceeds safety thresholds.

    The guard only triggers 

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## model_normalize.py

**路径**: `hermes_cli\model_normalize.py`
**行数**: 474

### 功能描述

Per-provider model name normalization.

Different LLM providers expect model identifiers in different formats:

- **Aggregators** (OpenRouter, Nous, AI Gateway, Kilo Code) need
  ``vendor/model`` slugs like ``anthropic/claude-sonnet-4.6``.
- **Anthropic** native API expects bare names with dots repl

### 核心函数

- `detect_vendor()`: Detect the vendor slug from a bare model name.

    Uses the first hyphen-delimited token of the mod
- `normalize_model_for_provider()`: Translate a model name into the format the target provider's API expects.

    This is the primary e

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## model_setup_flows.py

**路径**: `hermes_cli\model_setup_flows.py`
**行数**: 2732

### 功能描述

Per-provider model-selection wizard flows for ``hermes setup`` / ``hermes model``.

Extracted from ``hermes_cli/main.py`` as part of the god-file decomposition
campaign (``~/.hermes/plans/god-file-decomposition.md``, Phase 2 — splitting
main.py handler/flow bodies out of the module). These 18 ``_mod

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, llm-client, state-management
**跨组件调用**: 是

---

## model_switch.py

**路径**: `hermes_cli\model_switch.py`
**行数**: 2320

### 功能描述

Shared model-switching logic for CLI and gateway /model commands.

Both the CLI (cli.py) and gateway (gateway/run.py) /model handlers
share the same core pipeline:

  parse flags -> alias resolution -> provider resolution ->
  credential resolution -> normalize model name ->
  metadata lookup -> bui

### 核心类

- `ModelIdentity`: Vendor slug and family prefix used for catalog resolution.
- `DirectAlias`: Exact model mapping that bypasses catalog resolution.
- `ModelSwitchResult`: Result of a model switch attempt.

### 核心函数

- `is_nous_hermes_non_agentic()`: Return True if *model_name* is a real Nous Hermes 3/4 chat model.

    Used to decide whether to sur
- `parse_model_flags()`: Parse --provider, --global, --session, and --refresh flags from /model command args.

    Returns ``
- `resolve_persist_behavior()`: Decide whether a ``/model`` switch should persist to ``config.yaml``.

    Resolution order:

    1.
- `resolve_alias()`: Resolve a short alias against the current provider's catalog.

    Looks up *raw_input* in :data:`MO
- `get_authenticated_provider_slugs()`: Return slugs of providers that have credentials.

    Uses ``list_authenticated_providers()`` which 
- `resolve_display_context_length()`: Resolve the context length to show in /model output.

    models.dev reports per-vendor context (e.g
- `switch_model()`: Core model-switching pipeline shared between CLI and gateway.

    Resolution chain:

      If --pro
- `prewarm_picker_cache_async()`: Warm the provider-models disk cache in a background daemon thread.

    The no-args ``/model`` picke
- `list_authenticated_providers()`: Detect which providers have credentials and list their curated models.

    Uses the curated model l
- `list_picker_providers()`: Interactive-picker variant of :func:`list_authenticated_providers`.

    Post-processes the base lis

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, llm-client, state-management
**跨组件调用**: 是

---

## models.py

**路径**: `hermes_cli\models.py`
**行数**: 4172

### 功能描述

Canonical model catalogs and lightweight validation helpers.

Add, remove, or reorder entries here — both `hermes setup` and
`hermes` provider-selection will pick up the change automatically.

### 核心类

- `ProviderEntry`

### 核心函数

- `is_nous_free_tier()`: Return True if the account info indicates a free (unpaid) tier.

    Prefer the Portal's explicit ``
- `partition_nous_models_by_tier()`: Split Nous models into (selectable, unavailable) based on user tier.

    For paid-tier users: all m
- `union_with_portal_free_recommendations()`: Augment curated list + pricing with the Portal's ``freeRecommendedModels``.

    The Portal's ``/api
- `union_with_portal_paid_recommendations()`: Augment curated list with the Portal's ``paidRecommendedModels``.

    Mirror of :func:`union_with_p
- `check_nous_free_tier()`: Check if the current Nous Portal user is on a free (unpaid) tier.

    Results are cached for ``_FRE
- `fetch_nous_recommended_models()`: Fetch the Nous Portal's curated recommended-models payload.

    Hits ``<portal>/api/nous/recommende
- `get_nous_recommended_aux_model()`: Return the Portal's recommended model name for an auxiliary task.

    Picks the best field from the
- `provider_group_for_slug()`: Return the group_id a provider slug belongs to, or "" if ungrouped.
- `group_providers()`: Fold a flat ordered slug iterable into picker rows by provider group.

    DISPLAY ONLY. Used by eve
- `get_default_model_for_provider()`: Return a cost-safe default model for a provider, or "" if unknown.

    Used as a NON-INTERACTIVE fa
- `fetch_openrouter_models()`: Return the curated OpenRouter picker list, refreshed from the live catalog when possible.
- `model_ids()`: Return just the OpenRouter model-id strings.
- `get_curated_nous_model_ids()`: Return the curated Nous Portal model-id list.

    Prefers the remotely-hosted catalog manifest (pub
- `fetch_models_with_pricing()`: Fetch ``/v1/models`` and return ``{model_id: {prompt, completion}}`` pricing.

    Results are cache
- `get_pricing_for_provider()`: Return live pricing for providers that support it (openrouter, nous, novita).
- ... 还有 29 个函数

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, llm-client, state-management
**跨组件调用**: 是

---

## nous_account.py

**路径**: `hermes_cli\nous_account.py`
**行数**: 790

### 功能描述

Normalized Nous Portal account entitlement helpers.

### 核心类

- `NousPortalSubscriptionInfo`
- `NousPaidServiceAccessInfo`
- `NousToolAccessInfo`: Free tool-pool entitlement, decoupled from paid/billing access.

    Mirrors the Portal's ``tool_acc
- `NousPortalAccountInfo`

### 核心函数

- `nous_portal_billing_url()`: Return the billing URL for a normalized Nous account snapshot.
- `nous_portal_topup_url()`: Return the portal top-up URL that auto-opens the top-up modal.

    Prefers the org-pinned page ``{b
- `format_nous_portal_entitlement_message()`: Return user-facing guidance for a missing Nous tool-gateway entitlement.

    ``None`` means the acc
- `reset_nous_portal_account_info_cache()`: Clear the short-lived account-info cache used by tests.
- `get_nous_portal_account_info()`: Return normalized Nous Portal account entitlement information.

    By default, a valid unexpired OA

### 依赖关系

**依赖组件**: acp-adapter, state-management
**跨组件调用**: 是

---

## nous_auth_keepalive.py

**路径**: `hermes_cli\nous_auth_keepalive.py`
**行数**: 190

### 功能描述

Background keepalive for long-lived Nous Portal sessions.

### 核心函数

- `refresh_nous_auth_keepalive_once()`: Refresh Nous auth once if credentials are configured.
- `start_nous_auth_keepalive()`: Start the process-wide Nous auth keepalive thread.
- `stop_nous_auth_keepalive()`: Stop the keepalive thread. Intended for graceful shutdown/tests.

### 依赖关系

**依赖组件**: acp-adapter, state-management
**跨组件调用**: 是

---

## nous_billing.py

**路径**: `hermes_cli\nous_billing.py`
**行数**: 407

### 功能描述

Nous Portal terminal-billing HTTP client (Phase 2b).

Thin, fail-loud client for the four ``/api/billing/*`` endpoints the terminal
billing screens drive. Companion to ``hermes_cli/nous_account.py`` (which owns
read-only entitlement/balance) — this module owns the *write* side: buy credits,
poll a c

### 核心类

- `BillingError`: A billing HTTP call failed.

    Carries everything a surface needs to render the right message + af
- `BillingScopeRequired`: ``403 insufficient_scope`` — the held token lacks ``billing:manage``.

    The lazy step-up trigger:
- `BillingRateLimited`: ``429 rate_limited`` or ``503 temporarily_unavailable``.

    NOT a payment failure. Carries ``retry
- `BillingAuthError`: ``401`` — missing/invalid bearer token (not logged in / expired).

### 核心函数

- `resolve_portal_base_url()`: Resolve the portal base URL with login-time precedence.

    ``HERMES_PORTAL_BASE_URL`` → ``NOUS_POR
- `get_billing_state()`: ``GET /api/billing/state`` — role-tiered overview (no scope required).
- `patch_auto_top_up()`: ``PATCH /api/billing/auto-top-up`` — configure auto-reload (scope required).

    Body is strict ser
- `post_charge()`: ``POST /api/billing/charge`` — buy credits (scope required).

    ``Idempotency-Key`` header is MAND
- `get_charge_status()`: ``GET /api/billing/charge/{id}`` — poll a charge (scope required).

    Returns ``{status: "pending"

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## nous_subscription.py

**路径**: `hermes_cli\nous_subscription.py`
**行数**: 1286

### 功能描述

Helpers for Nous subscription managed-tool capabilities.

### 核心类

- `NousFeatureState`
- `NousSubscriptionFeatures`

### 核心函数

- `get_nous_subscription_features()`
- `apply_nous_managed_defaults()`
- `get_gateway_eligible_tools()`: Return (unconfigured, has_direct, already_managed) tool key lists.

    - unconfigured: tools with n
- `apply_gateway_defaults()`: Apply Tool Gateway config for the given tool keys.

    Sets ``use_gateway: true`` in each tool's co
- `prompt_enable_tool_gateway()`: If eligible tools exist, prompt the user (per tool) to enable the Tool
    Gateway.

    "Pool enabl
- `ensure_nous_portal_access()`: Make sure the user is entitled to the Nous Tool Gateway, logging in if
    needed.

    Used by ``he

### 依赖关系

**依赖组件**: acp-adapter, entry-points, state-management, tool-system
**跨组件调用**: 是

---

## oneshot.py

**路径**: `hermes_cli\oneshot.py`
**行数**: 382

### 功能描述

Oneshot (-z) mode: send a prompt, get the final content block, exit.

Bypasses cli.py entirely.  No banner, no spinner, no session_id line,
no stderr chatter.  Just the agent's final text to stdout.

Toolsets = explicit --toolsets when provided, otherwise whatever the user has
configured for "cli" i

### 核心函数

- `run_oneshot()`: Execute a single prompt and print only the final content block.

    Args:
        prompt: The user 

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## pairing.py

**路径**: `hermes_cli\pairing.py`
**行数**: 116

### 功能描述

CLI commands for the DM pairing system.

Usage:
    hermes pairing list              # Show all pending + approved users
    hermes pairing approve <platform> <code>  # Approve a pairing code
    hermes pairing revoke <platform> <user_id> # Revoke user access
    hermes pairing clear-pending     # C

### 核心函数

- `pairing_command()`: Handle hermes pairing subcommands.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## partial_compress.py

**路径**: `hermes_cli\partial_compress.py`
**行数**: 236

### 功能描述

Boundary-aware partial compression — "summarize up to here".

Inspired by Claude Code's Rewind menu "Summarize up to here" action
(v2.1.139–v2.1.142, Week 20, May 2026):
https://code.claude.com/docs/en/whats-new/2026-w20

Hermes already has ``/compress`` (full-history compaction) and an
automatic to

### 核心函数

- `parse_partial_compress_args()`: Parse the argument string after ``/compress``.

    Recognizes the boundary-aware forms:

    * ``he
- `split_history_for_partial_compress()`: Split ``history`` into ``(head, tail)`` for partial compression.

    ``head`` is the earlier portio
- `rejoin_compressed_head_and_tail()`: Concatenate a compressed head with the verbatim tail, defending
    the seam against an illegal user

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pets.py

**路径**: `hermes_cli\pets.py`
**行数**: 503

### 功能描述

CLI subcommand: ``hermes pets <subcommand>``.

Thin shell around :mod:`agent.pet`.  Browses the public petdex gallery,
installs pets into the profile's ``pets/`` directory, selects the active
mascot (writes ``display.pet.*`` to config.yaml), and runs a doctor check.

No side effects at import time —

### 核心函数

- `set_pet_scale()`: Set ``display.pet.scale`` (clamped to bounds). Returns ``(applied, error)``.

    The single write p
- `toggle_pet_display()`: Toggle ``display.pet.enabled``.

    Returns ``(enabled, display_name, error_message)``. *error_mess
- `print_pet_gallery()`: Print a slice of the public petdex gallery (CLI/TUI text fallback).
- `register_cli()`: Attach ``pets`` subcommands to *parent* (called by main.py).

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## platforms.py

**路径**: `hermes_cli\platforms.py`
**行数**: 85

### 功能描述

Shared platform registry for Hermes Agent.

Single source of truth for platform metadata consumed by both
skills_config (label display) and tools_config (default toolset
resolution).  Import ``PLATFORMS`` from here instead of maintaining
duplicate dicts in each module.

### 核心类

- `PlatformInfo`: Metadata for a single platform entry.

### 核心函数

- `platform_label()`: Return the display label for a platform key, or *default*.

    Checks the static PLATFORMS dict fir
- `get_all_platforms()`: Return PLATFORMS merged with any plugin-registered platforms.

    Plugin platforms are appended aft

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## plugins.py

**路径**: `hermes_cli\plugins.py`
**行数**: 2094

### 功能描述

Hermes Plugin System
====================

Discovers, loads, and manages plugins from four sources:

1. **Bundled plugins** – ``<repo>/plugins/<name>/`` (shipped with hermes-agent;
   ``memory/`` and ``context_engine/`` subdirs are excluded — they have their
   own discovery paths)
2. **User plugins

### 核心类

- `PluginManifest`: Parsed representation of a plugin.yaml manifest.
- `LoadedPlugin`: Runtime state for a single loaded plugin.
- `PluginContext`: Facade given to plugins so they can register tools and hooks.
- `PluginManager`: Central manager that discovers, loads, and invokes plugins.

### 核心函数

- `get_bundled_plugins_dir()`: Locate the bundled ``plugins/`` directory.

    Honours ``HERMES_BUNDLED_PLUGINS`` (set by the Nix w
- `get_plugin_manager()`: Return (and lazily create) the global PluginManager singleton.
- `discover_plugins()`: Discover and load all plugins.

    Default behavior is idempotent. Pass ``force=True`` to rescan pl
- `invoke_hook()`: Call all registered callbacks for *hook_name*.

        Each callback is wrapped in its own try/exce
- `invoke_middleware()`: Call registered middleware callbacks for *kind*.

        Each callback is isolated so one plugin ca
- `has_middleware()`: Return True when at least one callback is registered for middleware.
- `has_hook()`: Return True when at least one callback is registered for a hook.
- `set_thread_tool_whitelist()`
- `clear_thread_tool_whitelist()`
- `get_pre_tool_call_block_message()`: Check ``pre_tool_call`` hooks for a blocking directive.

    Plugins that need to enforce policy (ra
- `get_plugin_context_engine()`: Return the plugin-registered context engine, or None.
- `get_plugin_command_handler()`: Return the handler for a plugin-registered slash command, or ``None``.
- `resolve_plugin_command_result()`: Resolve a plugin command return value, awaiting async handlers when needed.

    Sync CLI/TUI dispat
- `get_plugin_commands()`: Return the full plugin commands dict (name → {handler, description, plugin}).

    Triggers idempote
- `get_plugin_auxiliary_tasks()`: Return all plugin-registered auxiliary tasks as a stable-ordered list.

    Each entry is the regist
- ... 还有 1 个函数

### 依赖关系

**依赖组件**: agent-engine, entry-points, gateway, state-management
**跨组件调用**: 是

---

## plugins_cmd.py

**路径**: `hermes_cli\plugins_cmd.py`
**行数**: 1836

### 功能描述

``hermes plugins`` CLI subcommand — install, update, remove, and list plugins.

Plugins are installed from Git repositories into ``~/.hermes/plugins/``.
Supports full URLs and ``owner/repo`` shorthand (resolves to GitHub).

After install, if the plugin ships an ``after-install.md`` file it is
render

### 核心类

- `PluginOperationError`: Recoverable plugin install/update failure (CLI exits; HTTP maps to 4xx).

### 核心函数

- `cmd_install()`: Install a plugin from a Git URL or owner/repo shorthand.

    After install, prompt "Enable now? [y/
- `cmd_update()`: Update an installed plugin by pulling latest from its git remote.
- `cmd_remove()`: Remove an installed plugin by name.
- `cmd_enable()`: Add a plugin to the enabled allow-list (and remove it from disabled).
- `cmd_disable()`: Remove a plugin from the enabled allow-list (and add to disabled).
- `cmd_list()`: List all plugins (bundled + user) with enabled/disabled state.
- `cmd_toggle()`: Interactive composite UI — general plugins + provider plugin categories.
- `dashboard_install_plugin()`: Non-interactive install for the web dashboard. Returns a JSON-serializable dict.
- `dashboard_set_agent_plugin_enabled()`: Enable or disable a plugin in ``config.yaml`` (runtime allow/deny lists).

    For plugins that prov
- `dashboard_update_user_plugin()`: ``git pull`` inside ``~/.hermes/plugins/<name>``.
- `dashboard_remove_user_plugin()`: Delete a plugin tree under ``~/.hermes/plugins/`` only.
- `plugins_command()`: Dispatch hermes plugins subcommands.

### 依赖关系

**依赖组件**: agent-engine, state-management
**跨组件调用**: 是

---

## portal_cli.py

**路径**: `hermes_cli\portal_cli.py`
**行数**: 246

### 功能描述

``hermes portal`` — the human-readable entry point for Nous Portal.

Running ``hermes portal`` with no subcommand performs the one-shot Portal
onboarding: OAuth login, pick a Nous model, switch the inference provider to
Nous, and offer to enable the Tool Gateway. It is the friendly alias for
``herme

### 核心函数

- `portal_command()`: Top-level dispatch for `hermes portal <subcommand>`.
- `add_parser()`: Register `hermes portal` on the given argparse subparsers object.

### 依赖关系

**依赖组件**: acp-adapter, entry-points
**跨组件调用**: 是

---

## profile_describer.py

**路径**: `hermes_cli\profile_describer.py`
**行数**: 299

### 功能描述

Profile describer — auto-generate ``description`` for a profile.

Used by ``hermes profile describe <name> --auto`` and the dashboard's
"auto-generate description" button. Reads the profile's installed
skills, model+provider, name, and optionally a small slice of memory,
then asks the auxiliary LLM 

### 核心类

- `DescribeOutcome`: Result of describing a single profile.

### 核心函数

- `describe_profile()`: Auto-generate a description for one profile.

    Returns an outcome describing what happened. Never
- `list_describable_profiles()`: Return profile names that can be described.

    ``missing_only=True`` (default) returns only profil

### 依赖关系

**依赖组件**: agent-engine, llm-client, state-management
**跨组件调用**: 是

---

## profile_distribution.py

**路径**: `hermes_cli\profile_distribution.py`
**行数**: 727

### 功能描述

Profile distributions — shareable, packaged Hermes profiles via git.

A distribution is a Hermes profile published as a git repository (or
installed from a local directory for development). Install with one command
from a git URL, update in place, and keep your local memories / sessions /
credential

### 核心类

- `DistributionError`: Raised for distribution install/update failures.
- `EnvRequirement`
- `DistributionManifest`
- `InstallPlan`: Summary of what an install will do, surfaced for user confirmation.

### 核心函数

- `read_manifest()`: Return the manifest for *profile_dir*, or None if it isn't a distribution.
- `write_manifest()`
- `check_hermes_requires()`: Raise DistributionError if ``current_version`` does not satisfy ``spec``.

    ``spec`` accepts a si
- `plan_install()`: Stage *source* and produce a plan describing what install would do.
- `install_distribution()`: Install a distribution from *source* into a new profile.

    Returns the resolved :class:`InstallPl
- `update_distribution()`: Re-pull the distribution for an existing profile and apply updates.

    The source is read from the
- `describe_distribution()`: Return a structured view of a profile's distribution metadata.

    Returns an empty dict if the pro

### 依赖关系

**依赖组件**: agent-engine
**跨组件调用**: 是

---

## profiles.py

**路径**: `hermes_cli\profiles.py`
**行数**: 1883

### 功能描述

Profile management for multiple isolated Hermes instances.

Each profile is a fully independent HERMES_HOME directory with its own
config.yaml, .env, memory, sessions, skills, gateway, cron, and logs.
Profiles live under ``~/.hermes/profiles/<name>/`` by default.

The "default" profile is ``~/.herme

### 核心类

- `ProfileInfo`: Summary information about a profile.

### 核心函数

- `has_bundled_skills_opt_out()`: Return True if the profile opted out of bundled-skill seeding.
- `normalize_profile_name()`: Return the canonical profile id used on disk and in CLI ``-p`` argv.

    Named profiles are stored 
- `validate_profile_name()`: Raise ``ValueError`` if *name* is not a valid profile identifier.

    Validates the input as-given 
- `get_profile_dir()`: Resolve a profile name to its HERMES_HOME directory.
- `profile_exists()`: Check whether a profile directory exists.
- `check_alias_collision()`: Return a human-readable collision message, or None if the name is safe.

    Checks: reserved names,
- `create_wrapper_script()`: Create a shell wrapper script at ~/.local/bin/<name>.

    The wrapper file is named after ``name`` 
- `remove_wrapper_script()`: Remove the wrapper script for a profile. Returns True if removed.
- `find_alias_for_profile()`: Return the alias name of the wrapper that activates *profile_name*, or None.

    A wrapper created 
- `read_profile_meta()`: Read ``<profile_dir>/profile.yaml`` and return a dict.

    Returns ``{"description": "", "descripti
- `write_profile_meta()`: Update ``<profile_dir>/profile.yaml`` in place.

    Only the explicitly passed fields are overwritt
- `list_profiles()`: Return info for all profiles, including the default.
- `profiles_to_serve()`: Return the ``(profile_name, hermes_home)`` pairs a gateway should serve.

    This is the single cho
- `create_profile()`: Create a new profile directory.

    Parameters
    ----------
    name:
        Profile identifier 
- `seed_profile_skills()`: Seed bundled skills into a profile via subprocess.

    Uses subprocess because sync_skills() caches
- ... 还有 9 个函数

### 依赖关系

**依赖组件**: agent-engine, state-management
**跨组件调用**: 是

---

## projects_cmd.py

**路径**: `hermes_cli\projects_cmd.py`
**行数**: 336

### 功能描述

``hermes project`` CLI — manage first-class, multi-folder Projects.

A Project is a human-named workspace spanning one or more folders, with one
designated primary repo. Projects anchor desktop session grouping and (when
bound to a kanban board) give kanban tasks a deterministic worktree + branch
co

### 核心函数

- `build_parser()`: Attach the ``project`` subcommand tree. Returns the top parser.
- `projects_command()`: Entry point from ``hermes project …`` argparse dispatch.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## projects_db.py

**路径**: `hermes_cli\projects_db.py`
**行数**: 728

### 功能描述

Per-profile first-class Project store.

A **Project** is a human-named, multi-folder workspace. Unlike the desktop's
old inferred "workspaces" (derived from each session's ``cwd`` + a git probe)
and unlike kanban's self-generated worktrees, a Project is an explicit,
persisted entity the user creates

### 核心类

- `ProjectFolder`
- `Project`

### 核心函数

- `projects_db_path()`: The per-profile projects DB path (``$HERMES_HOME/projects.db``).

    Profile-aware: ``get_hermes_ho
- `normalize_slug()`: Lowercase + strip a slug; validate; return ``None`` for empty.
- `connect()`: Open (and initialize if needed) the per-profile projects DB.

    WAL with DELETE fallback for netwo
- `connect_closing()`: Open a projects DB connection and guarantee it is closed on exit.

    sqlite3's connection context 
- `create_project()`: Create a project and return its id.

    ``folders`` are normalized to absolute paths. If ``primary_
- `list_projects()`
- `get_project()`: Look up a project by id first, then by slug.
- `update_project()`: Patch top-level project fields. Only provided fields change.

    ``icon``, ``color``, and ``board_s
- `add_folder()`: Add a folder to a project. Returns the normalized path.

    When ``is_primary`` is set, the folder 
- `remove_folder()`: Remove a folder from a project. Repoints primary if it was primary.
- `set_primary()`
- `archive_project()`
- `restore_project()`
- `delete_project()`: Hard-delete a project and its folders (cascade).
- `set_active()`: Set (or clear, when ``None``) the active project pointer.
- ... 还有 5 个函数

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## prompt_size.py

**路径**: `hermes_cli\prompt_size.py`
**行数**: 154

### 功能描述

Prompt-size diagnostic: ``hermes prompt-size``.

Reports a byte/char breakdown of the system prompt the agent would build for
a fresh session — system prompt total, the ``<available_skills>`` index,
memory + user profile, and tool-schema JSON. Lets users see where their fixed
prompt budget goes (iss

### 核心函数

- `compute_prompt_breakdown()`: Return a dict of prompt-size measurements for a fresh session.

    Keys: ``system_prompt`` (chars/b
- `render_breakdown()`: Render the breakdown as plain text suitable for a terminal.
- `cmd_prompt_size()`: Entry point for ``hermes prompt-size``.

### 依赖关系

**依赖组件**: agent-engine, entry-points
**跨组件调用**: 是

---

## provider_catalog.py

**路径**: `hermes_cli\provider_catalog.py`
**行数**: 182

### 功能描述

Unified provider catalog — one source of truth for the provider universe.

The provider list shown by ``hermes model`` (CLI/TUI) and the desktop Settings
→ Providers tabs (Accounts + API keys) **must be the same set**.  Historically
they were not: the CLI picker read :data:`hermes_cli.models.CANONIC

### 核心类

- `ProviderDescriptor`: One provider, as seen by every surface (CLI picker + both GUI tabs).

### 核心函数

- `tab_for_auth_type()`: Return the desktop tab ("keys"|"accounts") a provider's auth maps to.
- `provider_catalog()`: Return one descriptor per provider in the ``hermes model`` universe.

    Membership is :data:`CANON
- `provider_catalog_by_slug()`: Convenience: the catalog keyed by slug.

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## providers.py

**路径**: `hermes_cli\providers.py`
**行数**: 766

### 功能描述

Single source of truth for provider identity in Hermes Agent.

Two data sources, merged at runtime:

1. **models.dev catalog** — 109+ providers with base URLs, env vars, display
   names, and full model metadata (context, cost, capabilities).  This is
   the primary database.

2. **Hermes overlays**

### 核心类

- `HermesOverlay`: Hermes-specific provider metadata layered on top of models.dev.
- `ProviderDef`: Complete provider definition — merged from all sources.

### 核心函数

- `normalize_provider()`: Resolve aliases and normalise casing to a canonical provider id.

    Returns the canonical id strin
- `get_provider()`: Look up a built-in provider by id or alias.

    Resolution order:
      1. Hermes overlays (for pro
- `get_label()`: Get a human-readable display name for a provider.
- `is_aggregator()`: Return True when the provider is a multi-model aggregator.
- `is_routing_aggregator()`: Return True only for TRUE routing aggregators (e.g. OpenRouter, named
    ``custom:*`` proxies) — th
- `determine_api_mode()`: Determine the API mode (wire protocol) for a provider/endpoint.

    Resolution order:
      1. Know
- `resolve_user_provider()`: Resolve a provider from the user's config.yaml ``providers:`` section.

    Args:
        name: Prov
- `custom_provider_slug()`: Build a canonical slug for a custom_providers entry.

    Matches the convention used by runtime_pro
- `resolve_custom_provider()`: Resolve a provider from the user's config.yaml ``custom_providers`` list.
- `resolve_provider_full()`: Full resolution chain: built-in → models.dev → user config.

    This is the main entry point for --

### 依赖关系

**依赖组件**: agent-engine, entry-points
**跨组件调用**: 是

---

## __init__.py

**路径**: `hermes_cli\proxy\__init__.py`
**行数**: 21

### 功能描述

Local OpenAI-compatible proxy that forwards to OAuth-authenticated upstreams.

Lets external apps (OpenViking, Karakeep, Open WebUI, ...) ride the user's
already-logged-in provider subscription instead of needing a static API key
copy-pasted into each app's config.

The proxy listens on ``127.0.0.1:

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## __init__.py

**路径**: `hermes_cli\proxy\adapters\__init__.py`
**行数**: 38

### 功能描述

Upstream adapter registry for the local proxy server.

Each adapter wraps a provider's OAuth state and exposes a uniform interface
the proxy server can use to forward requests with a freshly-minted bearer
token. See :class:`UpstreamAdapter` for the contract.

### 核心函数

- `get_adapter()`: Instantiate an adapter by provider name.

    Raises:
        ValueError: if ``name`` is not a regis

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## base.py

**路径**: `hermes_cli\proxy\adapters\base.py`
**行数**: 109

### 功能描述

Abstract base for proxy upstream adapters.

An :class:`UpstreamAdapter` represents one OAuth-authenticated provider the
local proxy can forward requests to. The adapter is responsible for:

  - locating the user's auth state for that provider
  - refreshing/minting credentials when needed
  - report

### 核心类

- `UpstreamCredential`: A resolved bearer + base URL ready to forward to.
- `UpstreamAdapter`: Contract for an upstream provider the proxy can forward to.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## nous_portal.py

**路径**: `hermes_cli\proxy\adapters\nous_portal.py`
**行数**: 200

### 功能描述

Nous Portal upstream adapter.

Reads the user's Nous OAuth state from ``~/.hermes/auth.json`` through the
shared runtime resolver, validates or refreshes the inference JWT, then exposes
the upstream base URL plus bearer for the proxy server to forward to.

### 核心类

- `NousPortalAdapter`: Proxy upstream for the Nous Portal inference API.

### 依赖关系

**依赖组件**: acp-adapter, llm-client
**跨组件调用**: 是

---

## xai.py

**路径**: `hermes_cli\proxy\adapters\xai.py`
**行数**: 146

### 功能描述

xAI Grok OAuth upstream adapter.

### 核心类

- `XAIGrokAdapter`: Proxy upstream for xAI Grok via Hermes-managed OAuth credentials.

### 依赖关系

**依赖组件**: acp-adapter, llm-client, state-management
**跨组件调用**: 是

---

## cli.py

**路径**: `hermes_cli\proxy\cli.py`
**行数**: 143

### 功能描述

CLI handlers for the ``hermes proxy`` subcommand.

### 核心函数

- `cmd_proxy_start()`: Run the proxy server in the foreground.

    Returns process exit code (0 on clean shutdown).
- `cmd_proxy_status()`: Print the status of each configured upstream adapter.
- `cmd_proxy_list_providers()`: List available proxy upstream providers.
- `cmd_proxy()`: Dispatch ``hermes proxy <subcommand>``.

### 依赖关系

**依赖组件**: acp-adapter
**跨组件调用**: 是

---

## server.py

**路径**: `hermes_cli\proxy\server.py`
**行数**: 297

### 功能描述

HTTP server that forwards OpenAI-compatible requests to a configured upstream.

Listens on ``http://<host>:<port>/v1/<path>`` and forwards each request to
``<upstream-base-url>/<path>`` with the client's ``Authorization`` header
replaced by a freshly-resolved bearer from the configured adapter. The


### 核心函数

- `create_app()`: Build the aiohttp application bound to a specific upstream adapter.

### 依赖关系

**依赖组件**: gateway, llm-client
**跨组件调用**: 是

---

## psutil_android.py

**路径**: `hermes_cli\psutil_android.py`
**行数**: 109

### 功能描述

Helpers for the temporary psutil-on-Android compatibility installer.

### 核心类

- `PsutilAndroidInstallError`: Raised when the pinned psutil sdist is missing or unsafe.

### 核心函数

- `prepare_patched_psutil_sdist()`: Safely extract the pinned psutil sdist and patch it for Android.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pt_input_extras.py

**路径**: `hermes_cli\pt_input_extras.py`
**行数**: 121

### 功能描述

Augmentations to prompt_toolkit's input-parsing tables.

Imported once at CLI startup. Each helper installs a small mapping into
prompt_toolkit's `ANSI_SEQUENCES` so byte sequences emitted by modern
keyboard protocols (Kitty / xterm `modifyOtherKeys`) decode to existing
key tuples Hermes already bin

### 核心函数

- `install_shift_enter_alias()`: Map Shift+Enter byte sequences to the (Escape, ControlM) key tuple
    that Alt+Enter produces, so t
- `install_ctrl_enter_alias()`: Map Ctrl+Enter byte sequences to the (Escape, ControlM) key tuple
    that Alt+Enter produces, so th
- `install_ignored_terminal_sequences()`: Map terminal-emitted noise sequences to ``Keys.Ignore`` so they
    are consumed by the VT100 parser

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pty_bridge.py

**路径**: `hermes_cli\pty_bridge.py`
**行数**: 287

### 功能描述

PTY bridge for `hermes dashboard` chat tab.

Wraps a child process behind a pseudo-terminal so its ANSI output can be
streamed to a browser-side terminal emulator (xterm.js) and typed
keystrokes can be fed back in.  The only caller today is the
``/api/pty`` WebSocket endpoint in ``hermes_cli.web_ser

### 核心类

- `PtyUnavailableError`: Raised when a PTY cannot be created on this platform.

    Today this means native Windows (no ConPT
- `PtyBridge`: Thin wrapper around ``ptyprocess.PtyProcess`` for byte streaming.

    Not thread-safe.  A single br

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## relaunch.py

**路径**: `hermes_cli\relaunch.py`
**行数**: 205

### 功能描述

Unified self-relaunch for Hermes CLI.

Preserves critical flags (--tui, --dev, --profile, --model, etc.) across
process replacement so that ``hermes sessions browse`` or post-setup relaunch
doesn't silently drop the user's UI mode or other preferences.

Also works when ``hermes`` is not on PATH (e.g

### 核心函数

- `resolve_hermes_bin()`: Find the hermes entry point.

    Priority:
      1. ``sys.argv[0]`` if it resolves to a real execut
- `build_relaunch_argv()`: Construct an argv list for replacing the current process with hermes.

    Args:
        extra_args:
- `relaunch()`: Replace the current process with a fresh hermes invocation.

    On POSIX we use ``os.execvp`` which

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## runtime_provider.py

**路径**: `hermes_cli\runtime_provider.py`
**行数**: 1859

### 功能描述

Shared runtime provider resolution for CLI, gateway, cron, and helpers.

### 核心函数

- `resolve_requested_provider()`: Resolve provider request from explicit arg, config, then env.
- `has_named_custom_provider()`: Return True when config defines a custom provider matching the request.

    Thin public wrapper aro
- `find_custom_provider_identity()`: Map an endpoint URL back to its canonical ``custom:<name>`` menu key.

    Returns the ``custom:<nor
- `canonical_custom_identity()`: Recover a routable ``custom:<name>`` identity for a bare custom provider.

    The bare string ``"cu
- `resolve_runtime_provider()`: Resolve runtime provider credentials for agent execution.

    target_model: Optional override for m
- `format_runtime_provider_error()`

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, llm-client, state-management
**跨组件调用**: 是

---

## secret_prompt.py

**路径**: `hermes_cli\secret_prompt.py`
**行数**: 127

### 功能描述

Secret input prompts with masked typing feedback.

### 核心函数

- `masked_secret_prompt()`: Prompt for a secret while showing masked typing feedback.

    Falls back to ``getpass.getpass`` whe

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## secrets_cli.py

**路径**: `hermes_cli\secrets_cli.py`
**行数**: 601

### 功能描述

CLI handlers for ``hermes secrets bitwarden ...``.

Subcommands:
    setup    — interactive wizard: install bws, prompt for token + project, test fetch
    status   — show current config + binary version + last fetch outcome
    sync     — run a fetch right now and show what would be applied (dry-ru

### 核心函数

- `register_cli()`: Attach the ``bitwarden`` subcommand tree to a parent parser.

    Called from ``hermes_cli.main`` as
- `cmd_setup()`
- `cmd_status()`
- `cmd_sync()`
- `cmd_disable()`
- `cmd_install()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## security_advisories.py

**路径**: `hermes_cli\security_advisories.py`
**行数**: 454

### 功能描述

Security advisory checker for Hermes Agent.

Detects known-compromised Python packages installed in the active venv
(supply-chain attacks like the Mini Shai-Hulud worm of May 2026 that
poisoned ``mistralai 2.4.6`` on PyPI) and surfaces remediation guidance to
the user.

Design goals:

- **Cheap.** A

### 核心类

- `Advisory`: One security advisory entry.

    Attributes:
        id: stable identifier used for acks (e.g. ``sh
- `AdvisoryHit`: One package-version match against an advisory.

### 核心函数

- `detect_compromised()`: Scan installed packages and return all advisory hits.

    A "hit" means an advisory's listed packag
- `get_acked_ids()`: Return the set of advisory IDs the user has dismissed.

    Returns an empty set if config can't be 
- `ack_advisory()`: Persist an ack for ``advisory_id``. Returns True on success.

    Idempotent — acking an already-ack
- `filter_unacked()`: Return only hits whose advisories the user has not dismissed.
- `short_banner_lines()`: Return 1-3 short lines suitable for a startup banner.

    Caller is responsible for color/styling. 
- `full_remediation_text()`: Return a multi-line block describing the advisory + remediation.
- `hits_due_for_banner()`: Return only hits whose banner is due (not acked, not recently shown).

    Side effect: stamps the b
- `render_doctor_section()`: Render the security-advisory section for ``hermes doctor``.

    Returns ``(has_problems, lines)``. 
- `startup_banner()`: Return a printable startup banner, or None if nothing is due.

    Updates the banner cache as a sid
- `gateway_log_message()`: Return a one-line log message for gateway operators, or None.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## security_audit.py

**路径**: `hermes_cli\security_audit.py`
**行数**: 577

### 功能描述

On-demand supply-chain audit for Hermes Agent installs.

Scans three surfaces a Hermes user actually controls and we can map to
upstream advisories without auth or extra binaries:

1. The Hermes venv (every PyPI dist via ``importlib.metadata``).
2. Python deps declared by user-installed plugins unde

### 核心类

- `Component`: A single (name, version, ecosystem) tuple discovered on disk.
- `Vulnerability`
- `Finding`

### 核心函数

- `run_audit()`: Discover components, query OSV, return findings sorted by severity desc.
- `cmd_security_audit()`: Implementation of `hermes security audit`.

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## security_audit_startup.py

**路径**: `hermes_cli\security_audit_startup.py`
**行数**: 283

### 功能描述

Startup security posture audit (warn-on-load, never blocks).

Surfaces dangerous host / deployment posture at process start so operators
get an at-a-glance "you're exposed" signal. Motivated by the June 2026
MCP-config persistence campaign, where compromised boxes ran as root with an
exposed dashboa

### 核心函数

- `run_security_audit()`: Run all checks and return a list of human-readable warning strings.

    Pure: no logging, no side e
- `log_startup_security_warnings()`: Run the audit once per process and emit each finding via logger.warning.

    Returns the findings (

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## send_cmd.py

**路径**: `hermes_cli\send_cmd.py`
**行数**: 472

### 功能描述

CLI subcommand: ``hermes send`` — pipe text from shell scripts to any
configured messaging platform (Telegram, Discord, Slack, Signal, SMS, etc.).

This is a thin wrapper around ``tools.send_message_tool.send_message_tool``
that exposes its functionality as a standalone CLI entry point so ops
script

### 核心函数

- `cmd_send()`: Entry point wired into the top-level argparse dispatcher.
- `register_send_subparser()`: Create the ``send`` subparser and return it.

    Kept as a standalone function so the top-level par

### 依赖关系

**依赖组件**: gateway, tool-system
**跨组件调用**: 是

---

## service_manager.py

**路径**: `hermes_cli\service_manager.py`
**行数**: 1110

### 功能描述

Abstract service manager interface.

Wraps the existing systemd (Linux host), launchd (macOS host), Windows
Scheduled Task (native Windows host), and s6 (container) backends behind
a common Protocol. Only the s6 backend supports runtime registration
(for per-profile gateways) — host backends raise N

### 核心类

- `ServiceManager`: Abstract interface for init-system-specific service operations.

    Lifecycle methods (start / stop
- `_RegistrationUnsupportedMixin`: Mixin for host backends that don't support runtime registration.
- `SystemdServiceManager`: Thin wrapper around the ``systemd_*`` functions in hermes_cli.gateway.

    Existing host call sites
- `LaunchdServiceManager`: Thin wrapper around the ``launchd_*`` functions in hermes_cli.gateway.
- `WindowsServiceManager`: Thin wrapper around ``hermes_cli.gateway_windows`` (Scheduled Task /
    Startup-folder fallback).


- `S6Error`: Base error for S6ServiceManager lifecycle failures.

    Concrete subclasses carry the slot name (an
- `GatewayNotRegisteredError`: Raised when a lifecycle method targets a slot that doesn't exist.

    Most commonly: ``hermes -p ty
- `S6CommandError`: Raised when an s6 command fails for a reason other than a
    missing slot — e.g. permission denied 
- `S6ServiceManager`: Per-profile gateway supervision via s6-overlay.

    Only handles runtime-registered services under


### 核心函数

- `validate_profile_name()`: Raise ValueError if ``name`` is not usable as a profile name.

    Profile names are used as s6 serv
- `detect_service_manager()`: Detect which service manager is available in this environment.

    Returns:
        "s6" — s6-svsca
- `get_service_manager()`: Return the ServiceManager instance for the current environment.

    Raises:
        RuntimeError: w

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## session_listing.py

**路径**: `hermes_cli\session_listing.py`
**行数**: 98

### 功能描述

Shared session-listing helpers for CLI and gateway slash surfaces.

### 核心函数

- `parse_session_listing_args()`: Parse `/sessions`-style args into listing flags plus a resume target.

    Returns ``(include_all_so
- `query_session_listing()`: Return session rows for interactive listing surfaces.

    This is the shared selection policy behin
- `format_gateway_session_listing()`: Render a compact Markdown-ish session list for gateway messengers.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## session_recap.py

**路径**: `hermes_cli\session_recap.py`
**行数**: 317

### 功能描述

Session recap — summarize what's happened in the current session.

Inspired by Claude Code's `/recap` command (v2.1.114, April 2026), which
shows a one-line summary of what happened while a terminal was unfocused
so users juggling multiple sessions can re-orient quickly.

Source: https://code.claude

### 核心函数

- `build_recap()`: Build a multi-line recap of recent activity.

    Inputs:
        messages: the full conversation hi

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## setup.py

**路径**: `hermes_cli\setup.py`
**行数**: 3412

### 功能描述

Interactive setup wizard for Hermes Agent.

Modular wizard with independently-runnable sections:
  1. Model & Provider — choose your AI provider and model
  2. Terminal Backend — where your agent runs commands
  3. Agent Settings — iterations, compression, session reset
  4. Messaging Platforms — co

### 核心函数

- `print_header()`: Print a section header.
- `is_interactive_stdin()`: Return True when stdin looks like a usable interactive TTY.
- `print_noninteractive_setup_guidance()`: Print guidance for headless/non-interactive setup flows.
- `prompt()`: Prompt for input with optional default.
- `prompt_choice()`: Prompt for a choice from a list with arrow key navigation.

    Escape keeps the current default (sk
- `is_noninteractive()`: True when no human is available to answer a prompt.

    The dashboard/desktop spawn CLI actions wit
- `prompt_yes_no()`: Prompt for yes/no. Ctrl+C exits, empty input returns default.

    Non-interactive callers (``HERMES
- `prompt_checklist()`: Display a multi-select checklist and return the indices of selected items.

    Each item in `items`
- `setup_model_provider()`: Configure the inference provider and default model.

    Delegates to ``cmd_model()`` (the same flow
- `setup_tts()`: Standalone TTS setup (for 'hermes setup tts').
- `setup_terminal_backend()`: Configure the terminal execution backend.
- `setup_agent_settings()`: Configure agent behavior: iterations, progress display, compression, session reset.
- `setup_gateway()`: Configure messaging platform integrations.
- `setup_tools()`: Configure tools — delegates to the unified tools_command() in tools_config.py.

    Both `hermes set
- `run_setup_wizard()`: Run the interactive setup wizard.

    Supports full, quick, and section-specific setup:
      herme

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## setup_whatsapp_cloud.py

**路径**: `hermes_cli\setup_whatsapp_cloud.py`
**行数**: 542

### 功能描述

Interactive setup wizard for the WhatsApp Cloud API adapter.

Entry point: ``hermes whatsapp-cloud`` (dispatched from
``cmd_whatsapp_cloud`` in ``hermes_cli/main.py``).

Walks the user through the 6 credentials Meta requires + recipient
allowlist, auto-generates the verify token, and prints exact fo

### 核心函数

- `run_whatsapp_cloud_setup()`: Interactive wizard for the WhatsApp Cloud API adapter.

    Returns 0 on full success, 1 on user abo

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## skills_config.py

**路径**: `hermes_cli\skills_config.py`
**行数**: 184

### 功能描述

Skills configuration for Hermes Agent.
`hermes skills` enters this module.

Toggle individual skills or categories on/off, globally or per-platform.
Config stored in ~/.hermes/config.yaml under:

  skills:
    disabled: [skill-a, skill-b]          # global disabled list
    platform_disabled:       

### 核心函数

- `get_disabled_skills()`: Return disabled skill names: the global list unioned with the
    platform-specific list when a plat
- `save_disabled_skills()`: Persist disabled skill names to config.
- `skills_command()`: Entry point for `hermes skills`.

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## skills_hub.py

**路径**: `hermes_cli\skills_hub.py`
**行数**: 1974

### 功能描述

Skills Hub CLI — Unified interface for the Hermes Skills Hub.

Powers both:
  - `hermes skills <subcommand>` (CLI argparse entry point)
  - `/skills <subcommand>` (slash command in the interactive chat)

All logic lives in shared do_* functions. The CLI entry point and slash command
handler are thin

### 核心函数

- `do_search()`: Search registries and display results as a Rich table.

    When ``as_json=True`` writes a JSON arra
- `do_browse()`: Browse all available skills across registries, paginated.

    Official skills are always shown firs
- `do_install()`: Fetch, quarantine, scan, confirm, and install a skill.

    ``name_override`` lets non-interactive c
- `do_inspect()`: Preview a skill's SKILL.md content without installing.
- `browse_skills()`: Paginated hub browse for programmatic callers (e.g. TUI gateway).

    Returns ``{"items": [...], "p
- `inspect_skill()`: Skill metadata (+ SKILL.md preview) for programmatic callers.
- `do_list()`: List installed skills, distinguishing hub, builtin, and local skills.

    Args:
        source_filt
- `do_check()`: Check hub-installed skills for upstream updates.
- `do_update()`: Update hub-installed skills with upstream changes.
- `do_audit()`: Re-run security scan on installed hub skills.

    When ``deep=True``, also runs an opt-in AST-level
- `do_uninstall()`: Remove a hub-installed skill with confirmation.
- `do_reset()`: Reset a bundled skill's manifest tracking (+ optionally restore from bundled).
- `do_list_modified()`: List bundled skills the user has edited (which `hermes update` keeps).
- `do_diff()`: Show how the user's copy of a bundled skill differs from the stock version.
- `do_opt_out()`: Opt the active profile out of bundled-skill seeding.

    Always writes the .no-bundled-skills marke
- ... 还有 8 个函数

### 依赖关系

**依赖组件**: agent-engine, state-management, tool-system
**跨组件调用**: 是

---

## skin_engine.py

**路径**: `hermes_cli\skin_engine.py`
**行数**: 927

### 功能描述

Hermes CLI skin/theme engine.

A data-driven skin system that lets users customize the CLI's visual appearance.
Skins are defined as YAML files in ~/.hermes/skins/ or as built-in presets.
No code changes are needed to add a new skin.

SKIN YAML SCHEMA
================

All fields are optional. Missi

### 核心类

- `SkinConfig`: Complete skin configuration.

### 核心函数

- `list_skins()`: List all available skins (built-in + user-installed).

    Returns list of {"name": ..., "descriptio
- `load_skin()`: Load a skin by name. Checks user skins first, then built-in.
- `get_active_skin()`: Get the currently active skin config (cached).
- `set_active_skin()`: Switch the active skin. Returns the new SkinConfig.
- `get_active_skin_name()`: Get the name of the currently active skin.
- `init_skin_from_config()`: Initialize the active skin from CLI config at startup.

    Call this once during CLI init with the 
- `get_active_prompt_symbol()`: Return the interactive prompt symbol with a single trailing space.

    Skins store ``prompt_symbol`
- `get_active_help_header()`: Get the /help header from the active skin.
- `get_active_goodbye()`: Get the goodbye line from the active skin.
- `get_prompt_toolkit_style_overrides()`: Return prompt_toolkit style overrides derived from the active skin.

    These are layered on top of

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## slack_cli.py

**路径**: `hermes_cli\slack_cli.py`
**行数**: 192

### 功能描述

``hermes slack ...`` CLI subcommands.

Today only ``hermes slack manifest`` is implemented — it generates the
Slack app manifest JSON for registering every gateway command as a native
Slack slash (``/btw``, ``/stop``, ``/model``, …) so users get the same
first-class slash UX Discord and Telegram alr

### 核心函数

- `slack_manifest_command()`: Print or write a Slack app manifest JSON.

    Flags (all parsed in ``hermes_cli/main.py``):
      -

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## sqlite_util.py

**路径**: `hermes_cli\sqlite_util.py`
**行数**: 50

### 功能描述

Shared SQLite primitives for the small per-profile / board stores.

The projects and kanban stores open WAL SQLite files with the same two
primitives — an idempotent column-add migration and an IMMEDIATE write
transaction. One definition here keeps the two stores from drifting.

### 核心函数

- `add_column_if_missing()`: ``ALTER TABLE <table> ADD COLUMN <ddl>``, idempotent across races.

    Returns ``True`` when this c
- `write_txn()`: An IMMEDIATE write transaction: at most one concurrent writer wins.

    The explicit ROLLBACK is gu

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## status.py

**路径**: `hermes_cli\status.py`
**行数**: 587

### 功能描述

Status command for hermes CLI.

Shows the status of all Hermes Agent components.

### 核心函数

- `check_mark()`
- `redact_key()`: Redact an API key for display.

    Thin wrapper over :func:`agent.redact.mask_secret`. Preserves th
- `show_status()`: Show status of all Hermes Agent components.

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, gateway, state-management, tool-system
**跨组件调用**: 是

---

## stdio.py

**路径**: `hermes_cli\stdio.py`
**行数**: 252

### 功能描述

Windows-safe stdio configuration.

On Windows, Python's ``sys.stdout``/``sys.stderr`` default to the console's
active code page (often ``cp1252``, sometimes ``cp437``, occasionally ``cp932``
on Japanese locales, etc.).  Hermes's banners, tool output feed, and slash
command listings all contain Unico

### 核心函数

- `is_windows()`: Return True iff running on native Windows (not WSL).
- `configure_windows_stdio()`: Force UTF-8 stdio on Windows.  No-op elsewhere.

    Idempotent — safe to call multiple times from d

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `hermes_cli\subcommands\__init__.py`
**行数**: 19

### 功能描述

CLI subcommand parser builders for ``hermes <subcommand>``.

``hermes_cli/main.py:main()`` historically built the entire argparse tree
inline — 179 ``add_parser`` calls across ~26 subcommand groups, all wedged
into one 3,300-line function. This package breaks that tree apart: each
subcommand group o

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _shared.py

**路径**: `hermes_cli\subcommands\_shared.py`
**行数**: 30

### 功能描述

Shared parser helpers used across multiple CLI subcommand builders.

These were module-level helpers in ``hermes_cli/main.py``. They are pulled
into a neutral module so both ``main.py`` and every
``hermes_cli/subcommands/<group>.py`` builder can import them without an
import cycle. ``main.py`` re-ex

### 核心函数

- `add_accept_hooks_flag()`: Attach the ``--accept-hooks`` flag.

    Shared across every agent subparser so the flag works regar

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## acp.py

**路径**: `hermes_cli\subcommands\acp.py`
**行数**: 53

### 功能描述

``hermes acp`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_acp_parser()`: Attach the ``acp`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## auth.py

**路径**: `hermes_cli\subcommands\auth.py`
**行数**: 110

### 功能描述

``hermes auth`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_auth_parser()`: Attach the ``auth`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## backup.py

**路径**: `hermes_cli\subcommands\backup.py`
**行数**: 39

### 功能描述

``hermes backup`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_backup_parser()`: Attach the ``backup`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## claw.py

**路径**: `hermes_cli\subcommands\claw.py`
**行数**: 93

### 功能描述

``hermes claw`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_claw_parser()`: Attach the ``claw`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## config.py

**路径**: `hermes_cli\subcommands\config.py`
**行数**: 50

### 功能描述

``hermes config`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_config_parser()`: Attach the ``config`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## cron.py

**路径**: `hermes_cli\subcommands\cron.py`
**行数**: 164

### 功能描述

``hermes cron`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` — same arguments, same
``func=cmd_cron`` dispatch. The handler is injected so this module does not
import ``main`` (cycle avoidance).

### 核心函数

- `build_cron_parser()`: Attach the ``cron`` subcommand (and its sub-actions) to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## dashboard.py

**路径**: `hermes_cli\subcommands\dashboard.py`
**行数**: 150

### 功能描述

``hermes dashboard`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_dashboard_parser()`: Attach the ``dashboard`` subcommand (and its ``register`` action).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## debug.py

**路径**: `hermes_cli\subcommands\debug.py`
**行数**: 78

### 功能描述

``hermes debug`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_debug_parser()`: Attach the ``debug`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## doctor.py

**路径**: `hermes_cli\subcommands\doctor.py`
**行数**: 36

### 功能描述

``hermes doctor`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_doctor_parser()`: Attach the ``doctor`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## dump.py

**路径**: `hermes_cli\subcommands\dump.py`
**行数**: 29

### 功能描述

``hermes dump`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_dump_parser()`: Attach the ``dump`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## gateway.py

**路径**: `hermes_cli\subcommands\gateway.py`
**行数**: 346

### 功能描述

``hermes gateway`` and ``hermes proxy`` subcommand parsers.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Both parsers are built together because they shared one inline block (the
``gateway`` section also defined ``proxy``). Handlers injected to avoid
importing ``main``.

### 核心函数

- `build_gateway_parser()`: Attach the ``gateway`` and ``proxy`` subcommands to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## gui.py

**路径**: `hermes_cli\subcommands\gui.py`
**行数**: 64

### 功能描述

``hermes gui`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_gui_parser()`: Attach the ``gui`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## hooks.py

**路径**: `hermes_cli\subcommands\hooks.py`
**行数**: 78

### 功能描述

``hermes hooks`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_hooks_parser()`: Attach the ``hooks`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## import_cmd.py

**路径**: `hermes_cli\subcommands\import_cmd.py`
**行数**: 32

### 功能描述

``hermes import`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_import_cmd_parser()`: Attach the ``import`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## insights.py

**路径**: `hermes_cli\subcommands\insights.py`
**行数**: 26

### 功能描述

``hermes insights`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_insights_parser()`: Attach the ``insights`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## login.py

**路径**: `hermes_cli\subcommands\login.py`
**行数**: 79

### 功能描述

``hermes login`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_login_parser()`: Attach the deprecated ``login`` subcommand to ``subparsers``.

    ``hermes login`` was removed in f

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## logout.py

**路径**: `hermes_cli\subcommands\logout.py`
**行数**: 29

### 功能描述

``hermes logout`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_logout_parser()`: Attach the ``logout`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## logs.py

**路径**: `hermes_cli\subcommands\logs.py`
**行数**: 79

### 功能描述

``hermes logs`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_logs_parser()`: Attach the ``logs`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## mcp.py

**路径**: `hermes_cli\subcommands\mcp.py`
**行数**: 122

### 功能描述

``hermes mcp`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_mcp_parser()`: Attach the ``mcp`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

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

## model.py

**路径**: `hermes_cli\subcommands\model.py`
**行数**: 73

### 功能描述

``hermes model`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_model_parser()`: Attach the ``model`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pairing.py

**路径**: `hermes_cli\subcommands\pairing.py`
**行数**: 37

### 功能描述

``hermes pairing`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_pairing_parser()`: Attach the ``pairing`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## plugins.py

**路径**: `hermes_cli\subcommands\plugins.py`
**行数**: 95

### 功能描述

``hermes plugins`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_plugins_parser()`: Attach the ``plugins`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## postinstall.py

**路径**: `hermes_cli\subcommands\postinstall.py`
**行数**: 24

### 功能描述

``hermes postinstall`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_postinstall_parser()`: Attach the ``postinstall`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## profile.py

**路径**: `hermes_cli\subcommands\profile.py`
**行数**: 204

### 功能描述

``hermes profile`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_profile_parser()`: Attach the ``profile`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## prompt_size.py

**路径**: `hermes_cli\subcommands\prompt_size.py`
**行数**: 37

### 功能描述

``hermes prompt-size`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_prompt_size_parser()`: Attach the ``prompt-size`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## security.py

**路径**: `hermes_cli\subcommands\security.py`
**行数**: 63

### 功能描述

``hermes security`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_security_parser()`: Attach the ``security`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## setup.py

**路径**: `hermes_cli\subcommands\setup.py`
**行数**: 59

### 功能描述

``hermes setup`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_setup_parser()`: Attach the ``setup`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## skills.py

**路径**: `hermes_cli\subcommands\skills.py`
**行数**: 299

### 功能描述

``hermes skills`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_skills_parser()`: Attach the ``skills`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## slack.py

**路径**: `hermes_cli\subcommands\slack.py`
**行数**: 69

### 功能描述

``hermes slack`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_slack_parser()`: Attach the ``slack`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## status.py

**路径**: `hermes_cli\subcommands\status.py`
**行数**: 29

### 功能描述

``hermes status`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_status_parser()`: Attach the ``status`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tools.py

**路径**: `hermes_cli\subcommands\tools.py`
**行数**: 96

### 功能描述

``hermes tools`` subcommand parser.

Extracted from ``hermes_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_tools_parser()`: Attach the ``tools`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## uninstall.py

**路径**: `hermes_cli\subcommands\uninstall.py`
**行数**: 42

### 功能描述

``hermes uninstall`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_uninstall_parser()`: Attach the ``uninstall`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## update.py

**路径**: `hermes_cli\subcommands\update.py`
**行数**: 71

### 功能描述

``hermes update`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_update_parser()`: Attach the ``update`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## version.py

**路径**: `hermes_cli\subcommands\version.py`
**行数**: 19

### 功能描述

``hermes version`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_version_parser()`: Attach the ``version`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## webhook.py

**路径**: `hermes_cli\subcommands\webhook.py`
**行数**: 77

### 功能描述

``hermes webhook`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_webhook_parser()`: Attach the ``webhook`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## whatsapp.py

**路径**: `hermes_cli\subcommands\whatsapp.py`
**行数**: 23

### 功能描述

``hermes whatsapp`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

### 核心函数

- `build_whatsapp_parser()`: Attach the ``whatsapp`` subcommand to ``subparsers``.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## suggestions_cmd.py

**路径**: `hermes_cli\suggestions_cmd.py`
**行数**: 154

### 功能描述

Shared ``/suggestions`` command logic for CLI and gateway.

Both surfaces call ``handle_suggestions_command(args, origin=...)`` and present
the returned text however they present command output. Keeping the logic here
(not in cli.py / gateway/run.py) means the two surfaces can never drift.

Subcomma

### 核心函数

- `handle_suggestions_command()`: Dispatch a ``/suggestions`` invocation. Returns text to show the user.

    ``args`` is everything a

### 依赖关系

**依赖组件**: cron, gateway
**跨组件调用**: 是

---

## telegram_managed_bot.py

**路径**: `hermes_cli\telegram_managed_bot.py`
**行数**: 359

### 功能描述

Telegram Managed Bot onboarding client.

Uses Telegram's Managed Bots feature to create a user-owned child bot without
manual BotFather token copy-paste. Hermes talks only to the Nous onboarding
service; the raw Telegram token is saved locally after one-time retrieval.

### 核心类

- `TelegramPairing`: Pairing record returned by the Telegram onboarding service.
- `TelegramBotSetupResult`: Successful Telegram onboarding result returned by the setup service.

### 核心函数

- `is_valid_telegram_bot_token()`: Return True when *token* has Telegram's bot-token shape.
- `render_qr_terminal()`: Render a URL as a QR code string suitable for terminal output.
- `print_qr_code()`: Print a QR code to stdout, with URL fallback if qrcode is missing.
- `generate_username_slug()`: Generate a base32-ish slug for Telegram username correlation.

    Sixteen characters from a 32-symb
- `generate_bot_username()`: Generate a secure suggested bot username like ``hermes_<slug>_bot``.

    ``profile_name`` is accept
- `generate_deep_link()`: Build a ``t.me/newbot`` deep link for managed bot creation.
- `generate_pairing_nonce()`: Generate a legacy-compatible random nonce string.

    The new protocol uses service-created ``pairi
- `create_pairing()`: Create a Telegram onboarding pairing.

    ``POST /v1/telegram/pairings`` returns the deep link, QR 
- `poll_pairing_result_once()`: Poll the onboarding service once. Returns setup metadata when ready.
- `poll_pairing_once()`: Poll the onboarding service once. Returns the token when ready.
- `poll_for_setup_result()`: Poll the pairing API until setup metadata is available or timeout.
- `poll_for_token()`: Poll the pairing API until the bot token is available or timeout.
- `auto_setup_telegram_bot_result()`: Run the full automatic Telegram bot creation flow.
- `auto_setup_telegram_bot()`: Run automatic Telegram bot creation and return only the bot token.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## timeouts.py

**路径**: `hermes_cli\timeouts.py`
**行数**: 83

### 功能描述

Return a configured provider request timeout in seconds, if any.

### 核心函数

- `get_provider_request_timeout()`: Return a configured provider request timeout in seconds, if any.
- `get_provider_stale_timeout()`: Return a configured non-stream stale timeout in seconds, if any.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tips.py

**路径**: `hermes_cli\tips.py`
**行数**: 486

### 功能描述

Random tips shown at CLI session start to help users discover features.

### 核心函数

- `get_random_tip()`: Return a random tip string.

    Args:
        exclude_recent: not used currently; reserved for futu

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## tools_config.py

**路径**: `hermes_cli\tools_config.py`
**行数**: 4027

### 功能描述

Unified tool configuration for Hermes Agent.

`hermes tools` and `hermes setup tools` both enter this module.
Select a platform → toggle toolsets on/off → for newly enabled tools
that need API keys, run through provider-aware configuration.

Saves per-platform tool configuration to ~/.hermes/config.

### 核心函数

- `gui_toolset_label()`: Strip leading emoji/icons from toolset titles for GUI surfaces.

    Registry labels use ``<emoji> <
- `install_cua_driver()`: Install or refresh the cua-driver binary used by Computer Use.

    The upstream installer always pu
- `valid_post_setup_keys()`: Return the set of post-setup keys declared by any visible provider.

    Collected from ``TOOL_CATEG
- `run_post_setup_command()`: ``hermes tools post-setup <key>`` — non-interactive post-setup runner.

    Runs the install/bootstr
- `enabled_mcp_server_names()`: Names of MCP servers globally enabled in config.yaml.

    Shared by the gateway/CLI platform resolv
- `apply_provider_selection()`: Non-interactively persist a provider selection for a toolset.

    Resolves ``provider_name`` within
- `tools_command()`: Entry point for `hermes tools` and `hermes setup tools`.

    Args:
        first_install: When True
- `tools_disable_enable_command()`: Enable, disable, or list tools for a platform.

    Built-in toolsets use plain names (e.g. ``web``,

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, entry-points, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## toolset_validation.py

**路径**: `hermes_cli\toolset_validation.py`
**行数**: 75

### 功能描述

Validation for the ``platform_toolsets`` config section.

Pure, side-effect-free helpers so the logic is unit-testable without importing
the tool registry or launching Hermes (mirrors the decoupled-helper pattern used
elsewhere in the CLI).

Motivated by #38798: a config migration silently rewrote t

### 核心函数

- `validate_platform_toolsets()`: Return human-readable warnings for a ``platform_toolsets`` mapping.

    Two failure modes are repor

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## uninstall.py

**路径**: `hermes_cli\uninstall.py`
**行数**: 931

### 功能描述

Hermes Agent Uninstaller.

Provides options for:
- Full uninstall: Remove everything including configs and data
- Keep data: Remove code but keep ~/.hermes/ (configs, sessions, logs)

### 核心类

- `_UninstallArgs`: Lightweight args namespace for the module entrypoint below.

### 核心函数

- `log_info()`
- `log_success()`
- `log_warn()`
- `get_project_root()`: Get the project installation directory.
- `find_shell_configs()`: Find shell configuration files that might have PATH entries.
- `remove_path_from_shell_configs()`: Remove Hermes PATH entries from shell configuration files.
- `remove_wrapper_script()`: Remove the hermes wrapper script if it exists.
- `remove_node_symlinks()`: Remove the node/npm/npx symlinks the installer placed on PATH.

    The POSIX installer (``scripts/i
- `uninstall_gateway_service()`: Stop and uninstall the gateway service (systemd, launchd, Windows
    Scheduled Task / Startup folde
- `remove_path_from_windows_registry()`: Strip Hermes-owned entries from User-scope PATH in the registry.

    Returns the list of removed pa
- `remove_hermes_env_vars_windows()`: Delete HERMES_HOME and HERMES_GIT_BASH_PATH from User-scope env vars.
- `remove_portable_tooling_windows()`: Delete PortableGit and Node installs the Windows installer created under
    ``%LOCALAPPDATA%\hermes
- `run_gui_uninstall()`: GUI-only uninstall: remove the Chat GUI, leave the agent + data intact.

    Mirrors ``hermes uninst
- `run_uninstall()`: Run the uninstall process.
    
    Options:
    - Full uninstall: removes code + ~/.hermes/ (config
- `main()`: Module entrypoint: ``python -m hermes_cli.uninstall --mode <gui|lite|full>``.

    Exists so the des

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## voice.py

**路径**: `hermes_cli\voice.py`
**行数**: 847

### 功能描述

Process-wide voice recording + TTS API for the TUI gateway.

Wraps ``tools.voice_mode`` (recording/transcription) and ``tools.tts_tool``
(text-to-speech) behind idempotent, stateful entry points that the gateway's
``voice.record``, ``voice.toggle``, and ``voice.tts`` JSON-RPC handlers can
call from 

### 核心函数

- `voice_record_key_from_config()`: Shape-safe ``cfg.voice.record_key`` lookup.

    ``load_config()`` deep-merges raw YAML and preserve
- `normalize_voice_record_key_for_prompt_toolkit()`: Coerce ``voice.record_key`` into prompt_toolkit's ``c-x`` / ``a-x`` format.

    Mirrors the TUI par
- `format_voice_record_key_for_status()`: Render ``voice.record_key`` for ``/voice status`` in CLI-friendly form.

    Mirrors the TUI's ``for
- `start_recording()`: Begin capturing from the default input device (push-to-talk).

    Idempotent — calling again while 
- `stop_and_transcribe()`: Stop the active push-to-talk recording, transcribe, return text.

    Returns ``None`` when no recor
- `start_continuous()`: Start a VAD-driven continuous recording loop.

    The loop calls ``on_transcript(text)`` each time 
- `stop_continuous()`: Stop the active continuous loop and release the microphone.

    Idempotent — calling while not acti
- `is_continuous_active()`: Whether a continuous voice loop is currently running.
- `speak_text()`: Synthesize ``text`` with the configured TTS provider and play it.

    Mirrors cli.py:_voice_speak_r

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## web_server.py

**路径**: `hermes_cli\web_server.py`
**行数**: 13465

### 功能描述

Hermes Agent — Web UI server.

Provides a FastAPI backend serving the Vite/React frontend and REST API
endpoints for managing configuration, environment variables, and sessions.

Usage:
    python -m hermes_cli.main web          # Start on http://127.0.0.1:9119
    python -m hermes_cli.main web --po

### 核心类

- `ConfigUpdate`
- `EnvVarUpdate`
- `EnvVarDelete`
- `EnvVarReveal`
- `MemoryProviderConfigUpdate`
- `MessagingPlatformUpdate`
- `TelegramOnboardingStart`
- `TelegramOnboardingApply`
- `AudioTranscriptionRequest`
- `ManagedFileUpload`
- ... 还有 56 个类

### 核心函数

- `should_require_auth()`: Return True iff the dashboard auth gate must be active.

    Truth table:
      host == loopback    
- `get_model_info()`: Return resolved model metadata for the currently configured model.

    Calls the same context-lengt
- `get_model_options()`: Return authenticated providers + their curated model lists.

    REST equivalent of the ``model.opti
- `get_recommended_default_model()`: Return the recommended default model for a freshly-authenticated provider.

    Mirrors the model-cu
- `get_auxiliary_models()`: Return current auxiliary task assignments.

    Shape:
      {
        "tasks": [
          {"task":
- `get_moa_models()`: Return the configured Mixture-of-Agents provider/model slots.
- `set_moa_models()`: Persist the Mixture-of-Agents provider/model slots.
- `mount_spa()`: Mount the built SPA. Falls back to index.html for client-side routing.

    The session token is inj
- `start_server()`: Start the web UI server.

    ``initial_profile`` (when set) is appended to the auto-opened browser


### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cron, entry-points, gateway, llm-client, plugin-system, state-management, tool-system, tui
**跨组件调用**: 是

---

## webhook.py

**路径**: `hermes_cli\webhook.py`
**行数**: 299

### 功能描述

hermes webhook — manage dynamic webhook subscriptions from the CLI.

Usage:
    hermes webhook subscribe <name> [options]
    hermes webhook list
    hermes webhook remove <name>
    hermes webhook test <name> [--payload '{"key": "value"}']

Subscriptions persist to ~/.hermes/webhook_subscriptions.j

### 核心函数

- `webhook_command()`: Entry point for 'hermes webhook' subcommand.

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

## win_pty_bridge.py

**路径**: `hermes_cli\win_pty_bridge.py`
**行数**: 180

### 功能描述

Windows ConPTY bridge for the `hermes dashboard` chat tab.

Drop-in counterpart to ``hermes_cli.pty_bridge.PtyBridge`` for native
Windows. Mirrors the exact public surface the ``/api/pty`` WebSocket
handler in ``hermes_cli.web_server`` consumes: ``spawn``, ``read``,
``write``, ``resize``, ``close``,

### 核心类

- `PtyUnavailableError`: Raised when a PTY cannot be created on this platform.
- `WinPtyBridge`: pywinpty-backed bridge with the same interface as ``PtyBridge``.

    ``web_server`` calls :meth:`re

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## write_approval_commands.py

**路径**: `hermes_cli\write_approval_commands.py`
**行数**: 210

### 功能描述

Shared handlers for the /memory and /skills write-approval subcommands.

Both the interactive CLI (``cli.py``) and the gateway (``gateway/run.py``) call
into this module so the pending-review UX (list / approve / reject / diff /
mode) lives in one place. Each caller owns only its surface concerns:
f

### 核心函数

- `handle_pending_subcommand()`: Dispatch a /memory or /skills subcommand.

    Args:
        subsystem: ``memory`` or ``skills``.
  

### 依赖关系

**依赖组件**: acp-adapter, memory-system, tool-system
**跨组件调用**: 是

---

## xai_retirement.py

**路径**: `hermes_cli\xai_retirement.py`
**行数**: 254

### 功能描述

Detect xAI models retired on May 15, 2026.

Source: https://docs.x.ai/developers/migration/may-15-retirement

Pure logic: walks a Hermes config dict, returns issues for any reference
to a retired xAI model. No I/O, no CLI dependencies — testable in isolation
and reusable from both `hermes doctor` an

### 核心类

- `RetirementIssue`: A reference to a retired xAI model found in a Hermes config.
- `ApplyResult`: Outcome of an apply_migration call.

### 核心函数

- `find_retired_xai_refs()`: Walk all model slots in a Hermes config and return retirement issues.

    Slots scanned:
      - ``
- `format_issue()`: One-line human-readable rendering of a retirement issue.
- `apply_migration()`: Rewrite ``config_path`` in-place so each issue is resolved.

    For every issue, the model name is 

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

