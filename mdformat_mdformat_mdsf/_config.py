"""Configuration management for mdformat-mdsf."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any


class MdsfConfig:
    """Configuration for mdsf formatter."""

    def __init__(self) -> None:
        """Initialize configuration with defaults."""
        self._config_path: str | None = None
        self._timeout: int = 30
        self._languages: set[str] = set()
        self._fail_on_error: bool = False

    def update_from_options(self, options: Mapping[str, Any]) -> None:  # noqa: C901
        """Update configuration from mdformat options.

        Args:
            options: Options dictionary from mdformat context
        """
        # Try to get from API options first
        if api_config := options.get("mdformat", {}).get("mdsf_config"):
            self._config_path = api_config
        if api_timeout := options.get("mdformat", {}).get("mdsf_timeout"):
            self._timeout = int(api_timeout)
        if api_languages := options.get("mdformat", {}).get("mdsf_languages"):
            self._languages = set(api_languages)
        if api_fail := options.get("mdformat", {}).get("mdsf_fail_on_error"):
            self._fail_on_error = bool(api_fail)

        # Try to get from plugin configuration
        plugin_opts = (
            options.get("mdformat", {})
            .get("plugin", {})
            .get("mdsf", {})
        )
        if plugin_opts:
            if config := plugin_opts.get("config"):
                self._config_path = config
            if timeout := plugin_opts.get("timeout"):
                self._timeout = int(timeout)
            if languages := plugin_opts.get("languages"):
                if isinstance(languages, str):
                    self._languages = {lang.strip() for lang in languages.split(",")}
                else:
                    self._languages = set(languages)
            if fail := plugin_opts.get("fail_on_error"):
                self._fail_on_error = bool(fail)

    def update_from_env(self) -> None:
        """Update configuration from environment variables."""
        if config := os.environ.get("MDSF_CONFIG"):
            self._config_path = config
        if timeout := os.environ.get("MDSF_TIMEOUT"):
            with contextlib.suppress(ValueError):
                self._timeout = int(timeout)

    @property
    def config_path(self) -> str | None:
        """Get the mdsf config file path."""
        return self._config_path

    @property
    def timeout(self) -> int:
        """Get the timeout for mdsf operations."""
        return self._timeout

    @property
    def languages(self) -> set[str]:
        """Get the set of enabled languages (empty set means all)."""
        return self._languages

    @property
    def fail_on_error(self) -> bool:
        """Whether to fail on formatting errors."""
        return self._fail_on_error

    def is_language_enabled(self, language: str) -> bool:
        """Check if a language is enabled.

        Args:
            language: Language identifier

        Returns:
            True if language is enabled or no specific languages configured
        """
        # If no languages specified, all are enabled
        if not self._languages:
            return True
        return language in self._languages


# Global configuration instance
_global_config = MdsfConfig()


def get_config() -> MdsfConfig:
    """Get the global configuration instance.

    Returns:
        The global MdsfConfig instance
    """
    return _global_config


def find_mdsf_config() -> Path | None:
    """Find mdsf configuration file in current directory or parents.

    Returns:
        Path to mdsf.json if found, None otherwise
    """
    current = Path.cwd()
    while current != current.parent:
        config_file = current / "mdsf.json"
        if config_file.exists():
            return config_file
        current = current.parent
    return None
