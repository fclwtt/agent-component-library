"""Entry Points - Public API

入口点接口。提供应用级启动入口、服务注册、健康检查。
其他组件只能通过此模块与入口点层交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol


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
        from .hermes.modules.gateway.run import CLIEntryPoint
        return CLIEntryPoint()
    elif mode == "server":
        from .hermes.modules.gateway.run import ServerEntryPoint
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
