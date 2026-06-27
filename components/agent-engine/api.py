"""Agent Engine - Public API

Agent 核心引擎接口。协调 LLM 调用、工具执行、记忆管理、上下文管理。
其他组件只能通过此模块与 Agent 引擎交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol


# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class AgentConfig:
    """Agent 配置"""
    model: str = "gpt-4o-mini"
    max_turns: int = 50
    system_prompt: str = ""
    session_id: str = ""
    tools_enabled: bool = True
    memory_enabled: bool = True


@dataclass
class TurnResult:
    """单轮执行结果"""
    turn_number: int
    message: str
    tool_calls: list[dict] = field(default_factory=list)
    finish_reason: str = ""
    tokens_used: int = 0


@dataclass
class AgentRunResult:
    """Agent 完整运行结果"""
    turns: list[TurnResult] = field(default_factory=list)
    final_output: str = ""
    total_tokens: int = 0
    success: bool = True


# ── Protocols ────────────────────────────────────────────────────────────


class AgentRuntimeProtocol(Protocol):
    """Agent 运行时协议"""
    def execute_turn(self, message: str, session_id: str) -> TurnResult: ...
    def execute_tool(self, name: str, args: dict) -> str: ...
    def set_system_prompt(self, prompt: str) -> None: ...
    def get_history(self, session_id: str, limit: int = 50) -> list[dict]: ...


class ContextManagerProtocol(Protocol):
    """上下文管理器协议"""
    def compress(self, messages: list[dict], max_tokens: int) -> list[dict]: ...
    def estimate_tokens(self, text: str) -> int: ...
    def truncate(self, messages: list[dict], max_tokens: int) -> list[dict]: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_agent_runtime(config: Optional[AgentConfig] = None) -> AgentRuntimeProtocol:
    """创建 Agent 运行时

    需要依赖：llm-client / tool-system / memory-system / state-management
    这些组件应在调用此工厂前完成初始化。
    """
    from gateway.run import AgentRunner
    cfg = config or AgentConfig()
    return AgentRunner(
        model=cfg.model,
        max_turns=cfg.max_turns,
        system_prompt=cfg.system_prompt,
    )


def create_context_manager() -> ContextManagerProtocol:
    """创建上下文管理器"""
    from agent.context_compressor import ContextCompressor
    return ContextCompressor()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def run_agent(
    message: str,
    session_id: str = "default",
    config: Optional[AgentConfig] = None,
) -> AgentRunResult:
    """运行 Agent（单次交互）

    这是最高层级的便捷入口，适用于简单用例。
    复杂场景应直接使用 AgentRuntimeProtocol。
    """
    runtime = create_agent_runtime(config)

    result = AgentRunResult()
    # 执行 Agent 循环
    turn = runtime.execute_turn(message, session_id)
    result.turns.append(turn)
    result.final_output = turn.message
    return result


def set_system_prompt(prompt: str) -> None:
    """设置系统提示词"""
    create_agent_runtime().set_system_prompt(prompt)


def estimate_tokens(text: str) -> int:
    """估算文本 token 数"""
    ctx = create_context_manager()
    return ctx.estimate_tokens(text)


def compress_context(messages: list[dict], max_tokens: int) -> list[dict]:
    """压缩上下文"""
    ctx = create_context_manager()
    return ctx.compress(messages, max_tokens)


def clear_conversation_history(session_id: str = "default") -> None:
    """清除会话历史"""
    runtime = create_agent_runtime()
    runtime.get_history(session_id)  # ensure session exists for now
    from gateway.session import SessionManager
    SessionManager().close_session(session_id)


def get_conversation_history(session_id: str) -> list[dict]:
    """获取会话历史"""
    return create_agent_runtime().get_history(session_id)
