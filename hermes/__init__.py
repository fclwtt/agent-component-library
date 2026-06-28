"""Agent Component Library — Component Package Root"""
from __future__ import annotations
import os, sys, types

_COMPONENT_MAP: dict = {
    "acp_adapter": "acp-adapter", "agent_engine": "agent-engine",
    "cli": "cli", "cron": "cron",
    "entry_points": "entry-points", "gateway": "gateway",
    "infrastructure": "infrastructure", "llm_client": "llm-client",
    "memory_system": "memory-system", "plugin_system": "plugin-system",
    "security": "security", "skill_system": "skill-system",
    "state_management": "state-management", "tool_system": "tool-system",
    "tui": "tui",
}
_DIR = os.path.dirname(__file__)

def _load_api(dir_name: str):
    mod_name = f"hermes_component.{dir_name}"
    if mod_name in sys.modules:
        return sys.modules[mod_name]

    api_path = os.path.join(_DIR, dir_name, "api.py")
    if not os.path.exists(api_path):
        return None

    hmp = os.path.join(_DIR, dir_name, "modules")
    if hmp not in sys.path:
        sys.path.insert(0, hmp)

    mod = types.ModuleType(mod_name)
    mod.__file__ = api_path
    mod.__package__ = mod_name
    mod.__path__ = [api_path.replace('/api.py', '')]  # Mark as package for relative imports
    sys.modules[mod_name] = mod  # <-- register BEFORE exec

    with open(api_path) as f:
        exec(compile(f.read(), api_path, "exec"), mod.__dict__)

    # Register all aliases
    py_name = dir_name.replace("-", "_")
    for alias in [f"{mod_name}.api", f"hermes_component.{py_name}", f"hermes_component.{py_name}.api"]:
        sys.modules[alias] = mod
    return mod

def __getattr__(name: str):
    if name not in _COMPONENT_MAP:
        raise AttributeError(f"No component: {name}")
    return _load_api(_COMPONENT_MAP[name])

def __dir__():
    return list(_COMPONENT_MAP.keys())

