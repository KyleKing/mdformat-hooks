"""Plugin interface for mdformat integration."""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from ._config import get_config

if TYPE_CHECKING:
    from collections.abc import Mapping

    from markdown_it import MarkdownIt
    from mdformat.renderer.typing import Render


# Code formatters don't need custom renderers
RENDERERS: Mapping[str, Render] = {}


def add_cli_argument_group(parser: argparse.ArgumentParser) -> None:  # pragma: no cover
    """Add CLI arguments for mdsf configuration.

    Args:
        parser: The argument parser to add arguments to
    """
    group = parser.add_argument_group("mdsf options")

    group.add_argument(
        "--mdsf-config",
        type=str,
        metavar="PATH",
        help="Path to mdsf.json configuration file",
    )

    group.add_argument(
        "--mdsf-timeout",
        type=int,
        metavar="SECONDS",
        default=30,
        help="Timeout for mdsf operations (default: 30)",
    )

    group.add_argument(
        "--mdsf-languages",
        type=str,
        metavar="LANG1,LANG2",
        help="Comma-separated list of languages to format (default: all)",
    )

    group.add_argument(
        "--mdsf-fail-on-error",
        action="store_true",
        help="Fail if mdsf formatting errors occur (default: false)",
    )


def update_mdit(mdit: MarkdownIt) -> None:  # pragma: no cover
    """Update the markdown-it parser (no-op for code formatters).

    Args:
        mdit: The markdown-it parser instance
    """
    # Code formatters don't need to modify the parser
    # This is only needed for syntax extensions


def _setup_from_options(options: dict[str, object]) -> None:  # pragma: no cover
    """Set up configuration from mdformat options.

    Args:
        options: Options dictionary from mdformat
    """
    config = get_config()

    # Update from CLI arguments
    if (mdsf_config := options.get("mdsf_config")) and isinstance(mdsf_config, str):
        config._config_path = mdsf_config  # noqa: SLF001
    if (mdsf_timeout := options.get("mdsf_timeout")) and isinstance(mdsf_timeout, int):
        config._timeout = mdsf_timeout  # noqa: SLF001
    if (mdsf_languages := options.get("mdsf_languages")) and isinstance(
        mdsf_languages, str
    ):
        config._languages = {  # noqa: SLF001
            lang.strip() for lang in mdsf_languages.split(",")
        }
    if (mdsf_fail := options.get("mdsf_fail_on_error")) and isinstance(mdsf_fail, bool):
        config._fail_on_error = mdsf_fail  # noqa: SLF001

    # Update from mdformat options dict (API and TOML config)
    config.update_from_options(options)

    # Update from environment variables as fallback
    config.update_from_env()
