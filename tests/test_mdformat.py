"""Tests for mdformat-mdsf plugin."""

from __future__ import annotations

from pathlib import Path

import mdformat
import pytest


def test_mdformat_text() -> None:
    """Verify that using mdformat works as expected (idempotency test)."""
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text()

    # For code formatter plugins, we use codeformatters parameter
    result = mdformat.text(content, codeformatters={"python"})

    pth.write_text(result)  # Easier to debug with git
    assert result == content, "Differences found in format. Review in git."


def test_python_formatter(sample_python_code: str) -> None:
    """Test Python code formatting gracefully handles missing mdsf binary."""
    # If mdsf is not installed, it should return the original
    # If mdsf is installed, it might format it
    result = mdformat.text(sample_python_code, codeformatters={"python"})
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
    ids=["python", "javascript", "typescript", "rust", "go", "json"],
)
def test_multiple_languages(language: str) -> None:
    """Test that multiple languages can be processed."""
    unformatted = f"""```{language}
code here
```
"""
    result = mdformat.text(unformatted, codeformatters={language})
    assert f"```{language}" in result
    assert "code here" in result


@pytest.mark.parametrize(
    ("text", "codeformatters", "expected_content"),
    [
        # Test basic code block preservation
        (
            "```python\nx = 1\n```\n",
            {"python"},
            ["```python", "x = 1", "```"],
        ),
        # Test multiple code blocks
        (
            "```python\nx = 1\n```\n\n```python\ny = 2\n```\n",
            {"python"},
            ["```python", "x = 1", "y = 2"],
        ),
        # Test non-code content preservation
        (
            "# Title\n\n```python\nx = 1\n```\n\nParagraph\n",
            {"python"},
            ["# Title", "```python", "Paragraph"],
        ),
    ],
    ids=["single_block", "multiple_blocks", "mixed_content"],
)
def test_code_block_preservation(
    text: str,
    codeformatters: set[str],
    expected_content: list[str],
) -> None:
    """Test that code blocks and surrounding content are preserved."""
    result = mdformat.text(text, codeformatters=codeformatters)
    for expected in expected_content:
        assert expected in result


@pytest.mark.parametrize(
    ("options", "expected_in_result"),
    [
        # Test with custom language filter
        ({"mdsf_languages": ["python"]}, "```python"),
        # Test with timeout setting
        ({"mdsf_timeout": 10}, "```python"),
        # Test with multiple options
        ({"mdsf_languages": ["python"], "mdsf_timeout": 5}, "```python"),
    ],
    ids=["language_filter", "timeout", "multiple_options"],
)
def test_configuration_options(
    options: dict[str, object], expected_in_result: str
) -> None:
    """Test that configuration options are handled correctly."""
    unformatted = """```python
def test():
    pass
```
"""
    result = mdformat.text(
        unformatted,
        codeformatters={"python"},
        options=options,
    )
    assert expected_in_result in result


def test_idempotency(sample_mixed_content: str) -> None:
    """Test that formatting is idempotent (formatting twice gives same result)."""
    result1 = mdformat.text(sample_mixed_content, codeformatters={"python", "javascript"})
    result2 = mdformat.text(result1, codeformatters={"python", "javascript"})

    assert result1 == result2, "Formatting should be idempotent"
