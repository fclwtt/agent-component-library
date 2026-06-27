# skill-system 模块详细说明

本组件包含 28 个模块。

---

## _common.py

**路径**: `skills\creative\comfyui\scripts\_common.py`
**行数**: 836

### 功能描述

_common.py — Shared logic for ComfyUI skill scripts.

Single source of truth for:
- HTTP transport (with retry/backoff, streaming, timeout handling)
- Cloud detection and endpoint mapping (local ComfyUI vs Comfy Cloud)
- Workflow node-type catalogs (param patterns, model loaders, output nodes)
- API

### 核心类

- `HTTPResponse`

### 核心函数

- `folder_aliases_for()`: Return the search order of folder names (primary first).
- `is_cloud_host()`: True if the host points at Comfy Cloud (or staging/preview subdomain).
- `build_cloud_aware_url()`: Build a URL that adds /api prefix when targeting Comfy Cloud.

    Local ComfyUI accepts both `/foo`
- `cloud_endpoint()`: Map a cloud endpoint path to its current canonical form.

    Handles known renames documented in th
- `resolve_url()`: Top-level URL resolver. Applies cloud rename + /api prefix as needed.
- `resolve_api_key()`: Look up API key from CLI flag → env var. Strips whitespace and quotes.
- `http_request()`: Single entry point for all HTTP traffic.

    Behavior:
      - Retries on connection errors and on 
- `http_get()`
- `http_post()`
- `is_api_format()`: API format = top-level dict where each value has `class_type`.
- `unwrap_workflow()`: Unwrap common wrapper variants. Returns API-format workflow or raises ValueError.
- `is_link()`: True if `value` is a [node_id, output_index] connection (length-2 list).
- `iter_nodes()`: Yield (node_id, node) for each valid API-format node.
- `iter_model_deps()`: Yield {node_id, class_type, field, value, folder} for each model dependency.
- `iter_embedding_refs()`: Yield (node_id, embedding_name) for every embedding mention in prompts.
- ... 还有 9 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## auto_fix_deps.py

**路径**: `skills\creative\comfyui\scripts\auto_fix_deps.py`
**行数**: 226

### 功能描述

auto_fix_deps.py — Run check_deps.py, then attempt to install whatever is missing.

For local servers:
  - Missing custom nodes → `comfy node install <package>`
  - Missing models → `comfy model download` (only if a URL is supplied via
    --model-source-file or detected via well-known names)

For c

### 核心函数

- `comfy_cli_available()`: Return command prefix for comfy-cli, or None.
- `run_cmd()`
- `install_node()`
- `install_model()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## check_deps.py

**路径**: `skills\creative\comfyui\scripts\check_deps.py`
**行数**: 438

### 功能描述

check_deps.py — Verify a ComfyUI workflow's dependencies (custom nodes, models,
embeddings) against a running server.

Improvements over v1:
  - Cloud-aware endpoint mapping (handles `/api/experiment/models/{folder}` and
    `/api/object_info` variants verified against live cloud API)
  - Distinguis

### 核心函数

- `fetch_object_info()`: Returns (installed_node_set, error_info). Error info is a dict if we
    couldn't query (e.g. cloud 
- `fetch_models_for_folder()`: Fetch installed models for a folder, trying aliases.

    Folder renames over time (e.g. unet → diff
- `fetch_embeddings()`: Local ComfyUI exposes /embeddings; cloud uses /experiment/models/embeddings.
- `normalize_for_match()`: Generate matching variants of a model name (with/without extension, slashes, etc.)
- `model_present()`
- `suggest_install_command()`
- `suggest_git_url()`: For nodes not on the registry, return a git URL the user can hand to
    ComfyUI-Manager's `/manager
- `check_deps()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## extract_schema.py

**路径**: `skills\creative\comfyui\scripts\extract_schema.py`
**行数**: 316

### 功能描述

extract_schema.py — Analyze a ComfyUI API-format workflow and extract
controllable parameters.

Improvements over v1:
  - Catalogs live in `_common.py`, shared with `check_deps.py`
  - Coverage expanded for Flux / SD3 / Wan / Hunyuan / LTX / IPAdapter / rgthree
  - Symmetric duplicate-name resolutio

### 核心函数

- `infer_type()`
- `trace_to_node()`: Follow a [node_id, slot] link, hopping through Reroute / Primitive nodes
    if needed, to find the 
- `find_negative_prompt_node()`: Trace `negative` input of a sampler back to the source text encoder.
- `find_positive_prompt_node()`
- `extract_schema()`: Extract controllable parameters from a workflow.

    Returns:
        {
          "parameters": { f
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_logs.py

**路径**: `skills\creative\comfyui\scripts\fetch_logs.py`
**行数**: 158

### 功能描述

fetch_logs.py — Retrieve workflow execution diagnostics from a ComfyUI server.

When a workflow errors, the server's /history (local) or /jobs (cloud) entry
contains the full Python traceback. This script makes it easy to fetch by
prompt_id, with sensible formatting.

Usage:
    python3 fetch_logs.p

### 核心函数

- `fetch_history_entry()`
- `fetch_queue()`
- `extract_diagnostics()`: Pull out the parts a human cares about: status, errors, traceback, timing.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## hardware_check.py

**路径**: `skills\creative\comfyui\scripts\hardware_check.py`
**行数**: 498

### 功能描述

hardware_check.py — Detect whether this machine can realistically run ComfyUI locally.

Improvements over v1:
  - Multi-GPU detection: scans all NVIDIA / AMD GPUs, picks the best one (most VRAM)
  - Apple Silicon: detects Rosetta-via-x86_64 false negative; warns instead of misclassifying
  - Apple g

### 核心函数

- `is_wsl()`: Return True when running under Windows Subsystem for Linux.
- `is_rosetta()`: Return True when Python is running translated under Rosetta on Apple Silicon.
- `detect_nvidia()`: Detect NVIDIA GPUs. Returns the GPU with the most VRAM, plus list of all.
- `detect_rocm()`
- `detect_apple_silicon()`
- `detect_intel_arc()`
- `total_system_ram_gb()`
- `total_free_disk_gb()`
- `check_pytorch_cuda()`: Optional PyTorch availability check. Only run when --check-pytorch is set.
- `classify()`
- `build_report()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## health_check.py

**路径**: `skills\creative\comfyui\scripts\health_check.py`
**行数**: 224

### 功能描述

health_check.py — One-stop verification that the ComfyUI environment is ready.

Runs through the verification checklist:
  1. comfy-cli on PATH
  2. server reachable (/system_stats)
  3. at least one checkpoint installed
  4. (optional) a specific workflow's deps are met
  5. (optional) actually sub

### 核心函数

- `comfy_cli_status()`
- `server_status()`
- `checkpoint_status()`
- `smoke_test()`: Submit a tiny workflow and verify the server accepts it.

    Cancels the job immediately after acce
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## run_batch.py

**路径**: `skills\creative\comfyui\scripts\run_batch.py`
**行数**: 244

### 功能描述

run_batch.py — Run a workflow many times, varying parameters per run.

Two modes:
  1. --count N --randomize-seed
       Submit N runs, each with a fresh random seed. Use for quick variations.
  2. --sweep '{"seed": [1,2,3], "steps": [20,30]}'
       Cartesian product of values. With cloud subscript

### 核心函数

- `expand_sweep()`: Generate a list of args dicts for each run.
- `execute_one()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## run_workflow.py

**路径**: `skills\creative\comfyui\scripts\run_workflow.py`
**行数**: 797

### 功能描述

run_workflow.py — Inject parameters into a ComfyUI workflow, submit it, monitor
execution, and download outputs.

Improvements over v1:
  - Cloud-aware URL routing (handles /api prefix and /history_v2 / /experiment/models renames)
  - API key from CLI flag OR $COMFY_CLOUD_API_KEY env var
  - WebSock

### 核心类

- `WorkflowRunError`: Raised when a workflow run fails (validation, execution, timeout).
- `ComfyRunner`

### 核心函数

- `load_schema()`
- `inject_params()`: Inject user args into the workflow. Returns (new_workflow, warnings).
- `download_outputs()`: Walk the outputs dict and download every file. Cloud uses `video` (singular);
    local uses `videos
- `parse_input_image_arg()`: Parse `name=path` (or `path` alone, defaulting to name='image').
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## ws_monitor.py

**路径**: `skills\creative\comfyui\scripts\ws_monitor.py`
**行数**: 268

### 功能描述

ws_monitor.py — Real-time ComfyUI WebSocket monitor.

Connects to /ws and pretty-prints execution events: node start/finish, sampling
progress, cached nodes, errors. Optionally writes preview frames to disk.

Useful for:
  - Watching a long-running job in real time without parsing JSON yourself
  - 

### 核心函数

- `fmt_color()`
- `parse_binary_frame()`
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## upload.py

**路径**: `skills\creative\excalidraw\scripts\upload.py`
**行数**: 134

### 功能描述

Upload an .excalidraw file to excalidraw.com and print a shareable URL.

No account required. The diagram is encrypted client-side (AES-GCM) before
upload -- the encryption key is embedded in the URL fragment, so the server
never sees plaintext.

Requirements:
    pip install cryptography

Usage:
  

### 核心函数

- `concat_buffers()`: Build the Excalidraw v2 concat-buffers binary format.

    Layout: [version=1 (4B big-endian)] then 
- `upload()`: Encrypt and upload Excalidraw JSON to excalidraw.com.

    Args:
        excalidraw_json: The full .
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## fetch_transcript.py

**路径**: `skills\media\youtube-content\scripts\fetch_transcript.py`
**行数**: 125

### 功能描述

Fetch a YouTube video transcript and output it as structured JSON.

Usage:
    uv run python3 fetch_transcript.py <url_or_video_id> [--language en,tr] [--timestamps]

Output (JSON):
    {
        "video_id": "...",
        "language": "en",
        "segments": [{"text": "...", "start": 0.0, "duratio

### 核心函数

- `extract_video_id()`: Extract the 11-character video ID from various YouTube URL formats.
- `format_timestamp()`: Convert seconds to HH:MM:SS or MM:SS format.
- `fetch_transcript()`: Fetch transcript segments from YouTube.

    Returns a list of dicts with 'text', 'start', and 'dura
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## _hermes_home.py

**路径**: `skills\productivity\google-workspace\scripts\_hermes_home.py`
**行数**: 43

### 功能描述

Resolve HERMES_HOME for standalone skill scripts.

Skill scripts may run outside the Hermes process (e.g. system Python,
nix env, CI) where ``hermes_constants`` is not importable.  This module
provides the same ``get_hermes_home()`` and ``display_hermes_home()``
contracts as ``hermes_constants`` wit

### 依赖关系

**依赖组件**: state-management
**跨组件调用**: 是

---

## google_api.py

**路径**: `skills\productivity\google-workspace\scripts\google_api.py`
**行数**: 1226

### 功能描述

Google Workspace API CLI for Hermes Agent.

Uses the Google Workspace CLI (`gws`) when available, but preserves the
existing Hermes-facing JSON contract and falls back to the Python client
libraries if `gws` is not installed.

Usage:
  python google_api.py gmail search "is:unread" [--max 10]
  pytho

### 核心函数

- `get_credentials()`: Load and refresh credentials from token file.
- `build_service()`
- `gmail_search()`
- `gmail_get()`
- `gmail_send()`
- `gmail_reply()`
- `gmail_labels()`
- `gmail_modify()`
- `calendar_list()`
- `calendar_create()`
- `calendar_delete()`
- `drive_search()`
- `drive_get()`: Get metadata for a single Drive file by ID.
- `drive_upload()`: Upload a local file to Drive. Falls through to Python client even when gws
    is installed, because
- `drive_download()`: Download a Drive file to a local path. Google-native files (Docs/Sheets/Slides)
    must be exported
- ... 还有 12 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## gws_bridge.py

**路径**: `skills\productivity\google-workspace\scripts\gws_bridge.py`
**行数**: 112

### 功能描述

Bridge between Hermes OAuth token and gws CLI.

Refreshes the token if expired, then executes gws with the valid access token.

### 核心函数

- `get_token_path()`
- `refresh_token()`: Refresh the access token using the refresh token.
- `get_valid_token()`: Return a valid access token, refreshing if needed.
- `main()`: Refresh token if needed, then exec gws with remaining args.

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## setup.py

**路径**: `skills\productivity\google-workspace\scripts\setup.py`
**行数**: 482

### 功能描述

Google Workspace OAuth2 setup for Hermes Agent.

Fully non-interactive — designed to be driven by the agent via terminal commands.
The agent mediates between this script and the user (works on CLI, Telegram, Discord, etc.)

Commands:
  setup.py --check                          # Is auth valid? Exit 

### 核心函数

- `install_deps()`: Install Google API packages if missing. Returns True on success.
- `check_auth_live()`: Check auth with a real API call to detect disabled_client/account issues.
- `check_auth()`: Check if stored credentials are valid. Prints status, exits 0 or 1.
- `store_client_secret()`: Copy and validate client_secret.json to Hermes home.
- `get_auth_url()`: Print the OAuth authorization URL. User visits this in a browser.
- `exchange_auth_code()`: Exchange the authorization code for a token and save it.
- `revoke()`: Revoke stored token and delete it.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## maps_client.py

**路径**: `skills\productivity\maps\scripts\maps_client.py`
**行数**: 1298

### 功能描述

maps_client.py - CLI tool for maps, geocoding, routing, POI search, and more.
Uses only Python stdlib. Data from OpenStreetMap/Nominatim, Overpass API, OSRM,
and TimeAPI.io.

Commands:
  search     - Geocode a place name to coordinates
  reverse    - Reverse geocode coordinates to an address
  nearb

### 核心函数

- `print_json()`: Print data as pretty-printed JSON to stdout.
- `error_exit()`: Print an error result as JSON and exit.
- `http_get()`: Perform an HTTP GET request, returning parsed JSON.
    Adds the required User-Agent header. Retries
- `http_get_text()`: Like http_get but returns raw text instead of parsed JSON.
    Useful for APIs that may return non-J
- `http_post()`: Perform an HTTP POST with a plain-text body (for Overpass QL).
    Returns parsed JSON.
- `overpass_query()`: POST an Overpass QL query, trying each URL in OVERPASS_URLS in turn.

    A single public Overpass m
- `haversine_m()`: Return distance in metres between two lat/lon points (Haversine).
- `nominatim_search()`: Geocode a free-text query. Returns list of result dicts.
- `nominatim_reverse()`: Reverse geocode lat/lon. Returns a single result dict.
- `geocode_single()`: Geocode a query and return (lat, lon, display_name).
    Exits with error if nothing found.
- `build_overpass_nearby()`: Build an Overpass QL query for nearby POIs around a point.

    If ``tag_pairs`` is provided, the qu
- `build_overpass_bbox()`: Build an Overpass QL query for POIs within a bounding box.

    See ``build_overpass_nearby`` for ``
- `parse_overpass_elements()`: Parse Overpass elements into a clean list of POI dicts.
    If ref_lat/ref_lon are provided, compute
- `cmd_search()`: Geocode a place name and return top results.
- `cmd_reverse()`: Reverse geocode coordinates to a human-readable address.
- ... 还有 8 个函数

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## extract_marker.py

**路径**: `skills\productivity\ocr-and-documents\scripts\extract_marker.py`
**行数**: 88

### 功能描述

Extract text from documents using marker-pdf. High-quality OCR + layout analysis.

Requires ~3-5GB disk (PyTorch + models downloaded on first use).
Supports: PDF, DOCX, PPTX, XLSX, HTML, EPUB, images.

Usage:
    python extract_marker.py document.pdf
    python extract_marker.py document.pdf --outpu

### 核心函数

- `convert()`
- `check_requirements()`: Check disk space before installing.

### 依赖关系

**依赖组件**: cli
**跨组件调用**: 是

---

## extract_pymupdf.py

**路径**: `skills\productivity\ocr-and-documents\scripts\extract_pymupdf.py`
**行数**: 99

### 功能描述

Extract text from documents using pymupdf. Lightweight (~25MB), no models.

Usage:
    python extract_pymupdf.py document.pdf
    python extract_pymupdf.py document.pdf --markdown
    python extract_pymupdf.py document.pdf --pages 0-4
    python extract_pymupdf.py document.pdf --images output_dir/
 

### 核心函数

- `extract_text()`
- `extract_markdown()`
- `extract_tables()`
- `extract_images()`
- `show_metadata()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `skills\productivity\powerpoint\scripts\__init__.py`
**行数**: 1

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## add_slide.py

**路径**: `skills\productivity\powerpoint\scripts\add_slide.py`
**行数**: 196

### 功能描述

Add a new slide to an unpacked PPTX directory.

Usage: python add_slide.py <unpacked_dir> <source>

The source can be:
  - A slide file (e.g., slide2.xml) - duplicates the slide
  - A layout file (e.g., slideLayout2.xml) - creates from layout

Examples:
    python add_slide.py unpacked/ slide2.xml
 

### 核心函数

- `get_next_slide_number()`
- `create_slide_from_layout()`
- `duplicate_slide()`
- `parse_source()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## clean.py

**路径**: `skills\productivity\powerpoint\scripts\clean.py`
**行数**: 287

### 功能描述

Remove unreferenced files from an unpacked PPTX directory.

Usage: python clean.py <unpacked_dir>

Example:
    python clean.py unpacked/

This script removes:
- Orphaned slides (not in sldIdLst) and their relationships
- [trash] directory (unreferenced files)
- Orphaned .rels files for deleted reso

### 核心函数

- `get_slides_in_sldidlst()`
- `remove_orphaned_slides()`
- `remove_trash_directory()`
- `get_slide_referenced_files()`
- `remove_orphaned_rels_files()`
- `get_referenced_files()`
- `remove_orphaned_files()`
- `update_content_types()`
- `clean_unused_files()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## __init__.py

**路径**: `skills\productivity\powerpoint\scripts\office\helpers\__init__.py`
**行数**: 1

### 功能描述

（需从代码逻辑分析）

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## merge_runs.py

**路径**: `skills\productivity\powerpoint\scripts\office\helpers\merge_runs.py`
**行数**: 200

### 功能描述

Merge adjacent runs with identical formatting in DOCX.

Merges adjacent <w:r> elements that have identical <w:rPr> properties.
Works on runs in paragraphs and inside tracked changes (<w:ins>, <w:del>).

Also:
- Removes rsid attributes from runs (revision metadata that doesn't affect rendering)
- Rem

### 核心函数

- `merge_runs()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## simplify_redlines.py

**路径**: `skills\productivity\powerpoint\scripts\office\helpers\simplify_redlines.py`
**行数**: 198

### 功能描述

Simplify tracked changes by merging adjacent w:ins or w:del elements.

Merges adjacent <w:ins> elements from the same author into a single element.
Same for <w:del> elements. This makes heavily-redlined documents easier to
work with by reducing the number of tracked change wrappers.

Rules:
- Only m

### 核心函数

- `simplify_redlines()`
- `get_tracked_change_authors()`
- `infer_author()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## pack.py

**路径**: `skills\productivity\powerpoint\scripts\office\pack.py`
**行数**: 160

### 功能描述

Pack a directory into a DOCX, PPTX, or XLSX file.

Validates with auto-repair, condenses XML formatting, and creates the Office file.

Usage:
    python pack.py <input_directory> <output_file> [--original <file>] [--validate true|false]

Examples:
    python pack.py unpacked/ output.docx --original 

### 核心函数

- `pack()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## search_arxiv.py

**路径**: `skills\research\arxiv\scripts\search_arxiv.py`
**行数**: 115

### 功能描述

Search arXiv and display results in a clean format.

Usage:
    python search_arxiv.py "GRPO reinforcement learning"
    python search_arxiv.py "GRPO reinforcement learning" --max 10
    python search_arxiv.py "GRPO reinforcement learning" --sort date
    python search_arxiv.py --author "Yann LeCun"

### 核心函数

- `search()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

## polymarket.py

**路径**: `skills\research\polymarket\scripts\polymarket.py`
**行数**: 285

### 功能描述

Polymarket CLI helper — query prediction market data.

Usage:
    python3 polymarket.py search "bitcoin"
    python3 polymarket.py trending [--limit 10]
    python3 polymarket.py market <slug>
    python3 polymarket.py event <slug>
    python3 polymarket.py price <token_id>
    python3 polymarket.py

### 核心函数

- `cmd_search()`: Search for markets.
- `cmd_trending()`: Show trending events by volume.
- `cmd_market()`: Get market details by slug.
- `cmd_event()`: Get event details by slug.
- `cmd_price()`: Get current price for a token.
- `cmd_book()`: Get orderbook for a token.
- `cmd_history()`: Get price history for a market.
- `cmd_trades()`: Get recent trades.
- `main()`

### 依赖关系

**依赖组件**: 无
**跨组件调用**: 否

---

