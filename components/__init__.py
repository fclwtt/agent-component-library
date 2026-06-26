"""Agent Component Library — Component Package Root

使每个组件的 api.py 可通过 components.{name}.api 导入。
"""
from __future__ import annotations
import importlib
import os
import sys
from types import ModuleType

# 全部15个组件的目录名→Python名映射
_COMPONENT_MAP: dict[str, str] = {
    "acp_adapter": "acp-adapter",
    "agent_engine": "agent-engine",
    "cli": "cli",
    "cron": "cron",
    "entry_points": "entry-points",
    "gateway": "gateway",
    "infrastructure": "infrastructure",
    "llm_client": "llm-client",
    "memory_system": "memory-system",
    "plugin_system": "plugin-system",
    "security": "security",
    "skill_system": "skill-system",
    "state_management": "state-management",
    "tool_system": "tool-system",
    "tui": "tui",
}

def __getattr__(name: str) -> ModuleType:
    """components.{name} → components/{dir}/api.py"""
    if name not in _COMPONENT_MAP:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    actual = _COMPONENT_MAP[name]
    # 先尝试导入 api.py，失败则导入包本身
    try:
        return importlib.import_module(f".{actual}.api", __package__)
    except ImportError:
        return importlib.import_module(f".{actual}", __package__)

def __dir__() -> list[str]:
    return list(_COMPONENT_MAP.keys())
