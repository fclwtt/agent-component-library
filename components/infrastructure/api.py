"""Infrastructure - Public API

公共基础设施接口。提供日志、执行环境、通用工具等底层能力。
其他组件只能通过此模块使用基础设施层。
"""
from __future__ import annotations

from typing import Any, Optional, Protocol


# ── Protocols ────────────────────────────────────────────────────────────


class LoggerProtocol(Protocol):
    """日志协议"""
    def debug(self, msg: str, **kwargs) -> None: ...
    def info(self, msg: str, **kwargs) -> None: ...
    def warning(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...
    def critical(self, msg: str, **kwargs) -> None: ...


class ExecutionEnvProtocol(Protocol):
    """执行环境协议"""
    def is_available(self) -> bool: ...
    def execute(self, code: str, language: str = "python") -> str: ...
    def install_package(self, package_name: str) -> bool: ...


# ── Factory Functions ──────────────────────────────────────────────────


def get_logger(name: str) -> LoggerProtocol:
    """获取日志记录器"""
    import logging
    return logging.getLogger(name)


def create_execution_env(name: str = "docker") -> Optional[ExecutionEnvProtocol]:
    """创建代码执行环境"""
    try:
        from .hermes.modules.tools.environments.docker_env import DockerExecutionEnv
        return DockerExecutionEnv()
    except ImportError:
        return None


def create_evm_client() -> object:
    """创建 EVM 区块链客户端"""
    from .hermes.modules.gateway.evm_client import EVMClient
def create_evm_client() -> object:
    """创建 EVM 区块链客户端"""
    from .hermes.modules.gateway.evm_client import EVMClient
    return EVMClient()


    """创建代码执行环境"""
    try:
        from .hermes.modules.tools.environments.docker_env import DockerExecutionEnv
        return DockerExecutionEnv()
    except ImportError:
        return None




def evm_client() -> object:
    """创建 EVM 区块链客户端"""
    from .hermes.modules.gateway.evm_client import EVMClient
    return EVMClient()


def url_safety_checker() -> object:
    """创建 URL 安全检查器"""
    from .hermes.modules.tools.url_safety import URLSafetyChecker
    return URLSafetyChecker()


def path_security_checker() -> object:
    """创建路径安全检查器"""
    from .hermes.modules.tools.path_security import PathSecurityChecker
    return PathSecurityChecker()
