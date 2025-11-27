"""Shell command hooks for mdformat."""

from __future__ import annotations

import argparse
import subprocess  # noqa: S404
import sys
from collections.abc import Mapping
from typing import Any

from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess

from ._helpers import get_conf


def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
    """Add CLI options for shell hooks.

    Options are stored in `mdit.options["mdformat"]["plugin"]["hooks"]`

    """
    group.add_argument(
        "--pre-command",
        type=str,
        help="Shell command to run before formatting (receives text via stdin)",
    )
    group.add_argument(
        "--post-command",
        type=str,
        help="Shell command to run after formatting (receives text via stdin)",
    )
    group.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds for shell commands (default: 30)",
    )


def _run_shell_command(text: str, command: str | None, timeout: int) -> str:
    """Run a shell command with the text as stdin."""
    if not command:
        return text

    try:
        result = subprocess.run(  # noqa: S602
            command,
            input=text,
            capture_output=True,
            text=True,
            shell=True,
            timeout=timeout,
            check=False,
        )

        if result.returncode == 0:
            return result.stdout
        # On error, return original text and optionally log
        print(  # noqa: T201
            f"mdformat-hooks: Command failed with code {result.returncode}: {command}",
            file=sys.stderr,
        )
        if result.stderr:
            print(f"Error output: {result.stderr}", file=sys.stderr)  # noqa: T201
    except subprocess.TimeoutExpired:
        print(  # noqa: T201
            f"mdformat-hooks: Command timed out after {timeout} seconds: {command}",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"mdformat-hooks: Error running command: {e}", file=sys.stderr)  # noqa: T201
    return text


# mdformat doesn't have a preprocessor interface yet, so we'll use the
# postprocessor for both pre and post commands, running them in sequence
def _create_combined_processor(options: Mapping[str, Any]) -> Postprocess | None:
    """Create a combined processor for pre and post commands."""
    # Check if mdformat key exists in options
    if "mdformat" not in options:
        return None

    pre_command = get_conf(options, "pre_command")
    post_command = get_conf(options, "post_command")
    timeout = get_conf(options, "timeout") or 30

    if pre_command or post_command:

        def processor(text: str, _node: RenderTreeNode, _context: RenderContext) -> str:
            if pre_command:
                text = _run_shell_command(text, str(pre_command), int(timeout))
            if post_command:
                text = _run_shell_command(text, str(post_command), int(timeout))
            return text

        return processor

    return None


# For now, we don't need to modify the parser
def update_mdit(mdit: Any) -> None:  # noqa: ANN401
    """No parser modifications needed for hooks."""


# No custom renderers needed for shell hooks
RENDERERS: Mapping[str, Any] = {}


# Postprocessor needs to be dynamically created based on configuration
# but mdformat expects a static dict. We'll create a wrapper that checks
# options at runtime
def _dynamic_postprocessor(
    text: str, node: RenderTreeNode, context: RenderContext
) -> str:
    """Dynamic postprocessor that checks for commands at runtime."""
    # Only process the document root node
    if node.type != "document":
        return text

    options = context.options

    # The options might be under different keys depending on how mdformat is called
    # Check for configuration in the expected location
    processor = _create_combined_processor(options)
    if processor:
        return processor(text, node, context)
    return text


# Static postprocessor mapping expected by mdformat
POSTPROCESSORS: Mapping[str, Postprocess] = {"document": _dynamic_postprocessor}
