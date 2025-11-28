"""Tests for shell command hooks."""

from __future__ import annotations

from unittest.mock import Mock, patch

import mdformat
import pytest

from mdformat_hooks.plugin import (
    POSTPROCESSORS,
    _create_post_processor,
    _dynamic_postprocessor,
    _run_shell_command,
)


def test_run_shell_command_success():
    """Test successful shell command execution."""
    text = "Hello, World!"
    # Use a simple echo command that should work on all platforms
    result = _run_shell_command(text, "cat", timeout=5)
    assert result == text


def test_run_shell_command_with_none():
    """Test that None command returns original text."""
    text = "Hello, World!"
    result = _run_shell_command(text, None, timeout=5)
    assert result == text


def test_run_shell_command_error():
    """Test that command error returns original text."""
    text = "Hello, World!"
    # Use a command that will fail
    result = _run_shell_command(text, "false", timeout=5)
    assert result == text


def test_run_shell_command_timeout():
    """Test that command timeout returns original text."""
    text = "Hello, World!"
    # Use a command that will timeout
    result = _run_shell_command(text, "sleep 10", timeout=0.1)
    assert result == text


def test_postprocessors_dict():
    """Test POSTPROCESSORS is a proper dict with document processor."""
    assert isinstance(POSTPROCESSORS, dict)
    assert "document" in POSTPROCESSORS
    assert callable(POSTPROCESSORS["document"])


def test_dynamic_postprocessor_with_no_config():
    """Test dynamic postprocessor returns text unchanged with no config."""
    mock_context = Mock(options={"mdformat": {"plugin": {"hooks": {}}}})
    result = _dynamic_postprocessor("test text", Mock(), mock_context)
    assert result == "test text"


def test_dynamic_postprocessor_with_commands():
    """Test dynamic postprocessor applies commands."""
    mock_context = Mock(
        options={
            "mdformat": {
                "plugin": {
                    "hooks": {
                        "post_command": "cat",
                        "timeout": 10,
                    }
                }
            }
        }
    )
    result = _dynamic_postprocessor("test text", Mock(), mock_context)
    # The cat command should return the same text
    assert result == "test text"


@patch("subprocess.run")
def test_post_processor_runs_command(mock_run):
    """Test that post processor runs post command."""
    mock_run.return_value = Mock(
        returncode=0,
        stdout="processed text",
        stderr="",
    )

    options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "post-cmd",
                    "timeout": 10,
                }
            }
        }
    }

    processor = _create_post_processor(options)
    assert processor is not None

    mock_node = Mock()
    mock_context = Mock()
    result = processor("input text", mock_node, mock_context)  # noqa: F841

    # Should have been called once
    assert mock_run.call_count == 1


def test_mdformat_with_hooks():
    """Test mdformat integration with hooks."""
    text = "# Hello\n\nWorld!\n"

    # Test without any hooks (should just format normally)
    result = mdformat.text(text, extensions={"hooks"})
    assert result == "# Hello\n\nWorld!\n"


def test_mdformat_with_post_command():
    """Test mdformat with a simple post-command."""
    text = "# Hello\n\nWorld!\n"

    # Use cat command (should return the same text)
    options = {
        "plugin": {
            "hooks": {
                "post_command": "cat",
            }
        }
    }
    result = mdformat.text(text, extensions={"hooks"}, options=options)
    assert result == "# Hello\n\nWorld!\n"


# Strict mode tests
def test_strict_mode_success():
    """Strict mode passes when command succeeds."""
    text = "Hello, World!"
    result = _run_shell_command(text, "cat", timeout=5, strict=True)
    assert result == text


def test_strict_mode_failure_nonzero_exit():
    """Strict mode raises exception on non-zero exit."""
    text = "Hello, World!"
    with pytest.raises(RuntimeError, match="Command failed with exit code"):
        _run_shell_command(text, "false", timeout=5, strict=True)


def test_strict_mode_timeout():
    """Strict mode raises exception on timeout."""
    text = "Hello, World!"
    with pytest.raises(RuntimeError, match="Command timed out"):
        _run_shell_command(text, "sleep 10", timeout=0.1, strict=True)


def test_strict_mode_disabled_by_default():
    """Non-strict mode (default) returns original text on error."""
    text = "Hello, World!"
    # Command fails but strict is False (default), so should return original text
    result = _run_shell_command(text, "false", timeout=5, strict=False)
    assert result == text


def test_strict_mode_with_post_command_failure():
    """Strict mode raises exception on post_command failure."""
    mock_node = Mock()
    mock_node.type = "document"

    mock_context = Mock()
    mock_context.options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "false",  # Command that fails
                    "strict_hooks": True,
                    "timeout": 10,
                }
            }
        }
    }

    # Should raise because post_command fails and strict=True
    with pytest.raises(RuntimeError, match="Command failed with exit code"):
        _dynamic_postprocessor("test text", mock_node, mock_context)


def test_strict_mode_with_post_command_success():
    """Strict mode allows successful post_command to pass."""
    mock_node = Mock()
    mock_node.type = "document"

    mock_context = Mock()
    mock_context.options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "cat",  # Command that succeeds
                    "strict_hooks": True,
                    "timeout": 10,
                }
            }
        }
    }

    # Should work fine because command succeeds
    result = _dynamic_postprocessor("test text", mock_node, mock_context)
    assert result == "test text"


@patch("subprocess.run")
def test_strict_mode_post_processor(mock_run):
    """Test that strict mode is passed to post processor."""
    mock_run.return_value = Mock(
        returncode=1,  # Failure
        stdout="",
        stderr="error output",
    )

    options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "some-cmd",
                    "strict_hooks": True,
                    "timeout": 10,
                }
            }
        }
    }

    processor = _create_post_processor(options)
    assert processor is not None

    mock_node = Mock()
    mock_context = Mock()

    # Should raise because command fails and strict=True
    with pytest.raises(RuntimeError, match="Command failed with exit code"):
        processor("input text", mock_node, mock_context)
