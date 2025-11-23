"""Public Extension for mdslw-style sentence wrapping."""

from __future__ import annotations

import argparse
from collections.abc import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer.typing import Postprocess, Render

from ._helpers import get_conf
from ._sentence_wrapper import wrap_sentences


def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
    """Add options to the mdformat CLI.

    Stored in `mdit.options["mdformat"]["plugin"]["mdslw"]`

    """
    group.add_argument(
        "--wrap-sentences",
        action="store_const",
        const=True,
        help="If specified, wrap text by inserting line breaks after sentences (mdslw-style)",
    )
    group.add_argument(
        "--sentence-markers",
        type=str,
        default=".!?:",
        help="Characters that mark sentence endings (default: .!?:)",
    )
    group.add_argument(
        "--max-line-width",
        type=int,
        default=80,
        help="Maximum line width for wrapping (default: 80, 0 to disable)",
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser.

    mdslw doesn't add new syntax, so no parser modifications needed.
    All functionality is implemented via postprocessors.

    """
    # No markdown-it plugins needed for sentence wrapping


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
# mdslw doesn't need custom renderers, only postprocessors.
RENDERERS: Mapping[str, Render] = {}

# A mapping from `RenderTreeNode.type` to a `Postprocess` that does
# postprocessing for the output of the `Render` function. Unlike
# `Render` funcs, `Postprocess` funcs are collaborative: any number of
# plugins can define a postprocessor for a syntax type and all of them
# will run in series.
#
# Apply sentence wrapping to paragraphs and other text-containing nodes
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "paragraph": wrap_sentences,
}
