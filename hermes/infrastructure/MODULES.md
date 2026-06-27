# infrastructure 模块详细说明

本组件包含 79 个模块。

---

## evm_client.py

**路径**: `optional-skills\blockchain\evm\scripts\evm_client.py`
**行数**: 1509

### 功能描述

evm_client.py — EVM blockchain CLI tool for the Hermes Agent project.
Zero external dependencies. Uses stdlib only: urllib, json, argparse, time, os, sys, typing.

### 核心函数

- `hex_to_int()`
- `is_valid_address()`: Return True if `s` looks like a 20-byte hex Ethereum address.

    Does NOT validate EIP-55 checksum
- `is_valid_txhash()`: Return True if `s` looks like a 32-byte hex transaction hash.
- `require_address()`: Return `s` lowercased if valid, else exit with an error message.

    Centralizing validation here m
- `require_txhash()`: Return `s` lowercased if valid, else exit with an error message.
- `wei_to_native()`
- `gwei_from_wei()`
- `print_json()`
- `get_rpc_url()`
- `rpc_call()`
- `rpc_batch()`: Send a batch of JSON-RPC calls; returns list of results in same order.

    Auto-chunks at `batch_li
- `eth_call_erc20()`
- `decode_string()`: Decode ABI-encoded string from eth_call result.
- `decode_uint256()`
- `decode_uint8()`
- ... 还有 20 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## hyperliquid_client.py

**路径**: `optional-skills\blockchain\hyperliquid\scripts\hyperliquid_client.py`
**行数**: 1661

### 功能描述

Hyperliquid CLI Tool for Hermes Agent
-------------------------------------
Queries the Hyperliquid info endpoint for market and account data.
Uses only Python standard library - no external packages required.

Usage:
  python3 hyperliquid_client.py dexs
  python3 hyperliquid_client.py markets [--de

### 核心函数

- `run_dexs()`
- `run_markets()`
- `run_spots()`
- `run_candles()`
- `run_funding()`
- `run_l2()`
- `run_state()`
- `run_spot_balances()`
- `run_fills()`
- `run_orders()`
- `run_review()`
- `run_export()`
- `render_dexs()`
- `render_markets()`
- `render_spots()`
- ... 还有 11 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## solana_client.py

**路径**: `optional-skills\blockchain\solana\scripts\solana_client.py`
**行数**: 699

### 功能描述

Solana Blockchain CLI Tool for Hermes Agent
--------------------------------------------
Queries the Solana JSON-RPC API and CoinGecko for enriched on-chain data.
Uses only Python standard library — no external packages required.

Usage:
  python3 solana_client.py stats
  python3 solana_client.py wa

### 核心函数

- `rpc_batch()`: Send a batch of JSON-RPC requests (with retry on 429).
- `lamports_to_sol()`
- `print_json()`
- `fetch_prices()`: Fetch USD prices for mint addresses via CoinGecko (one per request).

    CoinGecko free tier doesn'
- `fetch_sol_price()`: Fetch current SOL price in USD via CoinGecko.
- `resolve_token_name()`: Look up token name and symbol from CoinGecko by mint address.

    Returns {"name": ..., "symbol": .
- `cmd_stats()`: Live Solana network: slot, epoch, TPS, supply, version, SOL price.
- `cmd_wallet()`: SOL balance + SPL token holdings with USD values.
- `cmd_tx()`: Full transaction details by signature.
- `cmd_token()`: SPL token metadata, supply, decimals, price, top holders.
- `cmd_activity()`: Recent transaction signatures for an address.
- `cmd_nft()`: NFTs owned by a wallet (amount=1 && decimals=0 heuristic).
- `cmd_whales()`: Scan the latest block for large SOL transfers.
- `cmd_price()`: Quick price lookup for a token by mint address or known symbol.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## bootstrap_pipeline.py

**路径**: `optional-skills\creative\kanban-video-orchestrator\scripts\bootstrap_pipeline.py`
**行数**: 500

### 功能描述

Bootstrap a video production kanban from a structured plan JSON.

Reads a plan.json describing the team + brief, expands templates from
../assets/, and writes a setup.sh that creates Hermes profiles and fires the
initial kanban task.

Profile-config patching, SOUL.md-per-profile, TEAM.md task-graph 

### 核心函数

- `load_template()`
- `validate_plan()`: Return a list of validation error strings; empty list = valid.
- `render_brief()`: Render brief.md from the plan.
- `render_team_md()`: Render TEAM.md from the team list + scene → tool mapping.
- `render_setup_sh()`: Render setup.sh from the plan.
- `render_soul_md()`: Render a profile's SOUL.md from a team member dict + plan context.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## monitor.py

**路径**: `optional-skills\creative\kanban-video-orchestrator\scripts\monitor.py`
**行数**: 196

### 功能描述

Monitor a running video-production kanban. Polls `hermes kanban list` and
`events` for a tenant and surfaces issues (stuck tasks, missing heartbeats,
repeated retries, dependency deadlocks).

Usage:
    monitor.py --tenant <project-slug> [--interval 30]

Outputs a periodic snapshot to stdout. Sends 

### 核心函数

- `hermes_available()`
- `kanban_list()`: Returns parsed task rows. Falls back to plain stdout parsing if JSON
    output isn't supported by t
- `kanban_show()`
- `detect_issues()`: Return a list of issue strings, one per concern.
- `snapshot()`
- `print_snapshot()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## generate_meme.py

**路径**: `optional-skills\creative\meme-generation\scripts\generate_meme.py`
**行数**: 471

### 功能描述

Generate a meme image by overlaying text on a template.

Usage:
    python generate_meme.py <template_id_or_name> <output_path> <text1> [text2] [text3] [text4]

Example:
    python generate_meme.py drake /tmp/meme.png "Writing tests" "Shipping to prod and hoping"
    python generate_meme.py "Disaste

### 核心函数

- `load_curated_templates()`: Load templates with hand-tuned text field positions.
- `fetch_imgflip_templates()`: Fetch popular meme templates from imgflip API. Cached for 24h.
- `resolve_template()`: Resolve a template by curated ID, imgflip name, or imgflip ID.

    Returns dict with: name, url, fi
- `get_template_image()`: Download a template image, caching it locally.
- `find_font()`: Find a bold font for meme text. Tries Impact, then falls back.
- `draw_outlined_text()`: Draw white text with black outline, auto-scaled to fit max_width.
- `generate_meme()`: Generate a meme from a template and save it. Returns the path.
- `generate_from_image()`: Generate a meme from a custom image (e.g. AI-generated). Returns the path.
- `list_templates()`: Print curated templates with custom positioning.
- `search_templates()`: Search imgflip templates by name.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `optional-skills\creative\pixel-art\scripts\__init__.py`
**行数**: 1

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## palettes.py

**路径**: `optional-skills\creative\pixel-art\scripts\palettes.py`
**行数**: 168

### 功能描述

Named RGB palettes for pixel_art() and pixel_art_video().

Palette RGB values sourced from pixel-art-studio (MIT License)
https://github.com/Synero/pixel-art-studio — see ATTRIBUTION.md.

### 核心函数

- `build_palette_image()`: Build a 1x1 PIL 'P'-mode image with the named palette for Image.quantize(palette=...).

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pixel_art.py

**路径**: `optional-skills\creative\pixel-art\scripts\pixel_art.py`
**行数**: 163

### 功能描述

Pixel art converter — Floyd-Steinberg dithering with preset or named palette.

Named hardware palettes (NES, GameBoy, PICO-8, C64, etc.) ported from
pixel-art-studio (MIT) — see ATTRIBUTION.md.

Usage (import):
    from pixel_art import pixel_art
    pixel_art("in.png", "out.png", preset="arcade")
 

### 核心函数

- `pixel_art()`: Convert an image to retro pixel art.

    Args:
        input_path: path to source image
        out
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pixel_art_video.py

**路径**: `optional-skills\creative\pixel-art\scripts\pixel_art_video.py`
**行数**: 346

### 功能描述

Pixel art video — overlay procedural animations onto a source image.

Takes any image (typically pre-processed with pixel_art()) and overlays
animated pixel effects (stars, rain, fireflies, etc.), then encodes to MP4
(and optionally GIF) via ffmpeg.

Scene animations ported from pixel-art-studio (MI

### 核心函数

- `init_stars()`
- `draw_stars()`
- `init_fireflies()`
- `draw_fireflies()`
- `init_leaves()`
- `draw_leaves()`
- `init_dust_motes()`
- `draw_dust_motes()`
- `init_sparkles()`
- `draw_sparkles()`
- `init_rain()`
- `draw_rain()`
- `init_lightning()`
- `draw_lightning()`
- `init_bubbles()`
- ... 还有 11 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _watermark.py

**路径**: `optional-skills\devops\watchers\scripts\_watermark.py`
**行数**: 149

### 功能描述

Shared watermark helper used by the three watcher scripts.

A watermark is just a JSON file that records the IDs we've seen on previous
runs, so the next run only emits items we haven't seen before.

Contract:
- First run: record all IDs from the fetched batch, emit nothing.
- Subsequent runs: emit 

### 核心类

- `Watermark`: Per-watcher state. Persisted to <state_dir>/<name>.json.

### 核心函数

- `format_items_as_markdown()`: Render a list of items as Markdown for cron delivery.

    One heading per item + its URL + optional

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## watch_github.py

**路径**: `optional-skills\devops\watchers\scripts\watch_github.py`
**行数**: 170

### 功能描述

Watch GitHub activity — issues, pulls, releases, or commits — with dedup.

Usage (via cron with --no-agent):

    hermes cron create hermes-issues \
      --schedule "*/5 * * * *" --no-agent \
      --script "$HERMES_HOME/skills/devops/watchers/scripts/watch_github.py" \
      --script-args "--name 

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## watch_http_json.py

**路径**: `optional-skills\devops\watchers\scripts\watch_http_json.py`
**行数**: 132

### 功能描述

Watch any JSON endpoint that returns a list of objects; dedup by ID field.

Usage (via cron with --no-agent):

    hermes cron create api-events \
      --schedule "*/1 * * * *" --no-agent \
      --script "$HERMES_HOME/skills/devops/watchers/scripts/watch_http_json.py" \
      --script-args "--name

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## watch_rss.py

**路径**: `optional-skills\devops\watchers\scripts\watch_rss.py`
**行数**: 122

### 功能描述

Watch an RSS 2.0 or Atom feed; print new items to stdout, silent on empty.

Usage (via cron with --no-agent):

    hermes cron create my-feed \
      --schedule "*/15 * * * *" --no-agent \
      --script "$HERMES_HOME/skills/devops/watchers/scripts/watch_rss.py" \
      --script-args "--name hn --ur

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## validate_dcf.py

**路径**: `optional-skills\finance\dcf-model\scripts\validate_dcf.py`
**行数**: 292

### 功能描述

DCF Model Validation Script
Validates Excel DCF models for formula errors and common DCF mistakes

### 核心类

- `DCFModelValidator`: Validates DCF models for errors and quality issues

### 核心函数

- `validate_dcf_model()`: Validate a DCF model Excel file

    Args:
        excel_path: Path to Excel DCF model

    Returns:
- `main()`: Command-line interface

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## recalc.py

**路径**: `optional-skills\finance\excel-author\scripts\recalc.py`
**行数**: 89

### 功能描述

Recalculate an .xlsx file's formulas using LibreOffice headless.

Usage: python recalc.py <path.xlsx> [timeout_seconds]

openpyxl writes formula strings but does not compute them. Downstream scripts
that open the file with data_only=True get None for every formula cell until
something has actually c

### 核心函数

- `find_libreoffice()`
- `recalc()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## stocks_client.py

**路径**: `optional-skills\finance\stocks\scripts\stocks_client.py`
**行数**: 756

### 功能描述

stocks_client.py - Stock market data CLI tool for the Hermes Agent project.
Zero external dependencies - Python stdlib only.

### 核心函数

- `print_json()`
- `fmt_price()`
- `fmt_large()`: Format large numbers with B/T suffix.
- `fmt_pct()`
- `safe_get()`: Safely traverse nested dict.
- `ts_to_date()`: Convert Unix timestamp to ISO date string.
- `fetch_url()`: Fetch a URL, parse JSON, retry on transient errors.
- `yf_url()`: Build a Yahoo Finance URL, injecting crumb if available.
- `yf_chart()`
- `yf_search()`
- `yf_quote_summary()`: Fetch detailed quote summary (quoteSummary) for PE, market cap, etc.
- `av_overview()`
- `extract_quote_from_chart()`: Extract current quote info from v8 chart response.
- `extract_quote_summary_fields()`: Extract PE, market cap, etc. from quoteSummary response.
- `cmd_quote()`
- ... 还有 6 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## body_calc.py

**路径**: `optional-skills\health\fitness-nutrition\scripts\body_calc.py`
**行数**: 210

### 功能描述

body_calc.py — All-in-one fitness calculator.

Subcommands:
  bmi      <weight_kg> <height_cm>
  tdee     <weight_kg> <height_cm> <age> <M|F> <activity 1-5>
  1rm      <weight> <reps>
  macros   <tdee_kcal> <cut|maintain|bulk>
  bodyfat  <M|F> <neck_cm> <waist_cm> [hip_cm] <height_cm>

No external d

### 核心函数

- `bmi()`
- `tdee()`
- `one_rep_max()`
- `macros()`
- `bodyfat()`
- `usage()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## nutrition_search.py

**路径**: `optional-skills\health\fitness-nutrition\scripts\nutrition_search.py`
**行数**: 85

### 功能描述

nutrition_search.py — Search USDA FoodData Central for nutrition info.

Usage:
  python3 nutrition_search.py "chicken breast"
  python3 nutrition_search.py "rice" "eggs" "broccoli"
  echo -e "oats\nbanana\nwhey protein" | python3 nutrition_search.py -

Reads USDA_API_KEY from environment, falls back

### 核心函数

- `search()`
- `display()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## scaffold_fastmcp.py

**路径**: `optional-skills\mcp\fastmcp\scripts\scaffold_fastmcp.py`
**行数**: 57

### 功能描述

Copy a FastMCP starter template into a working file.

### 核心函数

- `list_templates()`
- `render_template()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## api_wrapper.py

**路径**: `optional-skills\mcp\fastmcp\templates\api_wrapper.py`
**行数**: 55

### 功能描述

Check whether the upstream API is reachable.

### 核心函数

- `health_check()`: Check whether the upstream API is reachable.
- `get_resource()`: Fetch one resource by ID from the upstream API.
- `search_resources()`: Search upstream resources by query string.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## database_server.py

**路径**: `optional-skills\mcp\fastmcp\templates\database_server.py`
**行数**: 78

### 功能描述

List user-defined SQLite tables.

### 核心函数

- `list_tables()`: List user-defined SQLite tables.
- `describe_table()`: Describe columns for a SQLite table.
- `query()`: Run a read-only SELECT query and return rows plus column names.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## file_processor.py

**路径**: `optional-skills\mcp\fastmcp\templates\file_processor.py`
**行数**: 56

### 功能描述

Return basic metadata and a preview for a UTF-8 text file.

### 核心函数

- `summarize_text_file()`: Return basic metadata and a preview for a UTF-8 text file.
- `search_text_file()`: Find matching lines in a UTF-8 text file.
- `read_file_resource()`: Expose a text file as a resource.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## openclaw_to_hermes.py

**路径**: `optional-skills\migration\openclaw-migration\scripts\openclaw_to_hermes.py`
**行数**: 3137

### 功能描述

OpenClaw -> Hermes migration helper.

This script migrates the parts of an OpenClaw user footprint that map cleanly
into Hermes Agent, archives selected unmapped docs for manual review, and
reports exactly what was skipped and why.

### 核心类

- `ItemResult`
- `Migrator`

### 核心函数

- `parse_selection_values()`
- `resolve_selected_options()`
- `sha256_file()`
- `read_text()`
- `normalize_text()`
- `ensure_parent()`
- `resolve_secret_input()`: Resolve an OpenClaw SecretInput value to a plain string.

    SecretInput can be:
    - A plain stri
- `load_yaml_file()`
- `dump_yaml_file()`
- `parse_env_file()`
- `save_env_file()`
- `backup_existing()`
- `rebrand_text()`: Replace OpenClaw / ClawdBot / MoltBot brand names with Hermes.

    Preserves case so filesystem-pat
- `parse_existing_memory_entries()`
- `extract_markdown_entries()`
- ... 还有 6 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## basic_grpo_training.py

**路径**: `optional-skills\mlops\training\trl-fine-tuning\templates\basic_grpo_training.py`
**行数**: 229

### 功能描述

Basic GRPO Training Template
=============================

A minimal, production-ready template for GRPO training with TRL.
Adapt this for your specific task by modifying:
1. Dataset loading (get_dataset function)
2. Reward functions (reward_*_func)
3. System prompt (SYSTEM_PROMPT)
4. Hyperparamete

### 核心函数

- `get_dataset()`: Load and prepare your dataset.

    Returns: Dataset with columns:
    - 'prompt': List[Dict] with r
- `extract_xml_tag()`: Extract content between XML tags.
- `extract_answer()`: Extract the final answer from structured output.
- `correctness_reward_func()`: Reward correct answers.
    Weight: 2.0 (highest priority)
- `format_reward_func()`: Reward proper XML format.
    Weight: 0.5
- `incremental_format_reward_func()`: Incremental reward for partial format compliance.
    Weight: up to 0.5
- `setup_model_and_tokenizer()`: Load model and tokenizer with optimizations.
- `get_peft_config()`: LoRA configuration for parameter-efficient training.
- `main()`: Main training function.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## canvas_api.py

**路径**: `optional-skills\productivity\canvas\scripts\canvas_api.py`
**行数**: 161

### 功能描述

Canvas LMS API CLI for Hermes Agent.

A thin CLI wrapper around the Canvas REST API.
Authenticates using a personal access token from environment variables.

Usage:
  python canvas_api.py list_courses [--per-page N] [--enrollment-state STATE]
  python canvas_api.py list_assignments COURSE_ID [--per-

### 核心函数

- `list_courses()`: List enrolled courses.
- `list_assignments()`: List assignments for a course.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## memento_cards.py

**路径**: `optional-skills\productivity\memento-flashcards\scripts\memento_cards.py`
**行数**: 354

### 功能描述

Memento card storage, spaced-repetition engine, and CSV I/O.

Stdlib-only. All output is JSON for agent parsing.
Data file: $HERMES_HOME/skills/productivity/memento-flashcards/data/cards.json

### 核心函数

- `cmd_add()`
- `cmd_add_quiz()`
- `cmd_due()`
- `cmd_rate()`
- `cmd_list()`
- `cmd_stats()`
- `cmd_export()`
- `cmd_import()`
- `cmd_delete()`
- `cmd_delete_collection()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## youtube_quiz.py

**路径**: `optional-skills\productivity\memento-flashcards\scripts\youtube_quiz.py`
**行数**: 89

### 功能描述

Fetch YouTube transcripts for Memento quiz generation.

Requires: pip install youtube-transcript-api
The quiz question *generation* is done by the agent's LLM — this script only fetches transcripts.

### 核心函数

- `cmd_fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## telephony.py

**路径**: `optional-skills\productivity\telephony\scripts\telephony.py`
**行数**: 1344

### 功能描述

Telephony helper for the Hermes optional telephony skill.

Capabilities:
- Persist telephony provider credentials to the Hermes .env file ($HERMES_HOME/.env)
- Search for, buy, and remember Twilio phone numbers
- Make direct Twilio calls (TwiML <Say> or <Play>)
- Send SMS / MMS via Twilio
- Poll inb

### 核心类

- `TelephonyError`: Domain-specific failure surfaced to the skill/user.
- `OwnedTwilioNumber`

### 核心函数

- `diagnose()`
- `save_twilio()`
- `save_bland()`
- `save_vapi()`
- `main()`

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## parrot_openrouter.py

**路径**: `optional-skills\research\darwinian-evolver\scripts\parrot_openrouter.py`
**行数**: 219

### 功能描述

parrot_openrouter: same as the upstream `parrot` example but the LLM call goes
through OpenRouter (OpenAI SDK) instead of Anthropic native. Lets us run an
end-to-end evolution with whatever model the user already has paid access to.

Run with:
    uv --project darwinian_evolver run python parrot_ope

### 核心类

- `ParrotOrganism`
- `ParrotEvaluationFailureCase`
- `ImproveParrotMutator`
- `ParrotEvaluator`

### 核心函数

- `make_problem()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## show_snapshot.py

**路径**: `optional-skills\research\darwinian-evolver\scripts\show_snapshot.py`
**行数**: 93

### 功能描述

show_snapshot.py — Dump the population from a darwinian-evolver snapshot pickle.

Usage:
    python show_snapshot.py PATH/TO/iteration_N.pkl [--field prompt_template]

The script is intentionally Organism-agnostic: it walks `org.__dict__` and prints
all str fields. By default it shows `prompt_templa

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## custom_problem_template.py

**路径**: `optional-skills\research\darwinian-evolver\templates\custom_problem_template.py`
**行数**: 241

### 功能描述

Template: a custom darwinian-evolver problem.

Copy this file, fill in the THREE marked spots (Organism, Evaluator, Mutator),
then run it as a driver script. The skeleton handles all the wiring so you only
write the domain-specific logic.

To run:
    cd ~/.hermes/cache/darwinian-evolver/darwinian_e

### 核心类

- `MyOrganism`
- `MyFailureCase`
- `MyEvaluator`
- `MyMutator`

### 核心函数

- `make_problem()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## domain_intel.py

**路径**: `optional-skills\research\domain-intel\scripts\domain_intel.py`
**行数**: 398

### 功能描述

Domain Intelligence — Passive OSINT via Python stdlib.

Usage:
    python domain_intel.py subdomains example.com
    python domain_intel.py ssl example.com
    python domain_intel.py whois example.com
    python domain_intel.py dns example.com
    python domain_intel.py available example.com
    pyt

### 核心函数

- `subdomains()`: Find subdomains via Certificate Transparency logs.
- `check_ssl()`: Inspect the TLS certificate of a host.
- `whois_lookup()`: Query WHOIS servers for domain registration info.
- `dns_records()`: Resolve DNS records using system DNS + Google DoH.
- `check_available()`: Check domain availability using passive signals (DNS + WHOIS + SSL).
- `bulk_check()`: Run multiple checks across multiple domains in parallel.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## chembl_target.py

**路径**: `optional-skills\research\drug-discovery\scripts\chembl_target.py`
**行数**: 54

### 功能描述

chembl_target.py — Search ChEMBL for a target and retrieve top active compounds.
Usage: python3 chembl_target.py "EGFR" --min-pchembl 7 --limit 20
No external dependencies.

### 核心函数

- `get()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## ro5_screen.py

**路径**: `optional-skills\research\drug-discovery\scripts\ro5_screen.py`
**行数**: 45

### 功能描述

ro5_screen.py — Batch Lipinski Ro5 + Veber screening via PubChem API.
Usage: python3 ro5_screen.py aspirin ibuprofen paracetamol
No external dependencies beyond stdlib.

### 核心函数

- `fetch()`
- `check()`
- `report()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _http.py

**路径**: `optional-skills\research\osint-investigation\scripts\_http.py`
**行数**: 83

### 功能描述

Tiny stdlib HTTP helper used by fetch_*.py scripts.

Provides polite retry + JSON convenience + User-Agent enforcement.

### 核心函数

- `get()`: GET with retry on 5xx and Retry-After honoring.

    429 (rate-limit) is raised IMMEDIATELY with a c
- `get_json()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _normalize.py

**路径**: `optional-skills\research\osint-investigation\scripts\_normalize.py`
**行数**: 68

### 功能描述

Shared entity-name normalization helpers (stdlib-only).

Used by entity_resolution.py and timing_analysis.py.

### 核心函数

- `normalize_name()`: Standard normalization: uppercase, strip suffixes, drop punctuation.
- `normalize_aggressive()`: Aggressive normalization: sorted unique tokens (word-bag).
- `name_tokens()`: Token set used for overlap matching.
- `token_overlap_ratio()`: Return (jaccard-like ratio, shared token count) over min-len tokens.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## build_findings.py

**路径**: `optional-skills\research\osint-investigation\scripts\build_findings.py`
**行数**: 222

### 功能描述

Build a structured findings.json with evidence chains (stdlib-only).

Aggregates cross_links.csv (entity_resolution output) and an optional
timing.json (timing_analysis output) into a single evidence-chain document.

Output structure:
    {
      "metadata": {...},
      "findings": [
        {
    

### 核心函数

- `build_findings()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## entity_resolution.py

**路径**: `optional-skills\research\osint-investigation\scripts\entity_resolution.py`
**行数**: 229

### 功能描述

Cross-source entity resolution (stdlib-only).

Given two CSV files with name columns, find candidate matches using three
tiers of normalization:

  1. exact          — normalized strings equal
  2. fuzzy          — sorted-token (word-bag) match
  3. token_overlap  — >=60% Jaccard overlap on >=4-char

### 核心函数

- `resolve()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_courtlistener.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_courtlistener.py`
**行数**: 150

### 功能描述

Search court records via CourtListener (Free Law Project).

Covers ~10M federal and state court opinions, plus PACER docket data
where available. Public REST API v4 supports anonymous read access for
search; some endpoints require a token (free at courtlistener.com).

Set COURTLISTENER_TOKEN to auth

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_gdelt.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_gdelt.py`
**行数**: 162

### 功能描述

Search the GDELT 2.0 DOC API for news mentions.

GDELT monitors world news in 100+ languages and indexes the full text.
Free, anonymous, ~15-minute update frequency. Covers ~2015→present.

Useful for surfacing news mentions of a person, company, or topic across
international media — much wider net t

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_icij_offshore.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_icij_offshore.py`
**行数**: 235

### 功能描述

Search ICIJ Offshore Leaks via the bulk CSV database.

The old reconcile endpoint (https://offshoreleaks.icij.org/reconcile) returns
404 — ICIJ has removed it. The remaining stable access path is the public
bulk download:

    https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zi

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_nyc_acris.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_nyc_acris.py`
**行数**: 204

### 功能描述

Search NYC property records via ACRIS (Automated City Register Information System).

Uses the city's Socrata-backed open data API. No auth required for read access.

Datasets:
  bnx9-e6tj — Real Property Master (one row per recorded document)
  636b-3b5g — Real Property Parties (names — grantor, gra

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_ofac_sdn.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_ofac_sdn.py`
**行数**: 176

### 功能描述

Fetch OFAC SDN list (CSV format) and normalize.

Public endpoint: https://www.treasury.gov/ofac/downloads/sdn.csv
Format reference: https://ofac.treasury.gov/specially-designated-nationals-and-blocked-persons-list-sdn-human-readable-lists

The SDN CSV uses a specific 12-column format with no header 

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_opencorporates.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_opencorporates.py`
**行数**: 192

### 功能描述

Search OpenCorporates company registry data.

OpenCorporates aggregates ~200M companies from 130+ jurisdictions. The
public API requires an API token (free tier: 500 calls/month). Set
OPENCORPORATES_API_TOKEN in env or pass --token.

Without a token, this script falls back to scraping the public HTM

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_sec_edgar.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_sec_edgar.py`
**行数**: 185

### 功能描述

Fetch SEC EDGAR filings index for a given CIK or company name.

SEC requires a User-Agent header with contact info. Set SEC_USER_AGENT,
e.g. SEC_USER_AGENT="Research example@example.com".

Filings JSON is published at:
    https://data.sec.gov/submissions/CIK<10-digit-padded>.json

Company lookup us

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_senate_ld.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_senate_ld.py`
**行数**: 147

### 功能描述

Fetch Senate Lobbying Disclosure (LD-1 / LD-2) filings.

Anonymous: 120 req/hour. Token (SENATE_LDA_TOKEN): 1200 req/hour.

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_usaspending.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_usaspending.py`
**行数**: 171

### 功能描述

Fetch federal contracts/awards from USAspending.gov API v2.

No auth required. POST to /api/v2/search/spending_by_award/ with filters.

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_wayback.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_wayback.py`
**行数**: 143

### 功能描述

Search the Internet Archive Wayback Machine via the CDX server.

The CDX API indexes ~900B+ archived web pages. Anonymous read access,
no auth required. Useful for finding deleted / changed pages by URL,
domain, or substring match.

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_wikipedia.py

**路径**: `optional-skills\research\osint-investigation\scripts\fetch_wikipedia.py`
**行数**: 267

### 功能描述

Search Wikipedia + Wikidata for an entity (person, company, place, concept).

Two free APIs:
  - Wikipedia OpenSearch + REST summary endpoint for narrative bio
  - Wikidata SPARQL endpoint for structured facts (birth, employer, awards, etc.)

Both are anonymous-access. Useful for resolving who-is-th

### 核心函数

- `fetch()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## timing_analysis.py

**路径**: `optional-skills\research\osint-investigation\scripts\timing_analysis.py`
**行数**: 253

### 功能描述

Permutation test for donation/contract timing correlation (stdlib-only).

For each (donor, vendor) pair, compute the mean number of days between each
donation and the nearest contract award. Then shuffle contract award dates
N times within the observation window and compute the same statistic. The
o

### 核心函数

- `parse_date()`
- `analyze()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## auto_jailbreak.py

**路径**: `optional-skills\security\godmode\scripts\auto_jailbreak.py`
**行数**: 772

### 功能描述

Auto-Jailbreak Pipeline

Automatically tests jailbreak techniques against the current model,
finds what works, and locks it in by writing config.yaml + prefill.json.

Usage in execute_code:
    exec(open(os.path.expanduser(
        os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.he

### 核心函数

- `auto_jailbreak()`: Auto-jailbreak pipeline.
    
    1. Detects model family
    2. Tries strategies in order (model-sp
- `undo_jailbreak()`: Remove jailbreak settings from config.yaml and delete prefill.json.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## godmode_race.py

**路径**: `optional-skills\security\godmode\scripts\godmode_race.py`
**行数**: 531

### 功能描述

ULTRAPLINIAN Multi-Model Racing Engine
Ported from G0DM0D3 (elder-plinius/G0DM0D3).

Queries multiple models in parallel via OpenRouter, scores responses
on quality/filteredness/speed, returns the best unfiltered answer.

Usage in execute_code:
    exec(open(os.path.join(os.environ.get("HERMES_HOME"

### 核心函数

- `is_refusal()`: Check if response is a refusal.
- `count_hedges()`: Count hedge/disclaimer patterns in content.
- `score_response()`: Score a response. Higher is better.
    
    Returns dict with: score, is_refusal, hedge_count
- `race_models()`: Race multiple models against a query, return the best unfiltered response.
    
    Args:
        qu
- `race_godmode_classic()`: Race the 5 GODMODE CLASSIC combos — each with its own model + jailbreak template.
    
    Each comb

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## load_godmode.py

**路径**: `optional-skills\security\godmode\scripts\load_godmode.py`
**行数**: 46

### 功能描述

Loader for G0DM0D3 scripts. Handles the exec-scoping issues.

Usage in execute_code:
    exec(open(os.path.expanduser(
        os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "skills/red-teaming/godmode/scripts/load_godmode.py")
    )).read())
    
    # Now all function

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## parseltongue.py

**路径**: `optional-skills\security\godmode\scripts\parseltongue.py`
**行数**: 551

### 功能描述

Parseltongue v4 — Input Obfuscation Engine
Ported from G0DM0D3 (elder-plinius/G0DM0D3) JavaScript to Python.

33 text obfuscation techniques across 3 tiers for bypassing
LLM input-side safety classifiers.

Usage:
    # As a standalone script
    python parseltongue.py "How do I hack a WiFi network?"

### 核心函数

- `to_braille()`: Convert text to braille Unicode characters.
- `to_leetspeak()`: Convert text to leetspeak.
- `to_bubble()`: Convert text to bubble/circled text.
- `to_morse()`: Convert text to Morse code.
- `detect_triggers()`: Detect trigger words in text. Returns list of found triggers.
- `obfuscate_query()`: Apply one obfuscation technique to trigger words in a query.
    
    Args:
        query: The input
- `generate_variants()`: Generate obfuscated variants of a query up to the tier limit.
    
    Args:
        query: Input te
- `escalate_encoding()`: Get an encoding-escalated version of the query.
    
    Args:
        query: Input text
        lev

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## evidence-store.py

**路径**: `optional-skills\security\oss-forensics\scripts\evidence-store.py`
**行数**: 314

### 功能描述

OSS Forensics Evidence Store Manager
Manages a JSON-based evidence store for forensic investigations.

Commands:
  add      - Add a piece of evidence
  list     - List all evidence (optionally filter by type or actor)
  verify   - Re-check SHA-256 hashes for integrity
  query    - Search evidence by

### 核心类

- `EvidenceStore`

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## parse_deploy_output.py

**路径**: `optional-skills\web-development\cloudflare-temporary-deploy\scripts\parse_deploy_output.py`
**行数**: 123

### 功能描述

Parse `wrangler deploy --temporary` output into structured JSON.

Reads wrangler's stdout/stderr from STDIN and extracts the live workers.dev
URL, the claim URL, the temporary account name/state, the claim window, and
whether a deploy actually happened. Stdlib only — no dependencies.

Usage:
    npx

### 核心函数

- `parse()`: Extract deploy facts from wrangler output text.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## analyze_livetest.py

**路径**: `scripts\analyze_livetest.py`
**行数**: 115

### 功能描述

Compare enabled vs disabled runs and produce a readable report.

Reads scripts/out/_summary.json and the per-scenario JSONs, prints a side-by-
side comparison of what happened, and flags anomalies.

### 核心函数

- `load_record()`
- `fmt_tool_seq()`
- `fmt_bridge_seq()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## benchmark_browser_eval.py

**路径**: `scripts\benchmark_browser_eval.py`
**行数**: 139

### 功能描述

Quick benchmark: subprocess eval vs supervisor-WS eval.

Runs both paths against the same live Chrome and prints a comparison table.
Not a pytest — a script you run manually for the PR description.

Usage:
    .venv/bin/python scripts/benchmark_browser_eval.py [--iterations N]

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: tool-system
**跨组件调用**: 是

---

## build_model_catalog.py

**路径**: `scripts\build_model_catalog.py`
**行数**: 96

### 功能描述

Build the Hermes Model Catalog — a centralized JSON manifest of curated models.

This script reads the in-repo hardcoded curated lists (``OPENROUTER_MODELS``,
``_PROVIDER_MODELS["nous"]``) and writes them to a JSON manifest that the
Hermes CLI fetches at runtime. Publishing the catalog through the d

### 核心函数

- `build_catalog()`
- `main()`

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## build_skills_index.py

**路径**: `scripts\build_skills_index.py`
**行数**: 426

### 功能描述

Build the Hermes Skills Index — a centralized JSON catalog of all skills.

This script crawls every skill source (skills.sh, GitHub taps, official,
clawhub, lobehub, claude-marketplace) and writes a JSON index with resolved
GitHub paths. The index is served as a static file on the docs site so that


### 核心函数

- `crawl_source()`: Crawl a single source and return skill dicts.
- `crawl_skills_sh()`: Crawl skills.sh via its sitemap to enumerate the full catalog (~20k entries).

    Previously walked
- `batch_resolve_paths()`: Resolve GitHub paths for skills.sh entries using batch tree lookups.

    Instead of resolving each 
- `main()`

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## check-windows-footguns.py

**路径**: `scripts\check-windows-footguns.py`
**行数**: 633

### 功能描述

Grep-based checker for Windows cross-platform footguns.

Flags common patterns that break silently on Windows. Run before PRs —
cheap, fast, catches regressions in a codebase that runs on three OSes.

Usage:
    # Scan staged changes (default when run from a git checkout)
    python scripts/check-wi

### 核心类

- `Footgun`: A Windows cross-platform footgun pattern.

### 核心函数

- `should_scan_file()`: Return True if this file is in scope for the checker.
- `iter_files()`
- `scan_file()`: Return a list of (line_number, line, footgun) for unsuppressed matches.
- `get_staged_files()`: Return paths staged in the current git index. Empty on non-git trees.
- `get_diff_files()`: Return paths modified vs. the given git ref.
- `parse_args()`
- `print_rules()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## check_subprocess_stdin.py

**路径**: `scripts\check_subprocess_stdin.py`
**行数**: 178

### 功能描述

Check that subprocess calls in TUI-context code specify stdin=.

When Hermes runs in TUI mode, the gateway child process communicates with
the Node.js parent over a JSON-RPC protocol on stdin. Subprocess calls that
inherit this fd can cause the gateway to exit with stdin EOF during tool
execution (i

### 核心函数

- `find_subprocess_calls()`: Find all subprocess.run/Popen calls missing stdin= in content.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## classify_changes.py

**路径**: `scripts\ci\classify_changes.py`
**行数**: 107

### 功能描述

Classify a PR's changed files into CI work lanes.

Reads newline-separated changed paths on stdin and writes ``key=value``
booleans (one per lane) to ``$GITHUB_OUTPUT`` and stdout. The
``detect-changes`` composite action consumes them so steps gate on
``if: steps.changes.outputs.<lane> == 'true'``.


### 核心函数

- `classify()`: Map changed paths to ``{lane: should_run}``.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## contributor_audit.py

**路径**: `scripts\contributor_audit.py`
**行数**: 478

### 功能描述

Contributor Audit Script

Cross-references git authors, Co-authored-by trailers, and salvaged PR
descriptions to find any contributors missing from the release notes.

Usage:
    # Basic audit since a tag
    python scripts/contributor_audit.py --since-tag v2026.4.8

    # Audit with a custom endpoi

### 核心函数

- `is_ignored()`: Return True if this contributor is a bot/AI/machine account.
- `git()`: Run a git command and return stdout.
- `gh_pr_list()`: Fetch merged PRs from GitHub using the gh CLI.

    Returns a list of dicts with keys: number, title
- `collect_commit_authors()`: Collect contributors from git commit authors.

    Returns:
        contributors: dict mapping githu
- `collect_co_authors()`: Collect contributors from Co-authored-by trailers in commit messages.

    Returns:
        contribu
- `collect_salvaged_contributors()`: Scan merged PR bodies for salvage/cherry-pick/co-author attribution.

    Uses the gh CLI to fetch P
- `check_release_file()`: Check which contributors are mentioned in the release file.

    Returns:
        mentioned: set of 
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## discord-voice-doctor.py

**路径**: `scripts\discord-voice-doctor.py`
**行数**: 397

### 功能描述

Discord Voice Doctor — diagnostic tool for voice channel support.

Checks all dependencies, configuration, and bot permissions needed
for Discord voice mode to work correctly.

Usage:
    python scripts/discord-voice-doctor.py
    .venv/bin/python scripts/discord-voice-doctor.py

### 核心函数

- `mask()`: Mask sensitive value: show only first 4 chars.
- `check()`
- `warn()`
- `section()`
- `check_packages()`: Check Python package dependencies. Returns True if all critical deps OK.
- `check_system_tools()`: Check system-level tools (opus, ffmpeg). Returns True if all OK.
- `check_env_vars()`: Check environment variables. Returns (ok, token, groq_key, eleven_key).
- `check_config()`: Check hermes config.yaml.
- `check_bot_permissions()`: Check bot permissions via Discord API. Returns True if all OK.
- `main()`

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## docker_config_migrate.py

**路径**: `scripts\docker_config_migrate.py`
**行数**: 96

### 功能描述

Run Docker boot-time config migrations safely.

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## install_psutil_android.py

**路径**: `scripts\install_psutil_android.py`
**行数**: 103

### 功能描述

Install psutil on Termux/Android by patching upstream platform detection.

psutil's setup currently gates Linux sources behind
``sys.platform.startswith('linux')``. On Termux, Python reports
``sys.platform == 'android'``, so ``pip install psutil`` aborts with
"platform android is not supported" — ev

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## keystroke_diagnostic.py

**路径**: `scripts\keystroke_diagnostic.py`
**行数**: 82

### 功能描述

Diagnose how prompt_toolkit identifies keystrokes in the current terminal.

Useful when adding a keybinding to Hermes (or any prompt_toolkit app) and you
need to know what the terminal actually delivers — particularly on Windows,
where terminals can collapse, intercept, or silently remap key combina

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## lint_diff.py

**路径**: `scripts\lint_diff.py`
**行数**: 208

### 功能描述

Diff ruff + ty diagnostic reports between two git refs.

Produces a Markdown summary suitable for `$GITHUB_STEP_SUMMARY` and for PR
comments. Compares issues by a stable key (file, rule, line) so line-only
shifts from unrelated edits are treated as the same issue.

Usage:
    lint_diff.py \
        

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## profile-tui.py

**路径**: `scripts\profile-tui.py`
**行数**: 626

### 功能描述

Drive the Hermes TUI under HERMES_DEV_PERF and summarize the pipeline.

Usage:
  scripts/profile-tui.py [--session SID] [--hold KEY] [--seconds N] [--rate HZ]

Defaults: picks the session with the most messages, holds PageUp for 8s at
~30 Hz (matching xterm key-repeat), summarizes ~/.hermes/perf.log

### 核心函数

- `pick_longest_session()`
- `drain()`: Read whatever's available from fd within `timeout`, then return.
- `hold_key()`: Write `seq` to fd at ~rate_hz for `seconds`. Returns keystrokes sent.
- `summarize()`: Parse perf.log, keep only events newer than since_ts_ms, return stats.
- `pct()`
- `format_report()`
- `key_metrics()`: Flatten the report into a dict of scalar metrics for A/B diffing.
- `format_diff()`: Render a side-by-side A/B comparison table.
- `run_once()`
- `main()`
- `loop_mode()`: Watch source files, rebuild, rerun, print A/B diff against previous run.

    Keeps a rolling 'previ
- `wait_for_change()`: Poll every 1s until a watched file's mtime changes. Debounced 500ms.

### 依赖关系

**依赖组件**: gateway, state-management
**跨组件调用**: 是

---

## release.py

**路径**: `scripts\release.py`
**行数**: 2311

### 功能描述

Hermes Agent Release Script

Generates changelogs and creates GitHub releases with CalVer tags.

Usage:
    # Preview changelog (dry run)
    python scripts/release.py

    # Preview with semver bump
    python scripts/release.py --bump minor

    # Create the release
    python scripts/release.py -

### 核心函数

- `git()`: Run a git command and return stdout.
- `git_result()`: Run a git command and return the full CompletedProcess.
- `get_last_tag()`: Get the most recent CalVer tag.
- `next_available_tag()`: Return a tag/calver pair, suffixing same-day releases when needed.
- `get_current_version()`: Read current semver from __init__.py.
- `bump_version()`: Bump a semver version string.
- `update_version_files()`: Update version strings in source files.
- `build_release_artifacts()`: Build sdist/wheel artifacts for the current release.

    Tries ``uv build`` first (matching the CI 
- `resolve_author()`: Resolve a git author to a GitHub @mention.
- `categorize_commit()`: Categorize a commit by its conventional commit prefix.
- `clean_subject()`: Clean up a commit subject for display.
- `parse_coauthors()`: Extract Co-authored-by trailers from a commit message body.

    Returns a list of {'name': ..., 'em
- `get_commits()`: Get commits since a tag (or all commits if None).
- `get_pr_number()`: Extract PR number from commit subject if present.
- `generate_changelog()`: Generate markdown changelog from categorized commits.
- ... 还有 1 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## run_tests_parallel.py

**路径**: `scripts\run_tests_parallel.py`
**行数**: 863

### 功能描述

Per-file parallel test runner.

The minimum-viable replacement for pytest-xdist + a subprocess-isolation
plugin. Discovers test files under ``tests/`` (excluding integration/e2e
unless explicitly requested), then runs one ``python -m pytest <file>``
subprocess per file, with bounded parallelism (def

### 核心函数

- `main()`

### 依赖关系

**依赖组件**: gateway
**跨组件调用**: 是

---

## sample_and_compress.py

**路径**: `scripts\sample_and_compress.py`
**行数**: 410

### 功能描述

Sample and Compress HuggingFace Datasets

Downloads trajectories from multiple HuggingFace datasets, randomly samples them,
and runs trajectory compression to fit within a target token budget.

Usage:
    python scripts/sample_and_compress.py
    
    # Custom sample size
    python scripts/sample_a

### 核心函数

- `load_dataset_from_hf()`: Load a dataset from HuggingFace.
    
    Args:
        dataset_name: HuggingFace dataset name (e.g.
- `sample_from_datasets()`: Load all datasets, filter by token count, then randomly sample from combined pool.
    
    Args:
  
- `save_samples_for_compression()`: Save samples to JSONL files for trajectory compression.
    
    Args:
        samples: List of traj
- `run_compression()`: Run trajectory compression on the sampled data.
    
    Args:
        input_dir: Directory containi
- `merge_output_to_single_jsonl()`: Merge all JSONL files in a directory into a single JSONL file.
    
    Args:
        input_dir: Dir
- `main()`: Sample trajectories from HuggingFace datasets and run compression.
    
    Args:
        total_samp

### 依赖关系

**依赖组件**: entry-points
**跨组件调用**: 是

---

## tool_search_livetest.py

**路径**: `scripts\tool_search_livetest.py`
**行数**: 550

### 功能描述

Live test harness for Hermes Agent's Tool Search feature.

Spins up a real AIAgent against a real model, registers ~20 fake "MCP" tools
with realistic shapes (github-like, slack-like, calendar-like, search-like),
runs a small set of scenarios, and records exactly what the model did.

For each scenar

### 核心函数

- `setup_isolated_home()`: Create a fresh ~/.hermes/ for one test, copying minimal credentials.

    Also reads OPENROUTER_API_
- `register_fake_tools()`: Register the FAKE_MCP_TOOLS into the live tool registry.
- `reset_module_state()`: Drop cached modules so the new HERMES_HOME takes effect.
- `run_one_scenario()`: Run one (scenario, enabled) combination. Returns the recorded transcript.
- `main()`

### 依赖关系

**依赖组件**: cli, entry-points
**跨组件调用**: 是

---

## extract-automation-blueprints.py

**路径**: `website\scripts\extract-automation-blueprints.py`
**行数**: 51

### 功能描述

Generate the Automation Blueprints catalog JSON for the docs site.

Mirrors ``extract-skills.py``: imports the single-source-of-truth blueprint
definitions from ``cron/blueprint_catalog.py`` and emits a flat JSON array the
docs page renders into cards (description, schedule, copy-paste slash command

### 核心函数

- `build_index()`
- `main()`

### 依赖关系

**依赖组件**: cron
**跨组件调用**: 是

---

## extract-skills.py

**路径**: `website\scripts\extract-skills.py`
**行数**: 684

### 功能描述

Extract skill metadata into website/static/api/skills.json for the Skills Hub page.

Two data sources:

1. Local SKILL.md files under ``skills/`` (built-in) and ``optional-skills/``
   (official optional). These give us full metadata — overview prose, version,
   license, env vars, commands — that t

### 核心函数

- `extract_local_skills()`
- `extract_unified_index_skills()`: Read website/static/api/skills-index.json — the canonical multi-source index.

    Returns ``(skills
- `extract_legacy_cache_skills()`: Read the deprecated skills/index-cache/ snapshots — fallback only.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## generate-llms-txt.py

**路径**: `website\scripts\generate-llms-txt.py`
**行数**: 307

### 功能描述

Generate llms.txt and llms-full.txt for the Hermes docs site.

Outputs:
  website/static/llms.txt        — short curated index of the docs, one link per page,
                                    grouped by section. Conforms to https://llmstxt.org.
  website/static/llms-full.txt   — every `.md` file 

### 核心函数

- `read_frontmatter()`: Return ({title, description}, body-markdown) for a doc file.
- `resolve_desc()`: Resolve short description for llms.txt entry.
- `emit_llms_index()`: Build the short llms.txt index.
- `emit_llms_full()`: Concatenate every doc under website/docs/ into a single markdown file.

    Order: mirrors the curat
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## generate-skill-docs.py

**路径**: `website\scripts\generate-skill-docs.py`
**行数**: 774

### 功能描述

Generate per-skill Docusaurus pages from skills/ and optional-skills/ SKILL.md files.

Each skill gets website/docs/user-guide/skills/<source>/<category>/<skill-name>.md
where <source> is "bundled" or "optional".

Also regenerates:
- website/docs/reference/skills-catalog.md
- website/docs/reference/

### 核心函数

- `mdx_escape_body()`: Escape MDX-dangerous characters in markdown body, leaving fenced code blocks alone.

    Outside fen
- `rewrite_relative_links()`: Rewrite references/foo.md style links in the SKILL.md body.

    The source SKILL.md lives in `skill
- `parse_skill_md()`
- `sanitize_yaml_string()`: Make a string safe to embed in a YAML double-quoted scalar.
- `derive_skill_meta()`: Extract category + skill slug from filesystem layout.

    skills/<cat>/<skill>/SKILL.md           -
- `page_id()`: Stable slug used for filename + sidebar id.
- `page_output_path()`
- `sidebar_doc_id()`: Docusaurus sidebar id, relative to docs/.
- `render_skill_page()`
- `discover_skills()`
- `build_catalog_md_bundled()`
- `build_catalog_md_optional()`
- `build_sidebar_items()`: Build a dict representing the Skills sidebar tree.

    Structure:
    Skills
    ├── (hand-written 
- `write_sidebar()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

