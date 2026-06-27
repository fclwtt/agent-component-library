"""Plugin System - Public API

插件系统接口。提供插件注册、加载、管理，以及平台适配器管理。
其他组件只能通过此模块与插件系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.plugins.cron_providers.chronos.verify import get_fire_verifier
from .hermes.modules.plugins.platforms.matrix.adapter import MatrixAdapter
from .hermes.modules.plugins.platforms.telegram.adapter import TelegramAdapter, _strip_mdv2
from .hermes.modules.plugins.plugin_utils import SingletonSlot
from .hermes.modules.plugins.teams_pipeline.runtime import bind_gateway_runtime
from .hermes.modules.plugins.web.exa.provider import _get_exa_client
from .hermes.modules.plugins.web.firecrawl.provider import Firecrawl, _firecrawl_backend_help_suffix, _get_firecrawl_client, _get_firecrawl_gateway_url, _is_tool_gateway_ready, check_firecrawl_api_key
from .hermes.modules.plugins.web.parallel.provider import _get_async_parallel_client, _get_parallel_client
from .hermes.modules.plugins.web.tavily.provider import _normalize_tavily_documents, _normalize_tavily_search_results, _tavily_request

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    entry_point: str = ""


@dataclass
class PlatformEntry:
    """平台条目"""
    name: str
    adapter_class: type
    config_schema: dict = field(default_factory=dict)
    description: str = ""


# ── Protocols ────────────────────────────────────────────────────────────


class PluginLoaderProtocol(Protocol):
    """插件加载器协议"""
    def discover(self, path: Optional[str] = None) -> list[PluginInfo]: ...
    def load(self, name: str) -> Any: ...
    def unload(self, name: str) -> bool: ...
    def reload(self, name: str) -> Any: ...
    def list_loaded(self) -> list[PluginInfo]: ...
    def is_loaded(self, name: str) -> bool: ...


class PlatformRegistryProtocol(Protocol):
    """平台注册表协议"""
    def register(self, entry: PlatformEntry) -> None: ...
    def unregister(self, name: str) -> bool: ...
    def get(self, name: str) -> Optional[PlatformEntry]: ...
    def all_entries(self) -> list[PlatformEntry]: ...
    def create_adapter(self, name: str, config: Any) -> Optional[Any]: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_plugin_loader() -> PluginLoaderProtocol:
    """创建插件加载器"""
    from plugins.plugin_loader import PluginLoader
    return PluginLoader()


def create_platform_registry() -> PlatformRegistryProtocol:
    """创建平台注册表"""
    from plugins.platform_registry import PlatformRegistry
    return PlatformRegistry()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def discover_plugins(path: Optional[str] = None) -> list[PluginInfo]:
    """发现插件"""
    return create_plugin_loader().discover(path)


def load_plugin(name: str) -> Any:
    """加载插件"""
    return create_plugin_loader().load(name)


def register_platform(name: str, adapter_class: type, config_schema: Optional[dict] = None) -> None:
    """注册平台适配器"""
    entry = PlatformEntry(name=name, adapter_class=adapter_class, config_schema=config_schema or {})
    create_platform_registry().register(entry)


def get_platform(name: str) -> Optional[PlatformEntry]:
    """获取平台信息"""
    return create_platform_registry().get(name)


def list_platforms() -> list[PlatformEntry]:
    """列出已注册平台"""
    return create_platform_registry().all_entries()


def create_platform_adapter(name: str, config: Any) -> object:
    """创建平台适配器实例"""
    return create_platform_registry().create_adapter(name, config)
