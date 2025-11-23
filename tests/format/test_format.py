from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TypeVar

import mdformat
import pytest

from tests.helpers import print_text

T = TypeVar("T")


def flatten(nested_list: list[list[T]]) -> list[T]:
    return [*chain(*nested_list)]


def read_fixtures_with_options(filepath: Path) -> list[tuple[int, str, str, str, dict]]:
    """Read test fixtures and parse options from the file.

    Extended version of markdown_it.utils.read_fixture_file that also
    extracts options specified after the expected output.

    Fixture format:
        title
        .
        input text
        .
        expected output
        .
        --option (optional)
        --option (optional)

    Returns:
        List of (line_number, title, input_text, expected_output, options)

    """
    fixtures = []
    lines = filepath.read_text().splitlines()

    i = 0
    while i < len(lines):
        # Skip empty lines
        if not lines[i].strip():
            i += 1
            continue

        # Read title
        title = lines[i].strip()
        i += 1

        # Expect .
        if i >= len(lines) or lines[i] != ".":
            i += 1
            continue
        line_number = i + 1
        i += 1

        # Read input until .
        input_lines = []
        while i < len(lines) and lines[i] != ".":
            input_lines.append(lines[i])
            i += 1

        # Expect .
        if i >= len(lines):
            break
        i += 1

        # Read expected until .
        expected_lines = []
        while i < len(lines) and lines[i] != ".":
            expected_lines.append(lines[i])
            i += 1

        # Expect .
        if i >= len(lines):
            break
        i += 1

        # Read options until next title or empty line
        options = {}
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                break
            if line.startswith("--"):
                if line == "--wrap-sentences":
                    options["wrap_sentences"] = True
                i += 1
            else:
                # This is the next title, don't advance i
                break

        fixtures.append((
            line_number,
            title,
            "\n".join(input_lines) + "\n" if input_lines else "",
            "\n".join(expected_lines) + "\n" if expected_lines else "",
            options,
        ))

    return fixtures


fixtures = flatten(
    [
        read_fixtures_with_options(Path(__file__).parent / "fixtures" / fixture_path)
        for fixture_path in ("mdformat_mdsf.md",)
    ],
)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected", "options"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_format_fixtures(line, title, text, expected, options):
    output = mdformat.text(text, extensions={"mdslw"}, options=options)
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()
