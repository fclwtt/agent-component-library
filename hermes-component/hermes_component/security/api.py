"""Security - Public API

安全组件接口。提供认证、威胁检测、审计日志等安全能力。
其他组件只能通过此模块使用安全层。
"""
from __future__ import annotations

from typing import Optional, Protocol




# ── Re-exports (for cross-component isolation) ────────────────
from .hermes.modules.tools.path_security import validate_within_dir
from .hermes.modules.tools.threat_patterns import scan_for_threats
from .hermes.modules.tools.tirith_security import ensure_installed, is_platform_supported

# ── Protocols ────────────────────────────────────────────────────────────


class ThreatDetectorProtocol(Protocol):
    """威胁检测协议"""
    def check_code(self, code: str, language: str) -> list[str]: ...
    def check_url(self, url: str) -> bool: ...
    def check_command(self, command: str) -> tuple[bool, str]: ...


class SecurityAuditProtocol(Protocol):
    """安全审计协议"""
    def log_event(self, event: str, detail: Optional[str] = None) -> None: ...
    def query_events(self, limit: int = 100) -> list[dict]: ...


# ── Factory Functions ──────────────────────────────────────────────────


def create_threat_detector() -> ThreatDetectorProtocol:
    """创建威胁检测器"""
    from tools.threat_patterns import ThreatDetector
    return ThreatDetector()


def create_security_audit() -> SecurityAuditProtocol:
    """创建安全审计"""
    from tools.audit_logger import AuditLogger
    return AuditLogger()


# ── 便捷函数 ────────────────────────────────────────────────────────────


def is_command_safe(command: str) -> tuple[bool, str]:
    """检查命令是否安全"""
    detector = create_threat_detector()
    return detector.check_command(command)


def is_code_safe(code: str, language: str = "python") -> list[str]:
    """检查代码是否含有安全风险"""
    detector = create_threat_detector()
    return detector.check_code(code, language)


def audit_event(event: str, detail: str = "") -> None:
    """记录安全事件"""
    auditor = create_security_audit()
    auditor.log_event(event, detail)


def require_auth(token: str) -> bool:
    """验证令牌有效性"""
    from gateway.authz_mixin import AuthChecker
    return AuthChecker().verify_token(token)


def is_dangerous_command(command: str) -> bool:
    """判断是否为危险命令"""
    from tools.approval import detect_dangerous_command
    return detect_dangerous_command(command)
