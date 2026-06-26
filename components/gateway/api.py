"""Gateway - Public API

消息网关接口。提供消息路由、会话管理、多平台适配。
其他组件只能通过此模块与网关交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol


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
    from .hermes.modules.gateway.run import GatewayRunner
    return GatewayRunner(port=port)


def create_session_manager() -> SessionManagerProtocol:
    """创建会话管理器"""
    from .hermes.modules.gateway.session import SessionManager
    return SessionManager()


def create_platform_registry() -> object:
    """创建平台注册表"""
    from .hermes.modules.gateway.platform_registry import PlatformRegistry
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
