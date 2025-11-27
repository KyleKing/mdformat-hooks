"""Test formatting using fixture files.

These tests verify that the mdformat-mdsf plugin correctly formats
markdown documents with code blocks. Since this is a code formatter plugin,
we use the codeformatters parameter rather than extensions.
"""

from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TypeVar

import mdformat
import pytest
from markdown_it.utils import read_fixture_file

from tests.helpers import print_text

T = TypeVar("T")


def flatten(nested_list: list[list[T]]) -> list[T]:
    """Flatten a nested list into a single list."""
    return [*chain(*nested_list)]


# Load all test fixtures from the fixtures directory
fixtures = flatten(
    [
        read_fixture_file(Path(__file__).parent / "fixtures" / fixture_path)
        for fixture_path in ("mdformat_mdsf.md",)
    ],
)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_format_fixtures(line, title, text, expected):
    """Test formatting with fixture files.

    Note: This plugin is a code formatter, so we format without mdsf integration.
    The actual code formatting happens when mdsf is installed and configured.
    These tests verify that the markdown structure is preserved.
    """
    # Format with python codeformatter enabled
    # Note: If mdsf is not installed, code will remain unchanged
    output = mdformat.text(text, codeformatters={"python", "javascript"})
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()
