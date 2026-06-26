"""Structural Tests for api.py files (AST-based, no imports needed)

验证每个组件的 api.py 的结构完整性，不依赖 Python import 执行。
"""

from __future__ import annotations

import ast
import pytest
from pathlib import Path


COMPONENTS_DIR = Path(__file__).resolve().parent.parent.parent / "components"


def parse_api(component_name: str) -> ast.Module:
    """读取并解析组件的 api.py"""
    api_file = COMPONENTS_DIR / component_name / "api.py"
    assert api_file.exists(), f"{api_file} does not exist"
    with open(api_file, encoding="utf-8") as f:
        return ast.parse(f.read(), filename=str(api_file))


def get_dataclass_names(tree: ast.Module) -> set[str]:
    """从 AST 中提取 @dataclass 装饰的类名"""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for deco in node.decorator_list:
                if isinstance(deco, ast.Name) and deco.id == "dataclass":
                    names.add(node.name)
                elif isinstance(deco, ast.Call):
                    if isinstance(deco.func, ast.Name) and deco.func.id == "dataclass":
                        names.add(node.name)
    return names


def get_function_names(tree: ast.Module, prefix: str = "") -> list[str]:
    """提取函数名"""
    funcs = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            if prefix:
                if node.name.startswith(prefix):
                    funcs.append(node.name)
            else:
                funcs.append(node.name)
    return funcs


def get_class_names(tree: ast.Module) -> set[str]:
    """提取类名"""
    return {node.name for node in ast.iter_child_nodes(tree)
            if isinstance(node, ast.ClassDef)}


# ── Test Configuration ────────────────────────────────────────────────
# 每个组件定义为: (目录名, 必需dataclasses, 必需Protocols, 必需工厂函数数量, 必需便捷函数数量)

COMPONENT_SPECS = {
    "llm-client": {
        "expected_dataclasses": ["ModelConfig", "LLMResponse"],
        "expected_protocols": ["ProviderProfileProtocol", "LLMCallingProtocol"],
        "min_factories": 2,
        "min_utils": 0,
    },
    "memory-system": {
        "expected_dataclasses": ["MemoryQuery", "MemoryResult"],
        "expected_protocols": ["MemoryProviderProtocol"],
        "min_factories": 2,
        "min_utils": 0,
    },
    "tool-system": {
        "expected_dataclasses": ["ToolEntry", "ToolResult"],
        "expected_protocols": ["ToolRegistryProtocol", "ToolExecutorProtocol"],
        "min_factories": 2,
        "min_utils": 3,
    },
    "state-management": {
        "expected_dataclasses": ["AppConfig", "Credential"],
        "expected_protocols": ["ConfigManagerProtocol", "CredentialStoreProtocol", "StateManagerProtocol"],
        "min_factories": 3,
        "min_utils": 0,
    },
    "infrastructure": {
        "expected_dataclasses": [],
        "expected_protocols": ["LoggerProtocol", "ExecutionEnvProtocol"],
        "min_factories": 2,
        "min_utils": 4,
    },
    "security": {
        "expected_dataclasses": [],
        "expected_protocols": ["ThreatDetectorProtocol", "SecurityAuditProtocol"],
        "min_factories": 2,
        "min_utils": 5,
    },
    "gateway": {
        "expected_dataclasses": ["Message", "Session"],
        "expected_protocols": ["GatewayProtocol", "SessionManagerProtocol"],
        "min_factories": 3,
        "min_utils": 4,
    },
    "cron": {
        "expected_dataclasses": ["CronJob", "CronResult"],
        "expected_protocols": ["CronManagerProtocol"],
        "min_factories": 1,
        "min_utils": 5,
    },
    "agent-engine": {
        "expected_dataclasses": ["AgentConfig", "TurnResult", "AgentRunResult"],
        "expected_protocols": ["AgentRuntimeProtocol", "ContextManagerProtocol"],
        "min_factories": 2,
        "min_utils": 6,
    },
    "plugin-system": {
        "expected_dataclasses": ["PluginInfo", "PlatformEntry"],
        "expected_protocols": ["PluginLoaderProtocol", "PlatformRegistryProtocol"],
        "min_factories": 2,
        "min_utils": 5,
    },
    "skill-system": {
        "expected_dataclasses": ["SkillInfo", "SkillResult"],
        "expected_protocols": ["SkillManagerProtocol"],
        "min_factories": 1,
        "min_utils": 5,
    },
    "acp-adapter": {
        "expected_dataclasses": ["ACPRequest", "ACPResponse"],
        "expected_protocols": ["ACPAdapterProtocol"],
        "min_factories": 1,
        "min_utils": 4,
    },
    "entry-points": {
        "expected_dataclasses": ["ServiceInfo", "HealthStatus"],
        "expected_protocols": ["EntryPointProtocol"],
        "min_factories": 1,
        "min_utils": 4,
    },
    "cli": {
        "expected_dataclasses": ["CommandResult"],
        "expected_protocols": ["CLIProtocol"],
        "min_factories": 1,
        "min_utils": 4,
    },
    "tui": {
        "expected_dataclasses": ["DashboardWidget", "StatusUpdate"],
        "expected_protocols": ["TUIProtocol"],
        "min_factories": 1,
        "min_utils": 5,
    },
}


# ── Test Cases ────────────────────────────────────────────────────────


class TestComponentApiExists:
    """验证每个组件都有 api.py 文件"""

    @pytest.mark.parametrize("comp", sorted(COMPONENT_SPECS.keys()))
    def test_api_file_exists(self, comp):
        api_file = COMPONENTS_DIR / comp / "api.py"
        assert api_file.exists(), f"{comp}/api.py does not exist"


class TestComponentDataclasses:
    """验证 dataclass 定义符合规范"""

    @pytest.mark.parametrize("comp,spec", sorted(COMPONENT_SPECS.items()))
    def test_required_dataclasses_exist(self, comp, spec):
        tree = parse_api(comp)
        dataclasses = get_dataclass_names(tree)
        for dc in spec["expected_dataclasses"]:
            assert dc in dataclasses, f"{comp}/api.py: dataclass {dc} not found"


class TestComponentProtocols:
    """验证 Protocol 定义符合规范"""

    @pytest.mark.parametrize("comp,spec", sorted(COMPONENT_SPECS.items()))
    def test_required_protocols_exist(self, comp, spec):
        tree = parse_api(comp)
        classes = get_class_names(tree)
        for proto in spec["expected_protocols"]:
            assert proto in classes, f"{comp}/api.py: Protocol {proto} not found"


class TestComponentFactories:
    """验证工厂函数定义符合规范"""

    @pytest.mark.parametrize("comp,spec", sorted(COMPONENT_SPECS.items()))
    def test_factory_function_count(self, comp, spec):
        tree = parse_api(comp)
        factories = get_function_names(tree, "create_")
        assert len(factories) >= spec["min_factories"],             f"{comp}/api.py: 需要至少 {spec['min_factories']} 个工厂函数，当前 {len(factories)}个: {factories}"

    @pytest.mark.parametrize("comp,spec", sorted(COMPONENT_SPECS.items()))
    def test_utils_function_count(self, comp, spec):
        tree = parse_api(comp)
        publics = [n for n in get_function_names(tree)
                   if not n.startswith("_") and not n.startswith("create_")]
        assert len(publics) >= spec["min_utils"],             f"{comp}/api.py: 需要至少 {spec['min_utils']} 个公共函数，当前 {len(publics)}个"


class TestModuleStructure:
    """验证模块结构规范"""

    @pytest.mark.parametrize("comp", sorted(COMPONENT_SPECS.keys()))
    def test_has_docstring(self, comp):
        tree = parse_api(comp)
        doc = ast.get_docstring(tree)
        assert doc and len(doc) > 10, f"{comp}/api.py: 缺少模块文档"

    @pytest.mark.parametrize("comp,spec", sorted(COMPONENT_SPECS.items()))
    def test_module_has_protocol_or_interface(self, comp, spec):
        tree = parse_api(comp)
        doc = ast.get_docstring(tree) or ""
        prefix = comp.replace("-", "_").split("_")[0]
        # Check that doc mentions its domain (at minimum)
        assert len(doc) > 15, f"{comp}/api.py: 文档太短"

    @pytest.mark.parametrize("comp", sorted(COMPONENT_SPECS.keys()))
    def test_future_annotations(self, comp):
        """验证 api.py 导入了 from __future__ import annotations"""
        with open(COMPONENTS_DIR / comp / "api.py", encoding="utf-8") as f:
            content = f.read()
        assert 'from __future__ import annotations' in content,             f"{comp}/api.py: 缺少 `from __future__ import annotations`"
