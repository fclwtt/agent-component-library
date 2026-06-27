"""Gateway - Public API

消息网关接口。提供消息路由、会话管理、多平台适配。
其他组件只能通过此模块与网关交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from gateway.channel_directory import format_directory_for_display, load_directory, lookup_channel_type, resolve_channel_name
from gateway.config import HomeChannel, Platform, PlatformConfig, load_gateway_config
from gateway.delivery import DeliveryRouter, DeliveryTarget, _looks_like_int, _looks_like_telegram_private_chat_id
from gateway.drain_control import clear_drain_request, drain_requested, write_drain_request
from gateway.mirror import mirror_to_session
from gateway.pairing import PairingStore
from gateway.platform_registry import PlatformEntry, platform_registry
from gateway.platforms._http_client_limits import platform_httpx_limits
from gateway.platforms.base import BasePlatformAdapter, GATEWAY_SECRET_CAPTURE_UNSUPPORTED_MESSAGE, MessageEvent, MessageType, ProcessingOutcome, SUPPORTED_DOCUMENT_TYPES, SUPPORTED_IMAGE_DOCUMENT_TYPES, SUPPORTED_VIDEO_TYPES, SendResult, _TEXT_INJECT_EXTENSIONS, _ssrf_redirect_guard, cache_audio_from_bytes, cache_audio_from_url, cache_document_from_bytes, cache_image_from_bytes, cache_image_from_url, cache_media_bytes, cache_video_from_bytes, classify_send_error, is_host_excluded_by_no_proxy, is_network_accessible, merge_pending_message_event, proxy_kwargs_for_aiohttp, proxy_kwargs_for_bot, resolve_channel_prompt, resolve_channel_skills, resolve_proxy_url, safe_url_for_log, should_send_media_as_audio, utf16_len, validate_inbound_media_size
from gateway.platforms.bluebubbles import BlueBubblesAdapter, check_bluebubbles_requirements
from gateway.platforms.helpers import MessageDeduplicator, ThreadParticipationTracker, redact_phone, strip_markdown
from gateway.platforms.signal_format import markdown_to_signal
from gateway.platforms.signal_rate_limit import SIGNAL_BATCH_PACING_NOTICE_THRESHOLD, SIGNAL_MAX_ATTACHMENTS_PER_MSG, SIGNAL_RATE_LIMIT_MAX_ATTEMPTS, _extract_retry_after_seconds, _format_wait, _is_signal_rate_limit_error, _signal_send_timeout, get_scheduler
from gateway.platforms.weixin import check_weixin_requirements, qr_login, send_weixin_direct
from gateway.platforms.whatsapp_common import WhatsAppBehaviorMixin, resolve_whatsapp_bridge_dir
from gateway.platforms.yuanbao import get_active_adapter, send_yuanbao_direct
from gateway.platforms.yuanbao_sticker import get_random_sticker, get_sticker_by_id, get_sticker_by_name, search_stickers
from gateway.restart import DEFAULT_GATEWAY_RESTART_DRAIN_TIMEOUT, GATEWAY_FATAL_CONFIG_EXIT_CODE, GATEWAY_SERVICE_RESTART_EXIT_CODE, parse_restart_drain_timeout
from gateway.run import _gateway_runner_ref, _load_gateway_config, _redact_approval_command, _resolve_gateway_model, _resolve_runtime_agent_kwargs, cfg_get, start_gateway
from gateway.session import SessionSource, build_session_key
from gateway.session_context import _UNSET, _VAR_MAP, async_delivery_supported, clear_session_vars, get_session_env, set_current_session_id, set_session_vars
from gateway.status import _get_process_start_time, _pid_exists, _pid_from_record, _read_pid_record, _read_process_cmdline, acquire_scoped_lock, derive_gateway_busy, derive_gateway_drainable, get_process_start_time, get_running_pid, get_runtime_status_running_pid, is_gateway_running, is_gateway_runtime_lock_active, looks_like_gateway_command_line, looks_like_gateway_runtime_command_line, parse_active_agents, read_runtime_status, release_scoped_lock, remove_pid_file, terminate_pid, write_planned_stop_marker
from gateway.sticker_cache import STICKER_VISION_PROMPT, build_animated_sticker_injection, build_sticker_injection, cache_sticker_description, get_cached_description
from gateway.whatsapp_identity import to_whatsapp_jid

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class Message:
    """消息"""
    content: str
    platform: str
    user_id: str
    chat_id: str
    message_id: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class Session:
    """会话"""
    session_id: str
    platform: str
    user_id: str
    chat_id: str
    metadata: dict = field(default_factory=dict)


# ── Protocols ────────────────────────────────────────────────────────────


class GatewayProtocol(Protocol):
    """网关协议"""
    def start(self, host: str = "0.0.0.0", port: int = 8080) -> None: ...
    def stop(self) -> None: ...
    def send_message(self, message: Message) -> bool: ...
    def broadcast(self, message: Message) -> None: ...
    def register_platform(self, name: str, adapter: Any) -> None: ...
    def unregister_platform(self, name: str) -> bool: ...


class SessionManagerProtocol(Protocol):
    """会话管理器协议"""
    def create_session(self, platform: str, user_id: str, chat_id: str) -> Session: ...
    def get_session(self, session_id: str) -> Optional[Session]: ...
    def list_sessions(self, platform: Optional[str] = None) -> list[Session]: ...
    def close_session(self, session_id: str) -> bool: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_gateway(port: int = 8080) -> GatewayProtocol:
    """创建消息网关"""
    from gateway.run import GatewayRunner
    return GatewayRunner(port=port)


def create_session_manager() -> SessionManagerProtocol:
    """创建会话管理器"""
    from gateway.session import SessionManager
    return SessionManager()


def create_platform_registry() -> object:
    """创建平台注册表"""
    from gateway.platform_registry import PlatformRegistry
    return PlatformRegistry()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def send(platform: str, chat_id: str, content: str) -> bool:
    """发送消息到指定平台"""
    gateway = create_gateway()
    msg = Message(content=content, platform=platform, user_id="", chat_id=chat_id)
    return gateway.send_message(msg)


def register_platform_adapter(name: str, adapter_class: type) -> None:
    """注册平台适配器"""
    registry = create_platform_registry()
    registry.register(name, adapter_class)


def unregister_platform_adapter(name: str) -> bool:
    """注销平台适配器"""
    registry = create_platform_registry()
    return registry.unregister(name)


def list_registered_platforms() -> list[str]:
    """列出已注册的平台"""
    registry = create_platform_registry()
    return [entry["name"] for entry in registry.all_entries()]
