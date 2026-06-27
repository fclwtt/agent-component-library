"""ACP Adapter - Public API

ACP (Agent Communication Protocol) 适配器接口。
提供跨 Agent 通信能力。
其他组件只能通过此模块与 ACP 适配器交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from acp_adapter.edit_approval import maybe_require_edit_approval

# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class ACPRequest:
    """ACP 请求"""
    agent_id: str
    action: str
    payload: dict
    request_id: str = ""


@dataclass
class ACPResponse:
    """ACP 响应"""
    success: bool
    result: Any = None
    error: Optional[str] = None
    request_id: str = ""


# ── Protocols ────────────────────────────────────────────────────────────


class ACPAdapterProtocol(Protocol):
    """ACP 适配器协议"""
    def handle_request(self, request: ACPRequest) -> ACPResponse: ...
    def send_request(self, target_agent: str, request: ACPRequest) -> ACPResponse: ...
    def register_handler(self, action: str, handler: Any) -> None: ...
    def start_server(self, host: str = "0.0.0.0", port: int = 8765) -> None: ...
    def stop_server(self) -> None: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_acp_adapter() -> ACPAdapterProtocol:
    """创建 ACP 适配器"""
    from acp_adapter.acp_server import ACPServer
    return ACPServer()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def send_to_agent(agent_id: str, action: str, payload: dict) -> ACPResponse:
    """向另一个 Agent 发送请求"""
    adapter = create_acp_adapter()
    request = ACPRequest(agent_id=agent_id, action=action, payload=payload)
    return adapter.send_request(agent_id, request)


def register_acp_handler(action: str, handler: Any) -> None:
    """注册 ACP 动作处理器"""
    create_acp_adapter().register_handler(action, handler)


def start_acp_server(port: int = 8765) -> None:
    """启动 ACP 服务器"""
    create_acp_adapter().start_server(port=port)


def stop_acp_server() -> None:
    """停止 ACP 服务器"""
    create_acp_adapter().stop_server()
