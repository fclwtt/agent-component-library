"""Memory System - Public API

记忆系统接口。其他组件只能通过此模块与记忆系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.plugins.memory.honcho.cli import clone_honcho_for_profile, sync_honcho_profiles_quiet
from .hermes.modules.plugins.memory.honcho.client import HonchoClientConfig, get_honcho_client, reset_honcho_client, resolve_config_path
from .hermes.modules.tools.memory_tool import MemoryStore, apply_memory_pending, load_on_disk_store

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class MemoryQuery:
    """记忆查询参数"""
    query: str
    session_id: str
    limit: int = 10
    metadata_filter: Optional[dict] = None


@dataclass
class MemoryResult:
    """记忆查询结果"""
    content: str
    session_id: str
    relevance: float = 0.0
    metadata: dict = field(default_factory=dict)


# ── Protocols ────────────────────────────────────────────────────────────


class MemoryProviderProtocol(Protocol):
    """记忆提供者协议"""
    def name(self) -> str: ...
    def is_available(self) -> bool: ...
    def initialize(self, session_id: str, **kwargs) -> None: ...
    def system_prompt_block(self) -> str: ...
    def prefetch(self, query: str, session_id: str) -> str: ...
    def get_tool_schemas(self) -> list[dict]: ...
    def handle_tool_call(self, tool_name: str, args: dict, **kwargs) -> str: ...
    def shutdown(self) -> None: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_memory_provider(provider_type: str = "local", **config) -> MemoryProviderProtocol:
    """创建记忆提供者

    延迟导入 hermes 模块。
    """
    if provider_type == "local":
        from agent.memory_manager import MemoryManager
        return MemoryManager(**config)
    # mem0, holographic, honcho 等其他提供者按需添加
    raise ValueError(f"未知的记忆提供者类型: {provider_type}")


def create_memory_tool() -> object:
    """创建记忆工具（在 tool-system 中注册）"""
    from tools.memory_tool import MemoryTool
    return MemoryTool()
