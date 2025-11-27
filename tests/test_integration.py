"""Integration tests for mdformat-mdsf (requires mdsf to be installed)."""

from __future__ import annotations

import shutil
from unittest.mock import Mock, patch

import mdformat
import pytest

from mdformat_mdsf._config import get_config
from mdformat_mdsf._formatter import _find_mdsf_bin, _format_code_with_mdsf

MDSF_AVAILABLE = shutil.which("mdsf") is not None


@pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
def test_python_formatting() -> None:
    """Test Python code formatting with mdsf."""
    unformatted = """```python
def hello(  ):
    x=1+2
    return x
```
"""
    result = mdformat.text(unformatted, codeformatters={"python"})
    # mdsf should format this (exact output depends on mdsf config)
    assert "```python" in result
    assert "def hello" in result


@pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
@pytest.mark.parametrize(
    ("languages", "expected_markers"),
    [
        (
            {"python", "javascript", "json"},
            ["```python", "```javascript", "```json"],
        ),
        (
            {"python", "javascript"},
            ["```python", "```javascript"],
        ),
        (
            {"python"},
            ["```python"],
        ),
    ],
    ids=["all_languages", "python_and_js", "python_only"],
)
def test_multiple_languages(languages: set[str], expected_markers: list[str]) -> None:
    """Test formatting multiple language blocks."""
    unformatted = """# Test

```python
def foo():pass
```

```javascript
function bar(){return 1;}
```

```json
{"name":"test","value":123}
```
"""
    result = mdformat.text(unformatted, codeformatters=languages)
    for marker in expected_markers:
        assert marker in result


@pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
def test_language_filter_configuration() -> None:
    """Test that language filtering works."""
    unformatted = """```python
def hello():pass
```

```javascript
function bar(){return 1;}
```
"""
    # Only format Python
    result = mdformat.text(
        unformatted,
        codeformatters={"python", "javascript"},
        options={"mdsf_languages": ["python"]},
    )
    assert "python" in result
    # JavaScript should be in result but might not be formatted


@pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
@pytest.mark.parametrize(
    "timeout",
    [5, 10, 30],
    ids=["5s", "10s", "30s"],
)
def test_timeout_configuration(timeout: int) -> None:
    """Test timeout configuration."""
    unformatted = """```python
def hello():
    return 42
```
"""
    result = mdformat.text(
        unformatted,
        codeformatters={"python"},
        options={"mdsf_timeout": timeout},
    )
    assert "```python" in result


@pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
@pytest.mark.parametrize(
    ("description", "code_content"),
    [
        ("empty_block", ""),
        ("whitespace_only", "   \n  "),
        ("single_line", "x = 1"),
        ("with_trailing_newline", "def hello():\n    pass\n\n"),
    ],
    ids=["empty_block", "whitespace_only", "single_line", "with_trailing_newline"],
)
def test_edge_cases(description: str, code_content: str) -> None:
    """Test handling of edge cases in code blocks."""
    unformatted = f"""```python
{code_content}```
"""
    result = mdformat.text(unformatted, codeformatters={"python"})
    assert "```python" in result


@pytest.mark.skipif(MDSF_AVAILABLE, reason="mdsf is installed, testing fallback")
def test_without_mdsf() -> None:
    """Test that plugin works gracefully without mdsf."""
    sample_python_code = """```python
def hello():
    return 42
```
"""
    # Should not raise an error, just return unformatted
    result = mdformat.text(sample_python_code, codeformatters={"python"})
    assert "```python" in result
    assert "def hello" in result


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_find_mdsf_bin_not_found(self) -> None:
        """Test that _find_mdsf_bin raises RuntimeError when mdsf not found."""
        with patch("shutil.which", return_value=None):
            with pytest.raises(RuntimeError, match="mdsf is not installed"):
                _find_mdsf_bin()

    def test_format_with_fail_on_error_no_binary(self) -> None:
        """Test that formatting fails when mdsf binary not found and fail_on_error=True."""
        config = get_config()
        original_fail = config.fail_on_error
        config._fail_on_error = True  # noqa: SLF001

        try:
            with patch("shutil.which", return_value=None):
                with pytest.raises(RuntimeError, match="mdsf is not installed"):
                    _format_code_with_mdsf("x = 1", "python")
        finally:
            config._fail_on_error = original_fail  # noqa: SLF001

    def test_format_without_binary_graceful_fallback(self) -> None:
        """Test that formatting returns unformatted code when mdsf not found and fail_on_error=False."""
        config = get_config()
        config._fail_on_error = False  # noqa: SLF001

        with patch("shutil.which", return_value=None):
            result = _format_code_with_mdsf("x = 1", "python")
            assert result == "x = 1"

    def test_format_empty_code(self) -> None:
        """Test formatting empty code block."""
        result = _format_code_with_mdsf("", "python")
        assert result == ""

    def test_format_with_language_filter(self) -> None:
        """Test that language filtering works correctly."""
        config = get_config()
        original_languages = config._languages.copy()  # noqa: SLF001
        config._languages = {"javascript"}  # noqa: SLF001

        try:
            # Python should not be formatted
            result = _format_code_with_mdsf("x = 1", "python")
            assert result == "x = 1"
        finally:
            config._languages = original_languages  # noqa: SLF001

    @pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
    def test_format_with_config_path(self, tmp_path) -> None:
        """Test formatting with custom config path."""
        config_file = tmp_path / "mdsf.json"
        config_file.write_text('{"formatters": {}}')

        config = get_config()
        original_config_path = config._config_path  # noqa: SLF001
        config._config_path = str(config_file)  # noqa: SLF001

        try:
            result = _format_code_with_mdsf("x=1", "python")
            # Should complete without error (config file is valid)
            assert isinstance(result, str)
        finally:
            config._config_path = original_config_path  # noqa: SLF001

    @pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
    def test_format_with_subprocess_error_fail_on_error(self) -> None:
        """Test that CalledProcessError is raised when fail_on_error=True."""
        config = get_config()
        original_fail = config.fail_on_error
        config._fail_on_error = True  # noqa: SLF001

        try:
            # Mock subprocess.run to raise CalledProcessError
            error = Mock()
            error.stderr = "mocked error"
            with patch(
                "subprocess.run",
                side_effect=__import__("subprocess").CalledProcessError(
                    1, "cmd", stderr="mocked error"
                ),
            ), pytest.raises(RuntimeError, match="mdsf failed for python"):
                _format_code_with_mdsf("x = 1", "python")
        finally:
            config._fail_on_error = original_fail  # noqa: SLF001

    @pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
    def test_format_with_timeout_error_fail_on_error(self) -> None:
        """Test that TimeoutExpired is raised when fail_on_error=True."""
        config = get_config()
        original_fail = config.fail_on_error
        original_timeout = config.timeout
        config._fail_on_error = True  # noqa: SLF001
        config._timeout = 1  # noqa: SLF001

        try:
            # Mock subprocess.run to raise TimeoutExpired
            with patch(
                "subprocess.run",
                side_effect=__import__("subprocess").TimeoutExpired("cmd", 1),
            ), pytest.raises(RuntimeError, match="mdsf timed out for python"):
                _format_code_with_mdsf("x = 1", "python")
        finally:
            config._fail_on_error = original_fail  # noqa: SLF001
            config._timeout = original_timeout  # noqa: SLF001

    @pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
    def test_format_with_subprocess_error_no_fail(self) -> None:
        """Test that errors are ignored when fail_on_error=False."""
        config = get_config()
        config._fail_on_error = False  # noqa: SLF001

        # Mock subprocess.run to raise CalledProcessError
        with patch(
            "subprocess.run",
            side_effect=__import__("subprocess").CalledProcessError(
                1, "cmd", stderr="error"
            ),
        ):
            result = _format_code_with_mdsf("x = 1", "python")
            # Should return unformatted code
            assert result == "x = 1"

    @pytest.mark.skipif(not MDSF_AVAILABLE, reason="mdsf not installed")
    def test_format_with_timeout_error_no_fail(self) -> None:
        """Test that timeout is ignored when fail_on_error=False."""
        config = get_config()
        config._fail_on_error = False  # noqa: SLF001

        # Mock subprocess.run to raise TimeoutExpired
        with patch(
            "subprocess.run",
            side_effect=__import__("subprocess").TimeoutExpired("cmd", 1),
        ):
            result = _format_code_with_mdsf("x = 1", "python")
            # Should return unformatted code
            assert result == "x = 1"
