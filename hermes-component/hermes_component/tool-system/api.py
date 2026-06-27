"""Tool System - Public API

工具系统接口。其他组件只能通过此模块与工具系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol


#  Data Types 


@dataclass
class ToolEntry:
    """工具条目"""
    name: str
    toolset: str
    schema: dict
    handler: Callable
    description: str = ""
    emoji: str = ""


@dataclass
class ToolResult:
    """工具调用结果"""
    output: str
    status: str = "ok"
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


#  Protocols 


class ToolRegistryProtocol(Protocol):
    """工具注册表协议"""
    def register(self, name: str, toolset: str, schema: dict, handler: Callable) -> None: ...
    def deregister(self, name: str) -> None: ...
    def get_entry(self, name: str) -> Optional[ToolEntry]: ...
    def get_definitions(self, tool_names: set[str]) -> list[dict]: ...
    def dispatch(self, name: str, args: dict) -> str: ...
    def get_all_tool_names(self) -> list[str]: ...
    def is_toolset_available(self, toolset: str) -> bool: ...
    def get_available_toolsets(self) -> dict[str, dict]: ...


class ToolExecutorProtocol(Protocol):
    """工具执行器协议（扩展能力）"""
    def execute_terminal(self, command: str) -> ToolResult: ...
    def execute_file(self, path: str, operation: str, **kwargs) -> ToolResult: ...
    def execute_mcp(self, server_name: str, tool_name: str, args: dict) -> ToolResult: ...


#  Factory Functions 


def create_tool_registry() -> ToolRegistryProtocol:
    """创建工具注册表"""
    from tools.registry import ToolRegistry
    return ToolRegistry()


def create_tool_executor(registry: ToolRegistryProtocol) -> ToolExecutorProtocol:
    """创建工具执行器（包装终端/文件/MCP 等工具）"""
    from tools.terminal_tool import TerminalTool
    return TerminalTool()


#  便捷函数


def register_tool(name: str, toolset: str, schema: dict, handler: callable) -> None:
    """注册工具到注册表"""
    registry = create_tool_registry()
    registry.register(name, toolset, schema, handler) 


def execute_tool(name: str, args: dict) -> str:
    """便捷工具调用"""
    registry = create_tool_registry()
    return registry.dispatch(name, args)


def list_available_tools() -> list[ToolEntry]:
    """列出所有可用工具"""
    registry = create_tool_registry()
    return [ToolEntry(name=n, toolset="", schema={}, handler=lambda: None)
            for n in registry.get_all_tool_names()]


# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.tools.ansi_strip import strip_ansi
from .hermes.modules.tools.approval import _YOLO_MODE_FROZEN, _get_approval_mode, _normalize_approval_mode, detect_dangerous_command, detect_hardline_command, disable_session_yolo, enable_session_yolo, has_blocking_approval, is_session_yolo_enabled, load_permanent_allowlist, register_gateway_notify, reset_current_observability_context, reset_current_session_key, resolve_gateway_approval, set_current_observability_context, set_current_session_key, unregister_gateway_notify
from .hermes.modules.tools.async_delegation import active_count, interrupt_all, list_async_delegations
from .hermes.modules.tools.blueprints import BlueprintError, blueprint_spec_for_installed, register_blueprint_suggestion
from .hermes.modules.tools.browser_supervisor import SUPERVISOR_REGISTRY
from .hermes.modules.tools.browser_tool import _chromium_installed, _emergency_cleanup_all_sessions, _ensure_cdp_supervisor, _get_browser_engine, _get_cdp_override, _get_cloud_provider, _is_camofox_mode, _last_session_key, _run_browser_command, _running_in_docker, _stop_cdp_supervisor, _using_lightpanda_engine, cleanup_all_browsers, cleanup_browser
from .hermes.modules.tools.budget_config import BudgetConfig, DEFAULT_BUDGET, budget_for_context_window
from .hermes.modules.tools.checkpoint_manager import CHECKPOINT_BASE, CheckpointManager, clear_all, clear_legacy, format_checkpoint_list, maybe_auto_prune_checkpoints, prune_checkpoints, store_status
from .hermes.modules.tools.clarify_gateway import mark_awaiting_text, resolve_gateway_clarify
from .hermes.modules.tools.code_execution_tool import SANDBOX_ALLOWED_TOOLS, _get_execution_mode, build_execute_code_schema
from .hermes.modules.tools.computer_use.cua_backend import cua_driver_child_env, cua_driver_update_check
from .hermes.modules.tools.computer_use.doctor import run_doctor
from .hermes.modules.tools.computer_use.permissions import computer_use_status, request_permissions_grant
from .hermes.modules.tools.cronjob_tools import _scan_cron_prompt, _scan_cron_skill_assembled, cronjob
from .hermes.modules.tools.delegate_tool import _get_max_concurrent_children, _get_max_spawn_depth, interrupt_subagent, is_spawn_paused, list_active_subagents, set_spawn_paused
from .hermes.modules.tools.env_passthrough import clear_env_passthrough, register_env_passthrough
from .hermes.modules.tools.env_probe import get_environment_probe_line
from .hermes.modules.tools.environments.base import set_activity_callback
from .hermes.modules.tools.environments.docker import DockerEnvironment
from .hermes.modules.tools.environments.local import LocalEnvironment, _sanitize_subprocess_env
from .hermes.modules.tools.environments.modal import ModalEnvironment
from .hermes.modules.tools.file_tools import notify_other_tool_call, reset_file_dedup
from .hermes.modules.tools.fuzzy_match import fuzzy_find_and_replace
from .hermes.modules.tools.image_generation_tool import DEFAULT_MODEL, FAL_MODELS
from .hermes.modules.tools.interrupt import is_interrupted
from .hermes.modules.tools.kanban_tools import _profile_has_kanban_toolset, heartbeat_current_worker_from_env
from .hermes.modules.tools.lazy_deps import FeatureUnavailable, ensure, ensure_and_bind, feature_missing
from .hermes.modules.tools.managed_tool_gateway import is_managed_tool_gateway_ready, peek_nous_access_token, resolve_managed_tool_gateway
from .hermes.modules.tools.mcp_oauth import HermesTokenStorage
from .hermes.modules.tools.mcp_oauth_manager import get_manager
from .hermes.modules.tools.mcp_tool import _ENV_VAR_PATTERN, _connect_server, _ensure_mcp_loop, _interpolate_env_vars, _kill_orphaned_mcp_children, _lock, _run_on_mcp_loop, _servers, _stop_mcp_loop_if_idle, discover_mcp_tools, get_mcp_status, has_registered_mcp_tools, is_mcp_tool_parallel_safe, probe_mcp_server_tools, refresh_agent_mcp_tools, register_mcp_servers, shutdown_mcp_servers
from .hermes.modules.tools.microsoft_graph_auth import MicrosoftGraphConfigError, MicrosoftGraphTokenProvider
from .hermes.modules.tools.microsoft_graph_client import MicrosoftGraphAPIError, MicrosoftGraphClient
from .hermes.modules.tools.process_registry import format_process_notification, format_uptime_short, process_registry
from .hermes.modules.tools.project_tools import set_project_workspace_callback
from .hermes.modules.tools.registry import discover_builtin_tools, registry, tool_error, tool_result
from .hermes.modules.tools.schema_sanitizer import sanitize_tool_schemas, strip_nullable_unions, strip_pattern_and_format, strip_slash_enum
from .hermes.modules.tools.send_message_tool import _parse_target_ref, _send_telegram, _send_to_platform, send_message_tool
from .hermes.modules.tools.skill_manager_tool import _create_skill, _edit_skill, _find_skill, _resolve_skill_dir, apply_skill_pending
from .hermes.modules.tools.skill_provenance import set_current_write_origin
from .hermes.modules.tools.skill_usage import bump_use
from .hermes.modules.tools.skills_ast_audit import ast_scan_path, format_ast_report
from .hermes.modules.tools.skills_guard import format_scan_report, scan_skill, should_allow_install
from .hermes.modules.tools.skills_hub import BrowseShSource, ClaudeMarketplaceSource, ClawHubSource, GitHubAuth, GitHubSource, HubLockFile, LobeHubSource, OptionalSkillSource, SKILLS_DIR, SkillMeta, SkillsShSource, TapsManager, WellKnownSkillSource, append_audit_log, check_for_skill_updates, create_source_router, ensure_hub_dirs, install_from_quarantine, parallel_search_sources, quarantine_bundle, unified_search, uninstall_skill
from .hermes.modules.tools.skills_sync import _read_manifest, diff_bundled_skill, list_user_modified_bundled_skills, remove_pristine_bundled_skills, reset_bundled_skill, restore_official_optional_skill, set_bundled_skills_opt_out, sync_skills
from .hermes.modules.tools.skills_tool import SKILLS_DIR, _find_all_skills, _get_disabled_skill_names, _parse_frontmatter, _sort_skills, set_secret_capture_callback, skill_matches_environment, skill_matches_platform, skill_view
from .hermes.modules.tools.terminal_tool import _get_approval_callback, _get_env_config, cleanup_all_environments, cleanup_vm, clear_task_env_overrides, get_active_env, is_persistent_env, register_task_env_overrides, set_sudo_password_callback
from .hermes.modules.tools.thread_context import propagate_context_to_thread
from .hermes.modules.tools.todo_tool import TodoStore
from .hermes.modules.tools.tool_backend_helpers import fal_key_is_configured, has_direct_modal_credentials, managed_nous_tools_enabled, normalize_browser_cloud_provider, normalize_modal_mode, prefers_gateway, resolve_modal_backend_state, resolve_openai_audio_api_key
from .hermes.modules.tools.tool_result_storage import enforce_turn_budget, maybe_persist_tool_result
from .hermes.modules.tools.tool_search import assemble_tool_defs
from .hermes.modules.tools.transcription_tools import _HAS_FASTER_WHISPER, transcribe_audio
from .hermes.modules.tools.tts_tool import _import_elevenlabs, _import_sounddevice, _strip_markdown_for_tts, check_tts_requirements, stream_tts_to_speaker, text_to_speech_tool
from .hermes.modules.tools.url_safety import is_safe_url
from .hermes.modules.tools.vision_tools import _resize_image_for_vision, vision_analyze_tool
from .hermes.modules.tools.voice_mode import check_voice_requirements, cleanup_temp_recordings, create_audio_recorder, detect_audio_environment, is_whisper_hallucination, play_audio_file, play_beep, stop_playback, transcribe_recording
from .hermes.modules.tools.web_tools import web_extract_tool
from .hermes.modules.tools.website_policy import check_website_access
from .hermes.modules.tools.xai_http import has_xai_credentials, hermes_xai_user_agent, resolve_xai_http_credentials

