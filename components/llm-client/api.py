"""LLM Client - Public API

模型调用接口。其他组件只能通过此模块与 LLM 系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol


# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class ModelConfig:
    """模型配置定义"""
    model: str
    base_url: str = "https://api.openai.com/v1"
    api_key_env: str = "OPENAI_API_KEY"
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class LLMResponse:
    """LLM 调用返回结果"""
    content: str
    finish_reason: str = ""
    usage: dict = field(default_factory=dict)
    raw: dict = field(default_factory=dict)


# ── Protocols ────────────────────────────────────────────────────────────


class ProviderProfileProtocol(Protocol):
    """模型提供者配置协议"""
    def get_hostname(self) -> str: ...
    def prepare_messages(self, messages: list[dict]) -> list[dict]: ...
    def build_extra_body(self) -> Optional[dict]: ...
    def get_max_tokens(self, model: Optional[str] = None) -> Optional[int]: ...


class LLMCallingProtocol(Protocol):
    """LLM 调用协议"""
    def call(self, messages: list[dict], model: str, **kwargs) -> LLMResponse: ...
    async def async_call(self, messages: list[dict], model: str, **kwargs) -> LLMResponse: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_openai_client(config: Optional[ModelConfig] = None) -> LLMCallingProtocol:
    """创建 OpenAI 兼容的 LLM 客户端

    延迟导入 hermes 模块，启动时无需加载全部依赖。
    """
    from tools.openrouter_client import OpenRouterClient
    return OpenRouterClient()


def create_provider_profile(name: str, config: dict) -> ProviderProfileProtocol:
    """创建模型提供者配置"""
    from providers.base import ProviderProfile
    return ProviderProfile(**config)
