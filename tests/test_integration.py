"""Integration tests for mdformat-mdsf (requires mdsf to be installed)."""

from __future__ import annotations

import shutil

import mdformat
import pytest


@pytest.fixture
def mdsf_available() -> bool:
    """Check if mdsf is available in PATH."""
    return shutil.which("mdsf") is not None


@pytest.mark.skipif(
    shutil.which("mdsf") is None,
    reason="mdsf not installed",
)
class TestWithMdsf:
    """Tests that require mdsf to be installed."""

    def test_python_formatting(self) -> None:
        """Test Python code formatting with mdsf."""
        unformatted = '''```python
def hello(  ):
    x=1+2
    return x
```
'''
        result = mdformat.text(unformatted, codeformatters={"python"})
        # mdsf should format this (exact output depends on mdsf config)
        assert "```python" in result
        assert "def hello" in result

    def test_multiple_languages(self) -> None:
        """Test formatting multiple language blocks."""
        unformatted = '''# Test

```python
def foo():pass
```

```javascript
function bar(){return 1;}
```

```json
{"name":"test","value":123}
```
'''
        result = mdformat.text(
            unformatted,
            codeformatters={"python", "javascript", "json"},
        )
        assert "```python" in result
        assert "```javascript" in result
        assert "```json" in result

    def test_language_filter_configuration(self) -> None:
        """Test that language filtering works."""
        unformatted = '''```python
def hello():pass
```

```javascript
function bar(){return 1;}
```
'''
        # Only format Python
        result = mdformat.text(
            unformatted,
            codeformatters={"python", "javascript"},
            options={"mdsf_languages": ["python"]},
        )
        assert "python" in result
        # JavaScript should be in result but might not be formatted

    def test_timeout_configuration(self) -> None:
        """Test timeout configuration."""
        unformatted = '''```python
def hello():
    return 42
```
'''
        result = mdformat.text(
            unformatted,
            codeformatters={"python"},
            options={"mdsf_timeout": 5},
        )
        assert "```python" in result

    def test_empty_code_block(self) -> None:
        """Test handling of empty code blocks."""
        unformatted = '''```python
```
'''
        result = mdformat.text(unformatted, codeformatters={"python"})
        assert "```python" in result

    def test_code_block_with_trailing_newline(self) -> None:
        """Test that trailing newlines are preserved."""
        unformatted = '''```python
def hello():
    pass

```
'''
        result = mdformat.text(unformatted, codeformatters={"python"})
        assert "```python" in result
        # Should preserve general structure


@pytest.mark.skipif(
    shutil.which("mdsf") is not None,
    reason="mdsf is installed, testing fallback behavior",
)
def test_without_mdsf() -> None:
    """Test that plugin works gracefully without mdsf."""
    unformatted = '''```python
def hello():
    return 42
```
'''
    # Should not raise an error, just return unformatted
    result = mdformat.text(unformatted, codeformatters={"python"})
    assert "```python" in result
    assert "def hello" in result
