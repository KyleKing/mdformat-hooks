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
    group.add_argument(
        "--strict-hooks",
        action="store_true",
        help="Fail formatting if shell command returns non-zero exit code",
    )


def _run_shell_command(
    text: str, command: str | None, timeout: int, *, strict: bool = False
) -> str:
    """Run a shell command with the text as stdin.

    Args:
        text: Input text to pass to the command via stdin
        command: Shell command to execute
        timeout: Command timeout in seconds
        strict: If True, raise exception on non-zero exit codes

    Returns:
        Command stdout on success, or original text on failure (non-strict mode)

    Raises:
        RuntimeError: If strict=True and command fails, times out, or errors

    """
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
        # On error, log and either raise (strict mode) or return original text
        error_msg = (
            f"mdformat-hooks: Command failed with code {result.returncode}: {command}"
        )
        print(error_msg, file=sys.stderr)  # noqa: T201
        if result.stderr:
            print(f"Error output: {result.stderr}", file=sys.stderr)  # noqa: T201
        if strict:
            stderr_info = f"stderr: {result.stderr}"
            full_error = (
                f"Command failed with exit code {result.returncode}: {command}\n"
                f"{stderr_info}"
            )
            raise RuntimeError(full_error)  # noqa: TRY301
    except subprocess.TimeoutExpired as e:
        timeout_msg = (
            f"mdformat-hooks: Command timed out after {timeout} seconds: {command}"
        )
        print(timeout_msg, file=sys.stderr)  # noqa: T201
        if strict:
            raise RuntimeError(timeout_msg) from e
    except Exception as e:
        error_msg = f"mdformat-hooks: Error running command: {e}"
        print(error_msg, file=sys.stderr)  # noqa: T201
        if strict:
            raise
    return text


def _create_post_processor(options: Mapping[str, Any]) -> Postprocess | None:
    """Create a post processor for post commands."""
    # Check if mdformat key exists in options
    if "mdformat" not in options:
        return None

    post_command = get_conf(options, "post_command")
    timeout = get_conf(options, "timeout") or 30
    strict = get_conf(options, "strict_hooks") or False

    if post_command:

        def processor(text: str, _node: RenderTreeNode, _context: RenderContext) -> str:
            return _run_shell_command(
                text, str(post_command), int(timeout), strict=bool(strict)
            )

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
    processor = _create_post_processor(options)
    if processor:
        return processor(text, node, context)
    return text


# Static postprocessor mapping expected by mdformat
POSTPROCESSORS: Mapping[str, Postprocess] = {"document": _dynamic_postprocessor}
