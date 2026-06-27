"""CLI - Public API

命令行界面接口。提供命令解析、执行、交互式对话。
其他组件只能通过此模块与 CLI 层交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class CommandResult:
    """命令执行结果"""
    output: str
    success: bool = True
    error: Optional[str] = None


# ── Protocols ────────────────────────────────────────────────────────────


class CLIProtocol(Protocol):
    """CLI 协议"""
    def execute(self, command: str) -> CommandResult: ...
    def start_interactive(self) -> None: ...
    def register_command(self, name: str, handler: callable, help_text: str = "") -> None: ...
    def list_commands(self) -> list[dict]: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_cli() -> CLIProtocol:
    """创建 CLI 实例"""
    from hermes_cli.main import CLIApp
    return CLIApp()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def run_cli() -> None:
    """启动 CLI 应用"""
    create_cli().start_interactive()


def execute_command(cmd: str) -> CommandResult:
    """执行单条命令"""
    return create_cli().execute(cmd)


def register_cli_command(name: str, handler: callable, help_text: str = "") -> None:
    """注册 CLI 命令"""
    create_cli().register_command(name, handler, help_text)


def list_cli_commands() -> list[dict]:
    """列出所有 CLI 命令"""
    return create_cli().list_commands()
