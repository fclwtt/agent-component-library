"""CLI - Public API

命令行界面接口。提供命令解析、执行、交互式对话。
其他组件只能通过此模块与 CLI 层交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.hermes_cli._subprocess_compat import windows_detach_popen_kwargs, windows_hide_flags
from .hermes.modules.hermes_cli.active_sessions import coerce_max_concurrent_sessions, resolve_max_concurrent_sessions, transfer_active_session, try_acquire_active_session
from .hermes.modules.hermes_cli.auth import AuthError, CODEX_ACCESS_TOKEN_REFRESH_SKEW_SECONDS, DEFAULT_XAI_OAUTH_BASE_URL, PROVIDER_REGISTRY, _agent_key_is_usable, _auth_store_lock, _codex_access_token_is_expiring, _decode_jwt_claims, _load_auth_store, _load_provider_state, _nous_invoke_jwt_is_usable, _read_codex_tokens, _resolve_kimi_base_url, _resolve_zai_base_url, _save_auth_store, _save_provider_state, _store_provider_state, _xai_validate_inference_base_url, build_minimax_oauth_token_provider, clear_provider_auth, get_auth_status, get_provider_auth_state, has_usable_secret, is_provider_explicitly_configured, is_rate_limited_auth_error, read_credential_pool, resolve_api_key_provider_credentials, resolve_codex_runtime_credentials, resolve_external_process_provider_credentials, resolve_nous_access_token, resolve_nous_runtime_credentials, resolve_qwen_runtime_credentials, resolve_spotify_runtime_credentials, resolve_xai_oauth_runtime_credentials, step_up_nous_billing_scope, suppress_credential_source, write_credential_pool
from .hermes.modules.hermes_cli.banner import _format_context_length, build_welcome_banner, format_banner_version_label, get_available_skills, get_update_result, prefetch_update_check
from .hermes.modules.hermes_cli.blueprint_cmd import BlueprintCommandResult, handle_blueprint_command
from .hermes.modules.hermes_cli.browser_connect import DEFAULT_BROWSER_CDP_URL, is_browser_debug_ready, manual_chrome_debug_command, try_launch_chrome_debug
from .hermes.modules.hermes_cli.callbacks import prompt_for_secret
from .hermes.modules.hermes_cli.cli_agent_setup_mixin import CLIAgentSetupMixin
from .hermes.modules.hermes_cli.cli_commands_mixin import CLICommandsMixin
from .hermes.modules.hermes_cli.cli_output import print_error, print_header, print_info, print_success, print_warning, prompt, prompt_yes_no
from .hermes.modules.hermes_cli.clipboard import has_clipboard_image, save_clipboard_image
from .hermes.modules.hermes_cli.codex_models import get_codex_model_ids
from .hermes.modules.hermes_cli.colors import Colors, color
from .hermes.modules.hermes_cli.commands import COMMANDS, COMMANDS_BY_CATEGORY, COMMAND_REGISTRY, GATEWAY_KNOWN_COMMANDS, SUBCOMMANDS, SlashCommandAutoSuggest, SlashCommandCompleter, _build_description, _is_gateway_available, _iter_plugin_command_entries, _resolve_config_gates, _sanitize_telegram_name, discord_skill_commands_by_category, gateway_help_lines, is_gateway_known_command, resolve_command, should_bypass_active_session, slack_native_slashes, slack_subcommand_map, telegram_menu_commands, telegram_menu_max_commands
from .hermes.modules.hermes_cli.config import DEFAULT_CONFIG, OPTIONAL_ENV_VARS, _expand_env_vars, _normalize_root_model_keys, cfg_get, check_config_version, clear_model_endpoint_credentials, ensure_hermes_home, format_managed_message, get_compatible_custom_providers, get_config_path, get_custom_provider_context_length, get_env_path, get_env_value, get_env_var, get_hermes_home, is_managed, load_config, load_env, migrate_config, print_config_warnings, read_raw_config, recommended_update_command, reload_env, remove_env_value, save_config, save_env_value, save_env_value_secure, set_env_var, warn_deprecated_cwd_env_vars
from .hermes.modules.hermes_cli.context_switch_guard import enrich_model_switch_warnings_for_gateway, merge_preflight_compression_warning
from .hermes.modules.hermes_cli.copilot_auth import copilot_request_headers, get_copilot_api_token, resolve_copilot_token
from .hermes.modules.hermes_cli.cron import _contains_gateway_lifecycle_command
from .hermes.modules.hermes_cli.curses_ui import curses_radiolist, curses_single_select
from .hermes.modules.hermes_cli.debug import _GATEWAY_PRIVACY_NOTICE, _best_effort_sweep_expired_pastes, _capture_dump, _schedule_auto_delete, _sweep_expired_pastes, collect_debug_report, upload_to_pastebin
from .hermes.modules.hermes_cli.dep_ensure import ensure_dependency
from .hermes.modules.hermes_cli.dingtalk_auth import dingtalk_qr_auth
from .hermes.modules.hermes_cli.env_loader import get_secret_source, load_hermes_dotenv
from .hermes.modules.hermes_cli.fallback_config import get_fallback_chain
from .hermes.modules.hermes_cli.gateway import get_service_name
from .hermes.modules.hermes_cli.goals import GoalManager, draft_contract, migrate_goal_to_session, parse_contract
from .hermes.modules.hermes_cli.inventory import build_models_payload, load_picker_context
from .hermes.modules.hermes_cli.kanban import _check_dispatcher_presence, run_slash
from .hermes.modules.hermes_cli.kanban_diagnostics import SEVERITY_ORDER
from .hermes.modules.hermes_cli.main import _has_any_provider_configured, _print_version_info, _read_git_revision_fingerprint, _relative_time
from .hermes.modules.hermes_cli.mcp_config import _get_mcp_servers
from .hermes.modules.hermes_cli.mcp_startup import _resolve_discovery_timeout, start_background_mcp_discovery, wait_for_mcp_discovery
from .hermes.modules.hermes_cli.memory_setup import cmd_setup_provider
from .hermes.modules.hermes_cli.middleware import apply_llm_request_middleware, apply_tool_request_middleware, run_llm_execution_middleware, run_tool_execution_middleware
from .hermes.modules.hermes_cli.moa_config import build_moa_turn_prompt, decode_moa_turn, exact_moa_preset_name, moa_usage, normalize_moa_config, resolve_moa_preset
from .hermes.modules.hermes_cli.model_cost_guard import expensive_model_warning
from .hermes.modules.hermes_cli.model_normalize import _AGGREGATOR_PROVIDERS, normalize_model_for_provider
from .hermes.modules.hermes_cli.model_switch import is_nous_hermes_non_agentic, list_authenticated_providers, list_picker_providers, parse_model_flags, prewarm_picker_cache_async, resolve_display_context_length, resolve_persist_behavior, switch_model
from .hermes.modules.hermes_cli.models import OPENROUTER_MODELS, PROVIDER_GROUPS, _PROVIDER_MODELS, _is_model_free, _pricing_cache, _should_use_copilot_responses_api, clear_provider_models_cache, copilot_default_headers, copilot_model_api_mode, curated_models_for_provider, detect_provider_for_model, detect_static_provider_for_model, ensure_lmstudio_model_loaded, get_copilot_model_context, get_default_model_for_provider, get_nous_recommended_aux_model, github_model_reasoning_efforts, group_providers, list_available_providers, lmstudio_model_reasoning_options, model_supports_fast_mode, normalize_copilot_model_id, normalize_opencode_model_id, normalize_provider, opencode_model_api_mode, parse_model_input, provider_label, provider_model_ids, resolve_fast_mode_overrides
from .hermes.modules.hermes_cli.nous_account import format_nous_portal_entitlement_message, get_nous_portal_account_info, nous_portal_topup_url
from .hermes.modules.hermes_cli.nous_auth_keepalive import start_nous_auth_keepalive, stop_nous_auth_keepalive
from .hermes.modules.hermes_cli.nous_billing import BillingAuthError, BillingError, BillingRateLimited, BillingScopeRequired, _absolutize_portal_url, get_billing_state, get_charge_status, patch_auto_top_up, post_charge, resolve_portal_base_url
from .hermes.modules.hermes_cli.nous_subscription import get_nous_subscription_features
from .hermes.modules.hermes_cli.partial_compress import parse_partial_compress_args, rejoin_compressed_head_and_tail, split_history_for_partial_compress
from .hermes.modules.hermes_cli.pets import _clear_active_if, _rename_active_if, _set_active, _set_enabled, set_pet_scale
from .hermes.modules.hermes_cli.plugins import VALID_HOOKS, _ensure_plugins_discovered, _get_disabled_plugins, clear_thread_tool_whitelist, discover_plugins, get_plugin_auxiliary_tasks, get_plugin_command_handler, get_plugin_commands, get_plugin_context_engine, get_plugin_manager, get_pre_tool_call_block_message, has_hook, invoke_hook, resolve_plugin_command_result, set_thread_tool_whitelist
from .hermes.modules.hermes_cli.plugins_cmd import _discover_all_plugins, _get_disabled_set, _get_enabled_set, _plugin_status, dashboard_set_agent_plugin_enabled
from .hermes.modules.hermes_cli.profiles import _get_default_hermes_home, get_active_profile_name, get_profile_dir, list_profiles, profiles_to_serve
from .hermes.modules.hermes_cli.providers import determine_api_mode, get_label
from .hermes.modules.hermes_cli.psutil_android import PSUTIL_URL, PsutilAndroidInstallError, prepare_patched_psutil_sdist
from .hermes.modules.hermes_cli.pt_input_extras import install_ctrl_enter_alias, install_ignored_terminal_sequences, install_shift_enter_alias
from .hermes.modules.hermes_cli.relaunch import relaunch
from .hermes.modules.hermes_cli.runtime_provider import _auto_detect_local_model, _detect_api_mode_for_url, _get_model_config, _get_named_custom_provider, _resolve_azure_foundry_runtime, canonical_custom_identity, format_runtime_provider_error, has_named_custom_provider, resolve_runtime_provider
from .hermes.modules.hermes_cli.secret_prompt import masked_secret_prompt
from .hermes.modules.hermes_cli.security_advisories import detect_compromised, gateway_log_message, startup_banner
from .hermes.modules.hermes_cli.security_audit_startup import log_startup_security_warnings
from .hermes.modules.hermes_cli.session_listing import format_gateway_session_listing, parse_session_listing_args, query_session_listing
from .hermes.modules.hermes_cli.setup import get_env_value, print_header, print_info, print_success, print_warning, prompt, prompt_choice, prompt_yes_no, save_env_value
from .hermes.modules.hermes_cli.skills_hub import browse_skills, do_install, inspect_skill
from .hermes.modules.hermes_cli.skin_engine import SkinConfig, get_active_goodbye, get_active_help_header, get_active_prompt_symbol, get_active_skin, get_prompt_toolkit_style_overrides, init_skin_from_config
from .hermes.modules.hermes_cli.slack_cli import _build_full_manifest
from .hermes.modules.hermes_cli.stdio import configure_windows_stdio
from .hermes.modules.hermes_cli.suggestions_cmd import handle_suggestions_command
from .hermes.modules.hermes_cli.timeouts import get_provider_request_timeout, get_provider_stale_timeout
from .hermes.modules.hermes_cli.tips import get_random_tip
from .hermes.modules.hermes_cli.tools_config import CONFIGURABLE_TOOLSETS, _apply_mcp_change, _apply_toolset_change, _cua_driver_cmd, _get_effective_configurable_toolsets, _get_platform_tools, _get_plugin_toolset_keys, _parse_enabled_flag, _toolset_has_keys, enabled_mcp_server_names
from .hermes.modules.hermes_cli.voice import format_voice_record_key_for_status, normalize_voice_record_key_for_prompt_toolkit, speak_text, start_continuous, stop_continuous, voice_record_key_from_config
from .hermes.modules.hermes_cli.write_approval_commands import handle_pending_subcommand

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class CommandResult:
    """命令执行结果"""
    output: str
    success: bool = True
    error: Optional[str] = None


# ── Protocols ────────────────────────────────────────────────────────────


class CLIProtocol(Protocol):
    """CLI 协议"""
    def execute(self, command: str) -> CommandResult: ...
    def start_interactive(self) -> None: ...
    def register_command(self, name: str, handler: callable, help_text: str = "") -> None: ...
    def list_commands(self) -> list[dict]: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_cli() -> CLIProtocol:
    """创建 CLI 实例"""
    from hermes_cli.main import CLIApp
    return CLIApp()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def run_cli() -> None:
    """启动 CLI 应用"""
    create_cli().start_interactive()


def execute_command(cmd: str) -> CommandResult:
    """执行单条命令"""
    return create_cli().execute(cmd)


def register_cli_command(name: str, handler: callable, help_text: str = "") -> None:
    """注册 CLI 命令"""
    create_cli().register_command(name, handler, help_text)


def list_cli_commands() -> list[dict]:
    """列出所有 CLI 命令"""
    return create_cli().list_commands()
