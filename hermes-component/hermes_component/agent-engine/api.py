"""Agent Engine - Public API

Agent 核心引擎接口。协调 LLM 调用、工具执行、记忆管理、上下文管理。
其他组件只能通过此模块与 Agent 引擎交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.agent.account_usage import build_credits_view, fetch_account_usage, nous_credits_lines, render_account_usage_lines
from .hermes.modules.agent.agent_init import init_agent
from .hermes.modules.agent.agent_runtime_helpers import anthropic_prompt_cache_policy, apply_pending_steer_to_tool_results, cleanup_dead_connections, convert_to_trajectory_format, copy_reasoning_content_for_api, create_openai_client, drop_thinking_only_and_merge_users, dump_api_request_debug, extract_api_error_context, extract_reasoning, force_close_tcp_sockets, invoke_tool, looks_like_codex_intermediate_ack, reapply_reasoning_echo_for_provider, recover_with_credential_pool, repair_message_sequence, repair_tool_call, restore_primary_runtime, sanitize_api_messages, sanitize_tool_call_arguments, strip_think_blocks, switch_model, try_recover_primary_transport
from .hermes.modules.agent.anthropic_adapter import _COMMON_BETAS, _CONTEXT_1M_BETA, _HERMES_OAUTH_FILE, _OAUTH_ONLY_BETAS, _is_oauth_token, _write_claude_code_credentials, build_anthropic_bedrock_client, build_anthropic_client, create_anthropic_message, is_claude_code_token_valid, read_claude_code_credentials, read_hermes_oauth_credentials, refresh_anthropic_oauth_pure, resolve_anthropic_token, run_oauth_setup_token
from .hermes.modules.agent.async_utils import safe_schedule_threadsafe
from .hermes.modules.agent.auxiliary_client import OMIT_TEMPERATURE, _codex_cloudflare_headers, _fixed_temperature_for_model, _read_main_model, _read_main_provider, _to_openai_base_url, async_call_llm, build_nvidia_nim_headers, build_or_headers, call_llm, cleanup_stale_async_clients, extract_content_or_reasoning, get_async_text_auxiliary_client, get_auxiliary_extra_body, get_available_vision_backends, get_text_auxiliary_client, resolve_provider_client, resolve_vision_provider_client, shutdown_cached_clients
from .hermes.modules.agent.azure_identity_adapter import EntraIdentityConfig, SCOPE_AI_AZURE_DEFAULT, build_token_provider, describe_active_credential, has_azure_identity_installed, is_token_provider
from .hermes.modules.agent.background_review import _COMBINED_REVIEW_PROMPT, _MEMORY_REVIEW_PROMPT, _SKILL_REVIEW_PROMPT, build_memory_write_metadata, spawn_background_review_thread, summarize_background_review_actions
from .hermes.modules.agent.bedrock_adapter import bedrock_model_ids_or_none, discover_bedrock_models, has_aws_credentials, is_anthropic_bedrock_model, resolve_aws_auth_env_var, resolve_bedrock_region
from .hermes.modules.agent.billing_view import build_billing_state, format_money, new_idempotency_key, parse_money, validate_charge_amount
from .hermes.modules.agent.browser_provider import BrowserProvider
from .hermes.modules.agent.chat_completion_helpers import build_api_kwargs, build_assistant_message, cleanup_task_resources, estimate_request_context_tokens, handle_max_iterations, interruptible_api_call, interruptible_streaming_api_call, try_activate_fallback
from .hermes.modules.agent.codex_responses_adapter import _summarize_user_message_for_log
from .hermes.modules.agent.codex_runtime import _consume_codex_event_stream, run_codex_app_server_turn, run_codex_create_stream_fallback, run_codex_stream
from .hermes.modules.agent.coding_context import coding_selection, project_facts_for
from .hermes.modules.agent.context_compressor import ContextCompressor
from .hermes.modules.agent.context_engine import ContextEngine
from .hermes.modules.agent.context_references import preprocess_context_references, preprocess_context_references_async
from .hermes.modules.agent.conversation_compression import COMPACTION_STATUS_MARKER, check_compression_model_feasibility, compress_context, replay_compression_warning, try_shrink_image_parts_in_messages
from .hermes.modules.agent.conversation_loop import INTERRUPT_WAITING_FOR_MODEL_PREFIX, run_conversation
from .hermes.modules.agent.copilot_acp_client import CopilotACPClient
from .hermes.modules.agent.credential_persistence import sanitize_borrowed_credential_payload
from .hermes.modules.agent.credential_pool import AUTH_TYPE_API_KEY, AUTH_TYPE_OAUTH, CUSTOM_POOL_PREFIX, CredentialPool, PooledCredential, SOURCE_MANUAL, SOURCE_MANUAL_DEVICE_CODE, STATUS_EXHAUSTED, STRATEGY_FILL_FIRST, STRATEGY_LEAST_USED, STRATEGY_RANDOM, STRATEGY_ROUND_ROBIN, _exhausted_until, _get_custom_provider_config, _normalize_custom_pool_name, get_custom_provider_pool_key, get_pool_strategy, label_from_token, list_custom_pool_providers, load_pool
from .hermes.modules.agent.credential_sources import find_removal_step
from .hermes.modules.agent.credits_tracker import dev_fixture_credits_state, evaluate_credits_notices, is_free_tier_model, parse_credits_headers, seed_credits_at_session_start
from .hermes.modules.agent.curator import maybe_run_curator
from .hermes.modules.agent.display import build_tool_preview, capture_local_edit_snapshot, extract_edit_diff, get_cute_tool_message, get_tool_emoji, get_tool_preview_max_len, redact_browser_typed_text_for_display, redact_tool_args_for_display, render_edit_diff_with_delta, set_tool_preview_max_len
from .hermes.modules.agent.error_classifier import FailoverReason
from .hermes.modules.agent.errors import SSLConfigurationError
from .hermes.modules.agent.file_safety import _resolve_active_profile_name, build_write_denied_paths, build_write_denied_prefixes, get_container_mirror_warning, get_cross_profile_warning, get_read_block_error, get_sandbox_mirror_warning
from .hermes.modules.agent.gemini_native_adapter import probe_gemini_tier
from .hermes.modules.agent.gemini_schema import sanitize_gemini_tool_parameters
from .hermes.modules.agent.i18n import t
from .hermes.modules.agent.image_gen_provider import ImageGenProvider, normalize_reference_images
from .hermes.modules.agent.image_gen_registry import get_provider, list_providers, register_provider
from .hermes.modules.agent.image_routing import _lookup_supports_vision, _supports_vision_override, build_native_content_parts, decide_image_input_mode
from .hermes.modules.agent.insights import InsightsEngine
from .hermes.modules.agent.iteration_budget import IterationBudget
from .hermes.modules.agent.learn_prompt import build_learn_prompt
from .hermes.modules.agent.lmstudio_reasoning import resolve_lmstudio_effort
from .hermes.modules.agent.lsp.range_shift import build_line_shift
from .hermes.modules.agent.lsp.reporter import report_for_file, truncate
from .hermes.modules.agent.lsp.servers import SERVERS
from .hermes.modules.agent.manual_compression_feedback import summarize_manual_compression
from .hermes.modules.agent.memory_manager import inject_memory_provider_tools, sanitize_context
from .hermes.modules.agent.message_sanitization import _SURROGATE_RE, _escape_invalid_chars_in_json_strings, _repair_tool_call_arguments, _sanitize_messages_non_ascii, _sanitize_messages_surrogates, _sanitize_structure_non_ascii, _sanitize_structure_surrogates, _sanitize_surrogates, _sanitize_tools_non_ascii, _strip_images_from_messages, _strip_non_ascii
from .hermes.modules.agent.model_metadata import DEFAULT_FALLBACK_CONTEXT, MINIMUM_CONTEXT_LENGTH, estimate_messages_tokens_rough, estimate_request_tokens_rough, get_model_context_length, is_local_endpoint
from .hermes.modules.agent.models_dev import ModelCapabilities, ModelInfo, PROVIDER_TO_MODELS_DEV, _load_disk_cache, fetch_models_dev, get_model_capabilities, get_model_info, list_agentic_models, list_provider_models
from .hermes.modules.agent.nous_rate_guard import nous_rate_limit_remaining
from .hermes.modules.agent.onboarding import BUSY_INPUT_FLAG, OPENCLAW_RESIDUE_FLAG, PROFILE_BUILD_FLAG, TOOL_PROGRESS_FLAG, busy_input_hint_cli, busy_input_hint_gateway, detect_openclaw_residue, is_seen, mark_seen, openclaw_residue_hint_cli, profile_build_directive, profile_build_mode, tool_progress_hint_cli, tool_progress_hint_gateway
from .hermes.modules.agent.oneshot import run_oneshot
from .hermes.modules.agent.pet.constants import DEFAULT_SCALE, LOOP_MS, PetState, STATE_ROWS, clamp_scale, resolve_cols
from .hermes.modules.agent.pet.generate.imagegen import GenerationError, list_sprite_providers, resolve_provider
from .hermes.modules.agent.pet.manifest import ManifestError, fetch_manifest, prefetch
from .hermes.modules.agent.pet.render import PetRenderer, build_renderer, detect_terminal_graphics, resolve_mode
from .hermes.modules.agent.pet.state import derive_pet_state, todos_all_done
from .hermes.modules.agent.plugin_llm import PluginLlm
from .hermes.modules.agent.portal_tags import nous_portal_tags
from .hermes.modules.agent.process_bootstrap import OpenAI, _SafeWriter, _get_proxy_for_base_url, _get_proxy_from_env
from .hermes.modules.agent.prompt_builder import DEFAULT_AGENT_IDENTITY, build_context_files_prompt, build_environment_hints, build_nous_subscription_prompt, build_skills_system_prompt, clear_skills_system_prompt_cache, load_soul_md
from .hermes.modules.agent.rate_limit_tracker import format_rate_limit_compact, format_rate_limit_display, parse_rate_limit_headers
from .hermes.modules.agent.reasoning_timeouts import get_reasoning_stale_timeout_floor
from .hermes.modules.agent.redact import RedactingFormatter, _PREFIX_RE, mask_secret, redact_sensitive_text
from .hermes.modules.agent.retry_utils import jittered_backoff
from .hermes.modules.agent.runtime_cwd import clear_session_cwd, set_session_cwd
from .hermes.modules.agent.secret_scope import build_profile_secret_scope, is_multiplex_active, reset_secret_scope, set_multiplex_active, set_secret_scope
from .hermes.modules.agent.secret_sources.bitwarden import apply_bitwarden_secrets
from .hermes.modules.agent.shell_hooks import register_from_config
from .hermes.modules.agent.skill_bundles import _bundles_dir, build_bundle_invocation_message, delete_bundle, get_bundle, get_skill_bundles, list_bundles, reload_bundles, resolve_bundle_command_key, save_bundle, scan_bundles
from .hermes.modules.agent.skill_commands import _build_skill_message, _load_skill_payload, build_preloaded_skills_prompt, build_skill_invocation_message, extract_user_instruction_from_skill_message, get_skill_commands, reload_skills, resolve_skill_command_key, scan_skill_commands
from .hermes.modules.agent.skill_preprocessing import preprocess_skill_content
from .hermes.modules.agent.skill_utils import SKILL_CONFIG_PREFIX, _NAMESPACE_RE, discover_all_skill_config_vars, get_all_skills_dirs, get_disabled_skill_names, get_external_skills_dirs, is_excluded_skill_path, is_external_skill_path, is_valid_namespace, iter_skill_index_files, parse_frontmatter, parse_qualified_name, resolve_skill_config_values
from .hermes.modules.agent.ssl_guard import verify_ca_bundle_with_fallback
from .hermes.modules.agent.stream_diag import emit_stream_drop, flatten_exception_chain, log_stream_retry, stream_diag_capture_response, stream_diag_init
from .hermes.modules.agent.system_prompt import build_system_prompt, build_system_prompt_parts, format_tools_for_system_message, invalidate_system_prompt
from .hermes.modules.agent.title_generator import maybe_auto_title
from .hermes.modules.agent.tool_dispatch_helpers import _append_subdir_hint_to_multimodal, _extract_error_preview, _extract_file_mutation_targets, _extract_landed_file_mutation_paths, _extract_parallel_scope_path, _is_destructive_command, _is_multimodal_tool_result, _multimodal_text_summary, _paths_overlap, _should_parallelize_tool_batch, _trajectory_normalize_msg, make_tool_result_message
from .hermes.modules.agent.tool_executor import execute_tool_calls_concurrent, execute_tool_calls_sequential
from .hermes.modules.agent.tool_guardrails import ToolGuardrailDecision, append_toolguard_guidance, toolguard_synthetic_result
from .hermes.modules.agent.tool_result_classification import file_mutation_result_landed
from .hermes.modules.agent.trajectory import convert_scratchpad_to_think
from .hermes.modules.agent.transcription_provider import TranscriptionProvider
from .hermes.modules.agent.transcription_registry import get_provider
from .hermes.modules.agent.transports.chat_completions import _model_consumes_thought_signature
from .hermes.modules.agent.transports.codex_app_server import CodexAppServerClient, check_codex_binary
from .hermes.modules.agent.tts_provider import TTSProvider
from .hermes.modules.agent.tts_registry import _BUILTIN_NAMES, get_provider, list_providers
from .hermes.modules.agent.usage_pricing import get_pricing_entry, normalize_usage
from .hermes.modules.agent.verification_evidence import mark_workspace_edited, record_terminal_result, verification_status
from .hermes.modules.agent.video_gen_provider import COMMON_ASPECT_RATIOS, COMMON_RESOLUTIONS, DEFAULT_ASPECT_RATIO, DEFAULT_RESOLUTION, VideoGenProvider, error_response
from .hermes.modules.agent.video_gen_registry import get_active_provider, get_provider, list_providers
from .hermes.modules.agent.web_search_provider import WebSearchProvider
from .hermes.modules.agent.web_search_registry import get_active_extract_provider, get_active_search_provider

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class AgentConfig:
    """Agent 配置"""
    model: str = "gpt-4o-mini"
    max_turns: int = 50
    system_prompt: str = ""
    session_id: str = ""
    tools_enabled: bool = True
    memory_enabled: bool = True


@dataclass
class TurnResult:
    """单轮执行结果"""
    turn_number: int
    message: str
    tool_calls: list[dict] = field(default_factory=list)
    finish_reason: str = ""
    tokens_used: int = 0


@dataclass
class AgentRunResult:
    """Agent 完整运行结果"""
    turns: list[TurnResult] = field(default_factory=list)
    final_output: str = ""
    total_tokens: int = 0
    success: bool = True


# ── Protocols ────────────────────────────────────────────────────────────


class AgentRuntimeProtocol(Protocol):
    """Agent 运行时协议"""
    def execute_turn(self, message: str, session_id: str) -> TurnResult: ...
    def execute_tool(self, name: str, args: dict) -> str: ...
    def set_system_prompt(self, prompt: str) -> None: ...
    def get_history(self, session_id: str, limit: int = 50) -> list[dict]: ...


class ContextManagerProtocol(Protocol):
    """上下文管理器协议"""
    def compress(self, messages: list[dict], max_tokens: int) -> list[dict]: ...
    def estimate_tokens(self, text: str) -> int: ...
    def truncate(self, messages: list[dict], max_tokens: int) -> list[dict]: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_agent_runtime(config: Optional[AgentConfig] = None) -> AgentRuntimeProtocol:
    """创建 Agent 运行时

    需要依赖：llm-client / tool-system / memory-system / state-management
    这些组件应在调用此工厂前完成初始化。
    """
    from gateway.run import AgentRunner
    cfg = config or AgentConfig()
    return AgentRunner(
        model=cfg.model,
        max_turns=cfg.max_turns,
        system_prompt=cfg.system_prompt,
    )


def create_context_manager() -> ContextManagerProtocol:
    """创建上下文管理器"""
    from agent.context_compressor import ContextCompressor
    return ContextCompressor()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def run_agent(
    message: str,
    session_id: str = "default",
    config: Optional[AgentConfig] = None,
) -> AgentRunResult:
    """运行 Agent（单次交互）

    这是最高层级的便捷入口，适用于简单用例。
    复杂场景应直接使用 AgentRuntimeProtocol。
    """
    runtime = create_agent_runtime(config)

    result = AgentRunResult()
    # 执行 Agent 循环
    turn = runtime.execute_turn(message, session_id)
    result.turns.append(turn)
    result.final_output = turn.message
    return result


def set_system_prompt(prompt: str) -> None:
    """设置系统提示词"""
    create_agent_runtime().set_system_prompt(prompt)


def estimate_tokens(text: str) -> int:
    """估算文本 token 数"""
    ctx = create_context_manager()
    return ctx.estimate_tokens(text)


def compress_context(messages: list[dict], max_tokens: int) -> list[dict]:
    """压缩上下文"""
    ctx = create_context_manager()
    return ctx.compress(messages, max_tokens)


def clear_conversation_history(session_id: str = "default") -> None:
    """清除会话历史"""
    runtime = create_agent_runtime()
    runtime.get_history(session_id)  # ensure session exists for now
    from gateway.session import SessionManager
    SessionManager().close_session(session_id)


def get_conversation_history(session_id: str) -> list[dict]:
    """获取会话历史"""
    return create_agent_runtime().get_history(session_id)
