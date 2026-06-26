"""Common test fixtures"""
from __future__ import annotations
from typing import Any
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: Unit tests for individual api.py")
    config.addinivalue_line("markers", "integration: Cross-component integration tests")
    config.addinivalue_line("markers", "lint: Static analysis and import isolation checks")
