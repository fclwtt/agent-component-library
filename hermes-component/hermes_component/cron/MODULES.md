# cron 模块详细说明

本组件包含 9 个模块。

---

## __init__.py

**路径**: `cron\__init__.py`
**行数**: 43

### 功能描述

Cron job scheduling system for Hermes Agent.

This module provides scheduled task execution, allowing the agent to:
- Run automated tasks on schedules (cron expressions, intervals, one-shot)
- Self-schedule reminders and follow-up tasks
- Execute tasks in isolated sessions (no prior context)

Cron j

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## blueprint_catalog.py

**路径**: `cron\blueprint_catalog.py`
**行数**: 714

### 功能描述

Automation Blueprints — parameterized automation blueprints with typed slots.

A *blueprint* is a one-place definition of an automation that every surface
renders natively:

  * Dashboard / GUI app  -> a form (one field per slot)
  * CLI / TUI / messenger -> a pre-filled ``/blueprint`` slash command

### 核心类

- `BlueprintFillError`: Raised when supplied slot values fail validation.
- `BlueprintSlot`: A single fillable field on a blueprint.
- `AutomationBlueprint`: A parameterized automation blueprint.

### 核心函数

- `get_blueprint()`
- `blueprint_form_schema()`: Emit the JSON a form renderer (dashboard / GUI) needs for this blueprint.
- `blueprint_slash_command()`: Build the flattened ``/blueprint <key> slot=val …`` command string.

    Uses each slot's default wh
- `blueprint_deeplink()`: Build the ``hermes://blueprint/<key>?slot=val`` deep-link URL.
- `blueprint_catalog_entry()`: Unified serializable shape for a blueprint — used by the docs generator
    and the dashboard API. C
- `fill_blueprint()`: Validate ``values`` and return ``cron.jobs.create_job`` kwargs.

    Missing required (non-optional)

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## jobs.py

**路径**: `cron\jobs.py`
**行数**: 1694

### 功能描述

Cron job storage and management.

Jobs are stored in ~/.hermes/cron/jobs.json
Output is saved to ~/.hermes/cron/output/{job_id}/{timestamp}.md

### 核心类

- `AmbiguousJobReference`: Raised when a job name matches more than one job.

### 核心函数

- `ensure_dirs()`: Ensure cron directories exist with secure permissions.
- `parse_duration()`: Parse duration string into minutes.
    
    Examples:
        "30m" → 30
        "2h" → 120
       
- `parse_schedule()`: Parse schedule string into structured format.
    
    Returns dict with:
        - kind: "once" | "
- `compute_next_run()`: Compute the next run time for a schedule.

    Returns ISO timestamp string, or None if no more runs
- `record_ticker_heartbeat()`: Record a ticker liveness signal, and optionally a successful-tick signal.

    The ticker calls this
- `get_ticker_heartbeat_age()`: Seconds since the ticker loop last iterated, or None if unknown.

    None = heartbeat file missing/
- `get_ticker_success_age()`: Seconds since the ticker last completed a tick WITHOUT raising, or None.
- `load_jobs()`: Load all jobs from storage.
- `save_jobs()`: Save all jobs to storage.
- `create_job()`: Create a new cron job.

    Args:
        prompt: The prompt to run (must be self-contained, or a ta
- `get_job()`: Get a job by ID.
- `resolve_job_ref()`: Resolve a job reference (ID or name) to a job record.

    - Exact ID match wins (works even if a di
- `list_jobs()`: List all jobs, optionally including disabled ones.
- `update_job()`: Update a job by ID, refreshing derived schedule fields when needed.
- `pause_job()`: Pause a job without deleting it. Accepts a job ID or name.
- ... 还有 9 个函数

### 依赖关系

**依赖组件**: cli, entry-points, state-management
**跨组件调用**: 是

---

## scheduler.py

**路径**: `cron\scheduler.py`
**行数**: 3043

### 功能描述

Cron job scheduler - executes due jobs.

Provides tick() which checks for due jobs and runs them. The gateway
calls this every 60 seconds from a background thread.

Uses a file-based lock (~/.hermes/cron/.tick.lock) so only one tick
runs at a time if multiple processes overlap.

### 核心类

- `CronPromptInjectionBlocked`: Raised by _build_job_prompt when the fully-assembled prompt trips the
    injection scanner. Caught 

### 核心函数

- `cron_delivery_targets()`: Return the platforms a cron job can auto-deliver to.

    Single source of truth for any UI (dashboa
- `run_job()`: Execute a single cron job.
    
    Returns:
        Tuple of (success, full_output_doc, final_respo
- `run_one_job()`: Run ONE due job end-to-end: execute → save output → deliver → mark.

    This is the shared firing b
- `tick()`: Check and run all due jobs.
    
    Uses a file lock so only one tick runs at a time, even if the g

### 依赖关系

**依赖组件**: acp-adapter, agent-engine, cli, entry-points, gateway, llm-client, state-management, tool-system
**跨组件调用**: 是

---

## scheduler_provider.py

**路径**: `cron\scheduler_provider.py`
**行数**: 195

### 功能描述

CronScheduler provider interface (Axis B — the trigger).

⚠️ EXPERIMENTAL — this interface is validated by exactly ONE consumer (the
built-in) until an external provider (Chronos, Phase 4) shakes it out. Until
then the module path, method signatures, and start() kwargs MAY change without
a deprecati

### 核心类

- `CronScheduler`: Axis-B trigger provider. Decides WHEN a due cron job fires.

    Required surface is intentionally m
- `InProcessCronScheduler`: Default provider: the historical in-process 60s ticker.

    ``start()`` blocks in the tick loop unt

### 核心函数

- `resolve_cron_scheduler()`: Return the active cron scheduler provider.

    Reads ``cron.provider`` from config. Empty/absent → 

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## __init__.py

**路径**: `cron\scripts\__init__.py`
**行数**: 2

### 功能描述

Scripts shipped with the cron subsystem (runnable via ``python3 -m cron.scripts.<name>``).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## classify_items.py

**路径**: `cron\scripts\classify_items.py`
**行数**: 227

### 功能描述

Classify candidate items by urgency/importance and emit only the urgent ones.

The proactive-monitor pattern: a fetch step (a watcher script, an inbox dump, a
feed) produces a list of candidate items; this script scores each with a cheap
LLM and prints ONLY the items at or above a threshold. Below-t

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: llm-client
**跨组件调用**: 是

---

## suggestion_catalog.py

**路径**: `cron\suggestion_catalog.py`
**行数**: 155

### 功能描述

Curated catalog of starter cron-job suggestions.

These are the built-in automations Hermes can offer a new user out of the box —
the ``catalog`` source of the unified suggestion surface. Each entry is a
ready-to-run ``cron.jobs.create_job`` spec wrapped as a suggestion; the user
accepts via ``/sugg

### 核心类

- `CatalogEntry`: A curated starter automation offered as a suggestion.

### 核心函数

- `classify_items_script_path()`: Absolute path to the urgency classifier script shipped with cron/.
- `seed_catalog_suggestions()`: Register catalog entries as pending suggestions.

    ``add_fn`` defaults to ``cron.suggestions.add_

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## suggestions.py

**路径**: `cron\suggestions.py`
**行数**: 258

### 功能描述

Suggested cron jobs — proposed automations the user accepts with one tap.

A *suggestion* is a ready-to-run cron job spec that Hermes surfaces to the
user, who accepts it (creates the real cron job) or dismisses it (latched so
it is never re-offered). This is the single surface every automation prop

### 核心函数

- `load_suggestions()`: Return all suggestion records (any status).
- `list_pending()`: Return pending suggestions in creation order (oldest first).
- `add_suggestion()`: Register a pending suggestion. Returns the record, or None if skipped.

    Skipped when: the source
- `get_suggestion()`: Resolve a suggestion by id, 1-based pending index, or title (exact).
- `dismiss_suggestion()`: Dismiss a suggestion (latched — never re-offered for its dedup_key).
- `accept_suggestion()`: Accept a suggestion: create the real cron job from its ``job_spec``.

    Returns the created cron j
- `clear_resolved()`: Drop accepted/dismissed records from disk. Returns the count removed.

    Pending suggestions and t

### 依赖关系

**依赖组件**: entry-points, state-management
**跨组件调用**: 是

---

