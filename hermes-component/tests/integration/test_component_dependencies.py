"""Cross-Component Integration Tests

验证组件间的接口契约、依赖关系、包结构一致性。
"""

from __future__ import annotations

import ast
import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

import pytest


COMPONENTS_DIR = Path(__file__).resolve().parent.parent.parent / "hermes_component"


# ── 1. 组件列表──────────────────────────────────────────────────

ALL_COMPONENTS: dict[str, set[str]] = {
    "llm-client": set(),
    "memory-system": set(),
    "tool-system": {"memory-system", "state-management"},
    "state-management": set(),
    "infrastructure": set(),
    "security": {"state-management"},
    "gateway": {"tool-system", "memory-system", "state-management"},
    "cron": {"state-management"},
    "agent-engine": {"llm-client", "tool-system", "memory-system", "state-management"},
    "plugin-system": {"state-management", "security"},
    "skill-system": {"tool-system", "state-management", "agent-engine"},
    "acp-adapter": {"agent-engine", "tool-system"},
    "entry-points": {"agent-engine", "tool-system"},
    "cli": {"agent-engine", "tool-system", "memory-system"},
    "tui": {"agent-engine", "tool-system"},
}

# Layer definitions
# Read from component.yaml dynamically
def _read_layers():
    deps = {}
    for comp in ALL_COMPONENTS:
        with open(COMPONENTS_DIR / comp / "component.yaml") as f:
            data = yaml.safe_load(f)
        deps[comp] = set(data.get("dependencies", []))
    return deps

ALL_COMPONENTS = sorted([d.name for d in COMPONENTS_DIR.iterdir() if d.is_dir() and d.name != "__pycache__"])


# ── 2. Tests ────────────────────────────────────────────────────────────


class TestApiPyExists:
    """验证每个组件都有 api.py"""

    @pytest.mark.parametrize("comp", ALL_COMPONENTS)
    def test_api_file_exists(self, comp):
        assert (COMPONENTS_DIR / comp / "api.py").exists(), f"{comp}/api.py does not exist"


class TestPackageInit:
    """验证 hermes_component/__init__.py 可用"""

    def test_init_py_exists(self):
        init_file = COMPONENTS_DIR / "__init__.py"
        assert init_file.exists(), "hermes_component/__init__.py missing"

    def test_init_maps_all_components(self):
        """验证 __init__.py 映射了所有带中划线的组件"""
        init_file = COMPONENTS_DIR / "__init__.py"
        with open(init_file) as f:
            content = f.read()
        
        for comp in ALL_COMPONENTS:
            if "-" in comp:
                safe_name = comp.replace("-", "_")
                assert safe_name in content, f"__init__.py 缺少 {comp} 的映射"


class TestComponentYamlConsistency:
    """验证 component.yaml 与期望的接口契约一致"""

    @pytest.mark.parametrize("comp", ALL_COMPONENTS)
    def test_component_yaml_exists(self, comp):
        assert (COMPONENTS_DIR / comp / "component.yaml").exists()

    @pytest.mark.parametrize("comp", ALL_COMPONENTS)
    def test_interfaces_provides_are_lists(self, comp):
        with open(COMPONENTS_DIR / comp / "component.yaml") as f:
            data = yaml.safe_load(f)
        ifaces = data.get("interfaces", {})
        assert isinstance(ifaces.get("provides", []), list)
        assert isinstance(ifaces.get("requires", []), list)

    @pytest.mark.parametrize("comp", ALL_COMPONENTS)
    def test_dependencies_are_lists(self, comp):
        with open(COMPONENTS_DIR / comp / "component.yaml") as f:
            data = yaml.safe_load(f)
        deps = data.get("dependencies", [])
        assert isinstance(deps, list)

    def test_no_cyclic_deps_in_component_yaml(self):
        """从 component.yaml 读取 deps 并检查循环"""
        deps = {}
        for comp in ALL_COMPONENTS:
            with open(COMPONENTS_DIR / comp / "component.yaml") as f:
                data = yaml.safe_load(f)
            deps[comp] = set(data.get("dependencies", []))
        
        visited = set()
        path = []
        
        def dfs(node):
            if node in path:
                cycle = " -> ".join(path + [node])
                raise AssertionError(f"循环依赖: {cycle}")
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            for dep in deps.get(node, set()):
                if dep in deps:  # only if it's a known component
                    dfs(dep)
            path.pop()
        
        for comp in ALL_COMPONENTS:
            dfs(comp)



class TestIndexYaml:
    """验证 index.yaml 与实际情况一致"""

    def test_index_yaml_exists(self):
        index_file = COMPONENTS_DIR.parent / "index.yaml"
        assert index_file.exists()

    def test_index_lists_all_components(self):
        index_file = COMPONENTS_DIR.parent / "index.yaml"
        with open(index_file) as f:
            data = yaml.safe_load(f)
        
        indexed = {c["name"] for c in data.get("components", {}).get("list", [])}
        for comp in ALL_COMPONENTS:
            assert comp in indexed, f"index.yaml 缺少 {comp}"


class TestLayerDependencies:
    """验证依赖无循环，且 component.yaml 内声明正确"""

    def test_no_cyclic_deps_from_yaml(self):
        deps = _read_layers()
        visited = set()
        path = []
        def dfs(node):
            if node in path:
                path_str = " -> ".join(path + [node])
                raise AssertionError(f"循环依赖: {path_str}")
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            for dep in deps.get(node, set()):
                if dep in ALL_COMPONENTS:
                    dfs(dep)
            path.pop()
        for comp in ALL_COMPONENTS:
            dfs(comp)
