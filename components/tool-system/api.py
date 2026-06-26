"""Tool System - Public API

工具系统接口。其他组件只能通过此模块与工具系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol


#  Data Types 


@dataclass
class ToolEntry:
    """工具条目"""
    name: str
    toolset: str
    schema: dict
    handler: Callable
    description: str = ""
    emoji: str = ""


@dataclass
class ToolResult:
    """工具调用结果"""
    output: str
    status: str = "ok"
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


#  Protocols 


class ToolRegistryProtocol(Protocol):
    """工具注册表协议"""
    def register(self, name: str, toolset: str, schema: dict, handler: Callable) -> None: ...
    def deregister(self, name: str) -> None: ...
    def get_entry(self, name: str) -> Optional[ToolEntry]: ...
    def get_definitions(self, tool_names: set[str]) -> list[dict]: ...
    def dispatch(self, name: str, args: dict) -> str: ...
    def get_all_tool_names(self) -> list[str]: ...
    def is_toolset_available(self, toolset: str) -> bool: ...
    def get_available_toolsets(self) -> dict[str, dict]: ...


class ToolExecutorProtocol(Protocol):
    """工具执行器协议（扩展能力）"""
    def execute_terminal(self, command: str) -> ToolResult: ...
    def execute_file(self, path: str, operation: str, **kwargs) -> ToolResult: ...
    def execute_mcp(self, server_name: str, tool_name: str, args: dict) -> ToolResult: ...


#  Factory Functions 


def create_tool_registry() -> ToolRegistryProtocol:
    """创建工具注册表"""
    from .hermes.modules.tools.registry import ToolRegistry
    return ToolRegistry()


def create_tool_executor(registry: ToolRegistryProtocol) -> ToolExecutorProtocol:
    """创建工具执行器（包装终端/文件/MCP 等工具）"""
    from .hermes.modules.tools.terminal_tool import TerminalTool
    return TerminalTool()


#  便捷函数


def register_tool(name: str, toolset: str, schema: dict, handler: callable) -> None:
    """注册工具到注册表"""
    registry = create_tool_registry()
    registry.register(name, toolset, schema, handler) 


def execute_tool(name: str, args: dict) -> str:
    """便捷工具调用"""
    registry = create_tool_registry()
    return registry.dispatch(name, args)


def list_available_tools() -> list[ToolEntry]:
    """列出所有可用工具"""
    registry = create_tool_registry()
    return [ToolEntry(name=n, toolset="", schema={}, handler=lambda: None)
            for n in registry.get_all_tool_names()]
