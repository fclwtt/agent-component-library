"""State Management - Public API

状态管理接口。提供配置管理、凭据存储、全局状态等核心能力。
其他组件只能通过此模块访问状态管理层。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from tools.credential_files import clear_credential_files, to_agent_visible_cache_path

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class AppConfig:
    """应用配置结构"""
    name: str = "magic-orange"
    env: str = "development"
    log_level: str = "INFO"
    settings: dict = field(default_factory=dict)


@dataclass
class Credential:
    """凭据条目"""
    key: str
    value: str
    provider: str = ""


# ── Protocols ────────────────────────────────────────────────────────────


class ConfigManagerProtocol(Protocol):
    """配置管理器协议"""
    def get(self, key: str, default: Any = None) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def load(self, path: Optional[str] = None) -> AppConfig: ...
    def save(self) -> None: ...


class CredentialStoreProtocol(Protocol):
    """凭据存储协议"""
    def get(self, key: str) -> Optional[str]: ...
    def set(self, key: str, value: str) -> None: ...
    def delete(self, key: str) -> bool: ...
    def list_keys(self) -> list[str]: ...


class StateManagerProtocol(Protocol):
    """全局状态管理器协议"""
    def get(self, key: str, default: Any = None) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def update(self, key: str, **fields) -> None: ...
    def clear(self) -> None: ...
    def snapshot(self) -> dict: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_config_manager(path: Optional[str] = None) -> ConfigManagerProtocol:
    """创建配置管理器"""
    from gateway.config import ConfigManager
    cfg = ConfigManager()
    if path:
        cfg.load(path)
    return cfg


def create_credential_store(backend: str = "file") -> CredentialStoreProtocol:
    """创建凭据存储"""
    from agent.credential_pool import CredentialPool
    return CredentialPool()


def create_state_manager() -> StateManagerProtocol:
    """创建状态管理器"""
    from gateway.state_manager import StateManager
    return StateManager()
