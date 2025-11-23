from pathlib import Path

import pytest
from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file

from tests.helpers import print_text

FIXTURE_PATH = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    read_fixture_file(FIXTURE_PATH / "mdformat_mdsf.md"),
    ids=[f[1] for f in read_fixture_file(FIXTURE_PATH / "mdformat_mdsf.md")],
)
def test_render(line, title, text, expected):
    """Test HTML rendering.

    mdslw doesn't add markdown-it plugins (it only does postprocessing),
    so we just test basic CommonMark rendering.

    """
    md = MarkdownIt("commonmark")
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    output = md.render(text)
    print_text(output, expected, show_whitespace=False)
    assert output.rstrip() == expected.rstrip()
