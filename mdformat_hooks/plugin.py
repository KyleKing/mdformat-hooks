"""Shell command hooks for mdformat."""

from __future__ import annotations

import argparse
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import sys
from collections.abc import Mapping
from typing import Any

from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess

from ._helpers import get_conf


def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
    """Add CLI options for shell hooks.

    Options are stored in `mdit.options["mdformat"]["plugin"]["hooks"]`

    Every argument must keep a `None` default so that an absent flag falls
    through to the `.mdformat.toml` value; any other default overrides TOML.

    """
    group.add_argument(
        "--post-command",
        type=str,
        help="Shell command to run after formatting (receives text via stdin)",
    )
    group.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds for shell commands (default: 30)",
    )
    group.add_argument(
        "--strict-hooks",
        action="store_const",
        const=True,
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
        result = subprocess.run(  # ruff: ignore[subprocess-popen-with-shell-equals-true]
            command,
            input=text,
            capture_output=True,
            text=True,
            shell=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as err:
        timeout_msg = (
            f"mdformat-hooks: Command timed out after {timeout} seconds: {command}"
        )
        print(timeout_msg, file=sys.stderr)  # ruff: ignore[print]
        if strict:
            raise RuntimeError(timeout_msg) from err
        return text
    except Exception as err:
        error_msg = f"mdformat-hooks: Error running command: {err}"
        print(error_msg, file=sys.stderr)  # ruff: ignore[print]
        if strict:
            raise
        return text

    if result.returncode == 0:
        return result.stdout

    error_msg = (
        f"mdformat-hooks: Command failed with code {result.returncode}: {command}"
    )
    print(error_msg, file=sys.stderr)  # ruff: ignore[print]
    if result.stderr:
        print(f"Error output: {result.stderr}", file=sys.stderr)  # ruff: ignore[print]
    if strict:
        stderr_info = f"stderr: {result.stderr}"
        full_error = (
            f"Command failed with exit code {result.returncode}: {command}\n"
            f"{stderr_info}"
        )
        raise RuntimeError(full_error)
    return text


def _create_post_processor(options: Mapping[str, Any]) -> Postprocess | None:
    """Create a post processor for post commands."""
    if "mdformat" not in options:
        return None

    post_command = get_conf(options, "post_command")
    if not post_command:
        return None

    timeout = get_conf(options, "timeout") or 30
    strict = get_conf(options, "strict_hooks") or False

    def processor(text: str, _node: RenderTreeNode, _context: RenderContext) -> str:
        return _run_shell_command(
            text, str(post_command), int(timeout), strict=bool(strict)
        )

    return processor


# For now, we don't need to modify the parser
def update_mdit(mdit: Any) -> None:  # ruff: ignore[any-type]
    """No parser modifications needed for hooks."""


# No custom renderers needed for shell hooks
RENDERERS: Mapping[str, Any] = {}


ROOT_NODE_TYPE = "root"


def _dynamic_postprocessor(
    text: str, node: RenderTreeNode, context: RenderContext
) -> str:
    """Run the configured post command over the whole rendered document.

    Registered only for the root node so the command sees the document once.
    The command receives a trailing newline on stdin and its output is
    stripped of trailing newlines, because mdformat appends its own.
    """
    if node.type != ROOT_NODE_TYPE:
        return text

    processor = _create_post_processor(context.options)
    if not processor:
        return text

    stdin = text if text.endswith("\n") else text + "\n"
    return processor(stdin, node, context).rstrip("\n")


# Static postprocessor mapping expected by mdformat
POSTPROCESSORS: Mapping[str, Postprocess] = {ROOT_NODE_TYPE: _dynamic_postprocessor}
