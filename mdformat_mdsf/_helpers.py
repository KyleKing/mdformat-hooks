"""General Helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from . import __plugin_name__

ContextOptions = Mapping[str, Any]


def get_conf(options: ContextOptions, key: str) -> bool | str | int | list | None:
    """Read setting from mdformat configuration Context.

    Checks both API-level options and plugin-specific configuration.

    Args:
        options: Options dictionary from mdformat context
        key: Configuration key to retrieve

    Returns:
        Configuration value or None if not found
    """
    if (api := options.get("mdformat", {}).get(key)) is not None:
        return api  # From API
    return (
        options.get("mdformat", {}).get("plugin", {}).get(__plugin_name__, {}).get(key)
    )  # from cli_or_toml
