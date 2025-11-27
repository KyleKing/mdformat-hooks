"""Integration tests for mdformat-mdsf using the pre-commit test file.

These tests verify idempotency - that formatting the same content twice
produces the same result, and that the pre-commit test file remains stable.
"""

from __future__ import annotations

from pathlib import Path

import mdformat


def test_mdformat_text_idempotency():
    """Verify that formatting is idempotent using pre-commit test file.

    This test reads the pre-commit test file, formats it, and verifies
    that the output matches the original (assuming the file is already formatted).
    """
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text()

    # Use codeformatters parameter for code formatter plugins
    result = mdformat.text(content, codeformatters={"python", "javascript", "json", "rust"})

    pth.write_text(result)  # Easier to debug with git
    assert result == content, "Differences found in format. Review in git."
