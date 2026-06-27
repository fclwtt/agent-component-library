# security 模块详细说明

本组件包含 10 个模块。

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

**依赖组件**: cli, state-management
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

**依赖组件**: cli, state-management
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

