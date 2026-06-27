"""Entry Points - Public API

入口点接口。提供应用级启动入口、服务注册、健康检查。
其他组件只能通过此模块与入口点层交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.cli import AIAgent, CLI_CONFIG, ChatConsole, HermesCLI, _ACCENT, _BOLD, _DIM, _IMAGE_EXTENSIONS, _RST, _accent_hex, _assistant_copy_text, _cleanup_worktree, _cprint, _detect_file_drop, _git_repo_root, _maybe_remap_for_light_mode, _parse_reasoning_config, _prepare_deferred_agent_startup, _prune_stale_worktrees, _record_output_history_entry, _render_final_assistant_content, _resolve_attachment_path, _setup_worktree, _split_path_input, _strip_reasoning_tags, _suspend_output_history, _sync_process_session_id, _termux_example_image_path, get_job, load_cli_config, logger, save_config_value, set_approval_callback, set_secret_capture_callback, set_sudo_password_callback
from .hermes.modules.hermes_constants import FINISH_REASON_LENGTH, OPENROUTER_BASE_URL, OPENROUTER_MODELS_URL, PARTIAL_STREAM_STUB_ID, agent_browser_runnable, apply_ipv4_preference, apply_subprocess_home_env, display_hermes_home, find_node_executable, get_bundled_skills_dir, get_config_path, get_default_hermes_root, get_hermes_dir, get_hermes_home, get_hermes_home_override, get_optional_mcps_dir, get_optional_skills_dir, get_skills_dir, get_subprocess_home, is_container, is_termux, is_wsl, parse_reasoning_effort, reset_hermes_home_override, secure_parent_dir, set_hermes_home_override, with_hermes_node_path
from .hermes.modules.hermes_logging import COMPONENT_PREFIXES, _safe_stderr, set_session_context, setup_logging, setup_verbose_logging
from .hermes.modules.hermes_state import DEFAULT_DB_PATH, SessionDB, _db_opens_cleanly, apply_wal_with_fallback, format_session_db_unavailable, is_malformed_db_error, repair_state_db_schema
from .hermes.modules.mcp_serve import run_mcp_server
from .hermes.modules.model_tools import TOOLSET_REQUIREMENTS, _emit_post_tool_call_hook, _run_async, _sanitize_tool_error, check_tool_availability, get_tool_definitions, get_toolset_for_tool, handle_function_call
from .hermes.modules.run_agent import AIAgent, DEFAULT_AGENT_IDENTITY, _StreamErrorEvent
from .hermes.modules.toolsets import TOOLSETS, _HERMES_CORE_TOOLS, get_all_toolsets, get_toolset_info, get_toolset_names, resolve_toolset, validate_toolset
from .hermes.modules.trajectory_compressor import CompressionConfig, TrajectoryCompressor
from .hermes.modules.utils import atomic_json_write, atomic_replace, atomic_yaml_write, base_url_host_matches, base_url_hostname, env_bool, env_float, env_int, env_var_enabled, get_api_headers, is_truthy_value, model_forces_max_completion_tokens, normalize_proxy_env_vars, normalize_proxy_url, safe_json_loads

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class ServiceInfo:
    """服务信息"""
    name: str
    version: str
    status: str
    host: str = "localhost"
    port: int = 0


@dataclass
class HealthStatus:
    """健康状态"""
    status: str = "ok"
    services: dict = None
    uptime: float = 0.0

    def __post_init__(self):
        if self.services is None:
            self.services = {}


# ── Protocols ────────────────────────────────────────────────────────────


class EntryPointProtocol(Protocol):
    """入口点协议"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def health_check(self) -> HealthStatus: ...
    def register_service(self, name: str, service: Any) -> None: ...
    def get_service(self, name: str) -> Any: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_entry_point(mode: str = "cli") -> EntryPointProtocol:
    """创建入口点

    mode 可选: cli, server, agent
    """
    if mode == "cli":
        from gateway.run import CLIEntryPoint
        return CLIEntryPoint()
    elif mode == "server":
        from gateway.run import ServerEntryPoint
        return ServerEntryPoint()
    raise ValueError(f"未知入口点模式: {mode}")


# ── 便捷函数 ────────────────────────────────────────────────────────────


def start_app(mode: str = "cli", **kwargs) -> None:
    """启动应用"""
    entry = create_entry_point(mode)
    entry.start()


def health_check() -> HealthStatus:
    """检查应用健康状态"""
    entry = create_entry_point("server")
    return entry.health_check()


def register_service(name: str, service: Any) -> None:
    """注册服务"""
    entry = create_entry_point()
    entry.register_service(name, service)


def get_service(name: str) -> Any:
    """获取已注册的服务"""
    entry = create_entry_point()
    return entry.get_service(name)
