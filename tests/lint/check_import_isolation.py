"""Import Isolation Checker

静态分析工具，确保硬隔离规则不被违反。
规则：组件间只能通过 api.py 互相引用，禁止直接导入 hermes 内部模块。
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Optional


COMPONENT_API_DEPS: dict[str, set[str]] = {
    # Layer 0: 基础设施 → 无组件依赖
    "llm-client": set(),
    "memory-system": set(),
    "tool-system": set(),
    "state-management": set(),
    "infrastructure": set(),
    # Layer 1: 编排层 → 依赖 Layer 0
    "security": {"state-management"},
    "gateway": {"tool-system", "memory-system", "state-management"},
    "cron": {"state-management"},
    "agent-engine": {"llm-client", "tool-system", "memory-system", "state-management"},
    # Layer 2: 消费层 → 依赖 Layer 0 + Layer 1
    "plugin-system": {"state-management", "security"},
    "skill-system": {"tool-system", "state-management", "agent-engine"},
    "acp-adapter": {"agent-engine", "tool-system"},
    "entry-points": {"agent-engine", "tool-system"},
    "cli": {"agent-engine", "tool-system"},
    "tui": {"agent-engine", "tool-system"},
}


class CrossComponentImportFinder(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._check_import(alias.name, node.lineno)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self._check_import(node.module, node.lineno)

    def _check_import(self, module_name: str, lineno: int) -> None:
        parts = module_name.split(".")
        current_comp = self._detect_current_component()
        if not current_comp:
            return

        # Rule 1: Non-api.py must not import from other components directly
        is_api = self.file_path.endswith("/api.py")
        if not is_api and len(parts) >= 3 and parts[0] == "components":
            target = parts[1]
            if target != current_comp and ".api" not in module_name:
                self.violations.append(
                    f"{self.file_path}:{lineno}: 禁止直接导入 {module_name} （跨组件引用必须通过 api.py）"
                )

        # Rule 2: Must not import other component's hermes internals
        if "hermes" in parts and current_comp not in parts:
            self.violations.append(
                f"{self.file_path}:{lineno}: 禁止引用其他组件的 hermes 内部模块：{module_name}"
            )

    def _detect_current_component(self) -> Optional[str]:
        p = Path(self.file_path).resolve()
        parts = p.parts
        try:
            idx = parts.index("components")
            if idx + 1 < len(parts):
                return parts[idx + 1]
        except ValueError:
            pass
        return None


def check_file(path: str | Path) -> list[str]:
    path = Path(path)
    if not path.exists() or path.suffix != ".py" or path.name == "api.py":
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        try:
            tree = ast.parse(f.read(), filename=str(path))
        except SyntaxError as e:
            return [f"{path}: 语法错误: {e}"]
    finder = CrossComponentImportFinder(str(path))
    finder.visit(tree)
    return finder.violations


def check_repository(repo_root: str | Path) -> list[str]:
    root = Path(repo_root)
    comp_dir = root / "components"
    if not comp_dir.is_dir():
        return [f"{comp_dir} 不存在"]
    all_v = []
    for py_file in comp_dir.rglob("*.py"):
        all_v.extend(check_file(py_file))
    return all_v


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    violations = check_repository(root)
    if violations:
        print(f"发现 {len(violations)} 个 import 隔离违规:\n")
        for v in violations:
            print(f"  \u274c {v}")
        sys.exit(1)
    else:
        print("\u2705 Import 隔离检查通过，无违规")
        sys.exit(0)


if __name__ == "__main__":
    main()
