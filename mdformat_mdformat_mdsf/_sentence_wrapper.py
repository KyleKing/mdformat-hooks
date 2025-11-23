"""Sentence wrapping logic inspired by mdslw."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ._helpers import get_conf

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

    from mdformat.renderer import RenderContext, RenderTreeNode

    ContextOptions = Mapping[str, Any]


def should_wrap_sentences(options: ContextOptions) -> bool:
    """Check if sentence wrapping is enabled via CLI or config."""
    return bool(get_conf(options, "wrap_sentences"))


def get_sentence_markers(options: ContextOptions) -> str:
    """Get sentence ending markers from config (default: .!?:)."""
    markers = get_conf(options, "sentence_markers")
    return str(markers) if markers else ".!?:"


def get_max_line_width(options: ContextOptions) -> int:
    """Get maximum line width from config (default: 80)."""
    width = get_conf(options, "max_line_width")
    return int(width) if width else 80


def wrap_sentences(
    text: str,
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Wrap text by inserting line breaks after sentences.

    This is inspired by mdslw's sentence-wrapping behavior:
    - Insert line breaks after sentence-ending punctuation
    - Preserve existing formatting for code blocks and special syntax
    - Handle common abbreviations and edge cases

    Args:
        text: The rendered text to process
        node: The syntax tree node being rendered
        context: The rendering context

    Returns:
        The text with sentence breaks applied

    """
    if not should_wrap_sentences(context.options):
        return text

    # Don't wrap if text is empty or just whitespace
    if not text or not text.strip():
        return text

    sentence_markers = get_sentence_markers(context.options)
    max_width = get_max_line_width(context.options)

    # Build regex pattern for sentence endings
    # Match: sentence marker + optional closing punctuation + space
    marker_class = re.escape(sentence_markers)
    # Pattern: (marker)(optional closing chars)(whitespace)
    pattern = r"([" + marker_class + r"])(\s*[\"'\)\]\}]*)\s+"

    def replace_with_newline(match: re.Match) -> str:
        """Replace sentence ending with newline."""
        marker = match.group(1)
        closing = match.group(2)
        return f"{marker}{closing}\n"

    # Apply sentence breaks
    wrapped = re.sub(pattern, replace_with_newline, text)

    # Optional: wrap long lines that exceed max_width
    if max_width > 0:
        lines = wrapped.split("\n")
        wrapped_lines = []
        for line in lines:
            if len(line) <= max_width:
                wrapped_lines.append(line)
            else:
                # Simple word-wrap for long lines
                words = line.split()
                current_line = []
                current_length = 0

                for word in words:
                    word_len = len(word)
                    if current_length + word_len + 1 > max_width and current_line:
                        wrapped_lines.append(" ".join(current_line))
                        current_line = [word]
                        current_length = word_len
                    else:
                        current_line.append(word)
                        current_length += word_len + (1 if current_line else 0)

                if current_line:
                    wrapped_lines.append(" ".join(current_line))

        wrapped = "\n".join(wrapped_lines)

    return wrapped
