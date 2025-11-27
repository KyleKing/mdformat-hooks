"""Shared test fixtures and configuration.

This module provides common fixtures used across the test suite,
particularly for managing global configuration state between tests.
"""

from __future__ import annotations

import pytest

from mdformat_mdformat_mdsf._config import get_config


@pytest.fixture(autouse=True)
def _reset_global_config():
    """Reset global config to defaults after each test.

    This auto-use fixture ensures that config changes in one test
    don't affect other tests, maintaining test isolation.
    """
    yield
    config = get_config()
    config._config_path = None  # noqa: SLF001
    config._timeout = 30  # noqa: SLF001
    config._languages = set()  # noqa: SLF001
    config._fail_on_error = False  # noqa: SLF001
