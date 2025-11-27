"""Tests for configuration management."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from mdformat_mdsf._config import MdsfConfig, find_mdsf_config, get_config


@pytest.fixture
def config() -> MdsfConfig:
    """Create a fresh config instance for testing."""
    return MdsfConfig()


class TestMdsfConfigDefaults:
    """Test default configuration values."""

    def test_default_config_path(self, config: MdsfConfig) -> None:
        """Test default config path is None."""
        assert config.config_path is None

    def test_default_timeout(self, config: MdsfConfig) -> None:
        """Test default timeout is 30 seconds."""
        assert config.timeout == 30

    def test_default_languages(self, config: MdsfConfig) -> None:
        """Test default languages is empty set."""
        assert config.languages == set()

    def test_default_fail_on_error(self, config: MdsfConfig) -> None:
        """Test default fail_on_error is False."""
        assert config.fail_on_error is False


class TestUpdateFromOptions:
    """Test configuration updates from mdformat options."""

    def test_update_from_api_options(self, config: MdsfConfig) -> None:
        """Test updating config from API options."""
        options = {
            "mdformat": {
                "mdsf_config": "/path/to/config.json",
                "mdsf_timeout": 60,
                "mdsf_languages": ["python", "javascript"],
                "mdsf_fail_on_error": True,
            }
        }
        config.update_from_options(options)

        assert config.config_path == "/path/to/config.json"
        assert config.timeout == 60
        assert config.languages == {"python", "javascript"}
        assert config.fail_on_error is True

    def test_update_from_plugin_options(self, config: MdsfConfig) -> None:
        """Test updating config from plugin options."""
        options = {
            "mdformat": {
                "plugin": {
                    "mdformat_mdsf": {
                        "mdsf_config": "/path/to/plugin.json",
                        "mdsf_timeout": 45,
                        "mdsf_languages": ["rust", "go"],
                        "mdsf_fail_on_error": True,
                    }
                }
            }
        }
        config.update_from_options(options)

        assert config.config_path == "/path/to/plugin.json"
        assert config.timeout == 45
        assert config.languages == {"rust", "go"}
        assert config.fail_on_error is True

    def test_update_from_plugin_options_string_languages(
        self, config: MdsfConfig
    ) -> None:
        """Test updating config with comma-separated language string."""
        options = {
            "mdformat": {
                "plugin": {
                    "mdformat_mdsf": {
                        "mdsf_languages": "python, javascript, rust",
                    }
                }
            }
        }
        config.update_from_options(options)

        assert config.languages == {"python", "javascript", "rust"}

    def test_update_from_empty_options(self, config: MdsfConfig) -> None:
        """Test updating config with empty options dict."""
        options: dict[str, object] = {}
        config.update_from_options(options)

        # Should remain defaults
        assert config.config_path is None
        assert config.timeout == 30
        assert config.languages == set()
        assert config.fail_on_error is False


class TestUpdateFromEnv:
    """Test configuration updates from environment variables."""

    def test_update_from_env_config(self, config: MdsfConfig) -> None:
        """Test updating config from MDSF_CONFIG env var."""
        with patch.dict(os.environ, {"MDSF_CONFIG": "/env/config.json"}):
            config.update_from_env()
            assert config.config_path == "/env/config.json"

    def test_update_from_env_timeout(self, config: MdsfConfig) -> None:
        """Test updating timeout from MDSF_TIMEOUT env var."""
        with patch.dict(os.environ, {"MDSF_TIMEOUT": "120"}):
            config.update_from_env()
            assert config.timeout == 120

    def test_update_from_env_invalid_timeout(self, config: MdsfConfig) -> None:
        """Test that invalid timeout values are ignored."""
        original_timeout = config.timeout
        with patch.dict(os.environ, {"MDSF_TIMEOUT": "invalid"}):
            config.update_from_env()
            assert config.timeout == original_timeout

    def test_update_from_env_no_vars(self, config: MdsfConfig) -> None:
        """Test that config remains unchanged when no env vars are set."""
        with patch.dict(os.environ, {}, clear=True):
            original_config = config.config_path
            original_timeout = config.timeout
            config.update_from_env()
            assert config.config_path == original_config
            assert config.timeout == original_timeout


class TestIsLanguageEnabled:
    """Test language filtering logic."""

    def test_all_languages_enabled_by_default(self, config: MdsfConfig) -> None:
        """Test that all languages are enabled when none specified."""
        assert config.is_language_enabled("python")
        assert config.is_language_enabled("javascript")
        assert config.is_language_enabled("rust")
        assert config.is_language_enabled("unknown")

    def test_specific_language_enabled(self, config: MdsfConfig) -> None:
        """Test that only specified languages are enabled."""
        config._languages = {"python", "javascript"}  # noqa: SLF001

        assert config.is_language_enabled("python")
        assert config.is_language_enabled("javascript")
        assert not config.is_language_enabled("rust")
        assert not config.is_language_enabled("go")


class TestFindMdsfConfig:
    """Test finding mdsf.json config file."""

    def test_find_config_in_current_dir(self, tmp_path: Path) -> None:
        """Test finding config in current directory."""
        config_file = tmp_path / "mdsf.json"
        config_file.write_text("{}")

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = find_mdsf_config()
            assert result == config_file

    def test_find_config_in_parent_dir(self, tmp_path: Path) -> None:
        """Test finding config in parent directory."""
        config_file = tmp_path / "mdsf.json"
        config_file.write_text("{}")
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        with patch("pathlib.Path.cwd", return_value=subdir):
            result = find_mdsf_config()
            assert result == config_file

    def test_config_not_found(self, tmp_path: Path) -> None:
        """Test when config file is not found."""
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = find_mdsf_config()
            assert result is None


class TestGlobalConfig:
    """Test global configuration singleton."""

    def test_get_config_returns_same_instance(self) -> None:
        """Test that get_config returns the same instance."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2

    def test_global_config_persists_changes(self) -> None:
        """Test that changes to global config persist across calls."""
        config = get_config()
        config._timeout = 100  # noqa: SLF001

        config2 = get_config()
        assert config2.timeout == 100
