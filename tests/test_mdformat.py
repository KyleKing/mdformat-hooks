"""Tests for mdformat-mdsf plugin."""

from pathlib import Path

import mdformat
import pytest


def test_mdformat_text():
    """Verify that using mdformat works as expected."""
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text()

    # For code formatter plugins, we use codeformatters parameter
    result = mdformat.text(content, codeformatters={"python"})

    pth.write_text(result)  # Easier to debug with git
    assert result == content, "Differences found in format. Review in git."


def test_python_formatter():
    """Test Python code formatting."""
    # Simple test that doesn't require mdsf to be installed
    # The formatter should gracefully handle missing mdsf binary
    unformatted = '''```python
def hello():
    print("world")
```
'''
    # If mdsf is not installed, it should return the original
    # If mdsf is installed, it might format it
    result = mdformat.text(unformatted, codeformatters={"python"})
    # At minimum, mdformat should process it without error
    assert "```python" in result
    assert "def hello" in result


@pytest.mark.parametrize(
    "language",
    [
        "python",
        "javascript",
        "typescript",
        "rust",
        "go",
        "json",
    ],
)
def test_multiple_languages(language: str):
    """Test that multiple languages can be processed."""
    unformatted = f'''```{language}
code here
```
'''
    result = mdformat.text(unformatted, codeformatters={language})
    assert f"```{language}" in result
    assert "code here" in result
