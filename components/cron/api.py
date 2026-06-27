"""Cron - Public API

定时任务接口。提供定时任务注册、调度、管理。
其他组件只能通过此模块与定时任务系统交互。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol


# ── Data Types ──────────────────────────────────────────────────────────


@dataclass
class CronJob:
    """定时任务条目"""
    name: str
    schedule: str
    handler: Callable
    enabled: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class CronResult:
    """定时任务执行结果"""
    job_name: str
    success: bool
    output: str = ""
    error: Optional[str] = None


# ── Protocols ────────────────────────────────────────────────────────────


class CronManagerProtocol(Protocol):
    """定时任务管理器协议"""
    def register(self, job: CronJob) -> str: ...
    def unregister(self, name: str) -> bool: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def list_jobs(self) -> list[CronJob]: ...
    def get_job(self, name: str) -> Optional[CronJob]: ...
    def pause(self, name: str) -> bool: ...
    def resume(self, name: str) -> bool: ...
    def run_once(self, name: str) -> CronResult: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_cron_manager() -> CronManagerProtocol:
    """创建定时任务管理器"""
    from gateway.cron_manager import CronManager
    return CronManager()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def schedule(name: str, schedule: str, handler: Callable) -> str:
    """注册定时任务"""
    manager = create_cron_manager()
    job = CronJob(name=name, schedule=schedule, handler=handler)
    return manager.register(job)


def unschedule(name: str) -> bool:
    """取消定时任务"""
    return create_cron_manager().unregister(name)


def list_scheduled_jobs() -> list[CronJob]:
    """列出所有定时任务"""
    return create_cron_manager().list_jobs()


def start_scheduler() -> None:
    """启动定时调度器"""
    create_cron_manager().start()


def stop_scheduler() -> None:
    """停止定时调度器"""
    create_cron_manager().stop()
