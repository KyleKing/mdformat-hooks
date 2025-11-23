"""Code formatter using mdsf."""

from __future__ import annotations

import shutil
import subprocess  # noqa: S404
from typing import TYPE_CHECKING

from ._config import get_config

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


def _find_mdsf_bin() -> str:
    """Find the mdsf binary path.

    Raises:
        RuntimeError: If mdsf binary is not found in PATH
    """
    mdsf_bin = shutil.which("mdsf")
    if mdsf_bin is None:
        msg = "mdsf is not installed. Install it from https://github.com/hougesen/mdsf"
        raise RuntimeError(msg)
    return mdsf_bin


def _format_code_with_mdsf(unformatted: str, language: str) -> str:  # noqa: C901, PLR0912
    """Format code using mdsf.

    Args:
        unformatted: The unformatted code block content
        language: The language identifier (info string)

    Returns:
        The formatted code as a string

    Raises:
        RuntimeError: If mdsf fails and fail_on_error is True
    """
    if not unformatted:
        return unformatted

    # Get configuration
    config = get_config()

    # Check if language is enabled
    if not config.is_language_enabled(language):
        return unformatted

    # Create a markdown code block
    markdown_input = f"```{language}\n{unformatted}\n```\n"

    # Find mdsf binary
    try:
        mdsf_bin = _find_mdsf_bin()
    except RuntimeError:
        if config.fail_on_error:
            raise
        return unformatted

    # Build command
    cmd: list[str] = [mdsf_bin, "format", "--stdin"]
    if config.config_path:
        cmd.extend(["--config", config.config_path])

    # Call mdsf with stdin
    try:
        result = subprocess.run(  # noqa: S603
            cmd,
            input=markdown_input,
            capture_output=True,
            text=True,
            check=True,
            timeout=config.timeout,
        )
    except subprocess.CalledProcessError as e:
        # If mdsf fails, either raise or return unformatted code
        if config.fail_on_error:
            msg = f"mdsf failed for {language}: {e.stderr}"
            raise RuntimeError(msg) from e
        return unformatted
    except subprocess.TimeoutExpired as e:
        # If mdsf times out, either raise or return unformatted code
        if config.fail_on_error:
            msg = f"mdsf timed out for {language} after {config.timeout}s"
            raise RuntimeError(msg) from e
        return unformatted
    else:
        formatted_output = result.stdout

        # Extract the code from the formatted markdown
        # Remove the opening fence
        lines = formatted_output.strip().split("\n")
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        # Remove the closing fence
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        formatted_code = "\n".join(lines)

        # Ensure trailing newline if original had one
        if unformatted.endswith("\n") and not formatted_code.endswith("\n"):
            formatted_code += "\n"

        return formatted_code


# Common languages - users can enable/disable via configuration
SUPPORTED_LANGUAGES: Sequence[str] = (
    "python",
    "javascript",
    "typescript",
    "rust",
    "go",
    "java",
    "c",
    "cpp",
    "csharp",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "scala",
    "shell",
    "bash",
    "sh",
    "zsh",
    "json",
    "yaml",
    "toml",
    "html",
    "css",
    "scss",
    "sql",
    "graphql",
    "markdown",
    "md",
)


# Dynamically create formatter functions for each supported language
# This allows us to register them as entry points while keeping the code DRY


def _make_formatter(lang: str) -> Callable[[str, str], str]:
    """Create a formatter function for a specific language.

    Args:
        lang: Language identifier

    Returns:
        Formatter function with signature (unformatted: str, info_str: str) -> str
    """

    def formatter(unformatted: str, _info_str: str) -> str:
        return _format_code_with_mdsf(unformatted, lang)

    formatter.__name__ = f"format_{lang}"
    formatter.__doc__ = f"Format {lang} code using mdsf."
    return formatter


# Create formatter functions for all supported languages
for _lang in SUPPORTED_LANGUAGES:
    globals()[f"format_{_lang}"] = _make_formatter(_lang)
