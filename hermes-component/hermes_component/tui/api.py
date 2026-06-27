"""TUI - Public API

终端用户界面接口。提供仪表盘、状态显示、实时监控。
其他组件只能通过此模块与 TUI 层交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.tui_gateway.ws import handle_ws

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class DashboardWidget:
    """仪表盘小部件"""
    name: str
    component: Any
    position: tuple[int, int] = (0, 0)
    refresh_interval: float = 1.0


@dataclass
class StatusUpdate:
    """状态更新"""
    service: str
    status: str
    detail: str = ""
    timestamp: Optional[float] = None


# ── Protocols ────────────────────────────────────────────────────────────


class TUIProtocol(Protocol):
    """TUI 协议"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def add_widget(self, widget: DashboardWidget) -> None: ...
    def remove_widget(self, name: str) -> bool: ...
    def update_status(self, update: StatusUpdate) -> None: ...
    def log(self, message: str, level: str = "info") -> None: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_tui() -> TUIProtocol:
    """创建 TUI 实例"""
    from tui_gateway.dashboard import TUIDashboard
    return TUIDashboard()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def start_dashboard() -> None:
    """启动仪表盘"""
    create_tui().start()


def stop_dashboard() -> None:
    """停止仪表盘"""
    create_tui().stop()


def show_status(service: str, status: str, detail: str = "") -> None:
    """显示状态更新"""
    tui = create_tui()
    update = StatusUpdate(service=service, status=status, detail=detail)
    tui.update_status(update)


def log_to_dashboard(message: str, level: str = "info") -> None:
    """向仪表盘发送日志"""
    create_tui().log(message, level)


def register_widget(name: str, component: Any, refresh_interval: float = 1.0) -> None:
    """注册仪表盘小部件"""
    tui = create_tui()
    widget = DashboardWidget(name=name, component=component, refresh_interval=refresh_interval)
    tui.add_widget(widget)


def unregister_widget(name: str) -> bool:
    """注销仪表盘小部件"""
    return create_tui().remove_widget(name)
