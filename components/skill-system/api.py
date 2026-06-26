"""Skill System - Public API

技能系统接口。提供技能注册、加载、执行。
其他组件只能通过此模块与技能系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol


# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class SkillInfo:
    """技能信息"""
    name: str
    description: str = ""
    version: str = "1.0.0"
    author: str = ""


@dataclass
class SkillResult:
    """技能执行结果"""
    output: str
    success: bool = True
    error: Optional[str] = None


# ── Protocols ────────────────────────────────────────────────────────────


class SkillManagerProtocol(Protocol):
    """技能管理器协议"""
    def register(self, name: str, entry_point: Any) -> None: ...
    def unregister(self, name: str) -> bool: ...
    def execute(self, name: str, **kwargs) -> SkillResult: ...
    def list_skills(self) -> list[SkillInfo]: ...
    def get_skill(self, name: str) -> Optional[SkillInfo]: ...
    def is_available(self, name: str) -> bool: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_skill_manager() -> SkillManagerProtocol:
    """创建技能管理器"""
    from .hermes.modules.skills.skill_manager import SkillManager
    return SkillManager()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def register_skill(name: str, entry_point: Any) -> None:
    """注册技能"""
    create_skill_manager().register(name, entry_point)


def execute_skill(name: str, **kwargs) -> SkillResult:
    """执行技能"""
    return create_skill_manager().execute(name, **kwargs)


def list_skills() -> list[SkillInfo]:
    """列出所有技能"""
    return create_skill_manager().list_skills()


def unregister_skill(name: str) -> bool:
    """注销技能"""
    return create_skill_manager().unregister(name)


def run_skill(name: str, **kwargs) -> str:
    """便捷执行技能（直接返回输出文本）"""
    result = create_skill_manager().execute(name, **kwargs)
    return result.output
