# Common Testing Patterns Reference

Quick reference for pytest patterns commonly used in mdformat plugin testing.

## Pattern: Skipif for External Dependencies

Use when tests require external tools or binaries that may not be installed:

```python
import shutil
import pytest

BINARY_AVAILABLE = shutil.which("binary_name") is not None


@pytest.mark.skipif(not BINARY_AVAILABLE, reason="binary not installed")
def test_with_binary() -> None:
    """Test behavior when binary is available."""
    pass


@pytest.mark.skipif(BINARY_AVAILABLE, reason="testing fallback behavior")
def test_without_binary() -> None:
    """Test fallback behavior when binary is not available."""
    pass
```

## Pattern: Multiple Skip Conditions

Combine multiple conditions for more complex skip logic:

```python
import sys
import pytest

@pytest.mark.skipif(
    not BINARY_AVAILABLE or sys.platform == "win32",
    reason="binary not installed or on Windows",
)
def test_unix_with_binary() -> None:
    """Test that only runs on Unix systems with binary installed."""
    pass
```

## Pattern: Simple Parametrization

Use for tests with same logic but different single inputs:

```python
import pytest
import mdformat

@pytest.mark.parametrize(
    "language",
    ["python", "javascript", "typescript", "rust"],
    ids=["python", "javascript", "typescript", "rust"],
)
def test_multiple_languages(language: str) -> None:
    """Test formatting for multiple programming languages."""
    unformatted = f"```{language}\ncode\n```"
    result = mdformat.text(unformatted, codeformatters={language})
    assert f"```{language}" in result
```

## Pattern: Multiple Parameters

Use when tests need multiple inputs that vary together:

```python
import pytest
import mdformat

@pytest.mark.parametrize(
    ("text", "options", "expected"),
    [
        ("input1", {"opt": True}, "output1"),
        ("input2", {"opt": False}, "output2"),
        ("input3", {"opt": True, "other": 5}, "output3"),
    ],
    ids=["with_opt", "without_opt", "multiple_opts"],
)
def test_configurations(text: str, options: dict, expected: str) -> None:
    """Test different configuration combinations."""
    result = mdformat.text(text, options=options)
    assert expected in result
```

## Pattern: Complex Parametrization with Sets/Lists

Use when parameters are collections or need complex types:

```python
import pytest

@pytest.mark.parametrize(
    ("languages", "expected_markers"),
    [
        ({"python", "rust"}, ["```python", "```rust"]),
        ({"python"}, ["```python"]),
        (set(), []),
    ],
    ids=["multiple_languages", "single_language", "no_languages"],
)
def test_language_detection(
    languages: set[str],
    expected_markers: list[str],
) -> None:
    """Test language detection with various language sets."""
    result = format_text(SAMPLE_TEXT, languages=languages)
    for marker in expected_markers:
        assert marker in result
```

## Pattern: Edge Case Consolidation

Consolidate multiple edge case tests into one parametrized test:

```python
import pytest

@pytest.mark.parametrize(
    ("description", "code_content"),
    [
        ("empty_block", ""),
        ("whitespace_only", "   \n  "),
        ("single_line", "x = 1"),
        ("with_trailing_newline", "def hello():\n    pass\n\n"),
        ("multiple_blank_lines", "\n\n\n"),
        ("tabs_and_spaces", "\t  mixed  \t"),
    ],
    ids=["empty_block", "whitespace_only", "single_line", "with_trailing_newline", "multiple_blank_lines", "tabs_and_spaces"],
)
def test_edge_cases(description: str, code_content: str) -> None:
    """Test various edge cases in code formatting."""
    unformatted = f"```python\n{code_content}```"
    result = format_code(unformatted)
    assert "```python" in result
```

## Pattern: Fixture Files with markdown-it-py

Load test cases from fixture files (markdown-it-py style):

```python
from pathlib import Path
import pytest
from markdown_it.utils import read_fixture_file
import mdformat

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "test_cases.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_fixtures(line: int, title: str, text: str, expected: str) -> None:
    """Test cases loaded from fixture file."""
    output = mdformat.text(text, extensions={"your_plugin"})
    assert output.rstrip() == expected.rstrip()
```

**Fixture file format** (test_cases.md):

```markdown
test case title
.
input markdown
.
expected output
.

another test case
.
input
.
output
.
```

## Pattern: Idempotency Test

Essential test to ensure formatting is stable:

```python
import mdformat

def test_idempotency() -> None:
    """Test that formatting is idempotent (formatting twice gives same result)."""
    text = """# Example

```python
def hello():
    pass
```
"""
    result1 = mdformat.text(text, codeformatters={"python"})
    result2 = mdformat.text(result1, codeformatters={"python"})
    assert result1 == result2, "Formatting should be idempotent"
```

## Pattern: Smoke Test

Verify plugin loads and works with real content:

```python
from pathlib import Path
import mdformat

def test_plugin_loads() -> None:
    """Verify that the plugin loads without errors."""
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text()
    result = mdformat.text(content, extensions={"your_plugin"})
    pth.write_text(result)  # Easier to debug with git
    assert result == content, "Differences found. Review in git."
```

## Pattern: Test Helpers Module

Create `tests/helpers.py` for shared utilities:

```python
"""Test helper utilities."""

from __future__ import annotations

import os
import mdformat

_SHOW_TEXT = os.environ.get("SHOW_TEST_TEXT", "false").lower() == "true"


def print_text(output: str, expected: str, show_whitespace: bool = False) -> None:
    """Print text for debugging when SHOW_TEST_TEXT=true.

    Usage: SHOW_TEST_TEXT=true pytest tests/test_file.py
    """
    if _SHOW_TEXT:
        print("--  Output  --")
        print(repr(output) if show_whitespace else output)
        print("-- Expected --")
        print(repr(expected) if show_whitespace else expected)
        print("--  <End>   --")


def format_with_plugin(
    text: str,
    *,
    extensions: set[str] | None = None,
    codeformatters: set[str] | None = None,
    options: dict[str, object] | None = None,
) -> str:
    """Format text with the plugin using consistent defaults."""
    return mdformat.text(
        text,
        extensions=extensions or set(),
        codeformatters=codeformatters or set(),
        options=options or {},
    )
```

## Pattern: Testing Plugin Options

Test CLI options and configuration:

```python
import pytest
import mdformat

@pytest.mark.parametrize(
    ("option_value", "expected_behavior"),
    [
        (True, "formatted_with_option"),
        (False, "formatted_without_option"),
    ],
    ids=["option_enabled", "option_disabled"],
)
def test_plugin_option(option_value: bool, expected_behavior: str) -> None:
    """Test plugin behavior with different option values."""
    text = "# Test"
    result = mdformat.text(
        text,
        extensions={"your_plugin"},
        options={"your_option": option_value},
    )
    assert expected_behavior in result
```

## Pattern: Testing with Specific Extensions

Test interaction with other mdformat extensions:

```python
import pytest
import mdformat

@pytest.mark.parametrize(
    ("extensions", "expected"),
    [
        ({"your_plugin"}, "basic_output"),
        ({"your_plugin", "gfm"}, "output_with_gfm"),
        ({"your_plugin", "tables"}, "output_with_tables"),
    ],
    ids=["standalone", "with_gfm", "with_tables"],
)
def test_with_extensions(extensions: set[str], expected: str) -> None:
    """Test plugin interaction with other extensions."""
    text = "# Test"
    result = mdformat.text(text, extensions=extensions)
    assert expected in result
```

## Pattern: Before/After Comparison

Show clear transformation expectations:

```python
import pytest
import mdformat

@pytest.mark.parametrize(
    ("input_text", "expected_output"),
    [
        # Consistent spacing
        ("```python\ncode```", "```python\ncode\n```\n"),
        # Indentation normalization
        ("  ```python\n  code\n  ```", "```python\ncode\n```\n"),
        # Language tag normalization
        ("```PYTHON\ncode\n```", "```python\ncode\n```\n"),
    ],
    ids=["add_trailing_newline", "remove_indentation", "lowercase_language"],
)
def test_formatting_transformations(input_text: str, expected_output: str) -> None:
    """Test specific formatting transformations."""
    result = mdformat.text(input_text, extensions={"your_plugin"})
    assert result == expected_output
```

## Best Practices Summary

1. **Always provide IDs**: Makes test output readable and debugging easier
2. **Keep parameter names descriptive**: Use `input_text`/`expected_output` not `a`/`b`
3. **Use type hints**: Required for modern Python and helps catch errors
4. **Document with docstrings**: Brief explanation of what the test verifies
5. **Group related tests**: Use meaningful test file organization
6. **Test edge cases**: Empty strings, whitespace, special characters
7. **Verify idempotency**: Essential for formatters
8. **Add smoke tests**: Catch basic integration issues
9. **Use helpers for repetition**: Create `tests/helpers.py` for shared code
10. **Make tests independent**: Each test should be runnable in isolation

## Quick Command Reference

```bash
# Run all tests
tox

# Run specific parametrized test case
tox -e test -- tests/test_file.py::test_name[test_id]

# Show all test IDs
pytest --collect-only tests/

# Run with debugging output
SHOW_TEST_TEXT=true tox -e test -- -vv

# Run tests matching pattern
tox -e test -- -k "test_edge"

# Run last failed tests first
tox -e test -- --failed-first

# Update snapshots if using pytest-snapshot
tox -e test -- --snapshot-update
```
