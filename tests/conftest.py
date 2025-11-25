"""Shared test fixtures and configuration."""

from __future__ import annotations

import pytest

from mdformat_mdformat_mdsf._config import get_config


@pytest.fixture(autouse=True)
def _reset_global_config():
    """Reset global config to defaults after each test."""
    yield
    config = get_config()
    config._config_path = None  # noqa: SLF001
    config._timeout = 30  # noqa: SLF001
    config._languages = set()  # noqa: SLF001
    config._fail_on_error = False  # noqa: SLF001


@pytest.fixture
def sample_python_code() -> str:
    """Sample Python code for testing."""
    return """```python
def hello():
    print("world")
```
"""


@pytest.fixture
def sample_javascript_code() -> str:
    """Sample JavaScript code for testing."""
    return """```javascript
function greet() {
    return "hello";
}
```
"""


@pytest.fixture
def sample_mixed_content() -> str:
    """Sample markdown with mixed content."""
    return """# Example

```python
def hello():
    return "world"
```

Some text here.

```javascript
function greet() {
    return "hello";
}
```
"""
